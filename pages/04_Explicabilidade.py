"""Página Streamlit de explicabilidade acadêmica do modelo persistido."""

import pandas as pd
import streamlit as st

from src.models.explain import (
    EXPLAINABILITY_WARNING,
    build_reference_sample_for_explanation,
    get_global_feature_importance,
    get_shap_global_feature_importance,
    get_top_local_contributions,
    load_explainability_context,
)


REFERENCE_OPTIONS = {
    "Exemplo real WDBC — malignant (0)": 0,
    "Exemplo real WDBC — benign (1)": 1,
}


def _format_global_importance_table(global_importance: pd.DataFrame) -> pd.DataFrame:
    return global_importance.loc[
        :,
        [
            "feature",
            "coefficient",
            "coefficient_abs",
            "interpretive_direction",
        ],
    ].rename(
        columns={
            "feature": "Feature",
            "coefficient": "Coeficiente",
            "coefficient_abs": "Importância absoluta",
            "interpretive_direction": "Direção interpretativa acadêmica",
        }
    )


def _format_local_contributions_table(local_contributions: pd.DataFrame) -> pd.DataFrame:
    return local_contributions.loc[
        :,
        [
            "feature",
            "value",
            "coefficient",
            "contribution",
            "contribution_abs",
            "interpretive_direction",
        ],
    ].rename(
        columns={
            "feature": "Feature",
            "value": "Valor original",
            "coefficient": "Coeficiente",
            "contribution": "Contribuição local",
            "contribution_abs": "Contribuição absoluta",
            "interpretive_direction": "Direção interpretativa acadêmica",
        }
    )


def render_page() -> None:
    """Render the explainability page."""
    st.title("Explicabilidade")
    st.warning(
        "Esta página apresenta explicabilidade acadêmica do comportamento do "
        "modelo persistido. Ela não substitui diagnóstico médico, não substitui "
        "avaliação clínica, não substitui laudo anatomopatológico e não substitui "
        "decisão profissional. O médico sempre deve ter a palavra final."
    )
    st.info(
        "Explicabilidade não implica causalidade médica. As features não devem "
        "ser lidas como recomendação médica nem como prova de decisão clínica."
    )

    try:
        context = load_explainability_context()
    except (FileNotFoundError, TypeError, ValueError) as error:
        st.error(f"Não foi possível carregar o contexto de explicabilidade: {error}")
        return

    metadata = context["metadata"]
    st.subheader("Status do modelo")
    col_model, col_dataset = st.columns(2)
    col_model.metric("Modelo final acadêmico", metadata["model_name"])
    col_dataset.metric("Dataset", "WDBC")
    col_priority, col_features = st.columns(2)
    col_priority.metric("Classe prioritária técnica", "malignant (0)")
    col_features.metric("Features", metadata["feature_count"])

    st.caption(
        "O modelo persistido é um pipeline com `StandardScaler` e Regressão "
        "Logística. A interpretação abaixo é técnica e acadêmica."
    )

    st.subheader("Importância global das features")
    st.write(
        "A importância global usa os coeficientes da Regressão Logística em "
        "valor absoluto. Como o WDBC usa `0 = malignant` e `1 = benign`, o sinal "
        "dos coeficientes deve ser interpretado com cuidado: coeficientes "
        "positivos favorecem `benign (1)` no comportamento do modelo, enquanto "
        "coeficientes negativos favorecem `malignant (0)`."
    )
    global_importance = get_global_feature_importance(context)
    top_global = global_importance.head(15)
    st.bar_chart(top_global.set_index("feature")["coefficient_abs"])
    with st.expander("Ver tabela completa de importância global"):
        st.dataframe(
            _format_global_importance_table(global_importance).round(4),
            width="stretch",
            hide_index=True,
        )

    st.subheader("SHAP opcional")
    shap_payload = get_shap_global_feature_importance(context)
    if shap_payload["available"]:
        st.success(shap_payload["message"])
        with st.expander("Ver tabela SHAP calculada em memória"):
            st.dataframe(
                shap_payload["data"].round(4),
                width="stretch",
                hide_index=True,
            )
    else:
        st.info(shap_payload["message"])
        st.caption(
            "O fallback por coeficientes permanece válido para explicar o "
            "comportamento linear do modelo persistido nesta etapa."
        )

    st.subheader("Explicação local de uma amostra")
    st.write(
        "Selecione um exemplo real do WDBC para ver as 10 features com maiores "
        "contribuições locais em valor absoluto. A saída é uma interpretação "
        "acadêmica do modelo para uma amostra tabular pública, não uma explicação "
        "clínica real."
    )
    selected_reference = st.selectbox(
        "Exemplo de referência do WDBC",
        list(REFERENCE_OPTIONS.keys()),
    )
    target_label = REFERENCE_OPTIONS[selected_reference]
    reference_sample = build_reference_sample_for_explanation(target_label)
    local_contributions = get_top_local_contributions(reference_sample, context=context)
    st.dataframe(
        _format_local_contributions_table(local_contributions).round(4),
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "Contribuições positivas favorecem `benign (1)` e contribuições negativas "
        "favorecem `malignant (0)` no comportamento do classificador linear."
    )
    st.warning(EXPLAINABILITY_WARNING)


render_page()
