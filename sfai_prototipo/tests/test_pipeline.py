import core.pipeline as pipeline

def test_pipeline_sem_ia(monkeypatch):

    # mock do estrator de texto
    def fake_extrair_texto(_):
        return "teste automatizado e versionamento"
    
    monkeypatch.setattr(pipeline, "extrair_texto", fake_extrair_texto)

    resultado = pipeline.executar_pipeline("fake.pdf", usar_ia=False)
    
    assert resultado["ia_utilizada"] == False
    assert resultado["score_final"] >= 0
    assert "analise_id" in resultado