import selecionar_persona
from gerenciar_arquivo import gerar_arquivo_gemini
from selecionar_persona import personas
from flask import Flask, jsonify,render_template, request


import google.generativeai as genai
from dotenv import load_dotenv
import os



from time import sleep
import uuid



import tempfile


caminho_do_arquivo = None



load_dotenv()
CHAVE_API_GOOGLE = os.getenv("GOOGLE_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE)

app = Flask(__name__)
app.secret_key = 'bolo'

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    tipo = selecionar_persona.selecionar_persona(prompt)  
    resposta_bot = bot(prompt)        
    return jsonify({
        'categoria': tipo,
        'resposta': resposta_bot
    })


def criarChatBot():
    personalidade= "neutro"
    
    prompt_do_sistema = f"""
    #persona 
    Você é uma IA que tem uma função que é classificar emails em categorias predefinidas e também, sugerir respostas automáticas 
    baseadas na classificação realizada.

    Você não deve responder perguntas que não sejam dados desse sistema informado!

    As categorias são as seguintes: 
    Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
    Improdutivo Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

    Sua função será associar as mensagens as categorias corretas.

    #histórico
    Acesse sempre o histórico de mensagens, e recupere  informações ditas anteriormente.
    
      """
    configuracao_modelo={
        "temperature": 0.1, 
        "max_output_tokens": 9500,
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    chatbot = llm.start_chat(history=[])
    return chatbot 

chatbot = criarChatBot()

def bot(prompt): 
    maximo_tentativas= 1
    repeticao= 0
    global caminho_do_arquivo

    while True:
        try:
            personalidade = personas[selecionar_persona.selecionar_persona(prompt)]
            mensagem_usuario= f"""
                Considere esta personalidade para responder essa mensagem:
                {personalidade}
                Responda as seguinde mensagem, sempre lembrando do histórico:
                {prompt}
            """
            if caminho_do_arquivo:
                mensagem_usuario +=  "\n Utilize as caracteristicas da imagem em sua resposta"
                arquivo =  gerar_arquivo_gemini(caminho_do_arquivo)
                resposta = chatbot.send_message(
                    mensagem_usuario,
                    files=[arquivo]
                )
                os.remove(caminho_do_arquivo)
                caminho_do_arquivo = None
            else:
                resposta = chatbot.send_message(mensagem_usuario)
            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no gemini: %s" % str(erro)
            sleep(50)  


@app.route("/Upload_file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    if file:
        extensao = os.path.splitext(file.filename)[1].lower()
        caminho_temporario = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}{extensao}")
        
        print ("Caminho temporário do arquivo:", caminho_temporario)
        file.save(caminho_temporario)

        global caminho_do_arquivo
        caminho_do_arquivo = caminho_temporario

        return "Arquivo enviado com sucesso", 200
    else:
        return "Erro ao enviar o arquivo", 500

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)