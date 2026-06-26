"""Página de escopo, limitações e postura ética do projeto."""

import streamlit as st


st.title("Sobre e Ética")
st.write(
    "O FemHealth ML Triage é um projeto acadêmico do Tech Challenge — Fase 1, "
    "centrado em Machine Learning tabular explicável."
)
st.markdown(
    "- Dataset principal: Breast Cancer Wisconsin Diagnostic (WDBC).\n"
    "- Interface V1: Streamlit multipage.\n"
    "- Fora da V1: API, banco de dados, autenticação, React/Vite e uso clínico."
)
st.warning(
    "Esta aplicação não substitui avaliação médica, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O médico sempre deve ter a "
    "palavra final."
)
