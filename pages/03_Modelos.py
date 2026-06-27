"""Página Streamlit de comparação inicial de modelos candidatos."""

import pandas as pd
import streamlit as st

from src.models.compare import run_model_comparison
from src.models.persist import get_recommended_artifact_paths, recommended_artifacts_exist


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


def _format_roc_curve_table(roc_curves: dict) -> pd.DataFrame:
    """Return ROC curve points in long format for display."""
    rows = []
    for model_name, curve in roc_curves.items():
        model_label = MODEL_LABELS.get(model_name, model_name)
        for fpr, tpr, threshold in zip(
            curve["fpr"], curve["tpr"], curve["thresholds"]
        ):
            rows.append(
                {
                    "Modelo": model_label,
                    "FPR": fpr,
                    "TPR": tpr,
                    "Threshold": threshold,
                }
            )

    return pd.DataFrame(rows)


def _format_recommended_candidate_metrics(recommended_candidate: dict) -> pd.DataFrame:
    """Return the recommended candidate metrics as a one-row table."""
    metrics = recommended_candidate["metrics"]
    return pd.DataFrame(
        [
            {
                "Modelo": recommended_candidate["selected_model_name"],
                **{metric: metrics[metric] for metric in METRIC_COLUMNS},
            }
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
    roc_curves = payload["roc_curves"]
    recommended_candidate = payload["recommended_candidate"]
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
        width="stretch",
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
        width="stretch",
        hide_index=True,
    )

    st.subheader("Modelo candidato recomendado")
    st.write(
        "O modelo candidato recomendado é o modelo melhor ranqueado nesta "
        "comparação acadêmica inicial. A seleção usa `recall_malignant` como "
        "critério primário, seguido de `roc_auc_malignant` e `f1_malignant` em "
        "caso de empate."
    )
    st.metric("Candidato recomendado", recommended_candidate["selected_model_name"])
    st.dataframe(
        _format_recommended_candidate_metrics(recommended_candidate),
        width="stretch",
        hide_index=True,
    )
    st.caption(recommended_candidate["reason"])
    st.warning(
        "Esta seleção é técnica, acadêmica e inicial. Ela não é diagnóstico "
        "médico, não define uma ferramenta para uso real em saúde e a "
        "persistência do artefato é apenas técnica. SHAP e explicabilidade "
        "final serão tratados posteriormente."
    )

    st.subheader("Artefatos persistidos")
    artifact_paths = get_recommended_artifact_paths()
    artifact_status = recommended_artifacts_exist()
    all_artifacts_available = all(artifact_status.values())
    st.write(
        "A persistência controlada do candidato recomendado permite que etapas "
        "futuras usem o mesmo pipeline de forma reprodutível. Isso não transforma "
        "o projeto em ferramenta clínica."
    )
    st.metric(
        "Modelo candidato persistido",
        "sim" if all_artifacts_available else "não",
    )
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Artefato": artifact_name,
                    "Caminho": str(artifact_paths[artifact_name]),
                    "Existe": artifact_status[artifact_name],
                }
                for artifact_name in artifact_paths
            ]
        ),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Curva ROC")
    st.write(
        "A curva ROC avalia a separação entre classes em diferentes limiares. "
        "Neste projeto, ela usa a probabilidade da classe maligna (`0 = "
        "malignant`) e não representa diagnóstico médico."
    )
    roc_curve_table = _format_roc_curve_table(roc_curves)
    roc_chart_data = (
        roc_curve_table.pivot_table(
            index="FPR",
            columns="Modelo",
            values="TPR",
            aggfunc="max",
        )
        .sort_index()
    )
    st.line_chart(roc_chart_data)
    st.caption(
        "FPR = taxa de falsos positivos; TPR = sensibilidade/recall da classe "
        "maligna em cada limiar."
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
    st.dataframe(confusion_matrix, width="stretch")

    st.info(
        "Há um artefato técnico do candidato recomendado para fins acadêmicos. "
        "Predição individual final, SHAP e explicabilidade final serão tratados "
        "em etapas posteriores."
    )


render_page()
