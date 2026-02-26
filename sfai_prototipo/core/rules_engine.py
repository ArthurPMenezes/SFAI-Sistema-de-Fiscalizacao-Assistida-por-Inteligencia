def aplicar_regras(texto):
    resultado = {
        "regras_aplicadas": [
            "verificacao_testes",
            "verificacao_versionamento"
        ],
        "conformidades": [],
        "nao_conformidades": []
    }

    texto_lower = texto.lower()

    if "teste automatizado" in texto_lower:
        resultado["conformidades"].append("Presença de testes automatizados")
    else:
        resultado["nao_conformidades"].append("Ausência de testes automatizados")

    if "versionamento" in texto_lower:
        resultado["conformidades"].append("Evidência de versionamento")
    else:
        resultado["nao_conformidades"].append("Ausência de evidência de versionamento")

    return resultado