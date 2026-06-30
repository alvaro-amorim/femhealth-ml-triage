"""Página Streamlit de explicabilidade acadêmica do modelo persistido."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.models.explain import (
    EXPLAINABILITY_WARNING,
    build_reference_sample_for_explanation,
    get_global_feature_importance,
    get_shap_global_feature_importance,
    get_top_local_contributions,
    load_explainability_context,
)
from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_page_intro,
    render_soft_divider,
)
from src.ui.feature_dictionary import translate_feature_name
from src.ui.i18n import get_language, translate_target_label
from src.ui.theme import get_plotly_layout, get_theme_tokens


def _reference_options() -> dict[str, int]:
    if get_language() == "en":
        return {
            "Real WDBC example — Malignant (0)": 0,
            "Real WDBC example — Benign (1)": 1,
        }
    return {
        "Exemplo real WDBC — Maligno (0)": 0,
        "Exemplo real WDBC — Benigno (1)": 1,
    }


def _format_direction(value: float, language: str) -> str:
    """Translate coefficient/contribution direction for UI presentation."""
    if language == "en":
        return (
            "pulled the estimate toward Malignant (0)"
            if value < 0
            else "pulled the estimate toward Benign (1)"
        )
    return (
        "puxou a estimativa para Maligno (0)"
        if value < 0
        else "puxou a estimativa para Benigno (1)"
    )


def _format_global_importance_table(global_importance: pd.DataFrame) -> pd.DataFrame:
    language = get_language()
    table = global_importance.loc[
        :,
        [
            "feature",
            "coefficient",
            "coefficient_abs",
            "interpretive_direction",
        ],
    ].copy()
    table.insert(
        0,
        "Attribute" if language == "en" else "Atributo",
        table["feature"].map(lambda feature: translate_feature_name(feature, language)),
    )
    table["interpretive_direction"] = table["coefficient"].map(
        lambda value: _format_direction(float(value), language)
    )
    return table.rename(
        columns={
            "feature": "Technical name" if language == "en" else "Nome técnico",
            "coefficient": "Coefficient" if language == "en" else "Coeficiente",
            "coefficient_abs": "Absolute importance" if language == "en" else "Importância absoluta",
            "interpretive_direction": "Academic interpretive direction" if language == "en" else "Direção interpretativa acadêmica",
        }
    )


def _format_local_contributions_table(local_contributions: pd.DataFrame) -> pd.DataFrame:
    language = get_language()
    table = local_contributions.loc[
        :,
        [
            "feature",
            "value",
            "coefficient",
            "contribution",
            "contribution_abs",
            "interpretive_direction",
        ],
    ].copy()
    table.insert(
        0,
        "Attribute" if language == "en" else "Atributo",
        table["feature"].map(lambda feature: translate_feature_name(feature, language)),
    )
    table["interpretive_direction"] = table["contribution"].map(
        lambda value: _format_direction(float(value), language)
    )
    return table.rename(
        columns={
            "feature": "Technical name" if language == "en" else "Nome técnico",
            "value": "Original value" if language == "en" else "Valor original",
            "coefficient": "Coefficient" if language == "en" else "Coeficiente",
            "contribution": "Influence in this example" if language == "en" else "Influência neste exemplo",
            "contribution_abs": "Absolute influence" if language == "en" else "Influência absoluta",
            "interpretive_direction": "Academic interpretive direction" if language == "en" else "Direção interpretativa acadêmica",
        }
    )


def render_page() -> None:
    """Render the explainability page."""
    apply_global_style()
    language = get_language()
    is_en = language == "en"
    render_page_intro(
        "Why did the model estimate this?" if is_en else "Por que o modelo estimou isso?",
        "Model interpretation" if is_en else "Interpretação do modelo",
        (
            "Explainability helps understand the statistical behavior of the final academic model by combining global attribute importance and influence in one selected example."
            if is_en
            else "A explicabilidade ajuda a entender o comportamento estatístico do "
            "modelo final acadêmico, combinando importância global dos atributos "
            "e influência em um exemplo selecionado."
        ),
    )
    render_ethics_notice(short=True)
    st.info(
        (
            "Explainability does not imply medical causality. Attributes must not be read as medical recommendations or as proof of a professional decision."
            if is_en
            else "Explicabilidade não implica causalidade médica. Os atributos não devem "
            "ser lidos como recomendação médica nem como prova de decisão clínica."
        )
    )

    try:
        context = load_explainability_context()
    except (FileNotFoundError, TypeError, ValueError) as error:
        st.error(f"Não foi possível carregar o contexto de explicabilidade: {error}")
        return

    metadata = context["metadata"]
    st.subheader("Model status" if is_en else "Status do modelo")
    col_model, col_dataset = st.columns(2)
    col_model.metric(
        "Final academic model" if is_en else "Modelo final acadêmico",
        "Logistic Regression" if is_en else metadata["model_name"],
    )
    col_dataset.metric("Dataset", "WDBC")
    col_priority, col_features = st.columns(2)
    col_priority.metric("Technical priority class" if is_en else "Classe prioritária técnica", translate_target_label(0, language))
    col_features.metric("Attributes" if is_en else "Atributos", metadata["feature_count"])

    st.caption(
        (
            "The persisted model is a pipeline with `StandardScaler` and Logistic "
            "Regression. The interpretation below is technical and academic."
            if is_en
            else "O modelo persistido é um pipeline com `StandardScaler` e Regressão "
            "Logística. A interpretação abaixo é técnica e acadêmica."
        )
    )

    render_card_grid(
        [
            (
                "Global importance" if is_en else "Importância global",
                "Shows which attributes have the highest overall weight in the linear model behavior." if is_en else "Mostra quais atributos têm maior peso geral no comportamento do modelo linear.",
            ),
            (
                "Optional SHAP" if is_en else "SHAP opcional",
                "When the environment allows it, computes an additional in-memory reading without saving artifacts." if is_en else "Quando o ambiente permite, calcula uma leitura adicional em memória, sem salvar artefatos.",
            ),
            (
                "Influence in this example" if is_en else "Influência neste exemplo",
                "Shows which attributes most influenced the output for one selected real WDBC sample." if is_en else "Mostra quais atributos mais influenciaram a saída em uma amostra real selecionada do WDBC.",
            ),
        ]
    )

    render_soft_divider()

    st.subheader("Which attributes most influenced the model?" if is_en else "Quais atributos mais influenciaram o modelo?")
    st.write(
        (
            "Global importance uses the Logistic Regression coefficients in absolute value. Because WDBC uses `0 = Malignant` and `1 = Benign`, coefficient signs require care: positive coefficients favor `Benign (1)` in the model behavior, while negative coefficients favor `Malignant (0)`."
            if is_en
            else "A importância global usa os coeficientes da Regressão Logística em "
            "valor absoluto. Como o WDBC usa `0 = Maligno` e `1 = Benigno`, o sinal "
            "dos coeficientes deve ser interpretado com cuidado: coeficientes "
            "positivos puxam a estimativa para `Benigno (1)`, enquanto "
            "coeficientes negativos puxam a estimativa para `Maligno (0)`."
        )
    )
    global_importance = get_global_feature_importance(context)
    global_importance = global_importance.copy()
    global_importance["friendly_feature"] = global_importance["feature"].map(
        lambda feature: translate_feature_name(feature, language)
    )
    top_global = global_importance.head(15)
    top_global_chart = top_global.sort_values("coefficient_abs", ascending=True)
    importance_figure = px.bar(
        top_global_chart,
        x="coefficient_abs",
        y="friendly_feature",
        orientation="h",
        labels={
            "coefficient_abs": "Absolute importance" if is_en else "Importância absoluta",
            "friendly_feature": "Attribute" if is_en else "Atributo",
        },
        title="Top 15 attributes by global importance" if is_en else "Top 15 atributos por importância global",
    )
    tokens = get_theme_tokens()
    plotly_layout = get_plotly_layout()
    importance_figure.update_traces(marker_color=tokens["accent_2"])
    importance_figure.update_layout(
        **plotly_layout,
        height=520,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(
        importance_figure,
        config={"displayModeBar": False},
        width="stretch",
    )
    with st.expander("View full global importance table" if is_en else "Ver tabela completa de importância global"):
        st.dataframe(
            _format_global_importance_table(global_importance).round(4),
            width="stretch",
            hide_index=True,
        )

    with st.expander("Optional SHAP technical detail" if is_en else "Detalhe técnico de SHAP opcional"):
        shap_payload = get_shap_global_feature_importance(context)
        if shap_payload["available"]:
            st.success(shap_payload["message"])
            st.dataframe(
                shap_payload["data"].round(4),
                width="stretch",
                hide_index=True,
            )
        else:
            st.info(shap_payload["message"])
            st.caption(
                "The coefficient fallback remains valid for the persisted linear model on this page."
                if is_en
                else "O fallback por coeficientes permanece válido para explicar o "
                "comportamento linear do modelo persistido nesta tela."
            )

    st.subheader("How did attributes influence this example?" if is_en else "Como os atributos influenciaram este exemplo?")
    st.write(
        (
            "Select a real WDBC example to view the 10 attributes with the largest absolute influence in this example. The output is an academic interpretation of the model for a public tabular sample, not a real clinical explanation."
            if is_en
            else "Selecione um exemplo real do WDBC para ver os 10 atributos com maior "
            "influência absoluta neste exemplo. A saída é uma interpretação "
            "acadêmica do modelo para uma amostra tabular pública, não uma explicação "
            "clínica real."
        )
    )
    reference_options = _reference_options()
    selected_reference = st.selectbox(
        "WDBC reference example" if is_en else "Exemplo de referência do WDBC",
        list(reference_options.keys()),
    )
    target_label = reference_options[selected_reference]
    reference_sample = build_reference_sample_for_explanation(target_label)
    local_contributions = get_top_local_contributions(reference_sample, context=context)
    st.dataframe(
        _format_local_contributions_table(local_contributions).round(4),
        width="stretch",
        hide_index=True,
    )

    st.caption(
        (
            "Positive values pulled the estimate toward Benign (1), while negative values pulled it toward Malignant (0) in the linear classifier behavior."
            if is_en
            else "Valores positivos puxaram a estimativa para Benigno (1), enquanto valores negativos "
            "puxaram a estimativa para Maligno (0) no comportamento do classificador linear."
        )
    )
    with st.expander("How to interpret safely" if is_en else "Como interpretar com segurança"):
        if is_en:
            st.markdown(
                """
                - The local explanation describes model behavior for one specific tabular row.
                - It does not determine medical cause, severity, conduct, or care priority.
                - The correct reading is technical: which attributes moved the classifier output the most.
                - Real healthcare context would require professional analysis, additional data, and external validation.
                """
            )
        else:
            st.markdown(
                """
                - A explicação local descreve o comportamento do modelo para uma linha tabular específica.
                - Ela não determina causa médica, gravidade, conduta ou prioridade assistencial.
                - A leitura correta é técnica: quais atributos mais moveram a saída do classificador.
                - O contexto real em saúde exigiria análise profissional, dados adicionais e validação externa.
                """
            )
    st.warning(
        (
            "Explainability describes the statistical behavior of the model in this "
            "academic project. It does not replace medical diagnosis, does not imply "
            "medical causality, and must not be used as a professional recommendation."
            if is_en
            else EXPLAINABILITY_WARNING
        )
    )


render_page()
