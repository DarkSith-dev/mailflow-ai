import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GOOGLE_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE)

def gerar_arquivo_gemini(caminho_arquivo): 

    arquivo_temporario = genai.upload_file(
        path=caminho_arquivo, 
        display_name= "arquivo enviado"
    )
    return arquivo_temporario 