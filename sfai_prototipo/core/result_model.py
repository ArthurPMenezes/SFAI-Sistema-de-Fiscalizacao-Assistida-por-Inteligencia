import uuid
from datetime import datetime, timezone


def criar_resultado_base():
    return {
        "analise_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),

        # Estrutura principal
        "contrato": None,
        "evidencia": None,
        "comparacao": None,

        # Score consolidado
        "score_hibrido": None,

        # Controle de execução
        "modo_execucao": "hibrido",  # deterministico | ia | hibrido
        "ia_utilizada": False,

        # Governança
        "trilha_auditoria": []
    }