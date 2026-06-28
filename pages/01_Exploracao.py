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
    formatted = distribution.copy()
    formatted["Classe"] = formatted.apply(
        lambda row: f"{int(row['target'])} = {row['class_name']}", axis=1
    )
    formatted = formatted.rename(
        columns={
            "count": "Contagem",
            "percentage": "Percentual (%)",
        }
    )
    formatted["Percentual (%)"] = formatted["Percentual (%)"].round(2)
    return formatted[["Classe", "Contagem", "Percentual (%)"]]


def render_page() -> None:
    """Render the WDBC exploratory-data-analysis page."""
    st.title("Exploração dos Dados")
    st.warning(
        "Análise exploratória acadêmica do dataset público WDBC. Esta página "
        "não realiza diagnóstico médico e não substitui avaliação clínica, "
        "laudo ou decisão profissional."
    )
    st.write(
        "O WDBC contém 30 atributos numéricos derivados de características "
        "celulares e é carregado localmente via Scikit-learn, sem download "
        "manual ou dados inventados."
    )

    payload = _load_eda_payload()
    overview = payload["overview"]
    target_distribution = payload["target_distribution"]
    feature_group_summary = payload["feature_group_summary"]
    descriptive_statistics = payload["descriptive_statistics"]
    missing_values_summary = payload["missing_values_summary"]
    top_target_correlations = payload["top_target_correlations"]

    st.subheader("Visão geral")
    col_dataset, col_samples, col_features = st.columns(3)
    col_dataset.metric("Dataset", "WDBC")
    col_samples.metric("Amostras", overview["sample_count"])
    col_features.metric("Features", overview["feature_count"])

    col_classes, col_priority, col_missing = st.columns(3)
    col_classes.metric("Classes", overview["class_count"])
    col_priority.metric("Classe prioritária", "malignant (0)")
    col_missing.metric("Valores ausentes", overview["missing_values_total"])

    st.caption(
        "Mapeamento oficial do Scikit-learn: 0 = malignant; 1 = benign. "
        "As features não são renomeadas no backend."
    )

    st.subheader("Distribuição do target")
    st.write(
        "A tabela e o gráfico abaixo mostram a distribuição das duas classes "
        "do WDBC. O rótulo `0` representa malignant e o rótulo `1` representa "
        "benign."
    )
    formatted_distribution = _format_target_distribution(target_distribution)
    st.dataframe(formatted_distribution, width="stretch", hide_index=True)
    st.bar_chart(formatted_distribution.set_index("Classe")["Contagem"])

    st.subheader("Grupos de features")
    st.write(
        "As 30 features canônicas estão organizadas em três grupos de 10 "
        "variáveis: médias (`mean`), erros padrão (`error`) e piores valores "
        "observados (`worst`)."
    )
    st.dataframe(
        feature_group_summary[["group", "feature_count", "features"]],
        width="stretch",
        hide_index=True,
    )

    st.subheader("Estatísticas descritivas")
    st.write(
        "Resumo estatístico das 30 features numéricas. As medidas incluem "
        "média, desvio padrão, mínimo, quartis e máximo."
    )
    with st.expander("Ver tabela completa de estatísticas descritivas"):
        st.dataframe(
            descriptive_statistics.round(4),
            width="stretch",
            hide_index=True,
        )

    st.subheader("Valores ausentes")
    st.write(
        "O WDBC original carregado pelo Scikit-learn não possui valores "
        "ausentes nas 30 features usadas pelo projeto."
    )
    with st.expander("Ver resumo de valores ausentes"):
        st.dataframe(missing_values_summary, width="stretch", hide_index=True)

    st.subheader("Correlações exploratórias com o target")
    st.write(
        "A tabela lista as 10 maiores correlações absolutas entre features e "
        "target numérico. Como o target usa `0 = malignant` e `1 = benign`, o "
        "sinal da correlação precisa ser interpretado com cuidado."
    )
    st.dataframe(top_target_correlations.round(4), width="stretch", hide_index=True)
    st.info(
        "Correlação não implica causalidade médica. Estes padrões são úteis "
        "para análise exploratória e discussão acadêmica, não para diagnóstico."
    )


render_page()
