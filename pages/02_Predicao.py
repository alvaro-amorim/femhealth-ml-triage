"""Página Streamlit de predição individual acadêmica."""

import pandas as pd
import streamlit as st

from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_GROUPS, FEATURE_NAMES
from src.models.persist import get_recommended_artifact_paths
from src.models.predict import (
    ACADEMIC_PREDICTION_WARNING,
    build_reference_sample,
    load_prediction_artifacts,
    predict_single_sample,
)


REFERENCE_OPTIONS = {
    "Exemplo real WDBC — malignant (0)": 0,
    "Exemplo real WDBC — benign (1)": 1,
}
LAST_RESULT_KEY = "last_prediction_result"
LAST_INPUT_KEY = "last_prediction_input_sample"


def _render_manual_input(reference_sample: pd.DataFrame) -> pd.DataFrame:
    values = {}
    reference_row = reference_sample.iloc[0]

    for group_name, group_features in FEATURE_GROUPS.items():
        with st.expander(f"Features do grupo `{group_name}`", expanded=True):
            st.caption(
                "Valores reais do WDBC são usados como referência inicial. "
                "Ajustes manuais devem manter o formato numérico esperado."
            )
            columns = st.columns(2)
            for position, feature_name in enumerate(group_features):
                column = columns[position % 2]
                values[feature_name] = column.number_input(
                    feature_name,
                    min_value=0.0,
                    value=float(reference_row[feature_name]),
                    format="%.6f",
                    help="Feature numérica canônica do dataset WDBC.",
                )

    return pd.DataFrame([values], columns=list(FEATURE_NAMES))


def _render_prediction_result(result: dict, input_sample: pd.DataFrame) -> None:
    """Render the latest prediction result before detailed input values."""
    st.subheader("Resultado da estimativa acadêmica")
    st.success(
        "Estimativa acadêmica executada. Interprete os valores abaixo apenas "
        "como saída do modelo para demonstração educacional."
    )

    col_class, col_malignant, col_benign = st.columns(3)
    col_class.metric(
        "Classe estimada pelo modelo",
        f"{result['predicted_class']} ({result['predicted_label']})",
    )
    col_malignant.metric(
        "Probabilidade estimada de malignant",
        f"{result['probability_malignant']:.2%}",
    )
    col_benign.metric(
        "Probabilidade estimada de benign",
        f"{result['probability_benign']:.2%}",
    )

    st.warning(
        "Esta saída representa apenas a estimativa acadêmica do modelo. Não "
        "é diagnóstico médico, não substitui avaliação clínica, não substitui "
        "laudo anatomopatológico e não substitui decisão profissional. O médico "
        "sempre deve ter a palavra final."
    )
    st.info(result["academic_warning"])

    with st.expander("Ver valores usados na estimativa"):
        st.dataframe(
            input_sample.T.rename(columns={input_sample.index[0]: "Valor usado"}),
            width="stretch",
        )


def render_page() -> None:
    """Render the individual academic prediction page."""
    st.title("Predição Individual")
    st.warning(
        "Esta página executa uma estimativa acadêmica do modelo para uma amostra "
        "tabular no formato WDBC. Não é diagnóstico médico, não substitui "
        "avaliação clínica, não substitui laudo anatomopatológico e não substitui "
        "decisão profissional. O médico sempre deve ter a palavra final."
    )

    st.write(
        "A classe `malignant (0)` é tratada como classe prioritária apenas para "
        "análise técnica de Machine Learning. A saída do modelo deve ser lida "
        "como apoio à triagem analítica em contexto educacional."
    )

    artifact_paths = get_recommended_artifact_paths()

    try:
        artifacts = load_prediction_artifacts()
    except (FileNotFoundError, TypeError, ValueError) as error:
        st.error(f"Não foi possível carregar os artefatos de predição: {error}")
        return

    metrics_payload = artifacts["metrics"]
    metadata = metrics_payload.get("metadata", {})

    st.subheader("Status do modelo")
    col_model, col_features, col_priority = st.columns(3)
    col_model.metric(
        "Modelo carregado",
        metrics_payload.get("selected_model_name", "Modelo persistido"),
    )
    col_features.metric("Features esperadas", EXPECTED_FEATURE_COUNT)
    col_priority.metric("Classe prioritária", "malignant (0)")

    st.caption(
        f"Modelo: `{artifact_paths['model']}` | Métricas: "
        f"`{artifact_paths['metrics']}` | Features: "
        f"`{artifact_paths['feature_names']}`"
    )
    st.caption(
        "Artefato gerado para fins acadêmicos. Isso não transforma o projeto em "
        "ferramenta clínica ou sistema para uso real em saúde."
    )

    if metadata:
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Dataset": metadata.get("dataset", "WDBC"),
                        "test_size": metadata.get("test_size"),
                        "random_state": metadata.get("random_state"),
                        "priority_label": metadata.get("priority_label"),
                        "priority_class": metadata.get("priority_class"),
                    }
                ]
            ),
            width="stretch",
            hide_index=True,
        )

    st.subheader("Entrada da amostra")
    st.write(
        "Use um exemplo real do dataset público WDBC como ponto de partida e, se "
        "necessário, ajuste manualmente as 30 features. Os exemplos são apenas "
        "demonstrações do dataset público, não casos clínicos reais."
    )

    selected_reference = st.selectbox(
        "Exemplo de referência do WDBC",
        list(REFERENCE_OPTIONS.keys()),
    )
    target_label = REFERENCE_OPTIONS[selected_reference]
    reference_sample = build_reference_sample(target_label)
    input_sample = _render_manual_input(reference_sample)

    st.caption(
        "A entrada é validada com exatamente 30 features canônicas, na ordem "
        "esperada, sem colunas extras, sem colunas ausentes, sem nulos e com "
        "valores numéricos."
    )

    if st.button("Executar estimativa acadêmica"):
        try:
            result = predict_single_sample(input_sample)
        except (TypeError, ValueError) as error:
            st.error(f"Entrada inválida para predição acadêmica: {error}")
            return

        st.session_state[LAST_RESULT_KEY] = result
        st.session_state[LAST_INPUT_KEY] = input_sample.copy(deep=True)

    if LAST_RESULT_KEY in st.session_state and LAST_INPUT_KEY in st.session_state:
        _render_prediction_result(
            st.session_state[LAST_RESULT_KEY],
            st.session_state[LAST_INPUT_KEY],
        )

    st.info(ACADEMIC_PREDICTION_WARNING)


render_page()
