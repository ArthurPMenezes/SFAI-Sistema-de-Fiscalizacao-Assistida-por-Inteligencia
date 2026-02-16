import streamlit as st
import os
from config import UPLOAD_DIR
from core.pdf_reader import extrair_texto_pdf
from core.rules_engine import analisar_regras
from core.scorer import calcular_score
from core.logger import salvar_log
# from ai.llm_client import analisar_com_llm
from config import USE_IA

st.title("Sistema de Análise de Conformidade e Triagem Inteligente- SFAI")

upload_file = st.file_uploader("Envie a evidência em PDF", type=["pdf"])

if upload_file :
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    caminho_arquivo = os.path.join(UPLOAD_DIR, upload_file.name)

    with open(caminho_arquivo, "wb") as f:
        f.write(upload_file.read())

    texto = extrair_texto_pdf(caminho_arquivo)

    pendencias = analisar_regras(texto)
    total_regras = 4
    score = calcular_score(total_regras, pendencias)

    st.subheader("Score de Conformidade")
    st.write(f"{score}%")

    st.subheader("Pendências Identificadas")
    for p in pendencias:
        st.write(f"-", p)

    if st.button("Executar análise com IA") and USE_IA:
        resposta_ia = analisar_com_llm(texto)
        st.subheader("Análise da IA")
        st.write(resposta_ia)
    else:        
        st.info("Análise com IA desativada. Ative a variável USE_IA para habilitar.")

    salvar_log({
        "arquivo": upload_file.name,
        "score": score,
        "pendencias": pendencias
    })