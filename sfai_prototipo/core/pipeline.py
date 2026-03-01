import json
from datetime import datetime, timezone

from core.pdf_reader import extrair_texto_pdf as extrair_texto
from core.rules_engine import aplicar_regras
from core.scorer import calcular_score
from core.result_model import criar_resultado_base
from core.logger import registrar_log
from core.contract_models import CONTRATOS
from core.document_validator import validar_evidencia

from ai.llm_client import (
    estruturar_contrato,
    estruturar_evidencia,
    comparar_contrato_evidencia
)


# =========================
# 🔹 Helper de Auditoria
# =========================

def registrar_evento(resultado, descricao):
    if "trilha_auditoria" not in resultado:
        resultado["trilha_auditoria"] = []

    resultado["trilha_auditoria"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evento": descricao
    })


# =========================
# 🔹 Pipeline Principal
# =========================

def executar_pipeline(
    contrato_path=None,
    evidencia_path=None,
    tipo_contrato="desenvolvimento_software",
    usar_ia=False
):
    resultado = criar_resultado_base()
    registrar_log("Iniciando análise modular")
    registrar_evento(resultado, "Pipeline iniciado")

    resultado["contrato"] = None
    resultado["evidencia"] = None
    resultado["comparacao"] = None
    resultado["score_hibrido"] = None
    resultado["ia_utilizada"] = False

    contrato_estruturado = None
    evidencia_estruturada = None
    score_deterministico = None

    # =========================
    # 🔹 CONTRATO
    # =========================
    if contrato_path:
        texto_contrato = extrair_texto(contrato_path)
        registrar_evento(resultado, "Texto do contrato extraído")

        resultado["contrato"] = {
            "arquivo": contrato_path,
            "analise_ia": None
        }

        if usar_ia:
            try:
                contrato_estruturado = estruturar_contrato(texto_contrato)
                resultado["contrato"]["analise_ia"] = contrato_estruturado
                resultado["ia_utilizada"] = True

                registrar_evento(resultado, "Contrato estruturado via IA")

            except Exception as e:
                registrar_evento(resultado, "Erro na análise IA do contrato")

                resultado["contrato"]["analise_ia"] = {
                    "erro": True,
                    "mensagem": str(e)
                }

    # =========================
    # 🔹 EVIDÊNCIA
    # =========================
    if evidencia_path:

        texto_evidencia = extrair_texto(evidencia_path)
        registrar_evento(resultado, "Texto da evidência extraído")

        resultado["evidencia"] = {}

        # 🔹 Validação estrutural
        validacao = validar_evidencia(texto_evidencia)
        resultado["evidencia"]["indicador_confiabilidade"] = validacao

        registrar_evento(
            resultado,
            f"Validação estrutural realizada (Score: {validacao.get('score_confiabilidade')}%)"
        )

        # Bloqueio se documento inválido
        if validacao.get("score_confiabilidade", 0) < 40:
            resultado["evidencia"].update({
                "score_deterministico": 0,
                "nivel_risco": "alto",
                "nao_conformidades": [
                    "Documento com baixa confiabilidade estrutural"
                ],
                "conformidades": [],
                "regras_aplicadas": []
            })

            registrar_evento(resultado, "Análise bloqueada por baixa confiabilidade")

            salvar_resultado(resultado)
            return resultado

        # 🔹 Regras por tipo de contrato
        modelo = CONTRATOS.get(tipo_contrato)
        regras_ativas = modelo["regras"]

        regras = aplicar_regras(texto_evidencia, regras_ativas)
        score, nivel = calcular_score(regras)

        score_deterministico = score

        resultado["evidencia"].update({
            "arquivo": evidencia_path,
            "regras_aplicadas": regras.get("regras_aplicadas", []),
            "conformidades": regras.get("conformidades", []),
            "nao_conformidades": regras.get("nao_conformidades", []),
            "score_deterministico": score,
            "nivel_risco": nivel,
            "analise_ia": None
        })

        registrar_evento(resultado, f"Score determinístico calculado: {score}%")

        # 🔹 IA Evidência
        if usar_ia:
            try:
                evidencia_estruturada = estruturar_evidencia(texto_evidencia)
                resultado["evidencia"]["analise_ia"] = evidencia_estruturada
                resultado["ia_utilizada"] = True

                registrar_evento(resultado, "Evidência estruturada via IA")

            except Exception as e:
                registrar_evento(resultado, "Erro na análise IA da evidência")

                resultado["evidencia"]["analise_ia"] = {
                    "erro": True,
                    "mensagem": str(e)
                }

    # =========================
    # 🔹 COMPARAÇÃO
    # =========================
    if (
        usar_ia
        and contrato_estruturado
        and evidencia_estruturada
        and not contrato_estruturado.get("erro_parse")
        and not evidencia_estruturada.get("erro_parse")
    ):
        try:
            comparacao = comparar_contrato_evidencia(
                contrato_estruturado,
                evidencia_estruturada
            )

            resultado["comparacao"] = comparacao

            registrar_evento(resultado, "Comparação contrato x evidência realizada")

            percentual_aderencia = comparacao.get("percentual_aderencia")

            if percentual_aderencia is not None and score_deterministico is not None:
                score_hibrido = round(
                    (score_deterministico * 0.5) +
                    (percentual_aderencia * 0.5)
                )

                resultado["score_hibrido"] = score_hibrido

                registrar_evento(
                    resultado,
                    f"Score híbrido calculado: {score_hibrido}%"
                )

        except Exception as e:
            registrar_evento(resultado, "Erro na comparação IA")

            resultado["comparacao"] = {
                "erro": True,
                "mensagem": str(e)
            }

    registrar_evento(resultado, "Análise finalizada")
    salvar_resultado(resultado)
    registrar_log("Análise finalizada")

    return resultado


# =========================
# 🔹 Persistência
# =========================

def salvar_resultado(resultado):
    caminho = f"data/logs/{resultado['analise_id']}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)