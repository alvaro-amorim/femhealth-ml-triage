# FemHealth ML Triage

Plataforma demonstrativa acadêmica de Machine Learning explicável para análise tabular em saúde da mulher, com classificação supervisionada, estimativa individual, explicabilidade e interface multipage em Streamlit.

## Contexto acadêmico

Este repositório é o projeto do Tech Challenge — Fase 1 da pós-graduação. A V1 prioriza um pipeline reproduzível de classificação supervisionada, análise exploratória, comparação de modelos, explicabilidade e documentação técnica.

O app foi organizado como uma plataforma demonstrativa guiada: entender o projeto, conhecer o dataset, revisar a comparação de modelos, executar uma estimativa acadêmica e interpretar o comportamento do modelo com limites éticos claros.

## Dataset

O dataset principal é o **Breast Cancer Wisconsin Diagnostic (WDBC)**, carregado localmente pelo Scikit-learn com `sklearn.datasets.load_breast_cancer(as_frame=True)`. Ele contém 569 amostras e 30 atributos numéricos extraídos de características celulares. A fonte original é a [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic).

O carregamento não baixa nem versiona dados: o WDBC é distribuído com a instalação do Scikit-learn.

## Exploração dos dados

A página `pages/01_Exploracao.py` apresenta EDA real do WDBC carregado localmente, incluindo visão geral do dataset, distribuição das classes, grupos de features, estatísticas descritivas, resumo de valores ausentes e correlações exploratórias com o target.

## Pré-processamento

O projeto já possui separação de features/target, split treino/teste estratificado e reproduzível (`test_size=0.2`, `random_state=42`) e pipelines de pré-processamento em `src/features/preprocess.py`.

O pipeline com `StandardScaler` deve ser usado para modelos sensíveis à escala, como Regressão Logística, KNN e SVM. Para modelos baseados em árvore, há pipeline de passthrough. O scaler deve ser ajustado apenas no treino para evitar vazamento de dados.

## Modelagem inicial

A camada inicial de modelagem em `src/models/` permite construir, treinar em memória e avaliar candidatos simples: Regressão Logística, Árvore de Decisão e KNN. As métricas priorizam a classe maligna do WDBC (`0 = malignant`) e incluem accuracy, precision, recall, F1, ROC AUC e matriz de confusão.

A página `pages/03_Modelos.py` consome uma comparação em memória e exibe tabela de métricas, ranking por recall maligno, ROC AUC e F1, Curva ROC didática dos candidatos, matriz de confusão interpretada e a declaração do modelo final acadêmico da V1.

A seleção técnica que fundamentou o modelo final acadêmico segue os critérios `recall_malignant`, `roc_auc_malignant` e `f1_malignant`. O modelo final acadêmico atual é Regressão Logística.

## Modelo final acadêmico da V1

O modelo final acadêmico da V1/MVP é o artefato já persistido em:

```text
models/artifacts/recommended_model.joblib
models/artifacts/recommended_model_metrics.json
models/artifacts/recommended_model_feature_names.json
```

Esse modelo é uma **Regressão Logística** treinada com o WDBC e selecionada pelo critério controlado de maior `recall_malignant`, seguido por `roc_auc_malignant` e `f1_malignant` em caso de empate.

Para regenerar os artefatos:

```powershell
python -m src.models.persist
```

O `.joblib` é um artefato técnico pequeno do projeto acadêmico. Ele não transforma a aplicação em ferramenta clínica e não deve ser usado para diagnóstico médico, avaliação clínica, laudo anatomopatológico ou decisão profissional. O médico sempre deve ter a palavra final.

## Predição individual acadêmica

A página `pages/02_Predicao.py` usa o artefato persistido em `models/artifacts/recommended_model.joblib` para executar uma estimativa acadêmica de uma única amostra no formato WDBC.

A entrada é validada contra as 30 features canônicas, na ordem esperada, sem colunas extras, sem colunas ausentes, sem valores nulos e com valores numéricos. A página oferece exemplos reais do WDBC para demonstração (`malignant (0)` e `benign (1)`) e permite ajuste manual dos atributos agrupados em `mean`, `error` e `worst`.

Essa saída é apenas uma estimativa acadêmica do modelo para apoio à triagem analítica em contexto educacional. Ela não substitui diagnóstico médico, avaliação clínica, laudo anatomopatológico ou decisão profissional.

## Interface e usabilidade

A interface Streamlit possui seletor de idioma (`Português`/`English`) e seletor de tema (`Claro`/`Escuro`) na sidebar. Os nomes técnicos originais do WDBC são preservados no backend, mas a interface apresenta nomes amigáveis e descrições didáticas dos 30 atributos para melhorar a leitura do app.

## Explicabilidade inicial

A página `pages/04_Explicabilidade.py` apresenta explicabilidade acadêmica inicial do modelo persistido. Ela mostra importância global das features por coeficientes da Regressão Logística, tenta calcular SHAP em memória quando o ambiente permite e mantém fallback técnico por coeficientes quando SHAP não está disponível.

A explicação local usa exemplos reais do WDBC (`malignant (0)` e `benign (1)`) e exibe as principais contribuições para uma amostra tabular. Esses resultados descrevem comportamento do modelo e não implicam causalidade médica, recomendação profissional ou decisão clínica.

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

Para reduzir warnings de compatibilidade do artefato persistido, o ambiente recomendado fixa `scikit-learn==1.9.0` e `joblib==1.5.3`. Detalhes estão em `docs/environment_reproducibility.md`.

## Executar

```powershell
streamlit run app.py
```

Nesta etapa, as páginas ainda são incrementais. O carregamento e a validação do WDBC estão disponíveis em `src/data/`, a EDA reutilizável está em `src/analysis/`, a base de pré-processamento/split está em `src/features/`, a modelagem inicial, a persistência controlada, a predição e a explicabilidade inicial do modelo final acadêmico estão em `src/models/`, e as páginas de exploração, predição, modelos e explicabilidade já exibem análises acadêmicas iniciais.

A página de predição individual acadêmica já consome o modelo final acadêmico persistido:

```powershell
streamlit run app.py
```

## Testes

```powershell
pytest
pytest --cov=src
```

## Quality gate

Antes de commit ou push, rode:

```powershell
python scripts/quality_gate.py
```

Esse comando valida higiene básica do repositório, artefatos permitidos, pins de reprodutibilidade, JSONs persistidos, schema das 30 features e carregamento do modelo acadêmico persistido.

## Status atual

Base de dados, EDA inicial, pré-processamento, modelagem inicial em memória, comparação inicial com Curva ROC didática, seleção acadêmica, modelo final acadêmico da V1 declarado, persistência controlada, predição individual acadêmica, explicabilidade inicial, tema claro/escuro, idioma PT/EN e quality gate local concluídos. Relatório PDF e vídeo seguem pendentes.

## Aviso ético

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.
