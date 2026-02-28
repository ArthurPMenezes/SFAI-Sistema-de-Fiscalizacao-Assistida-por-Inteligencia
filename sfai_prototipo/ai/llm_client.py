import os
import json
import re
from google import genai
from dotenv import load_dotenv
from ai.prompts import (
    CONTEXTO_SFAI,
    PROMPT_ESTRUTURAR_CONTRATO,
    PROMPT_ESTRUTURAR_EVIDENCIA,
    PROMPT_COMPARAR_CONTRATO_EVIDENCIA
)

load_dotenv()


# ==============================
# 🔹 UTILITÁRIOS
# ==============================

def _limpar_markdown_json(texto: str) -> str:
    """
    Remove blocos ```json ``` e ruídos comuns
    """
    texto = texto.strip()

    texto = re.sub(r"^```json", "", texto, flags=re.IGNORECASE).strip()
    texto = re.sub(r"^```", "", texto).strip()
    texto = re.sub(r"```$", "", texto).strip()

    return texto


def _extrair_json_seguro(texto: str):
    """
    Tenta extrair o primeiro bloco JSON válido da resposta.
    """
    try:
        texto_limpo = _limpar_markdown_json(texto)

        # tenta parse direto
        return json.loads(texto_limpo)

    except Exception:
        # tenta extrair trecho entre { ... }
        match = re.search(r"\{.*\}", texto_limpo, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception as e:
                return {
                    "erro_parse": True,
                    "erro_detalhe": str(e),
                    "resposta_bruta": texto
                }

        return {
            "erro_parse": True,
            "resposta_bruta": texto
        }


def _gerar_resposta(prompt: str, esperar_json=True):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    client = genai.Client(api_key=api_key)

    prompt_final = f"""
    {CONTEXTO_SFAI}

    {prompt}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_final
    )

    texto = response.text.strip()

    if not esperar_json:
        return texto

    return _extrair_json_seguro(texto)


# ==============================
# 🔹 FUNÇÕES PRINCIPAIS
# ==============================

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