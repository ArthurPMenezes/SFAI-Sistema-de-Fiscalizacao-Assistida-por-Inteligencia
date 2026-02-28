import streamlit as st
import json
import pandas as pd
from core.pipeline import executar_pipeline
import plotly.graph_objects as go

st.set_page_config(
    page_title="SFAI – Sistema de Fiscalização Assistida por IA",
    layout="wide"
)

st.title("SFAI – Sistema de Fiscalização Assistida por IA")
st.markdown("---")

# =========================
# Upload de Arquivos
# =========================

col1, col2 = st.columns(2)

with col1:
    contrato_file = st.file_uploader("Upload do Contrato (PDF)", type=["pdf"])

with col2:
    evidencia_file = st.file_uploader("Upload da Evidência (PDF)", type=["pdf"])

usar_ia = st.checkbox("Ativar análise com IA", value=True)

# =========================
# Execução
# =========================

if st.button("Executar Análise"):

    if contrato_file and evidencia_file:

        with open("contrato_temp.pdf", "wb") as f:
            f.write(contrato_file.read())

        with open("evidencia_temp.pdf", "wb") as f:
            f.write(evidencia_file.read())

        resultado = executar_pipeline(
            contrato_path="contrato_temp.pdf",
            evidencia_path="evidencia_temp.pdf",
            usar_ia=usar_ia
        )

        st.success("Análise concluída com sucesso.")

        st.markdown("---")

        # =========================
        # Indicadores Gerenciais
        # =========================

        st.subheader("Indicadores Gerenciais")

        score_det = resultado["evidencia"]["score_deterministico"]
        score_hibrido = resultado.get("score_hibrido")
        nivel = resultado["evidencia"]["nivel_risco"]

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Score Determinístico", f"{score_det}%")

        k2.metric(
            "Score Híbrido",
            f"{score_hibrido}%" if score_hibrido is not None else "N/A"
        )

        k3.metric("Nível de Risco", nivel.capitalize())

        k4.metric(
            "IA Utilizada",
            "Ativa" if resultado["ia_utilizada"] else "Inativa"
        )

        # Barra visual
        st.write("### Grau Geral de Conformidade")
        st.progress(score_det / 100)

        # =========================
        # Alerta de Risco
        # =========================

        if nivel == "alto":
            st.error("⚠ Alto risco de não conformidade contratual.")
        elif nivel == "moderado":
            st.warning("⚠ Risco moderado identificado.")
        else:
            st.success("✔ Baixo risco de não conformidade.")

        st.markdown("---")

        # =========================
        # Gauge de Conformidade
        # =========================

        st.subheader("Índice Geral de Conformidade")

        valor_gauge = score_hibrido if score_hibrido is not None else score_det

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor_gauge,
            title={'text': "Score (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'thickness': 0.3},
                'steps': [
                    {'range': [0, 49], 'color': "#ff4d4d"},
                    {'range': [50, 79], 'color': "#ffcc00"},
                    {'range': [80, 100], 'color': "#4CAF50"}
                ],
            }
        ))

        fig.update_layout(height=350)

        st.plotly_chart(fig, width='stretch')

        # =========================
        # Detalhamento Técnico
        # =========================

        st.subheader("Detalhamento Técnico")

        with st.expander("Regras Aplicadas"):
            st.write(resultado["evidencia"]["regras_aplicadas"])

        with st.expander("Análise IA - Contrato"):
            st.json(resultado["contrato"]["analise_ia"])

        with st.expander("Análise IA - Evidência"):
            st.json(resultado["evidencia"]["analise_ia"])

        with st.expander("Comparação Contrato x Evidência"):
            st.json(resultado["comparacao"])

    else:
        st.warning("Envie contrato e evidência para iniciar a análise.")