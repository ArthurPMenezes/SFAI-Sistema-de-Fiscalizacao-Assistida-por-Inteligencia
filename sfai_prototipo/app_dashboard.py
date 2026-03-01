import streamlit as st
import json
import plotly.graph_objects as go
from core.pipeline import executar_pipeline

def renderizar_bloco_ia(titulo, objeto):
    st.markdown(f"### {titulo}")

    if not objeto:
        st.info("Não analisado.")
        return

    # Caso venha estrutura {"erro": True, "mensagem": "..."}
    if isinstance(objeto, dict) and objeto.get("erro"):
        st.error(f"Erro na análise: {objeto.get('mensagem', 'Falha desconhecida')}")
        return

    # Caso venha erro de parse da IA
    if isinstance(objeto, dict) and objeto.get("erro_parse"):
        st.error("Erro ao interpretar resposta da IA.")
        st.code(objeto.get("resposta_bruta", ""))
        return

    # Caso seja JSON válido
    if isinstance(objeto, dict):
        st.json(objeto)
        return

    # Caso seja texto puro
    if isinstance(objeto, str):
        st.write(objeto)
        return

    # Qualquer coisa inesperada
    st.warning("Formato inesperado retornado pela IA.")

st.set_page_config(
    page_title="SFAI – Sistema de Fiscalização Assistida por IA",
    layout="wide"
)

st.title("SFAI – Sistema de Fiscalização Assistida por IA")
st.markdown("---")

# =========================
# Upload
# =========================

col1, col2 = st.columns(2)

with col1:
    contrato_file = st.file_uploader("Upload do Contrato (PDF)", type=["pdf"])

with col2:
    evidencia_file = st.file_uploader("Upload da Evidência (PDF)", type=["pdf"])

tipo_contrato = st.selectbox(
    "Tipo de Contrato",
    ["desenvolvimento_software", "suporte_tecnico"]
)

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
            tipo_contrato=tipo_contrato,
            usar_ia=usar_ia
        )

        st.success("Análise concluída com sucesso.")
        st.markdown("---")

        # =========================
        # ABAS
        # =========================

        aba1, aba2, aba3 = st.tabs([
            " Dashboard Gerencial",
            " Relatório Técnico",
            " Trilha de Auditoria"
        ])

        # =========================
        # DASHBOARD
        # =========================

        with aba1:

            score_det = resultado["evidencia"]["score_deterministico"]
            score_hibrido = resultado.get("score_hibrido")
            nivel = resultado["evidencia"]["nivel_risco"]

            k1, k2, k3, k4 = st.columns(4)

            k1.metric("Score Determinístico", f"{score_det}%")
            k2.metric(
                "Score Híbrido",
                f"{score_hibrido}%" if score_hibrido else "N/A"
            )
            k3.metric("Nível de Risco", nivel.capitalize())
            k4.metric(
                "IA Utilizada",
                "Sim" if resultado["ia_utilizada"] else "Não"
            )

            valor_gauge = score_hibrido if score_hibrido else score_det

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=valor_gauge,
                title={'text': "Índice Geral de Conformidade"},
                gauge={
                    'axis': {'range': [0, 100]},
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
        # 📑 ABA 2 – RELATÓRIO TÉCNICO
        # =========================

        with aba2:

            with st.expander("Regras Aplicadas"):
                st.json(resultado["evidencia"]["regras_aplicadas"])

            with st.expander("Análise IA - Contrato"):
                renderizar_bloco_ia(
                    "Análise Estruturada do Contrato (IA)",
                    resultado.get("contrato", {}).get("analise_ia")
                )

            with st.expander("Análise IA - Evidência"):
                renderizar_bloco_ia(
                    "Análise Estruturada da Evidência (IA)",
                    resultado.get("evidencia", {}).get("analise_ia")
                )

            with st.expander("Comparação Contrato x Evidência"):
                renderizar_bloco_ia(
                    "Parecer Técnico Comparativo",
                    resultado.get("comparacao")
                )


        # =========================
        # TRILHA DE AUDITORIA
        # =========================

        with aba3:

            trilha = resultado.get("trilha_auditoria", [])

            if trilha:
                for evento in trilha:
                    st.markdown(f"**[{evento['timestamp']}]** – {evento['evento']}")
            else:
                st.info("Nenhum evento registrado.")

    else:
        st.warning("Envie contrato e evidência para iniciar a análise.")