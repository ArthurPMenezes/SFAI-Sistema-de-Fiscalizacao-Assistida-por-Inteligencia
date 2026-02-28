import os
import json
import re
from google import genai
from dotenv import load_dotenv
from ai.prompts import (
    PROMPT_ESTRUTURAR_CONTRATO,
    PROMPT_ESTRUTURAR_EVIDENCIA,
    PROMPT_COMPARAR_CONTRATO_EVIDENCIA
)

load_dotenv()


def _limpar_markdown_json(texto: str) -> str:
    """
    Remove blocos ```json ``` caso existam
    """
    texto = texto.strip()

    # remove ```json ou ```
    texto = re.sub(r"^```json", "", texto, flags=re.IGNORECASE).strip()
    texto = re.sub(r"^```", "", texto).strip()
    texto = re.sub(r"```$", "", texto).strip()

    return texto


def _gerar_resposta(prompt: str, esperar_json=True):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    texto = response.text.strip()

    if not esperar_json:
        return texto

    try:
        texto_limpo = _limpar_markdown_json(texto)
        return json.loads(texto_limpo)
    except Exception as e:
        return {
            "erro_parse": True,
            "erro_detalhe": str(e),
            "resposta_bruta": texto
        }


def estruturar_contrato(texto: str):
    prompt = f"""
    {PROMPT_ESTRUTURAR_CONTRATO}

    CONTRATO:
    {texto}
    """

    return _gerar_resposta(prompt, esperar_json=True)


def estruturar_evidencia(texto: str):
    prompt = f"""
    {PROMPT_ESTRUTURAR_EVIDENCIA}

    EVIDÊNCIA:
    {texto}
    """

    return _gerar_resposta(prompt, esperar_json=True)


def comparar_contrato_evidencia(contrato_json: dict, evidencia_json: dict):
    prompt = f"""
    {PROMPT_COMPARAR_CONTRATO_EVIDENCIA}

    CONTRATO ESTRUTURADO:
    {json.dumps(contrato_json, ensure_ascii=False, indent=2)}

    EVIDÊNCIA ESTRUTURADA:
    {json.dumps(evidencia_json, ensure_ascii=False, indent=2)}
    """

    return _gerar_resposta(prompt, esperar_json=True)