from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ContratoEstruturado:
    objeto: Optional[str]
    entregaveis: List[str]
    prazos: Dict[str, str]
    criterios_aceite: List[str]
    valor_global: Optional[str]