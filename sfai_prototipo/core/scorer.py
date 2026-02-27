def calcular_score(resultado_regras):
    total = len(resultado_regras["conformidades"]) + len(resultado_regras["nao_conformidades"])
    total_conformes = len(resultado_regras["conformidades"])

    if total == 0:
        return 0, "indefinido"

    score = int((len(resultado_regras["conformidades"]) / total) * 100)

    if score >= 80:
        nivel = "baixo"
    elif score >= 50:
        nivel = "moderado"
    else:
        nivel = "alto"

    return score, nivel