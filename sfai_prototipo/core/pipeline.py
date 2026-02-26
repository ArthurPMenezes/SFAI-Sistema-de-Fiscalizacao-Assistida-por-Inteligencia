import json
from core.pdf_reader import extrair_texto_pdf as extrair_texto
from core.rules_engine import aplicar_regras
from core.scorer import calcular_score
from core.result_model import criar_resultado_base
from ai.llm_client import analisar_documento
from core.logger import registrar_log

def executar_pipeline(caminho_pdf, usar_ia=None):
    resultado = criar_resultado_base()

    registrar_log("Iniciando análise")

    texto = extrair_texto(caminho_pdf)

    regras = aplicar_regras(texto)

    resultado["regras_aplicadas"] = regras["regras_aplicadas"]
    resultado["conformidades"] = regras["conformidades"]
    resultado["nao_conformidades"] = regras["nao_conformidades"]

    score, nivel = calcular_score(regras)

    resultado["score_final"] = score
    resultado["nivel_risco"] = nivel

    if usar_ia:
        try:
            resposta_ia = analisar_documento(texto)

            resultado["analise_ia"] = resposta_ia
            resultado["ia_utilizada"] = True
            resultado["modo_execucao"] = "hibrido"

            registrar_log("IA executada com sucesso")

        except Exception as e:
            registrar_log(f"Erro na IA: {str(e)}")

            resultado["analise_ia"] = "Falha na análise de IA"
            resultado["ia_utilizada"] = False
            resultado["modo_execucao"] = "deterministico_fallback"

    salvar_resultado(resultado)

    registrar_log(f"Análise finalizada: {resultado['analise_id']}")

    return resultado


def salvar_resultado(resultado):
    caminho = f"data/logs/{resultado['analise_id']}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)