from pypdf import PdfReader

def extrair_texto_pdf(caminho_arquivo):
    reader = PdfReader(caminho_arquivo)
    texto = ""

    for page in reader.pages:
        conteudo = page.extract_text()
        if conteudo:
            texto += conteudo + "\n"

    return texto