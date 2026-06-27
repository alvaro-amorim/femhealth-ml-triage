"""Página inicial do FemHealth ML Triage."""

import streamlit as st


st.set_page_config(page_title="FemHealth ML Triage", page_icon="📊", layout="wide")

st.title("FemHealth ML Triage")
st.subheader("Apoio acadêmico à triagem analítica em saúde da mulher")
st.write(
    "Esta aplicação demonstra, de forma educacional, um pipeline de Machine "
    "Learning tabular com o dataset público Breast Cancer Wisconsin Diagnostic."
)

st.info(
    "Use a navegação lateral para acessar exploração dos dados, predição "
    "individual acadêmica, comparação de modelos, explicabilidade e seção de "
    "ética/limitações."
)

st.warning(
    "O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem "
    "analítica e não substitui diagnóstico médico, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O médico sempre deve ter a "
    "palavra final."
)
