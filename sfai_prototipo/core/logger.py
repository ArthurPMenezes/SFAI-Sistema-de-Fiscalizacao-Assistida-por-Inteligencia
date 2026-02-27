from datetime import datetime, UTC

def registrar_log(mensagem):
    with open("data/logs/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(UTC).isoformat()} - {mensagem}\n")