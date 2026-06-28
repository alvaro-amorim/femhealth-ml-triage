"""Página inicial do FemHealth ML Triage."""

import streamlit as st


st.set_page_config(page_title="FemHealth ML Triage", page_icon="📊", layout="wide")

st.title("FemHealth ML Triage")
st.subheader("Apoio acadêmico à triagem analítica em saúde da mulher")
st.write(
    "MVP acadêmico em Streamlit para demonstrar um pipeline de Machine Learning "
    "tabular com o dataset público Breast Cancer Wisconsin Diagnostic (WDBC)."
)

col_dataset, col_model, col_scope = st.columns(3)
col_dataset.metric("Dataset", "WDBC")
col_model.metric("Modelo final acadêmico", "Regressão Logística")
col_scope.metric("Features", "30")

st.markdown(
    """
    O app já cobre o fluxo principal da V1:

    - exploração real dos dados;
    - comparação de modelos candidatos;
    - modelo final acadêmico persistido;
    - predição individual acadêmica;
    - explicabilidade global e local;
    - seção de escopo, limitações e ética.
    """
)

with st.expander("Como navegar pelo MVP"):
    st.markdown(
        """
        - **Exploração:** visão geral, distribuição das classes, estatísticas e correlações.
        - **Predição:** estimativa acadêmica para uma amostra tabular WDBC.
        - **Modelos:** métricas, ranking, Curva ROC e matriz de confusão.
        - **Explicabilidade:** importância global e contribuição local de features.
        - **Sobre Ética:** escopo, limites e postura responsável.
        """
    )

st.warning(
    "O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem "
    "analítica e não substitui diagnóstico médico, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O médico sempre deve ter a "
    "palavra final."
)
