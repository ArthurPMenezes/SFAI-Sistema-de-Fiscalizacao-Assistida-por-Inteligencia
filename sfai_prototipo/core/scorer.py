def calcular_score(resultado_regras):
    total = len(resultado_regras["conformidades"]) + len(resultado_regras["nao_conformidades"])
    total_conformes = len(resultado_regras["conformidades"])

    if total == 0:
        return 0, "indefinido"

    score = int((total_conformes / total) * 100)

    # Penalização se documento for fraco
    if "Documento muito curto para evidência formal" in resultado_regras["nao_conformidades"]:
        score = min(score, 50)

    if score >= 80:
        nivel = "baixo"
    elif score >= 50:
        nivel = "moderado"
    else:
        nivel = "alto"

    return score, nivel