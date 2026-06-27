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

### 2026-06-26 — Seleção controlada do modelo candidato recomendado

- Etapa: Rodada 7 do Codex.
- Objetivo: formalizar uma seleção acadêmica controlada do modelo candidato recomendado, usando o ranking em memória já definido por `recall_malignant`, `roc_auc_malignant` e `f1_malignant`.
- Ações: criação de `select_recommended_candidate()` em `src/models/select.py`; inclusão de `recommended_candidate` no payload de `run_model_comparison()`; atualização da página de modelos com seção “Modelo candidato recomendado”; testes unitários e smoke atualizados.
- Cuidados: a seleção segue o ranking já calculado, não treina novamente, não altera split, não altera critérios de ranking, não persiste `.joblib`, não salva métricas JSON e não define ferramenta para uso real em saúde.
- Problemas: durante a revisão, arquivos de página foram regravados pelo PowerShell com mojibake; os acentos foram corrigidos antes do commit. O aviso `use_container_width` do Streamlit também foi removido com `width="stretch"`.
- Testes: 60 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: seleção técnica e inicial do candidato recomendado disponível em código, página e documentação; alterações revisadas, commitadas e publicadas.
- Commit: `a483031 feat: seleciona candidato recomendado de forma controlada`.
- Próximo passo: decidir se o candidato recomendado será persistido como modelo final com model card, métricas e artefatos em uma rodada futura.

### 2026-06-27 — Persistência controlada do modelo candidato recomendado

- Etapa: Rodada 8 do Codex.
- Objetivo: persistir o modelo candidato recomendado como artefato técnico acadêmico e atualizar o model card operacional.
- Ações: criação de `src/models/persist.py`; geração dos artefatos em `models/artifacts/`; atualização da página de modelos para indicar status dos artefatos; atualização do README, checklist, model cards e testes.
- Artefatos criados: `models/artifacts/recommended_model.joblib`, `models/artifacts/recommended_model_metrics.json` e `models/artifacts/recommended_model_feature_names.json`.
- Decisão técnica: versionar o `.joblib` específico do candidato recomendado porque é pequeno, determinístico, necessário para o app acadêmico e documentado; a regra permanece restrita a `models/artifacts/`.
- Cuidados: sem SHAP, sem explicabilidade final, sem predição individual final, sem API, sem banco, sem autenticação e sem alteração do split oficial.
- Problemas: textos inicialmente apareceram com mojibake no PowerShell; checagem Python confirmou os arquivos críticos sem mojibake antes do commit.
- Testes: 65 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: modelo candidato recomendado persistido como artefato acadêmico, com métricas, feature names e model card operacional; alterações revisadas, commitadas e publicadas.
- Commit: `6769ead feat: persiste candidato recomendado com model card`.
- Próximo passo: avançar para predição individual usando artefatos persistidos ou explicabilidade em rodada futura.

### 2026-06-27 — Predição individual acadêmica com artefato persistido

- Etapa: Rodada 9 do Codex.
- Objetivo: implementar predição individual acadêmica usando o modelo candidato persistido na Rodada 8, sem retreinar e sem regenerar artefatos.
- Ações: criação da camada `src/models/predict.py`; atualização da página `pages/02_Predicao.py` com exemplos reais do WDBC, formulário manual agrupado por `mean`, `error` e `worst`, validação rígida de entrada e saída com linguagem não diagnóstica; testes unitários e smoke adicionados.
- Ajuste pré-commit: a UX da página de predição foi refinada para exibir o resultado imediatamente após a execução, usar métricas em cards, organizar grupos de features em expanders e mover os valores usados para o expander "Ver valores usados na estimativa".
- Ajuste final de UX pré-commit: o último resultado passou a ser armazenado em `st.session_state`, mantendo a seção "Resultado da estimativa acadêmica" visível após a execução, com três cards de métricas antes da tabela de valores usados.
- Artefato usado: `models/artifacts/recommended_model.joblib`, com métricas e feature names persistidos na Rodada 8.
- Cuidados: sem SHAP, sem explicabilidade final, sem novo `.joblib`, sem novo JSON, sem CSV, sem retreino, sem alteração do split oficial e sem linguagem de diagnóstico.
- Problemas: o primeiro teste completo falhou porque a checagem de artefatos do teste não incluía os nomes canônicos `recommended_model_metrics.json` e `recommended_model_feature_names.json`; o teste foi corrigido sem alterar artefatos. O carregamento do `.joblib` emitiu `InconsistentVersionWarning` do Scikit-learn no ambiente local, mas a predição e os testes passaram.
- Testes: 78 testes passaram em `python -m pytest -q`.
- Resultado: predição individual acadêmica disponível no app Streamlit usando o artefato persistido e exemplos reais do WDBC.
- Commit: pendente de revisão humana.
- Próximo passo: implementar explicabilidade/SHAP ou revisar compatibilidade de ambiente para reduzir warnings de persistência.
