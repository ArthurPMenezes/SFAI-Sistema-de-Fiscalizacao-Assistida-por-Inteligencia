import re

def validar_evidencia(texto):

    score_confiabilidade = 0
    criterios = {}
    texto_lower = texto.lower()

    # 1️⃣ Tamanho mínimo
    if len(texto.strip()) >= 800:
        score_confiabilidade += 20
        criterios["tamanho"] = True
    else:
        criterios["tamanho"] = False

    # 2️⃣ Data formal
    if re.search(r"\d{2}/\d{2}/\d{4}", texto):
        score_confiabilidade += 20
        criterios["datas_formais"] = True
    else:
        criterios["datas_formais"] = False

    # 3️⃣ Identificação responsável
    if "responsável" in texto_lower or "assinatura" in texto_lower:
        score_confiabilidade += 20
        criterios["responsavel"] = True
    else:
        criterios["responsavel"] = False

    # 4️⃣ Referência contratual
    if "contrato" in texto_lower or "processo administrativo" in texto_lower:
        score_confiabilidade += 20
        criterios["referencia_contrato"] = True
    else:
        criterios["referencia_contrato"] = False

    # 5️⃣ Linguagem técnica mínima
    termos_tecnicos = ["relatório", "execução", "serviço", "entrega"]
    if any(t in texto_lower for t in termos_tecnicos):
        score_confiabilidade += 20
        criterios["linguagem_tecnica"] = True
    else:
        criterios["linguagem_tecnica"] = False

    # Classificação
    if score_confiabilidade >= 70:
        nivel = "alta"
    elif score_confiabilidade >= 40:
        nivel = "media"
    else:
        nivel = "baixa"

    return {
        "score_confiabilidade": score_confiabilidade,
        "nivel_confiabilidade": nivel,
        "criterios_avaliados": criterios
    }