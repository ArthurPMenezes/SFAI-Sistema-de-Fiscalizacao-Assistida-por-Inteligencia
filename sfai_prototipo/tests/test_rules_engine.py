from core.rules_engine import aplicar_regras

def test_documento_completo():
    texto = "Este projeto possui teste automatizado e versionamento em Git."
    resultado = aplicar_regras(texto)

    assert len(resultado["nao_conformidades"]) == 0
    assert len(resultado["conformidades"]) == 2

def test_documento_incompleto():
    texto = "Documento sem evidências tecnicas."
    resultado = aplicar_regras(texto)

    assert len(resultado["conformidades"]) == 0
    assert len(resultado["nao_conformidades"]) == 2
