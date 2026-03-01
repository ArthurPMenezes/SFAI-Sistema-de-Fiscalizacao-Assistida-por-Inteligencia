def aplicar_regras(texto, regras_ativas):
    resultado = {
        "regras_aplicadas": regras_ativas,
        "conformidades": [],
        "nao_conformidades": []
    }

    texto_lower = texto.lower()

    for regra in regras_ativas:

        if regra == "verificacao_testes":
            if "teste automatizado" in texto_lower:
                resultado["conformidades"].append("Presença de testes automatizados")
            else:
                resultado["nao_conformidades"].append("Ausência de testes automatizados")

        elif regra == "verificacao_versionamento":
            if "versionamento" in texto_lower or "github" in texto_lower:
                resultado["conformidades"].append("Evidência de versionamento")
            else:
                resultado["nao_conformidades"].append("Ausência de evidência de versionamento")

        elif regra == "verificacao_sla":
            if "sla" in texto_lower:
                resultado["conformidades"].append("SLA documentado")
            else:
                resultado["nao_conformidades"].append("Ausência de SLA")

        elif regra == "verificacao_tempo_resposta":
            if "tempo de resposta" in texto_lower:
                resultado["conformidades"].append("Tempo de resposta documentado")
            else:
                resultado["nao_conformidades"].append("Tempo de resposta não informado")

    return resultado