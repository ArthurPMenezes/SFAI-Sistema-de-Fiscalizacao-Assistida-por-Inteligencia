def calcular_score(resultado_regras):
    total_regras = len(resultado_regras["regras_aplicadas"])
    total_conformes = len(resultado_regras["conformidades"])

    if total_regras == 0:
        return 0, "alto"

    score = int((total_conformes / total_regras) * 100)

    if score >= 80:
        nivel = "baixo"
    elif score >= 50:
        nivel = "moderado"
    else:
        nivel = "alto"

    return score, nivel