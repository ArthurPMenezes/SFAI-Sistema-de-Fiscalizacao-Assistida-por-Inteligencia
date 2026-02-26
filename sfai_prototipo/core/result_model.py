import uuid
from datetime import datetime, timezone

now_utc = datetime.now(timezone.utc)

def criar_resultado_base():
    return {
        "analise_id": str(uuid.uuid4()),
        "timestamp": now_utc.isoformat(),
        "regras_aplicadas": [],
        "conformidades": [],
        "nao_conformidades": [],
        "score_final": 0,
        "nivel_risco": "None",
        "modo_execucao": "deterministico",
        "ia_utilizada": False
    }