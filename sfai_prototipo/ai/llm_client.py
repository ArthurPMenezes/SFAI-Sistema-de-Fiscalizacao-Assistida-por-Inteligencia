import os
import json
from google import genai
from ai.prompts import CONTEXTO_SFAI, FORMATO_SAIDA
from dotenv import load_dotenv
load_dotenv()

def analisar_documento(texto):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    client = genai.Client(api_key=api_key)

    prompt = f"""
{CONTEXTO_SFAI}

{FORMATO_SAIDA}

Texto do contrato:
{texto}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "erro_parse": True,
            "resposta_bruta": response.text
        }