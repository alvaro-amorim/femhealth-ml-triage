"""Página reservada para a predição individual demonstrativa."""

import streamlit as st


st.title("Predição Individual")
st.info(
    "A entrada por exemplo, CSV e formulário será disponibilizada depois do "
    "treinamento e da validação de dados."
)
st.warning(
    "Resultados futuros serão estimativas acadêmicas do modelo; não devem ser "
    "utilizados como diagnóstico médico."
)
