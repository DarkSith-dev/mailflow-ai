import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GOOGLE_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE)

personas={
    'produtivo':"""
        Assuma que você é uma atendente virtual que irá fornecer o máximo de suporte técnico possivel ao cliente 

    """,

    'improdutivo': """
        Assuma que você é um atendente alegre que irá responder coisas como felicitações e agradecimentos 
    """
}

def selecionar_persona(mensagem_usuario):
    prompt_do_sistema = f""" 
        Assuma que você é um analisador de tipos de mensagens.

        1.Faça uma análise da mensagem informada pelo usuário para identificar se o tipo de mensagem 
        é do tipo Produtivo (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema). OU
        Improdutivo: (ex.: mensagens de felicitações, agradecimentos).

        2.Retorne apenas um dos dois tipos de mensagens informadas como resposta.

        Formato de saída: Apenas o tipo de mensagem em letras minusculas, sem espaços ou caracteres especiais ou quebras de linhas.

        #Exemplos

        Se a mensagem for algo como: "Preciso de ajuda com o sistema" ou algo como "O sistema caiu" ou "Preciso de ajuda" 
        Saída: produtivo

        Se a mensagem for algo como: "Feliz natal" ou  algo como "Feliz Aniversário" ou algo como "Obrigado pela ajuda vocês incriveis <3"
        Saída: improdutivo

       

    """
    configuracao_modelo = {
        "temperature" : 0.1,
        "max_output_tokens" : 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    resposta = llm.generate_content(mensagem_usuario)

    return resposta.text.strip().lower()