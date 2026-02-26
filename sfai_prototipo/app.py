import streamlit as st
from core.pipeline import executar_pipeline

st.title("SFAI - Sistema de Fiscalização Assistida por IA")

uploaded_file = st.file_uploader("Envie um PDF", type=["pdf"])

if uploaded_file is not None:
    caminho = f"data/uploads/{uploaded_file.name}"

    with open(caminho, "wb") as f:
        f.write(uploaded_file.read())


    usar_ia = st.checkbox("Ativar análise assistida (modo híbrido)")
    resultado = executar_pipeline(caminho, usar_ia=usar_ia)


    st.success("Análise concluída!")

    st.subheader("Resultado da Análise")
    st.json(resultado)