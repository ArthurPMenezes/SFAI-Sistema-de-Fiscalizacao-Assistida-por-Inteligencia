import json
from core.pdf_reader import extrair_texto_pdf as extrair_texto
from core.rules_engine import aplicar_regras
from core.scorer import calcular_score
from core.result_model import criar_resultado_base
from core.logger import registrar_log
from ai.llm_client import (
    estruturar_contrato,
    estruturar_evidencia,
    comparar_contrato_evidencia
)


def executar_pipeline(contrato_path=None, evidencia_path=None, usar_ia=False):
    resultado = criar_resultado_base()
    registrar_log("Iniciando análise modular")

    resultado["contrato"] = None
    resultado["evidencia"] = None
    resultado["comparacao"] = None
    resultado["ia_utilizada"] = False

    # =========================
    # 🔹 ANÁLISE DO CONTRATO
    # =========================
    if contrato_path:
        texto_contrato = extrair_texto(contrato_path)

        resultado["contrato"] = {
            "arquivo": contrato_path,
            "analise_ia": None
        }

        if usar_ia:
            try:
                resposta = estruturar_contrato(texto_contrato)

                resultado["contrato"]["analise_ia"] = resposta
                resultado["ia_utilizada"] = True

            except Exception as e:
                registrar_log(f"Erro IA contrato: {str(e)}")
                resultado["contrato"]["analise_ia"] = {
                    "erro": True,
                    "mensagem": str(e)
                }

    # =========================
    # 🔹 ANÁLISE DA EVIDÊNCIA
    # =========================
    if evidencia_path:
        texto_evidencia = extrair_texto(evidencia_path)

        regras = aplicar_regras(texto_evidencia)
        score, nivel = calcular_score(regras)

        resultado["evidencia"] = {
            "arquivo": evidencia_path,
            "regras_aplicadas": regras.get("regras_aplicadas", []),
            "conformidades": regras.get("conformidades", []),
            "nao_conformidades": regras.get("nao_conformidades", []),
            "score": score,
            "nivel_risco": nivel,
            "analise_ia": None
        }

        if usar_ia:
            try:
                resposta = estruturar_evidencia(texto_evidencia)

                resultado["evidencia"]["analise_ia"] = resposta
                resultado["ia_utilizada"] = True

            except Exception as e:
                registrar_log(f"Erro IA evidência: {str(e)}")
                resultado["contrato"]["analise_ia"] = {
                    "erro": True,
                    "mensagem": str(e)
                }

    # =========================
    # 🔹 COMPARAÇÃO CONTRATO x EVIDÊNCIA
    # =========================
    if contrato_path and evidencia_path and usar_ia:
        try:
            resposta = comparar_contrato_evidencia(
                resultado["contrato"]["analise_ia"],
                resultado["evidencia"]["analise_ia"]
            )

            resultado["comparacao"] = resposta
            resultado["ia_utilizada"] = True

        except Exception as e:
            registrar_log(f"Erro IA comparação: {str(e)}")
            resultado["contrato"]["analise_ia"] = {
                "erro": True,
                "mensagem": str(e)
            }

    salvar_resultado(resultado)
    registrar_log("Análise finalizada")

    return resultado


def salvar_resultado(resultado):
    caminho = f"data/logs/{resultado['analise_id']}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)