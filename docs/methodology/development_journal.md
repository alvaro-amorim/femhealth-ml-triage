# Diário de Desenvolvimento — FemHealth ML Triage

Este arquivo registra a evolução cronológica do projeto para apoiar o relatório técnico final, a rastreabilidade acadêmica e o roteiro do vídeo de demonstração.

## Entradas registradas

### 2026-06-26 — Constituição do projeto

- Objetivo: definir a fonte oficial da verdade do projeto.
- Resultado: `PROJECT_CONSTITUTION.md` criado, com escopo, stack, dataset, arquitetura, testes e regras de desenvolvimento.
- Próximo passo: bootstrap estrutural.

### 2026-06-26 — Bootstrap estrutural

- Etapa: Rodada 1 do Codex.
- Ações: criação da estrutura inicial com `app.py`, `pages/`, `src/`, `data/`, `models/`, `notebooks/`, `tests/`, `docs/`, `requirements.txt` e `pytest.ini`.
- Problemas: `pytest` inicialmente não encontrava `src`; depois houve problema de BOM no `pytest.ini`.
- Solução: `pytest.ini` criado com `pythonpath = .` e regravado em UTF-8 sem BOM.
- Testes: 3 testes passaram.
- Commit: `556ce05 chore: bootstrap inicial do projeto`.

### 2026-06-26 — Carregamento real do WDBC e validação de schema

- Etapa: Rodada 2 do Codex.
- Ações: implementação de `load_wdbc_data()`, `load_wdbc_dataframe()`, schema e validações estritas.
- Problemas: comando manual assumiu retorno com atributos, mas a função retorna tupla `(features, target, metadata)`.
- Solução: interface confirmada com desempacotamento da tupla.
- Testes: 14 testes passaram.
- Commit: `ba2aa27 data: implementa carregamento e validação do WDBC`.

### 2026-06-26 — Pré-processamento e split treino/teste

- Etapa: Rodada 3 do Codex.
- Ações: criação de `separate_features_and_target`, `split_train_test`, `build_scaling_pipeline`, `build_passthrough_pipeline` e `validate_train_test_split`.
- Testes: 25 testes passaram.
- Resultado: alterações revisadas, commitadas e publicadas.
- Commit: `a6b8f9f feat: adiciona pré-processamento e split treino-teste`.

### 2026-06-26 — Modelagem inicial e avaliação controlada

- Etapa: Rodada 4 do Codex.
- Objetivo: implementar treinamento em memória e avaliação de modelos candidatos sem escolher modelo final.
- Ações: candidatos Regressão Logística, Árvore de Decisão e KNN; treino em memória; métricas da classe maligna; ranking por recall maligno, ROC AUC e F1; testes unitários.
- Cuidados: ROC AUC da classe maligna usa probabilidade da classe `0 = malignant`; precision, recall e F1 usam `pos_label=0`.
- Testes: 37 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: alterações revisadas, commitadas e publicadas; sem persistência de artefatos finais.
- Commit: `7180bda feat: adiciona modelagem inicial e avaliação`.

### 2026-06-26 — Integração da comparação inicial na página de modelos

- Etapa: Rodada 5 do Codex.
- Objetivo: integrar a modelagem inicial e avaliação em uma base controlada para a página de comparação de modelos.
- Ações: criação de `run_model_comparison()` em `src/models/compare.py`; atualização de `pages/03_Modelos.py` para exibir configuração, candidatos, tabela de métricas, ranking inicial e matriz de confusão do modelo melhor ranqueado nesta comparação inicial.
- Cuidados: sem escolha de modelo final, sem persistência de `.joblib`, sem `metrics.json`, sem `feature_names.json`, sem CSV, sem SHAP e sem predição individual final.
- Problemas: smoke test da página falhou inicialmente porque o ambiente local não tinha `streamlit` instalado e uma checagem textual era frágil.
- Solução: teste de import passou a usar stub de Streamlit e a checagem textual foi tornada menos frágil.
- Testes: 43 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: alterações revisadas, commitadas e publicadas.
- Commit: `7b142dd feat: integra comparação inicial de modelos à página`.

### 2026-06-26 — Curva ROC na comparação inicial de modelos

- Etapa: Rodada 6A do Codex.
- Objetivo: adicionar Curva ROC à comparação inicial de modelos na página `pages/03_Modelos.py`, mantendo tudo em memória.
- Ações: criação de `calculate_roc_curve_points()` em `src/models/evaluate.py`; inclusão de `roc_curves` no payload de `run_model_comparison()`; exibição da Curva ROC dos candidatos na página de modelos com `st.line_chart`; testes unitários e smoke atualizados.
- Cuidados: a Curva ROC usa a probabilidade da classe `0 = malignant`, com `y_test == 0` mapeado para classe positiva; não houve escolha de modelo final nem persistência de artefatos.
- Testes: 45 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: alterações revisadas, commitadas e publicadas; sem `.joblib`, `metrics.json`, `feature_names.json`, CSV, imagem salva, SHAP ou predição individual final.
- Commit: `d7e3a48 feat: adiciona curva ROC à comparação de modelos`.

### 2026-06-26 — EDA real do WDBC na página de exploração

- Etapa: Rodada 6B do Codex.
- Objetivo: substituir o placeholder da página `pages/01_Exploracao.py` por uma análise exploratória real do WDBC carregado localmente.
- Ações: criação de `src/analysis/eda.py` e `src/analysis/__init__.py`; implementação de overview, distribuição do target, grupos de features, estatísticas descritivas, missing values e correlações com target; atualização da página de exploração com tabelas, métricas e gráfico de barras; testes unitários e smoke adicionados.
- Cuidados: sem treino de modelos, sem alteração de ranking, sem SHAP, sem predição individual, sem download de dataset e sem persistência de artefatos.
- Testes: 54 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: alterações revisadas, commitadas e publicadas; EDA inicial do WDBC disponível no app Streamlit e em camada Python testável.
- Commit: `4e8b9bc feat: adiciona EDA real à página de exploração`.
- Próximo passo: notebook/relatório de EDA ou etapa de seleção controlada de modelo final.
