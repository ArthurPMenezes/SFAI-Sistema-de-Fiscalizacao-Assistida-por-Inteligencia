import re


def aplicar_regras(texto):
    resultado = {
        "regras_aplicadas": [
            "verificacao_testes",
            "verificacao_versionamento",
            "verificacao_estrutura_tecnica",
            "verificacao_tamanho_documento"
        ],
        "conformidades": [],
        "nao_conformidades": []
    }

    texto_lower = texto.lower()

    # =========================
    # 🔹 REGRA 1 - TESTES
    # =========================
    if any(p in texto_lower for p in [
        "teste automatizado",
        "testes unitarios",
        "test result",
        "passed",
        "failed"
    ]):
        resultado["conformidades"].append("Evidência real de testes encontrada")
    else:
        resultado["nao_conformidades"].append("Ausência de evidência real de testes")

    # =========================
    # 🔹 REGRA 2 - VERSIONAMENTO
    # =========================
    if re.search(r"commit\s+[a-f0-9]{6,40}", texto_lower):
        resultado["conformidades"].append("Hash de commit identificado")
    else:
        resultado["nao_conformidades"].append("Nenhum hash de commit identificado")

    # =========================
    # 🔹 REGRA 3 - INDICADORES TÉCNICOS
    # =========================
    indicadores = 0

    if re.search(r"\d+%", texto_lower):
        indicadores += 1

    if re.search(r"\d{2}/\d{2}/\d{4}", texto_lower):
        indicadores += 1

    if "pipeline" in texto_lower or "build" in texto_lower:
        indicadores += 1

    if indicadores >= 2:
        resultado["conformidades"].append("Indicadores técnicos estruturais presentes")
    else:
        resultado["nao_conformidades"].append("Documento fraco em indicadores técnicos")

    # =========================
    # 🔹 REGRA 4 - TAMANHO
    # =========================
    if len(texto) > 800:
        resultado["conformidades"].append("Documento com volume compatível")
    else:
        resultado["nao_conformidades"].append("Documento muito curto para evidência formal")

    return resultado