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
- Problemas: durante a revisão, arquivos de página foram regravados pelo PowerShell com mojibake; os acentos foram corrigidos antes do commit. O parâmetro depreciado de largura do Streamlit também foi removido e substituído por `width="stretch"`.
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
- Testes: 78 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: predição individual acadêmica disponível no app Streamlit usando o artefato persistido e exemplos reais do WDBC; alterações revisadas, commitadas e publicadas.
- Commit: `3efa07f feat: adiciona predicao individual academica`.
- Próximo passo: implementar explicabilidade/SHAP ou revisar compatibilidade de ambiente para reduzir warnings de persistência.

### 2026-06-27 — Explicabilidade inicial do modelo persistido

- Etapa: Rodada 10 do Codex.
- Objetivo: ativar a página `pages/04_Explicabilidade.py` com explicabilidade global e local do modelo persistido, sem retreinar e sem gerar novos artefatos.
- Ações: implementação de `src/models/explain.py`; extração de coeficientes da Regressão Logística dentro do pipeline persistido; cálculo de importância global; cálculo de contribuições locais para exemplos reais WDBC; SHAP opcional em memória com fallback por coeficientes; atualização da página de explicabilidade, testes e documentação.
- Decisão técnica: usar coeficientes como caminho estável e SHAP apenas quando disponível no ambiente, sem quebrar a aplicação em caso de incompatibilidade.
- Cuidados: sem novo `.joblib`, sem JSON novo, sem CSV, sem notebook, sem API, sem banco, sem autenticação, sem retreino e sem afirmação de causalidade médica.
- Testes: 86 testes passaram em `python -m pytest -q`.
- Problemas: foram revisados warnings externos do SHAP (`PendingDeprecationWarning` em `shap/plots/colors/_colors.py`) observados em execução manual. Foi aplicado filtro localizado apenas dentro da função opcional de SHAP para esse tipo de warning externo, sem desativar warnings globalmente nem mascarar erros reais. No ambiente do Codex, os warnings restantes são `InconsistentVersionWarning` do Scikit-learn ao carregar o `.joblib`; a explicabilidade e os testes passaram.
- Fallback: quando SHAP não fica disponível ou estável no ambiente, a página mantém `fallback_coefficients` com coeficientes da Regressão Logística.
- Resultado: página de explicabilidade funcional com importância global e explicação local acadêmica; alterações revisadas, commitadas e publicadas.
- Commit: `af1bfc1 feat: adiciona explicabilidade inicial`.
- Próximo passo: seguir para revisão final do app, cobertura/testes, polimento visual ou preparação de relatório/vídeo.

### 2026-06-27 — Revisão final de qualidade e higiene técnica

- Etapa: Rodada 11 do Codex.
- Objetivo: revisar consistência textual, ética, técnica e preparação de entrega sem criar funcionalidade grande.
- Ações: revisão das páginas Streamlit principais; remoção de textos desatualizados sobre páginas futuras; atualização de aviso em Sobre/Ética para evitar linguagem de uso operacional em saúde; ajuste de texto da página de modelos para reconhecer predição e explicabilidade já implementadas; atualização de model cards, checklist e metodologia.
- Checagens: linguagem proibida, parâmetros depreciados do Streamlit, mojibake, artefatos indevidos, testes e cobertura.
- Testes: `python -m pytest -q` e `pytest -q` passaram com 86 testes; `pytest --cov=src` passou com cobertura total de 88%.
- Problemas: o ambiente não tinha `pytest-cov` disponível no primeiro `pytest --cov=src`; foi instalado no ambiente local porque já faz parte da stack e do `requirements.txt`. Persistem warnings não bloqueantes de `InconsistentVersionWarning` do Scikit-learn ao carregar o `.joblib`.
- Custos/tokens: não disponível.
- Resultado: app e documentação ficaram mais coerentes para revisão humana; relatório PDF e vídeo seguem pendentes.
- Commit: `d343d9f chore: revisa qualidade final da V1`.

### 2026-06-27 — Reprodutibilidade do ambiente e quality gate

- Etapa: Rodada 12 do Codex.
- Objetivo: consolidar reprodutibilidade do ambiente e automatizar checagens recorrentes antes de commit/push.
- Ações: fixação de `scikit-learn==1.9.0` e `joblib==1.5.3` em `requirements.txt`; criação de `docs/environment_reproducibility.md`; criação de `scripts/quality_gate.py`; atualização do README, checklist e registros metodológicos.
- Decisão técnica: fixar as versões usadas na geração do artefato persistido para reduzir warnings de compatibilidade do `.joblib` e deixar a entrega mais previsível em Python 3.11.
- Cuidados: sem retreino, sem novo `.joblib`, sem novo JSON de modelo, sem CSV, sem API, sem banco, sem autenticação e sem alteração de dataset.
- Testes: validações finais executadas com quality gate, `python -m pytest -q`, `pytest -q`, `pytest --cov=src`, `git diff --check`, `git status --short` e `git diff --stat`.
- Custos/tokens: não disponível.
- Próximo passo: revisão humana do diff e commit da rodada, se aprovado.

### 2026-06-27 — Declaração do modelo final acadêmico da V1

- Etapa: Rodada 13 do Codex.
- Objetivo: eliminar a ambiguidade entre modelo candidato recomendado e modelo final acadêmico da V1/MVP.
- Decisão: o modelo final acadêmico da V1 é a Regressão Logística já persistida em `models/artifacts/recommended_model.joblib`.
- Critério: seleção controlada por maior `recall_malignant`, seguida por `roc_auc_malignant` e `f1_malignant` em caso de empate.
- Ações: atualização do README, checklist, model cards e rastreabilidade de decisões para registrar a decisão formal.
- Cuidados: sem retreino, sem regenerar `.joblib`, sem alterar JSONs de métricas/features, sem alterar split, dataset, predição, explicabilidade ou páginas visuais.
- Custos/tokens: não disponível.
- Próximo passo: validação final da rodada e revisão humana antes de commit.

### 2026-06-27 — Polimento visual inicial do app Streamlit

- Etapa: Rodada 14 do Codex.
- Objetivo: melhorar a apresentação visual do MVP Streamlit sem alterar lógica de Machine Learning, dataset, métricas ou artefatos.
- Ações: inspeção visual real do app renderizado via Streamlit local e Chrome DevTools; refinamento da página inicial; organização de tabelas longas em expanders na EDA; ajuste visual da página de predição; alinhamento da página de modelos ao termo "modelo final acadêmico da V1"; refinamento da página de explicabilidade; expansão da página Sobre e Ética para banca/revisão humana.
- Cuidados: sem retreino, sem novo `.joblib`, sem JSON novo, sem CSV, sem alteração de `models/artifacts/`, sem API, sem banco, sem autenticação, sem React/Vite/FastAPI e sem alteração de dataset ou lógica de ML.
- Testes: validações finais executadas com quality gate, `python -m pytest -q`, `pytest -q`, `pytest --cov=src`, `git diff --check`, `git status --short` e `git diff --stat`.
- Custos/tokens: não disponível.
- Próximo passo: revisão humana do polimento visual antes de commit.
