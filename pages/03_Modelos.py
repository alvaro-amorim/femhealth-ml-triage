"""Página Streamlit de comparação e modelo final acadêmico da V1."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.models.compare import run_model_comparison
from src.models.persist import get_recommended_artifact_paths, recommended_artifacts_exist
from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_page_intro,
    render_soft_divider,
)
from src.ui.i18n import get_language, translate_target_label
from src.ui.theme import get_plotly_layout, get_theme_tokens


MODEL_LABELS = {
    "logistic_regression": "Regressão Logística",
    "decision_tree": "Árvore de Decisão",
    "knn": "KNN",
}

MODEL_LABELS_EN = {
    "logistic_regression": "Logistic Regression",
    "decision_tree": "Decision Tree",
    "knn": "KNN",
}

METRIC_COLUMNS = [
    "accuracy",
    "precision_malignant",
    "recall_malignant",
    "f1_malignant",
    "roc_auc_malignant",
]


def _model_label(model_name: str) -> str:
    labels = MODEL_LABELS_EN if get_language() == "en" else MODEL_LABELS
    return labels.get(model_name, model_name)


@st.cache_data(show_spinner=False)
def _load_comparison_payload() -> dict:
    """Run and cache the in-memory comparison for the current Streamlit session."""
    return run_model_comparison()


def _format_results_table(results: dict) -> pd.DataFrame:
    rows = []
    for model_name, metrics in results.items():
        rows.append(
            {
                "Modelo" if get_language() == "pt" else "Model": _model_label(model_name),
                **{metric: metrics[metric] for metric in METRIC_COLUMNS},
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values(
        by=["recall_malignant", "roc_auc_malignant", "f1_malignant"],
        ascending=False,
        )
        .round(4)
    )


def _format_ranking_table(ranking: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Posição" if get_language() == "pt" else "Rank": position,
                "Modelo" if get_language() == "pt" else "Model": _model_label(row["model_name"]),
                "recall_malignant": row["recall_malignant"],
                "roc_auc_malignant": row["roc_auc_malignant"],
                "f1_malignant": row["f1_malignant"],
            }
            for position, row in enumerate(ranking, start=1)
        ]
    ).round(4)


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
                "Modelo" if get_language() == "pt" else "Model": (
                    "Logistic Regression"
                    if get_language() == "en"
                    else recommended_candidate["selected_model_name"]
                ),
                **{metric: metrics[metric] for metric in METRIC_COLUMNS},
            }
        ]
    ).round(4)


def _build_roc_figure(roc_curves: dict, results: dict) -> go.Figure:
    """Build a didactic ROC curve with fixed 0-1 axes and AUC legend."""
    language = get_language()
    is_en = language == "en"
    tokens = get_theme_tokens()
    figure = go.Figure()
    line_colors = {
        "logistic_regression": tokens["accent_2"],
        "decision_tree": tokens["accent"],
        "knn": "#34D399",
    }
    for model_name, curve in roc_curves.items():
        auc = results[model_name]["roc_auc_malignant"]
        figure.add_trace(
            go.Scatter(
                x=curve["fpr"],
                y=curve["tpr"],
                mode="lines",
                name=f"{_model_label(model_name)} — AUC {auc:.3f}",
                line={"width": 3, "color": line_colors.get(model_name)},
            )
        )

    figure.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Reference" if is_en else "Referência",
            line={"dash": "dash", "color": tokens["subtle"], "width": 2},
        )
    )
    plotly_layout = get_plotly_layout()
    plotly_layout["xaxis"].update({"range": [0, 1], "dtick": 0.2})
    plotly_layout["yaxis"].update({"range": [0, 1], "dtick": 0.2})
    plotly_layout["legend"].update({"orientation": "h", "y": -0.25})
    chart_title = (
        "ROC Curve — Malignant class probability"
        if is_en
        else "Curva ROC — probabilidade da classe Maligno"
    )
    figure.update_layout(
        **plotly_layout,
        title={"text": chart_title, "font": {"color": tokens["text"]}},
        xaxis_title="False positive rate (FPR)" if is_en else "Taxa de falsos positivos (FPR)",
        yaxis_title="True positive rate (TPR)" if is_en else "Taxa de verdadeiros positivos (TPR)",
        height=520,
        margin={"l": 20, "r": 20, "t": 60, "b": 110},
    )
    return figure


def _confusion_matrix_interpretation(confusion_matrix: list[list[int]]) -> pd.DataFrame:
    """Return a didactic interpretation of a [0, 1] confusion matrix."""
    language = get_language()
    true_malignant = confusion_matrix[0][0]
    false_benign = confusion_matrix[0][1]
    false_malignant = confusion_matrix[1][0]
    true_benign = confusion_matrix[1][1]
    if language == "en":
        return pd.DataFrame(
            [
                {"Item": "True malignant records", "Count": true_malignant, "Meaning": "Malignant (0) records estimated as Malignant (0)."},
                {"Item": "False benign records", "Count": false_benign, "Meaning": "Malignant (0) records estimated as Benign (1) by the model."},
                {"Item": "True benign records", "Count": true_benign, "Meaning": "Benign (1) records estimated as Benign (1)."},
                {"Item": "False malignant records", "Count": false_malignant, "Meaning": "Benign (1) records estimated as Malignant (0) by the model."},
            ]
        )
    return pd.DataFrame(
        [
            {"Item": "Verdadeiros malignos", "Quantidade": true_malignant, "Significado": "Registros Maligno (0) estimados como Maligno (0)."},
            {"Item": "Falsos benignos", "Quantidade": false_benign, "Significado": "Registros Maligno (0) estimados como Benigno (1) pelo modelo."},
            {"Item": "Verdadeiros benignos", "Quantidade": true_benign, "Significado": "Registros Benigno (1) estimados como Benigno (1)."},
            {"Item": "Falsos malignos", "Quantidade": false_malignant, "Significado": "Registros Benigno (1) estimados como Maligno (0) pelo modelo."},
        ]
    )


def render_page() -> None:
    """Render the controlled initial model-comparison page."""
    apply_global_style()
    language = get_language()
    is_en = language == "en"
    render_page_intro(
        "Academic model decision center" if is_en else "Central de decisão do modelo acadêmico",
        "Model decision" if is_en else "Decisão do modelo",
        (
            "This page shows how candidate models were compared, why Logistic Regression was declared the final academic V1 model, and which evidence supports that technical decision."
            if is_en
            else "Esta tela mostra como os modelos candidatos foram comparados, por que "
            "a Regressão Logística foi declarada modelo final acadêmico da V1 e "
            "quais evidências sustentam essa decisão técnica."
        ),
    )
    render_ethics_notice(short=True)

    with st.spinner("Treinando e avaliando modelos candidatos em memória..."):
        payload = _load_comparison_payload()

    metadata = payload["metadata"]
    results = payload["results"]
    ranking = payload["ranking"]
    roc_curves = payload["roc_curves"]
    recommended_candidate = payload["recommended_candidate"]
    top_model = ranking[0]

    final_metrics = recommended_candidate["metrics"]
    final_confusion_matrix = top_model["confusion_matrix"]
    true_malignant = final_confusion_matrix[0][0]
    false_benign = final_confusion_matrix[0][1]
    false_malignant = final_confusion_matrix[1][0]
    true_benign = final_confusion_matrix[1][1]
    total_errors = false_benign + false_malignant

    st.subheader("Decision summary" if is_en else "Resumo da decisão")
    col_dataset, col_final, col_recall, col_auc = st.columns(4)
    col_dataset.metric("Dataset", "WDBC")
    col_final.metric(
        "Final academic model" if is_en else "Modelo final acadêmico",
        "Logistic Regression" if is_en else recommended_candidate["selected_model_name"],
    )
    col_recall.metric(
        "Malignant recall" if is_en else "Recall da classe Maligno",
        f"{final_metrics['recall_malignant']:.2%}",
    )
    col_auc.metric("ROC AUC", f"{final_metrics['roc_auc_malignant']:.3f}")

    col_errors, col_split, col_priority = st.columns(3)
    col_errors.metric("Test errors" if is_en else "Erros no teste", total_errors)
    col_split.metric("Test split" if is_en else "Split de teste", f"{metadata['test_size']:.0%}")
    col_priority.metric("Priority class" if is_en else "Classe prioritária", translate_target_label(0, language))

    st.caption(
        (
            f"Samples: {metadata['sample_count']} | Attributes: {metadata['feature_count']} | Train: {metadata['train_size']} | Test: {metadata['test_sample_count']} | random_state={metadata['random_state']}"
            if is_en
            else f"Amostras: {metadata['sample_count']} | Atributos: "
            f"{metadata['feature_count']} | Treino: {metadata['train_size']} | "
            f"Teste: {metadata['test_sample_count']} | random_state="
            f"{metadata['random_state']}"
        )
    )
    st.success(
        (
            f"In the test set, the model identified {true_malignant} of {true_malignant + false_benign} malignant records and {true_benign} of {true_benign + false_malignant} benign records."
            if is_en
            else f"No conjunto de teste, o modelo identificou {true_malignant} de {true_malignant + false_benign} registros malignos e {true_benign} de {true_benign + false_malignant} registros benignos."
        )
    )

    render_card_grid(
        [
            (
                "Why compare models" if is_en else "Por que comparar modelos",
                "The comparison avoids choosing an algorithm by preference and records quantitative evidence for V1." if is_en else "A comparação evita escolher um algoritmo por preferência e registra evidência quantitativa para a V1.",
            ),
            (
                "Main criterion" if is_en else "Critério principal",
                "The ranking prioritizes recall for Malignant (0), reducing the technical risk of missing that class in the test set." if is_en else "O ranking prioriza recall da classe Maligno (0), reduzindo o risco técnico de deixar essa classe sem atenção no teste.",
            ),
            (
                "Limited decision" if is_en else "Decisão limitada",
                "The choice is academic and reproducible; it does not make the app a real healthcare tool." if is_en else "A escolha é acadêmica e reproduzível; não transforma o app em ferramenta para uso real em saúde.",
            ),
        ]
    )

    render_soft_divider()

    with st.expander("Candidate models" if is_en else "Modelos candidatos"):
        st.markdown(
            (
                "- Logistic Regression with `StandardScaler`\n"
                "- Decision Tree with passthrough\n"
                "- KNN with `StandardScaler`"
                if is_en
                else "- Regressão Logística com `StandardScaler`\n"
                "- Árvore de Decisão com passthrough\n"
                "- KNN com `StandardScaler`"
            )
        )

    st.subheader("Metrics table" if is_en else "Tabela de métricas")
    st.dataframe(
        _format_results_table(results),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Technical ranking" if is_en else "Ranking técnico")
    st.write(
        (
            "The ranking prioritizes `recall_malignant`; ties use `roc_auc_malignant` and then `f1_malignant`. This ranking supports the final academic V1 model decision."
            if is_en
            else "O ranking prioriza `recall_malignant`; em caso de empate, usa "
            "`roc_auc_malignant` e depois `f1_malignant`. Esse ranking fundamenta "
            "a seleção do modelo final acadêmico da V1."
        )
    )
    st.dataframe(
        _format_ranking_table(ranking),
        width="stretch",
        hide_index=True,
    )

    with st.expander("How to interpret these metrics" if is_en else "Como interpretar as métricas nesta comparação"):
        if is_en:
            st.markdown(
                """
                - `recall_malignant`: priority metric for the class that receives the most technical attention in the project.
                - `roc_auc_malignant`: evaluates class separation using the probability of Malignant (0).
                - `f1_malignant`: summarizes balance between precision and recall for Malignant (0).
                - `accuracy`: useful as a general reference, but not the main selection criterion.
                """
            )
        else:
            st.markdown(
                """
                - `recall_malignant`: métrica prioritária para a classe de maior atenção técnica no projeto.
                - `roc_auc_malignant`: avalia separação entre classes usando probabilidade de Maligno (0).
                - `f1_malignant`: resume equilíbrio entre precision e recall para Maligno (0).
                - `accuracy`: útil como referência geral, mas não é o critério principal de seleção.
                """
            )

    st.subheader("Final academic V1 model" if is_en else "Modelo final acadêmico da V1")
    st.write(
        (
            "The persisted Logistic Regression is the final academic V1/MVP model. "
            "The decision is technical and limited: it uses `recall_malignant` as "
            "the primary criterion, followed by `roc_auc_malignant` and "
            "`f1_malignant` in case of ties."
            if is_en
            else "A Regressão Logística persistida é o modelo final acadêmico da V1/MVP. "
            "A decisão é técnica e limitada: usa `recall_malignant` como critério "
            "primário, seguido de `roc_auc_malignant` e `f1_malignant` em caso de empate."
        )
    )
    st.metric(
        "Final academic model" if is_en else "Modelo final acadêmico",
        "Logistic Regression" if is_en else recommended_candidate["selected_model_name"],
    )
    with st.expander("View final academic model metrics" if is_en else "Ver métricas do modelo final acadêmico"):
        st.dataframe(
            _format_recommended_candidate_metrics(recommended_candidate),
            width="stretch",
            hide_index=True,
        )
    st.caption(
        (
            "Final academic V1 model selected from the technical ranking: malignant recall as primary criterion, malignant ROC AUC as first tie-breaker, and malignant F1 as second tie-breaker."
            if is_en
            else "Modelo final acadêmico da V1 definido a partir do ranking técnico: "
            "recall da classe maligna como critério primário, ROC AUC maligno "
            "como primeiro desempate e F1 maligno como segundo desempate."
        )
    )
    st.warning(
        (
            "This decision is academic and demonstrative. It is not a medical diagnosis, does not define a tool for real healthcare use, and does not replace clinical analysis, pathology reports, or professional decisions."
            if is_en
            else "Esta decisão é acadêmica e demonstrativa. Ela não é diagnóstico médico, "
            "não define uma ferramenta para uso real em saúde e não substitui análise "
            "clínica, laudo anatomopatológico ou decisão profissional."
        )
    )

    st.subheader("Persisted artifacts" if is_en else "Artefatos persistidos")
    artifact_paths = get_recommended_artifact_paths()
    artifact_status = recommended_artifacts_exist()
    all_artifacts_available = all(artifact_status.values())
    st.write(
        (
            "Controlled persistence allows prediction and explainability to use the same pipeline reproducibly. This does not turn the project into a clinical tool."
            if is_en
            else "A persistência controlada permite que predição e explicabilidade usem "
            "o mesmo pipeline de forma reprodutível. Isso não transforma o projeto "
            "em ferramenta clínica."
        )
    )
    st.metric(
        "Persisted final academic model" if is_en else "Modelo final acadêmico persistido",
        ("yes" if all_artifacts_available else "no") if is_en else ("sim" if all_artifacts_available else "não"),
    )
    with st.expander("View artifact paths" if is_en else "Ver caminhos dos artefatos"):
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

    st.subheader("ROC Curve" if is_en else "Curva ROC")
    st.write(
        (
            "The ROC Curve evaluates class separation across thresholds. Here it uses the probability of the Malignant class (0), with fixed 0-1 axes and a diagonal reference line."
            if is_en
            else "A Curva ROC avalia a separação entre classes em diferentes limiares. "
            "Aqui ela usa a probabilidade da classe Maligno (0), com eixos fixos "
            "de 0 a 1 e linha diagonal de referência."
        )
    )
    with st.expander(
        "View ROC curve technical detail" if is_en else "Ver detalhe técnico da Curva ROC",
        expanded=True,
    ):
        st.plotly_chart(
            _build_roc_figure(roc_curves, results),
            config={"displayModeBar": False},
            width="stretch",
        )
    st.caption(
        (
            "FPR = false positive rate; TPR = true positive rate/recall for Malignant (0) at each threshold."
            if is_en
            else "FPR = taxa de falsos positivos; TPR = taxa de verdadeiros positivos/recall da classe Maligno (0) em cada limiar."
        )
    )

    st.subheader("Confusion matrix of the final academic model" if is_en else "Matriz de confusão do modelo final acadêmico")
    st.caption(
        (
            "Class order: 0 = Malignant, 1 = Benign. The matrix below is calculated on the test set."
            if is_en
            else "Ordem das classes: 0 = Maligno, 1 = Benigno. A matriz abaixo é "
            "calculada no conjunto de teste."
        )
    )
    confusion_matrix = pd.DataFrame(
        final_confusion_matrix,
        index=[
            "Actual Malignant (0)" if is_en else "Real Maligno (0)",
            "Actual Benign (1)" if is_en else "Real Benigno (1)",
        ],
        columns=[
            "Predicted Malignant (0)" if is_en else "Previsto Maligno (0)",
            "Predicted Benign (1)" if is_en else "Previsto Benigno (1)",
        ],
    )
    st.dataframe(confusion_matrix, width="stretch")
    st.dataframe(
        _confusion_matrix_interpretation(final_confusion_matrix),
        width="stretch",
        hide_index=True,
    )

    st.info(
        (
            "There is a technical artifact for the final academic V1 model. Prediction and explainability consume this artifact without turning it into a tool for real healthcare use."
            if is_en
            else "Há um artefato técnico do modelo final acadêmico da V1. A predição "
            "individual e a explicabilidade consomem esse artefato sem transformá-lo "
            "em ferramenta para uso real em saúde."
        )
    )


render_page()
