"""Página inicial do FemHealth ML Triage."""

import streamlit as st

from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_sidebar_controls,
    render_soft_divider,
)
from src.ui.i18n import get_language, t


st.set_page_config(page_title="FemHealth ML Triage", page_icon="📊", layout="wide")
render_sidebar_controls()


def render_home() -> None:
    """Render the landing page for the demonstrative platform."""
    apply_global_style()
    language = get_language()

    if language == "en":
        kicker = "Explainable ML demonstrative platform"
        subtitle = "Tabular analysis for women's health with clear ethical boundaries"
        description = (
            "Explore an academic Machine Learning pipeline with WDBC tabular data: "
            "understand the data, compare models, run an individual academic estimate, "
            "and interpret the factors that influenced the model output."
        )
        metrics = {
            "dataset": "Dataset",
            "model": "Final academic model",
            "features": "Attributes",
            "explainability": "Explainability",
            "model_value": "Logistic Regression",
            "explainability_value": "Global and local",
        }
        flow_title = "Recommended use flow"
        cards = [
            (
                "1. Start with the data",
                "Review WDBC, its 569 samples, 30 attributes, and the class distribution: Malignant (0) and Benign (1).",
            ),
            (
                "2. Understand the model",
                "See how Logistic Regression, KNN, and Decision Tree were compared before the academic V1 decision.",
            ),
            (
                "3. Run an estimate",
                "Use real WDBC examples or adjust attributes to observe the academic model output.",
            ),
            (
                "4. Interpret the output",
                "Use global and local explainability to understand which attributes most influenced the model behavior.",
            ),
            (
                "5. Review the limits",
                "Check scope, stack, AI-assisted methodology, and ethical limits of the demonstrative application.",
            ),
            (
                "6. Use responsibly",
                "The application is educational and must not be used for professional decisions, reports, or diagnosis.",
            ),
        ]
        resources_title = "Available resources"
        resources = """
        - **Data exploration:** overview, classes, attribute groups, and exploratory relationships.
        - **Model center:** comparison, technical ranking, ROC Curve, and confusion matrix.
        - **Estimate simulator:** validated individual input with real WDBC examples.
        - **Explainability:** global importance, optional SHAP, and local influence.
        - **About and Ethics:** scope, limitations, stack, and responsible use.
        """
        details_title = "MVP technical details"
        details = """
        - Dataset loaded locally via Scikit-learn.
        - Reproducible stratified train/test split.
        - Final academic model persisted in `models/artifacts/`.
        - Local quality gate to check artifacts, schema, environment, and critical language.
        """
    else:
        kicker = "Plataforma demonstrativa de ML explicável"
        subtitle = "Análise tabular em saúde da mulher com limites éticos claros"
        description = (
            "Explore um pipeline acadêmico de Machine Learning com dados tabulares "
            "do WDBC: entenda os dados, compare modelos, execute uma estimativa "
            "individual e interprete os fatores que influenciaram a saída."
        )
        metrics = {
            "dataset": "Dataset",
            "model": "Modelo final acadêmico",
            "features": "Atributos",
            "explainability": "Explicabilidade",
            "model_value": "Regressão Logística",
            "explainability_value": "Global e local",
        }
        flow_title = "Fluxo de uso recomendado"
        cards = [
            (
                "1. Comece pelos dados",
                "Conheça o WDBC, suas 569 amostras, 30 atributos e a distribuição das classes Maligno (0) e Benigno (1).",
            ),
            (
                "2. Entenda o modelo",
                "Veja como Regressão Logística, KNN e Árvore de Decisão foram comparados até a escolha acadêmica da V1.",
            ),
            (
                "3. Execute uma estimativa",
                "Use exemplos reais do WDBC ou ajuste atributos para observar a saída acadêmica do modelo.",
            ),
            (
                "4. Interprete a saída",
                "Consulte a explicabilidade global e local para entender quais atributos mais influenciaram o comportamento do modelo.",
            ),
            (
                "5. Revise os limites",
                "Consulte escopo, stack, metodologia assistida por IA e limites éticos da aplicação demonstrativa.",
            ),
            (
                "6. Use com responsabilidade",
                "A aplicação é educacional e não deve ser usada para decisão profissional, laudo ou diagnóstico.",
            ),
        ]
        resources_title = "Recursos disponíveis"
        resources = """
        - **Exploração dos dados:** visão geral, classes, grupos de atributos e relações exploratórias.
        - **Central de modelos:** comparação, ranking técnico, Curva ROC e matriz de confusão.
        - **Simulador de estimativa:** entrada individual validada com exemplos reais do WDBC.
        - **Explicabilidade:** importância global, SHAP opcional e influência neste exemplo.
        - **Sobre e Ética:** escopo, limitações, stack e uso responsável.
        """
        details_title = "Detalhes técnicos do MVP"
        details = """
        - Dataset carregado localmente via Scikit-learn.
        - Split treino/teste estratificado e reproduzível.
        - Modelo final acadêmico persistido em `models/artifacts/`.
        - Quality gate local para checar artefatos, schema, ambiente e linguagem crítica.
        """

    st.markdown(
        f'<div class="fh-kicker">{kicker}</div>',
        unsafe_allow_html=True,
    )
    st.title("FemHealth ML Triage")
    st.subheader(subtitle)
    st.write(description)

    col_dataset, col_model, col_scope, col_explain = st.columns(4)
    col_dataset.metric(metrics["dataset"], "WDBC")
    col_model.metric(metrics["model"], metrics["model_value"])
    col_scope.metric(metrics["features"], "30")
    col_explain.metric(metrics["explainability"], metrics["explainability_value"])

    render_soft_divider()

    st.subheader(flow_title)
    render_card_grid(cards)

    render_soft_divider()

    st.subheader(resources_title)
    st.markdown(resources)

    with st.expander(details_title):
        st.markdown(details)

    render_ethics_notice()


page = st.navigation(
    [
        st.Page(render_home, title=t("nav.home"), icon="🏠", url_path="", default=True),
        st.Page("pages/01_Exploracao.py", title=t("nav.exploration"), icon="🔎"),
        st.Page("pages/02_Predicao.py", title=t("nav.prediction"), icon="🧮"),
        st.Page("pages/03_Modelos.py", title=t("nav.models"), icon="📈"),
        st.Page("pages/04_Explicabilidade.py", title=t("nav.explainability"), icon="🧭"),
        st.Page("pages/05_Sobre_Etica.py", title=t("nav.about"), icon="⚖️"),
    ],
    position="sidebar",
    expanded=True,
)
page.run()
