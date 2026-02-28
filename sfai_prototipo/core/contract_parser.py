# texto do contrato
#         ↓
# [1] Parsing heurístico
#         ↓
# [2] Parsing via IA
#         ↓
# [3] Consolidação + validação
#         ↓
# Contrato Estruturado

import re
import json
from typing import Dict
from core.contract_schema import ContratoEstruturado
from ai.llm_client import analisar_documento
from ai.prompts import PROMPT_ESTRUTURAR_CONTRATO

def extrair_heuristico(texto: str) -> Dict:
    resultado = {
        "objeto": None,
        "entregaveis": [],
        "prazos": {},
        "criterios_aceite": [],
        "valor_global": None
    }

    # OBJETO
    match_objeto = re.search(r"(Objeto|OBJETO)\s*[:\-]\s*(.+)", texto)
    if match_objeto:
        resultado["objeto"] = match_objeto.group(2).strip()

    # VALOR GLOBAL
    match_valor = re.search(r"(Valor Global|VALOR GLOBAL)\s*[:\-]\s*(R?\$?\s?[\d\.,]+)", texto)
    if match_valor:
        resultado["valor_global"] = match_valor.group(2).strip()

    # PRAZOS (simplificado)
    prazos = re.findall(r"prazo\s*de\s*(\d+\s*dias|\d+\s*meses)", texto, re.IGNORECASE)
    if prazos:
        resultado["prazos"]["geral"] = prazos[0]

    return resultado

def extrair_com_ia(texto: str) -> Dict:
    prompt = PROMPT_ESTRUTURAR_CONTRATO + texto

    try:
        resposta = analisar_documento(prompt)

        # Limpeza defensiva (caso venha com markdown)
        resposta = resposta.strip().replace("```json", "").replace("```", "")

        return json.loads(resposta)

    except Exception:
        return {}
    
def consolidar(heuristico: Dict, ia: Dict) -> Dict:
    resultado = {}

    for chave in heuristico.keys():

        if heuristico.get(chave):
            resultado[chave] = heuristico[chave]

        elif ia.get(chave):
            resultado[chave] = ia[chave]

        else:
            resultado[chave] = None if chave != "entregaveis" and chave != "criterios_aceite" else []

    return resultado

def estruturar_contrato(texto: str, usar_ia: bool = True) -> ContratoEstruturado:

    heuristico = extrair_heuristico(texto)

    ia = extrair_com_ia(texto) if usar_ia else {}

    consolidado = consolidar(heuristico, ia)

    return ContratoEstruturado(
        objeto=consolidado["objeto"],
        entregaveis=consolidado["entregaveis"] or [],
        prazos=consolidado["prazos"] or {},
        criterios_aceite=consolidado["criterios_aceite"] or [],
        valor_global=consolidado["valor_global"]
    )