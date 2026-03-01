from datetime import datetime


def registrar_evento(resultado: dict, evento: str, detalhes: dict = None):
    """
    Registra evento na trilha de auditoria do resultado.
    """

    if "trilha_auditoria" not in resultado:
        resultado["trilha_auditoria"] = []

    resultado["trilha_auditoria"].append({
        "timestamp": datetime.now().isoformat(),
        "evento": evento,
        "detalhes": detalhes or {}
    })