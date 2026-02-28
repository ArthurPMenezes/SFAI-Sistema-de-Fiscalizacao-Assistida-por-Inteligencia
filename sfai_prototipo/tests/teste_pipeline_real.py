from core.pdf_reader import extrair_texto_pdf
from ai.llm_client import analisar_documento  # ajuste pro nome real

CAMINHO_PDF = "tests/contrato.pdf"

def main():
    print("Lendo PDF...")
    texto = extrair_texto_pdf(CAMINHO_PDF)

    if not texto or len(texto) < 100:
        print("⚠ Texto muito pequeno ou vazio")
        return

    print("Texto extraído com sucesso.")
    print("Enviando para IA...")

    resposta = analisar_documento(texto)

    print("\nResposta da IA:")
    print(resposta)

if __name__ == "__main__":
    main()