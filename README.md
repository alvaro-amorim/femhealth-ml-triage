# FemHealth ML Triage

Aplicação acadêmica de Machine Learning para apoio à triagem analítica em saúde da mulher, com classificação tabular, explicabilidade e interface multipage em Streamlit.

## Contexto acadêmico

Este repositório é o projeto do Tech Challenge — Fase 1 da pós-graduação. A V1 prioriza um pipeline reproduzível de classificação supervisionada, análise exploratória, comparação de modelos, explicabilidade e documentação técnica.

## Dataset

O dataset principal é o **Breast Cancer Wisconsin Diagnostic (WDBC)**, carregado localmente pelo Scikit-learn com `sklearn.datasets.load_breast_cancer(as_frame=True)`. Ele contém 569 amostras e 30 atributos numéricos extraídos de características celulares. A fonte original é a [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic).

O carregamento não baixa nem versiona dados: o WDBC é distribuído com a instalação do Scikit-learn.

## Pré-processamento

O projeto já possui separação de features/target, split treino/teste estratificado e reproduzível (`test_size=0.2`, `random_state=42`) e pipelines de pré-processamento em `src/features/preprocess.py`.

O pipeline com `StandardScaler` deve ser usado para modelos sensíveis à escala, como Regressão Logística, KNN e SVM. Para modelos baseados em árvore, há pipeline de passthrough. O scaler deve ser ajustado apenas no treino para evitar vazamento de dados.

## Modelagem inicial

A camada inicial de modelagem em `src/models/` permite construir, treinar em memória e avaliar candidatos simples: Regressão Logística, Árvore de Decisão e KNN. As métricas priorizam a classe maligna do WDBC (`0 = malignant`) e incluem accuracy, precision, recall, F1, ROC AUC e matriz de confusão.

Esta etapa ainda não escolhe modelo final e não salva `.joblib`, `metrics.json` ou `feature_names.json`.

## Stack V1

- Python 3.11
- Pandas, NumPy e Scikit-learn
- SHAP e Joblib
- Matplotlib e Plotly
- Streamlit
- JupyterLab
- Pytest e Pytest-cov

## Estrutura planejada

```text
app.py                 # Página inicial do Streamlit
pages/                 # Exploração, predição, modelos, explicabilidade e ética
src/                   # Lógica de dados, features, modelos, gráficos e utilidades
data/                  # Dados locais futuros e exemplos pequenos
models/                # Artefatos de modelo futuros e model card
notebooks/             # EDA, modelagem e explicabilidade
tests/                 # Testes unitários, smoke e e2e
docs/                  # ADRs, wireframes e checklist de entrega
```

## Setup local (Windows/PowerShell)

Requer Python 3.11.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Executar

```powershell
streamlit run app.py
```

Nesta etapa, as páginas ainda são a base de navegação. O carregamento e a validação do WDBC estão disponíveis em `src/data/`, a base de pré-processamento/split está em `src/features/`, e a modelagem inicial em memória está em `src/models/`; artefatos finais serão implementados nas etapas seguintes.

## Testes

```powershell
pytest
pytest --cov=src
```

## Status atual

Base de dados, pré-processamento e modelagem inicial em memória concluídos: o WDBC é carregado localmente via Scikit-learn, as 30 features são verificadas contra o schema canônico, o split treino/teste está testado e candidatos simples podem ser treinados/avaliados sem persistência. Não há modelo final escolhido, dados de exemplo ou artefatos `.joblib` nesta etapa.

## Aviso ético

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.
