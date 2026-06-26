"""Página inicial do FemHealth ML Triage.

Esta etapa fornece somente a navegação e o contexto do projeto. As páginas
futuras consumirão lógica testável dos módulos em ``src``.
"""

import streamlit as st


st.set_page_config(page_title="FemHealth ML Triage", page_icon="📊", layout="wide")

st.title("FemHealth ML Triage")
st.subheader("Apoio acadêmico à triagem analítica em saúde da mulher")
st.write(
    "Esta aplicação demonstra, de forma educacional, um pipeline de Machine "
    "Learning tabular com o dataset público Breast Cancer Wisconsin Diagnostic."
)

st.info(
    "Nesta etapa, a base estrutural está pronta. Use a navegação lateral para "
    "conhecer as páginas planejadas da V1."
)

st.warning(
    "O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem "
    "analítica e não substitui diagnóstico médico, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O médico sempre deve ter a "
    "palavra final."
)
