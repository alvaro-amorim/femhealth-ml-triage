# FemHealth ML Triage

Aplicação acadêmica de Machine Learning para apoio à triagem analítica em saúde da mulher, com classificação tabular, explicabilidade e interface multipage em Streamlit.

## Contexto acadêmico

Este repositório é o projeto do Tech Challenge — Fase 1 da pós-graduação. A V1 prioriza um pipeline reproduzível de classificação supervisionada, análise exploratória, comparação de modelos, explicabilidade e documentação técnica.

## Dataset

O dataset principal é o **Breast Cancer Wisconsin Diagnostic (WDBC)**, carregado preferencialmente por `sklearn.datasets.load_breast_cancer(as_frame=True)`. Ele contém 569 amostras e 30 atributos numéricos extraídos de características celulares. A fonte original é a [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic).

Nenhum dataset é baixado ou versionado nesta etapa de bootstrap.

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

Nesta rodada, as páginas são apenas a base de navegação. O carregamento do WDBC, o treino e os artefatos serão implementados nas etapas seguintes.

## Testes

```powershell
pytest
pytest --cov=src
```

## Status atual

Bootstrap estrutural concluído: estrutura de diretórios, módulos-base, schema canônico das 30 features do WDBC, documentação inicial e smoke test. Não há modelo treinado, dados de exemplo ou artefatos `.joblib` nesta etapa.

## Aviso ético

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.
