from core.scorer import calcular_score

def test_score_sem_falhas():
    total_regras = {
        "conformidades": ["a", "b"],
        "nao_conformidades": []
    }

    score, nivel = calcular_score(total_regras)

    assert score == 100
    assert nivel == "baixo"

def test_score_com_falhas():
    total_regras = {
        "conformidades": [],
        "nao_conformidades": ["erro1", "erro2"]
    }

    score, nivel = calcular_score(total_regras)

    assert score < 100
    assert nivel in ["medio", "alto"]

