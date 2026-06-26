"""Página reservada para feature importance e SHAP."""

import streamlit as st


st.title("Explicabilidade")
st.info(
    "Feature importance e SHAP serão apresentados quando existir um modelo "
    "treinado e artefatos de explicabilidade."
)
st.caption(
    "Explicabilidade descreve o comportamento do modelo; não estabelece "
    "causalidade médica."
)
