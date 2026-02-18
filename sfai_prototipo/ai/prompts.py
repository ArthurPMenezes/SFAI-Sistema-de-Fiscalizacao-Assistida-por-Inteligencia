ANALISE_TECNICA_PROMPT = """
    Você é um sistema de fiscalização contratual.
        Analisé o texto abaixo e identifique:

        - Presença de testes automatizados
        - Evidências de homologação 
        - Evidências de versionamento
        - Inconsistências técnicas
        
        Seja objetivo e direto.

        Texto:
        {documento}

        Retorne em formato JSON.
        """