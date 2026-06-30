"""Página Streamlit de exploração real do dataset WDBC."""

import pandas as pd
import streamlit as st

from src.analysis.eda import (
    get_dataset_overview,
    get_descriptive_statistics,
    get_feature_group_summary,
    get_missing_values_summary,
    get_target_distribution,
    get_top_target_correlations,
)
from src.data.schema import FEATURE_GROUPS
from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_page_intro,
    render_soft_divider,
)
from src.ui.feature_dictionary import translate_feature_name
from src.ui.i18n import get_language, translate_group_name, translate_target_label


@st.cache_data(show_spinner=False)
def _load_eda_payload() -> dict:
    """Load reusable EDA tables for the current Streamlit session."""
    return {
        "overview": get_dataset_overview(),
        "target_distribution": get_target_distribution(),
        "feature_group_summary": get_feature_group_summary(),
        "descriptive_statistics": get_descriptive_statistics(),
        "missing_values_summary": get_missing_values_summary(),
        "top_target_correlations": get_top_target_correlations(top_n=10),
    }


def _format_target_distribution(distribution: pd.DataFrame) -> pd.DataFrame:
    """Return target distribution with labels suitable for display."""
    language = get_language()
    formatted = distribution.copy()
    formatted["Classe"] = formatted.apply(
        lambda row: translate_target_label(int(row["target"]), language), axis=1
    )
    formatted = formatted.rename(
        columns={
            "count": "Contagem" if language == "pt" else "Count",
            "percentage": "Percentual (%)" if language == "pt" else "Percentage (%)",
        }
    )
    percentage_column = "Percentual (%)" if language == "pt" else "Percentage (%)"
    count_column = "Contagem" if language == "pt" else "Count"
    formatted[percentage_column] = formatted[percentage_column].round(2)
    return formatted[["Classe", count_column, percentage_column]]


def _format_feature_group_summary() -> pd.DataFrame:
    """Return feature groups with friendly names and technical detail."""
    language = get_language()
    return pd.DataFrame(
        [
            {
                "Grupo" if language == "pt" else "Group": translate_group_name(
                    group_name, language
                ),
                "Grupo técnico" if language == "pt" else "Technical group": group_name,
                "Atributos" if language == "pt" else "Attributes": len(features),
                "Nomes amigáveis" if language == "pt" else "Friendly names": ", ".join(
                    translate_feature_name(feature_name, language)
                    for feature_name in features
                ),
                "Nomes técnicos WDBC" if language == "pt" else "Technical WDBC names": ", ".join(
                    features
                ),
            }
            for group_name, features in FEATURE_GROUPS.items()
        ]
    )


def _format_feature_table(table: pd.DataFrame) -> pd.DataFrame:
    """Add friendly feature names to an EDA table without changing source data."""
    language = get_language()
    formatted = table.copy()
    formatted.insert(
        0,
        "Atributo" if language == "pt" else "Attribute",
        formatted["feature"].map(lambda feature: translate_feature_name(feature, language)),
    )
    formatted = formatted.rename(
        columns={
            "feature": "Nome técnico" if language == "pt" else "Technical name",
            "correlation_with_target": (
                "Correlação com a classe do registro"
                if language == "pt"
                else "Correlation with record class"
            ),
            "absolute_correlation": (
                "Correlação absoluta" if language == "pt" else "Absolute correlation"
            ),
            "mean": "Média" if language == "pt" else "Mean",
            "std": "Desvio padrão" if language == "pt" else "Standard deviation",
            "min": "Mínimo" if language == "pt" else "Minimum",
            "max": "Máximo" if language == "pt" else "Maximum",
        }
    )
    return formatted


def render_page() -> None:
    """Render the WDBC exploratory-data-analysis page."""
    apply_global_style()
    language = get_language()
    is_en = language == "en"
    render_page_intro(
        "Explore the data" if is_en else "Conheça os dados",
        "WDBC data" if is_en else "Dados do WDBC",
        (
            "This page explains the technical data base of the MVP: WDBC size, "
            "record classes, attribute groups, data quality, and exploratory "
            "relationships with the record class."
            if is_en
            else "A exploração mostra a base técnica do MVP: tamanho do WDBC, "
            "classes dos registros, grupos de atributos, qualidade dos dados e "
            "relações exploratórias com a classe do registro."
        ),
    )
    render_ethics_notice(short=True)

    payload = _load_eda_payload()
    overview = payload["overview"]
    target_distribution = payload["target_distribution"]
    feature_group_summary = payload["feature_group_summary"]
    descriptive_statistics = payload["descriptive_statistics"]
    missing_values_summary = payload["missing_values_summary"]
    top_target_correlations = payload["top_target_correlations"]

    st.subheader("Dataset overview" if is_en else "Resumo do dataset")
    col_dataset, col_samples, col_features = st.columns(3)
    col_dataset.metric("Dataset", "WDBC")
    col_samples.metric("Samples" if is_en else "Amostras", overview["sample_count"])
    col_features.metric("Attributes" if is_en else "Atributos", overview["feature_count"])

    col_classes, col_priority, col_missing = st.columns(3)
    col_classes.metric("Classes", overview["class_count"])
    col_priority.metric(
        "Priority class" if is_en else "Classe prioritária",
        translate_target_label(0, language),
    )
    col_missing.metric(
        "Missing values" if is_en else "Valores ausentes",
        overview["missing_values_total"],
    )

    st.caption(
        (
            "Official Scikit-learn mapping: 0 = Malignant; 1 = Benign. "
            "Technical WDBC feature names remain unchanged in the backend."
            if is_en
            else "Mapeamento oficial do Scikit-learn: 0 = Maligno; 1 = Benigno. "
            "Os nomes técnicos WDBC continuam preservados no backend."
        )
    )

    render_card_grid(
        [
            (
                "Why this matters" if is_en else "Por que esta análise importa",
                (
                    "EDA confirms the pipeline starts from real, numeric, stable data with no missing values in the original WDBC."
                    if is_en
                    else "A EDA confirma que o pipeline parte de dados reais, numéricos, estáveis e sem valores ausentes no WDBC original."
                ),
            ),
            (
                "How to read labels" if is_en else "Como ler os rótulos",
                (
                    "The record class follows Scikit-learn: 0 = Malignant and 1 = Benign. This coding guides metrics and explainability."
                    if is_en
                    else "A classe do registro segue o padrão do Scikit-learn: 0 = Maligno e 1 = Benigno. Essa codificação orienta métricas e explicabilidade."
                ),
            ),
            (
                "Interpretation limit" if is_en else "Limite interpretativo",
                (
                    "Statistical patterns and correlations help discuss data behavior, but they do not prove medical causality."
                    if is_en
                    else "Padrões estatísticos e correlações ajudam a discutir o comportamento dos dados, mas não provam causalidade médica."
                ),
            ),
        ]
    )

    render_soft_divider()

    st.subheader("Class distribution" if is_en else "Distribuição das classes")
    st.write(
        (
            "The distribution shows how many samples belong to each class. It helps contextualize model comparison and metric selection."
            if is_en
            else "A distribuição mostra quantas amostras pertencem a cada classe. Ela "
            "ajuda a contextualizar a comparação dos modelos e a escolha de métricas."
        )
    )
    formatted_distribution = _format_target_distribution(target_distribution)
    st.dataframe(formatted_distribution, width="stretch", hide_index=True)
    st.bar_chart(formatted_distribution.set_index("Classe")["Contagem"])

    st.subheader("Attribute groups" if is_en else "Grupos de atributos")
    st.write(
        (
            "The 30 canonical attributes keep their original Scikit-learn technical names and are organized into three groups for easier reading."
            if is_en
            else "Os 30 atributos canônicos mantêm os nomes técnicos originais do "
            "Scikit-learn e são organizados em três grupos para facilitar leitura."
        )
    )
    render_card_grid(
        [
            (
                translate_group_name("mean", language),
                "10 mean measurements for the tabular attributes." if is_en else "10 medidas médias dos atributos tabulares.",
            ),
            (
                translate_group_name("error", language),
                "10 estimated variations associated with the same attributes." if is_en else "10 variações estimadas associadas aos mesmos atributos.",
            ),
            (
                translate_group_name("worst", language),
                "10 largest observed values for each attribute." if is_en else "10 maiores valores observados para cada atributo.",
            ),
        ]
    )
    with st.expander("View attributes by group" if is_en else "Ver atributos por grupo"):
        st.dataframe(_format_feature_group_summary(), width="stretch", hide_index=True)

    st.subheader("Descriptive statistics" if is_en else "Estatísticas descritivas")
    st.write(
        (
            "Statistical summary of the 30 numeric attributes. It includes mean, standard deviation, minimum, quartiles, and maximum."
            if is_en
            else "Resumo estatístico dos 30 atributos numéricos. As medidas incluem "
            "média, desvio padrão, mínimo, quartis e máximo."
        )
    )
    with st.expander(
        "View full descriptive statistics table" if is_en else "Ver tabela completa de estatísticas descritivas"
    ):
        st.dataframe(
            _format_feature_table(descriptive_statistics).round(4),
            width="stretch",
            hide_index=True,
        )

    st.subheader("Missing values" if is_en else "Valores ausentes")
    st.write(
        (
            "The original WDBC loaded by Scikit-learn has no missing values in the 30 attributes used by the project."
            if is_en
            else "O WDBC original carregado pelo Scikit-learn não possui valores "
            "ausentes nos 30 atributos usados pelo projeto."
        )
    )
    with st.expander("View missing values summary" if is_en else "Ver resumo de valores ausentes"):
        st.dataframe(missing_values_summary, width="stretch", hide_index=True)

    st.subheader(
        "Exploratory relationships with the record class"
        if is_en
        else "Relações exploratórias com a classe do registro"
    )
    st.write(
        (
            "The table lists the 10 strongest absolute correlations between attributes and the numeric record class. Because the class uses `0 = Malignant` and `1 = Benign`, the correlation sign requires care."
            if is_en
            else "A tabela lista as 10 maiores correlações absolutas entre atributos e "
            "classe numérica do registro. Como a classe usa `0 = Maligno` e "
            "`1 = Benigno`, o sinal da correlação precisa ser interpretado com cuidado."
        )
    )
    st.dataframe(
        _format_feature_table(top_target_correlations).round(4),
        width="stretch",
        hide_index=True,
    )
    st.info(
        (
            "Correlation does not imply medical causality. These patterns are useful for exploratory analysis and academic discussion, not for diagnosis."
            if is_en
            else "Correlação não implica causalidade médica. Estes padrões são úteis "
            "para análise exploratória e discussão acadêmica, não para diagnóstico."
        )
    )


render_page()
