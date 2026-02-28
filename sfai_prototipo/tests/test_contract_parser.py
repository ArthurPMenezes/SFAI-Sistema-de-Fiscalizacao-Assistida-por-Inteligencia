from core.contract_parser import estruturar_contrato

def test_parser_heuristico_basico():

    texto = """
    OBJETO: Desenvolvimento de sistema de fiscalização.
    VALOR GLOBAL: R$ 120.000,00
    prazo de 90 dias
    """

    contrato = estruturar_contrato(texto, usar_ia=False)

    assert contrato.objeto == "Desenvolvimento de sistema de fiscalização."
    assert contrato.valor_global == "R$ 120.000,00"
    assert contrato.prazos["geral"] == "90 dias"