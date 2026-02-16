import json
import os
from datetime import datetime
from config import LOG_DIR

def salvar_log(resultado: dict):
    os.makedirs(LOG_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(LOG_DIR, f"log_{timestamp}.json")

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)