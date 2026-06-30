"""Página de escopo, limitações e postura ética do projeto."""

import streamlit as st

from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_page_intro,
    render_soft_divider,
)
from src.ui.i18n import get_language


language = get_language()
is_en = language == "en"

apply_global_style()
render_page_intro(
    "About, methodology, and ethics" if is_en else "Sobre, metodologia e ética",
    "Scope and responsibility" if is_en else "Escopo e responsabilidade",
    (
        "This page consolidates the MVP purpose, what is in and out of scope, the technical stack, and the ethical limits of the demonstration."
        if is_en
        else "Esta página consolida o propósito do MVP, o que está dentro e fora do "
        "escopo, a stack usada e os limites éticos da demonstração."
    ),
)

col_dataset, col_model, col_scope = st.columns(3)
col_dataset.metric("Dataset", "WDBC")
col_model.metric("Final academic model" if is_en else "Modelo final acadêmico", "Logistic Regression" if is_en else "Regressão Logística")
col_scope.metric("Interface", "Streamlit")

render_soft_divider()

st.subheader("Project objective" if is_en else "Objetivo do projeto")
st.write(
    (
        "FemHealth ML Triage demonstrates an academic explainable Machine Learning solution for tabular analysis in women's health. The focus is a reproducible, tested, and understandable pipeline in an interactive interface."
        if is_en
        else "O FemHealth ML Triage demonstra uma solução acadêmica de Machine Learning "
        "explicável para análise tabular em saúde da mulher. O foco é oferecer "
        "um pipeline reproduzível, testado e compreensível em uma interface interativa."
    )
)

st.subheader("What the MVP demonstrates" if is_en else "O que o MVP demonstra")
render_card_grid(
    (
    [
        (
            "Data and EDA",
            "Local WDBC loading, class distribution, statistics, and exploratory relationships.",
        ),
        (
            "Modeling",
            "Model comparison, technical ranking, and Logistic Regression declared as the final academic model.",
        ),
        (
            "Demonstrative use",
            "Individual academic estimate with real WDBC examples and validation of the 30 attributes.",
        ),
        (
            "Explainability",
            "Global importance, optional SHAP, and local explanation with safe technical fallback.",
        ),
        (
            "Quality",
            "Automated tests, local quality gate, model card, and methodological documentation.",
        ),
        (
            "Ethics",
            "Explicit notices, educational scope, and no promise of real healthcare use.",
        ),
    ]
    if is_en
    else [
        (
            "Dados e EDA",
            "Carregamento local do WDBC, distribuição de classes, estatísticas e correlações exploratórias.",
        ),
        (
            "Modelagem",
            "Comparação de modelos, ranking técnico e declaração da Regressão Logística como modelo final acadêmico.",
        ),
        (
            "Uso demonstrativo",
            "Estimativa individual acadêmica com exemplos reais do WDBC e validação dos 30 atributos.",
        ),
        (
            "Explicabilidade",
            "Importância global, SHAP opcional e explicação local com fallback técnico seguro.",
        ),
        (
            "Qualidade",
            "Testes automatizados, quality gate local, model card e documentação metodológica.",
        ),
        (
            "Ética",
            "Avisos explícitos, escopo educacional e ausência de promessa de uso real em saúde.",
        ),
    ]
    )
)

st.subheader("Out of V1 scope" if is_en else "Fora do escopo da V1")
if is_en:
    st.markdown(
        "- does not use private data, medical records, or images as input;\n"
        "- does not include API, database, authentication, React/Vite, or FastAPI;\n"
        "- has not been externally validated for real healthcare use;\n"
        "- must not be used by final patients or in operational workflows."
    )
else:
    st.markdown(
        "- não usa dados privados, prontuários ou imagens como entrada;\n"
        "- não possui API, banco de dados, autenticação, React/Vite ou FastAPI;\n"
        "- não foi validado externamente para uso real em saúde;\n"
        "- não deve ser usado por pacientes finais ou em fluxo operacional."
    )

st.subheader("Technical stack" if is_en else "Stack técnica")
if is_en:
    st.markdown(
        "- Python 3.11, Pandas, NumPy, and Scikit-learn;\n"
        "- optional SHAP, Joblib, and Streamlit multipage;\n"
        "- Pytest, Pytest-cov, and local quality gate;\n"
        "- controlled artifacts in `models/artifacts/`."
    )
else:
    st.markdown(
        "- Python 3.11, Pandas, NumPy e Scikit-learn;\n"
        "- SHAP opcional, Joblib e Streamlit multipage;\n"
        "- Pytest, Pytest-cov e quality gate local;\n"
        "- artefatos controlados em `models/artifacts/`."
    )

with st.expander("Methodology and responsible AI use" if is_en else "Metodologia e uso responsável de IA"):
    st.write(
        (
            "Development was conducted in controlled rounds with Codex support, recorded in `docs/methodology/`. Technical decisions, tests, and limitations were documented to support traceability and human review."
            if is_en
            else "O desenvolvimento foi conduzido em rodadas controladas com apoio do "
            "Codex, registradas em `docs/methodology/`. As decisões técnicas, "
            "testes e limitações foram documentados para apoiar rastreabilidade "
            "e revisão humana."
        )
    )
    st.markdown(
        """
        - ChatGPT/Codex apoiaram planejamento, implementação, revisão e documentação.
        - As mudanças foram validadas por testes automatizados e inspeções locais.
        - Custos e tokens são registrados como `não disponível` quando a interface não informa valores exatos.
        - A responsabilidade pela revisão final e entrega permanece humana.
        """
    )

with st.expander("Future optional evolution" if is_en else "Evolução futura opcional"):
    st.write(
        (
            "A future extension may add file-assisted/OCR-assisted input only for structured tabular reports containing the 30 WDBC attributes. This is not mammography, ultrasound, or real medical-image interpretation."
            if is_en
            else "Uma evolução futura pode adicionar entrada assistida por arquivo/OCR apenas para relatórios tabulares estruturados contendo os 30 atributos WDBC. Isso não é leitura de mamografia, ultrassom ou imagem médica real."
        )
    )

render_ethics_notice()
