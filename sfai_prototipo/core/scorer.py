def calcular_score(total_regras, pendencias):
    if total_regras == 0:
        return 0
    
    conformidades = total_regras - len(pendencias)
    score = (conformidades / total_regras) * 100
    
    return round(score, 2)