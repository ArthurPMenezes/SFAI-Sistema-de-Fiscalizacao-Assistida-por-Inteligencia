def analisar_regras(texto: str):
    texto = texto.lower()
    pendencias = []

    regras = {
        "teste automatizado": "Aussência de menção a testes automazados.",
        "homologação": "Aussência de evidência de homologação.",
        "repositório": "Não há referência ao versionamento em repositório.",
        "pitomba": "Não há referência ao Pitomba."
    }

    for termo, mensagem in regras.items():
        if termo not in texto:
            pendencias.append(mensagem)

    return pendencias