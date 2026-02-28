import streamlit as st
from core.pipeline import executar_pipeline
import os

st.title("SFAI - Sistema de Fiscalização Assistida por IA")

contrato_file = st.file_uploader("Envie o CONTRATO", type=["pdf"], key="contrato")
evidencia_file = st.file_uploader("Envie a EVIDÊNCIA", type=["pdf"], key="evidencia")

usar_ia = st.checkbox("Ativar análise assistida (modo híbrido)")

contrato_path = None
evidencia_path = None

if contrato_file:
    contrato_path = f"data/uploads/{contrato_file.name}"
    with open(contrato_path, "wb") as f:
        f.write(contrato_file.read())

if evidencia_file:
    evidencia_path = f"data/uploads/{evidencia_file.name}"
    with open(evidencia_path, "wb") as f:
        f.write(evidencia_file.read())

if st.button("Executar Análise"):
    resultado = executar_pipeline(
        contrato_path=contrato_path,
        evidencia_path=evidencia_path,
        usar_ia=usar_ia
    )

    st.success("Análise concluída!")

    if resultado["contrato"]:
        st.subheader("Análise do Contrato")
        st.json(resultado["contrato"])

    if resultado["evidencia"]:
        st.subheader("Análise da Evidência")
        st.json(resultado["evidencia"])

    if resultado["comparacao"]:
        st.subheader("Comparação Contrato x Evidência")
        st.write(resultado["comparacao"])