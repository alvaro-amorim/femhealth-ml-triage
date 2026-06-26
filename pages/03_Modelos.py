"""Página Streamlit de comparação inicial de modelos candidatos."""

import pandas as pd
import streamlit as st

from src.models.compare import run_model_comparison


MODEL_LABELS = {
    "logistic_regression": "Regressão Logística",
    "decision_tree": "Árvore de Decisão",
    "knn": "KNN",
}

METRIC_COLUMNS = [
    "accuracy",
    "precision_malignant",
    "recall_malignant",
    "f1_malignant",
    "roc_auc_malignant",
]


@st.cache_data(show_spinner=False)
def _load_comparison_payload() -> dict:
    """Run and cache the in-memory comparison for the current Streamlit session."""
    return run_model_comparison()


def _format_results_table(results: dict) -> pd.DataFrame:
    rows = []
    for model_name, metrics in results.items():
        rows.append(
            {
                "Modelo": MODEL_LABELS.get(model_name, model_name),
                **{metric: metrics[metric] for metric in METRIC_COLUMNS},
            }
        )
    return pd.DataFrame(rows).sort_values(
        by=["recall_malignant", "roc_auc_malignant", "f1_malignant"],
        ascending=False,
    )


def _format_ranking_table(ranking: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Posição": position,
                "Modelo": MODEL_LABELS.get(row["model_name"], row["model_name"]),
                "recall_malignant": row["recall_malignant"],
                "roc_auc_malignant": row["roc_auc_malignant"],
                "f1_malignant": row["f1_malignant"],
            }
            for position, row in enumerate(ranking, start=1)
        ]
    )


def render_page() -> None:
    """Render the controlled initial model-comparison page."""
    st.title("Comparação Inicial de Modelos")
    st.warning(
        "Comparação acadêmica inicial. Esta aplicação não realiza diagnóstico "
        "médico e não substitui avaliação clínica, laudo ou decisão profissional."
    )

    with st.spinner("Treinando e avaliando modelos candidatos em memória..."):
        payload = _load_comparison_payload()

    metadata = payload["metadata"]
    results = payload["results"]
    ranking = payload["ranking"]
    top_model = ranking[0]

    st.subheader("Configuração da comparação")
    st.write(
        "O fluxo usa o WDBC carregado localmente via Scikit-learn, split "
        "treino/teste estratificado e avaliação no conjunto de teste."
    )
    col_dataset, col_split, col_priority = st.columns(3)
    col_dataset.metric("Dataset", "WDBC")
    col_split.metric("Split de teste", f"{metadata['test_size']:.0%}")
    col_priority.metric("Classe prioritária", "malignant (0)")

    st.caption(
        f"Amostras: {metadata['sample_count']} | Features: "
        f"{metadata['feature_count']} | Treino: {metadata['train_size']} | "
        f"Teste: {metadata['test_sample_count']} | random_state="
        f"{metadata['random_state']}"
    )

    st.subheader("Modelos candidatos")
    st.markdown(
        "- Regressão Logística com `StandardScaler`\n"
        "- Árvore de Decisão com passthrough\n"
        "- KNN com `StandardScaler`"
    )

    st.subheader("Tabela de métricas")
    st.dataframe(
        _format_results_table(results),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Ranking inicial")
    st.write(
        "O ranking prioriza `recall_malignant`; em caso de empate, usa "
        "`roc_auc_malignant` e depois `f1_malignant`. Esse ranking organiza a "
        "análise, mas ainda não define um modelo final."
    )
    st.dataframe(
        _format_ranking_table(ranking),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Matriz de confusão do modelo melhor ranqueado nesta comparação inicial")
    st.caption(
        "Ordem das classes: 0 = malignant, 1 = benign. A matriz abaixo é "
        "calculada no conjunto de teste."
    )
    confusion_matrix = pd.DataFrame(
        top_model["confusion_matrix"],
        index=["Real malignant (0)", "Real benign (1)"],
        columns=["Previsto malignant (0)", "Previsto benign (1)"],
    )
    st.dataframe(confusion_matrix, use_container_width=True)

    st.info(
        "Ainda não há modelo final persistido. A seleção final, artefatos "
        "`.joblib`, métricas salvas e explicabilidade serão tratados em etapas "
        "posteriores."
    )


render_page()
