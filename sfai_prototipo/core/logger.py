from datetime import datetime

def registrar_log(mensagem):
    with open("data/logs/system.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {mensagem}\n")