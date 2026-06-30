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
from src.ui.components import (
    apply_global_style,
    render_card_grid,
    render_ethics_notice,
    render_page_intro,
    render_soft_divider,
)
from src.ui.feature_dictionary import get_feature_help, translate_feature_name
from src.ui.i18n import get_language, translate_group_name, translate_target_label


LAST_RESULT_KEY = "last_prediction_result"
LAST_INPUT_KEY = "last_prediction_input_sample"


def _reference_options() -> dict[str, int]:
    language = get_language()
    if language == "en":
        return {
            "Real WDBC example — Malignant (0)": 0,
            "Real WDBC example — Benign (1)": 1,
        }
    return {
        "Exemplo real WDBC — Maligno (0)": 0,
        "Exemplo real WDBC — Benigno (1)": 1,
    }


def _render_manual_input(reference_sample: pd.DataFrame) -> pd.DataFrame:
    values = {}
    reference_row = reference_sample.iloc[0]

    for group_name, group_features in FEATURE_GROUPS.items():
        with st.expander(
            (
                f"{translate_group_name(group_name)} ({group_name})"
                if get_language() == "pt"
                else f"{translate_group_name(group_name)} ({group_name})"
            ),
            expanded=group_name == "mean",
        ):
            st.caption(
                (
                    "Real WDBC values are used as the initial reference. Manual edits must keep the expected numeric format."
                    if get_language() == "en"
                    else "Valores reais do WDBC são usados como referência inicial. "
                    "Ajustes manuais devem manter o formato numérico esperado."
                )
            )
            columns = st.columns(2)
            for position, feature_name in enumerate(group_features):
                column = columns[position % 2]
                values[feature_name] = column.number_input(
                    translate_feature_name(feature_name),
                    min_value=0.0,
                    value=float(reference_row[feature_name]),
                    format="%.6f",
                    help=get_feature_help(feature_name),
                )

    return pd.DataFrame([values], columns=list(FEATURE_NAMES))


def _render_prediction_result(result: dict, input_sample: pd.DataFrame) -> None:
    """Render the latest prediction result before detailed input values."""
    language = get_language()
    is_en = language == "en"
    predicted_class = translate_target_label(result["predicted_label"], language)
    st.subheader("Academic estimate result" if is_en else "Resultado da estimativa acadêmica")
    st.success(
        (
            "Academic estimate completed. Interpret the values below only as the model output for an educational demonstration."
            if is_en
            else "Estimativa acadêmica executada. Interprete os valores abaixo apenas "
            "como saída do modelo para demonstração educacional."
        )
    )

    col_class, col_malignant, col_benign = st.columns(3)
    col_class.metric(
        "Estimated model class" if is_en else "Classe estimada pelo modelo",
        predicted_class,
    )
    col_malignant.metric(
        "Estimated probability of Malignant" if is_en else "Probabilidade estimada de Maligno",
        f"{result['probability_malignant']:.2%}",
    )
    col_benign.metric(
        "Estimated probability of Benign" if is_en else "Probabilidade estimada de Benigno",
        f"{result['probability_benign']:.2%}",
    )

    st.warning(
        (
            "This output is only the model's academic estimate. It is not a medical diagnosis, does not replace clinical evaluation, does not replace a pathology report, and does not replace a professional decision. A physician must always have the final say."
            if is_en
            else "Esta saída representa apenas a estimativa acadêmica do modelo. Não "
            "é diagnóstico médico, não substitui avaliação clínica, não substitui "
            "laudo anatomopatológico e não substitui decisão profissional. O médico "
            "sempre deve ter a palavra final."
        )
    )
    st.info(result["academic_warning"])

    with st.expander("How to interpret this output" if is_en else "Como interpretar esta saída"):
        if is_en:
            st.markdown(
                """
                - The estimated class is the persisted pipeline output for the provided tabular sample.
                - The probabilities belong to the model and to this WDBC-formatted example; they are not a medical conclusion.
                - The class `Malignant (0)` is prioritized only as a technical project criterion.
                - To inspect the factors that influenced the output, open **Explainability**.
                """
            )
        else:
            st.markdown(
                """
                - A classe estimada é a saída estatística do pipeline persistido para a amostra informada.
                - As probabilidades pertencem ao modelo e a este exemplo tabular no formato WDBC; não são uma conclusão médica.
                - A classe `Maligno (0)` é priorizada apenas como critério técnico do projeto.
                - Para entender os fatores que influenciaram a saída, avance para a página **Explicabilidade**.
                """
            )

    with st.expander("View values used in the estimate" if is_en else "Ver valores usados na estimativa"):
        values_table = input_sample.T.rename(
            columns={input_sample.index[0]: "Used value" if is_en else "Valor usado"}
        )
        values_table.insert(
            0,
            "Attribute" if is_en else "Atributo",
            [translate_feature_name(feature_name, language) for feature_name in values_table.index],
        )
        values_table.insert(
            1,
            "Technical name" if is_en else "Nome técnico",
            values_table.index,
        )
        st.dataframe(values_table.reset_index(drop=True), width="stretch")


def render_page() -> None:
    """Render the individual academic prediction page."""
    apply_global_style()
    language = get_language()
    is_en = language == "en"
    render_page_intro(
        "Guided academic estimate simulator" if is_en else "Simulador guiado de estimativa acadêmica",
        "Individual estimate" if is_en else "Estimativa individual",
        (
            "Use a real WDBC example as a starting point, adjust the 30 attributes if needed, and view the output from the persisted final academic model."
            if is_en
            else "Use um exemplo real do WDBC como ponto de partida, ajuste os 30 atributos "
            "se necessário e veja a saída do modelo final acadêmico persistido."
        ),
    )
    render_ethics_notice(short=True)

    render_card_grid(
        [
            (
                "1. Choose an example" if is_en else "1. Escolha um exemplo",
                (
                    "Use a real WDBC sample, Malignant (0) or Benign (1), only as a public demonstration."
                    if is_en
                    else "Use uma amostra real do WDBC, Maligno (0) ou Benigno (1), apenas como demonstração pública."
                ),
            ),
            (
                "2. Review attributes" if is_en else "2. Revise os atributos",
                (
                    "Values are grouped as mean, variation, and largest observed values to reduce visual noise."
                    if is_en
                    else "Os valores aparecem agrupados em medidas médias, variações e maiores valores observados para reduzir ruído visual."
                ),
            ),
            (
                "3. Run the estimate" if is_en else "3. Execute a estimativa",
                (
                    "The model returns an estimated class and probabilities, always with academic interpretation."
                    if is_en
                    else "O modelo retorna classe estimada e probabilidades, sempre com interpretação acadêmica."
                ),
            ),
        ]
    )

    artifact_paths = get_recommended_artifact_paths()

    try:
        artifacts = load_prediction_artifacts()
    except (FileNotFoundError, TypeError, ValueError) as error:
        st.error(f"Não foi possível carregar os artefatos de predição: {error}")
        return

    metrics_payload = artifacts["metrics"]
    metadata = metrics_payload.get("metadata", {})

    render_soft_divider()

    st.subheader("Model used in this simulation" if is_en else "Modelo usado nesta simulação")
    col_model, col_features, col_priority = st.columns(3)
    col_model.metric(
        "Final academic model" if is_en else "Modelo final acadêmico",
        metrics_payload.get("selected_model_name", "Modelo persistido"),
    )
    col_features.metric("Expected attributes" if is_en else "Atributos esperados", EXPECTED_FEATURE_COUNT)
    col_priority.metric("Technical priority class" if is_en else "Classe prioritária técnica", translate_target_label(0, language))

    with st.expander("View artifact paths and technical metadata" if is_en else "Ver caminhos e metadados técnicos do artefato"):
        st.caption(
            f"Modelo: `{artifact_paths['model']}` | Métricas: "
            f"`{artifact_paths['metrics']}` | Features: "
            f"`{artifact_paths['feature_names']}`"
        )
        st.caption(
            "Artefato gerado para fins acadêmicos. Isso não transforma o projeto "
            "em ferramenta clínica ou sistema para uso real em saúde."
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

    st.subheader("Quick mode" if is_en else "Modo rápido")
    st.write(
        (
            "Choose a real example from the public WDBC dataset to run an estimate without manually filling all 30 attributes. These examples do not represent real clinical cases."
            if is_en
            else "Escolha um exemplo real do dataset público WDBC para executar uma "
            "estimativa sem preencher os 30 atributos manualmente. Os exemplos não "
            "representam casos clínicos reais."
        )
    )

    reference_options = _reference_options()
    selected_reference = st.selectbox(
        "WDBC reference example" if is_en else "Exemplo de referência do WDBC",
        list(reference_options.keys()),
    )
    target_label = reference_options[selected_reference]
    reference_sample = build_reference_sample(target_label)

    with st.expander("Advanced attribute adjustment" if is_en else "Ajuste avançado dos atributos"):
        st.write(
            (
                "Use this section only if you want to manually change values before running the estimate. Attributes remain grouped by mean measurements, measurement variations, and largest observed values."
                if is_en
                else "Use esta seção apenas se quiser alterar manualmente os valores "
                "antes de executar a estimativa. Os atributos continuam agrupados "
                "em medidas médias, variações das medidas e maiores valores observados."
            )
        )
        input_sample = _render_manual_input(reference_sample)

    st.caption(
        (
            "The input is validated with exactly 30 canonical attributes, in the expected order, with no extra columns, no missing columns, no nulls, and numeric values."
            if is_en
            else "A entrada é validada com exatamente 30 atributos canônicos, na ordem "
            "esperada, sem colunas extras, sem colunas ausentes, sem nulos e com "
            "valores numéricos."
        )
    )

    if st.button("Run academic estimate" if is_en else "Executar estimativa acadêmica"):
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

    render_soft_divider()
    st.info(ACADEMIC_PREDICTION_WARNING)


render_page()
