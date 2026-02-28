from core.pdf_reader import extrair_texto_pdf
from core.contract_parser import estruturar_contrato

texto = """
CONTRATO Nº 01/2026

OBJETO: Desenvolvimento de sistema de fiscalização contratual baseado em UST.

VALOR GLOBAL: R$ 450.000,00

O prazo de execução será de 180 dias.

Critério de aceite: validação técnica pela equipe da SEAD.
"""

contrato = estruturar_contrato(texto, usar_ia=True)

print("\n--- RESULTADO ESTRUTURADO ---\n")
print("Objeto:", contrato.objeto)
print("Valor:", contrato.valor_global)
print("Prazos:", contrato.prazos)
print("Critérios:", contrato.criterios_aceite)
print("Entregáveis:", contrato.entregaveis)