"""Página de escopo, limitações e postura ética do projeto."""

import streamlit as st


st.title("Sobre e Ética")
st.write(
    "O FemHealth ML Triage é um projeto acadêmico do Tech Challenge — Fase 1, "
    "centrado em Machine Learning tabular explicável para apoio à triagem "
    "analítica em saúde da mulher."
)

col_dataset, col_model, col_scope = st.columns(3)
col_dataset.metric("Dataset", "WDBC")
col_model.metric("Modelo final acadêmico", "Regressão Logística")
col_scope.metric("Interface", "Streamlit")

st.subheader("O que o MVP demonstra")
st.markdown(
    "- carregamento local do WDBC via Scikit-learn;\n"
    "- EDA real, métricas e comparação de modelos;\n"
    "- modelo final acadêmico persistido para reprodutibilidade;\n"
    "- predição individual acadêmica com exemplos reais do WDBC;\n"
    "- explicabilidade global e local com fallback técnico seguro."
)

st.subheader("Limites da V1")
st.markdown(
    "- não usa dados privados, prontuários ou imagens como entrada;\n"
    "- não possui API, banco de dados, autenticação, React/Vite ou FastAPI;\n"
    "- não foi validado externamente para uso real em saúde;\n"
    "- não deve ser usado por pacientes finais ou em fluxo operacional."
)

with st.expander("Metodologia e uso responsável de IA"):
    st.write(
        "O desenvolvimento foi conduzido em rodadas controladas com apoio do "
        "Codex, registradas em `docs/methodology/`. As decisões técnicas, "
        "testes e limitações foram documentados para apoiar revisão humana, "
        "relatório e vídeo."
    )

st.warning(
    "Esta aplicação não substitui diagnóstico médico, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O profissional de saúde sempre "
    "deve ter a palavra final."
)
