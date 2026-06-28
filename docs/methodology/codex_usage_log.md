# Registro de Rodadas do Codex

Este arquivo registra as rodadas da ferramenta de implementação no VS Code.

## Resumo das rodadas

| Rodada | Data | Objetivo | Testes | Resultado | Commit |
|---|---|---|---|---|---|
| 1 | 2026-06-26 | Bootstrap estrutural | 3 testes passaram | Estrutura inicial criada | `556ce05` |
| 2 | 2026-06-26 | Carregamento e validação do WDBC | 14 testes passaram | Base de dados implementada | `ba2aa27` |
| 3 | 2026-06-26 | Pré-processamento e split treino/teste | 25 testes passaram | Pré-processamento, split e pipelines base implementados | `a6b8f9f` |
| 4 | 2026-06-26 | Modelagem inicial e avaliação controlada | 37 testes passaram | Candidatos treináveis em memória e métricas iniciais implementados | `7180bda` |
| 5 | 2026-06-26 | Integração da comparação inicial na página de modelos | 43 testes passaram | Comparação em memória exibida no Streamlit | `7b142dd` |
| 6A | 2026-06-26 | Curva ROC na comparação inicial de modelos | 45 testes passaram | Curva ROC calculada em memória e exibida no Streamlit | `d7e3a48` |
| 6B | 2026-06-26 | EDA real do WDBC na página de exploração | 54 testes passaram | Exploração real do WDBC exibida no Streamlit | `4e8b9bc` |
| 7 | 2026-06-26 | Seleção controlada do candidato recomendado | 60 testes passaram | Candidato recomendado selecionado em memória | `a483031` |
| 8 | 2026-06-27 | Persistência controlada do candidato recomendado | 65 testes passaram | Artefatos acadêmicos gerados em `models/artifacts/` | `6769ead` |
| 9 | 2026-06-27 | Predição individual acadêmica com artefato persistido | 78 testes passaram | Página de predição consome o modelo persistido com validação rígida | `3efa07f` |
| 10 | 2026-06-27 | Explicabilidade inicial do modelo persistido | 86 testes passaram | Página de explicabilidade exibe importância global e explicação local | `af1bfc1` |
| 11 | 2026-06-27 | Revisão final de qualidade e higiene técnica | 86 testes passaram; cobertura 88% | Textos, ética, checklist e validações finais revisados | `d343d9f` |
| 12 | 2026-06-27 | Reprodutibilidade do ambiente e quality gate | 86 testes passaram; cobertura 88%; quality gate OK | Pins de ambiente e quality gate local criados | pendente |
| 13 | 2026-06-27 | Declaração do modelo final acadêmico da V1 | 86 testes passaram; cobertura 88%; quality gate OK | Regressão Logística persistida declarada como modelo final acadêmico da V1 | pendente |

## Rodada 7 — Seleção controlada do modelo candidato recomendado

- Rodada: 7
- Data: 2026-06-26
- Objetivo: formalizar uma seleção acadêmica controlada do modelo candidato recomendado com base no ranking existente.
- Arquivos alterados: `src/models/select.py`, `src/models/compare.py`, `pages/03_Modelos.py`, `tests/unit/test_select.py`, `tests/unit/test_compare.py`, `tests/smoke/test_models_page.py`, `README.md`, `docs/delivery_checklist.md` e registros em `docs/methodology/`.
- Comandos executados: `git status --short`, leitura da constituição e metodologia, `python -m pytest -q`, `pytest -q`, `git diff --check`, revisão visual da página Streamlit, `git commit` e `git push`.
- Testes: 60 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: seleção do candidato recomendado disponível no payload de comparação e exibida na página de modelos como escolha acadêmica inicial, não diagnóstica; commit e push realizados com sucesso.
- Problemas: smoke test textual falhou inicialmente por checagem frágil; depois, os arquivos de páginas foram regravados pelo PowerShell com mojibake e foram corrigidos antes do commit.
- Commit relacionado: `a483031 feat: seleciona candidato recomendado de forma controlada`.
- Tokens/custo: não disponível.
- Observações: não houve persistência de artefatos finais, SHAP, predição individual final, API, banco ou autenticação.

## Observação para relatório final

A Rodada 7 pode ser descrita como a etapa em que o projeto passou a indicar um modelo candidato recomendado, mantendo o cuidado metodológico de não tratar a escolha como diagnóstico médico nem como modelo final persistido.

## Rodada 8 — Persistência controlada do modelo candidato recomendado

- Rodada: 8
- Data: 2026-06-27
- Objetivo: persistir o modelo candidato recomendado como artefato técnico acadêmico e atualizar o model card operacional.
- Arquivos alterados: `src/models/persist.py`, `pages/03_Modelos.py`, `tests/unit/test_persist.py`, `tests/smoke/test_model_card.py`, `README.md`, `docs/delivery_checklist.md`, `docs/model_card.md`, `models/model_card.md`, `models/artifacts/` e registros em `docs/methodology/`.
- Artefatos criados: `models/artifacts/recommended_model.joblib`, `models/artifacts/recommended_model_metrics.json`, `models/artifacts/recommended_model_feature_names.json`.
- Comandos executados: `git status --short`, leitura da constituição e metodologia, `python -m src.models.persist`, `python -m pytest -q`, `pytest -q`, `git diff --check`, revisão de artefatos e model card, `git commit` e `git push`.
- Testes: 65 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: artefatos acadêmicos do candidato recomendado gerados em `models/artifacts/`, com model card operacional e testes de persistência; commit e push realizados com sucesso.
- Problemas: textos inicialmente apareceram com mojibake no PowerShell; checagem Python confirmou os arquivos críticos sem mojibake antes do commit.
- Commit relacionado: `6769ead feat: persiste candidato recomendado com model card`.
- Tokens/custo: não disponível.
- Observações: não houve SHAP, explicabilidade final, predição individual final, API, banco, autenticação, dataset novo ou alteração do split oficial.

## Rodada 9 — Predição individual acadêmica com artefato persistido

- Rodada: 9
- Data: 2026-06-27
- Objetivo: implementar uma página de predição individual acadêmica usando o modelo candidato persistido na Rodada 8.
- Arquivos alterados: `src/models/predict.py`, `pages/02_Predicao.py`, `tests/unit/test_predict.py`, `tests/smoke/test_prediction_page.py`, `README.md`, `docs/delivery_checklist.md` e registros em `docs/methodology/`.
- Artefatos usados: `models/artifacts/recommended_model.joblib`, `models/artifacts/recommended_model_metrics.json` e `models/artifacts/recommended_model_feature_names.json`.
- Comandos executados: `git status --short`, leitura da constituição e metodologia, `python -m pytest -q`, `pytest -q`, `git diff --check`, revisão visual da página Streamlit, `git commit` e `git push`.
- Testes: 78 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: a página `pages/02_Predicao.py` permite usar exemplos reais do WDBC e ajustar manualmente as 30 features para obter uma estimativa acadêmica, com validação rígida, cards de resultado e avisos não diagnósticos.
- Ajuste pré-commit: a apresentação visual foi refinada com seção de resultado mais direta, cards de métricas, expanders para os grupos de features e expander para os valores usados na estimativa.
- Ajuste final de UX pré-commit: a página passou a manter o último resultado em `st.session_state`, garantindo que os cards de classe estimada e probabilidades fiquem visíveis logo abaixo do botão após a execução.
- Problemas: um teste inicial de checagem de artefatos precisou ser corrigido para reconhecer os nomes canônicos dos JSONs persistidos; o ambiente local emitiu `InconsistentVersionWarning` do Scikit-learn ao carregar o `.joblib`, mas a predição e os testes passaram.
- Commit relacionado: `3efa07f feat: adiciona predicao individual academica`.
- Tokens/custo: não disponível.
- Observações: não houve retreino, novo `.joblib`, novo JSON, CSV, SHAP, API, banco, autenticação, dataset novo ou alteração do split oficial.

## Rodada 10 — Explicabilidade inicial do modelo persistido

- Rodada: 10
- Data: 2026-06-27
- Objetivo: implementar explicabilidade global e local para o modelo persistido, mantendo tudo em memória.
- Arquivos alterados: `src/models/explain.py`, `pages/04_Explicabilidade.py`, `tests/unit/test_explain.py`, `tests/smoke/test_explainability_page.py`, `README.md`, `docs/delivery_checklist.md`, `docs/model_card.md`, `models/model_card.md` e registros em `docs/methodology/`.
- Artefatos usados: `models/artifacts/recommended_model.joblib`, `models/artifacts/recommended_model_metrics.json` e `models/artifacts/recommended_model_feature_names.json`.
- Comandos executados: `git status --short`, `git pull --ff-only`, leitura da constituição e metodologia, `python -m pytest -q`, validações finais da rodada, revisão visual da página Streamlit, `git commit` e `git push`.
- Testes: 86 testes passaram em `python -m pytest -q`.
- Resultado: a página `pages/04_Explicabilidade.py` exibe importância global por coeficientes da Regressão Logística, tenta SHAP em memória quando possível e apresenta explicação local para exemplos reais WDBC; commit e push realizados com sucesso.
- Problemas: warnings externos do SHAP (`PendingDeprecationWarning` em `shap/plots/colors/_colors.py`) foram tratados com filtro localizado apenas na função opcional de SHAP. No ambiente do Codex, os warnings restantes são `InconsistentVersionWarning` do Scikit-learn ao carregar o `.joblib`; não bloquearam testes nem execução.
- Fallback: `fallback_coefficients` por coeficientes da Regressão Logística permanece ativo quando SHAP não está disponível ou estável.
- Commit relacionado: `af1bfc1 feat: adiciona explicabilidade inicial`.
- Tokens/custo: não disponível.
- Observações: não houve retreino, novo `.joblib`, novo JSON, CSV, notebook, API, banco, autenticação, dataset novo ou alteração do split oficial.

## Rodada 11 — Revisão final de qualidade e higiene técnica

- Rodada: 11
- Data: 2026-06-27
- Objetivo: revisar páginas, textos, ética, documentação, cobertura, artefatos e higiene técnica antes da preparação de entrega.
- Arquivos alterados: `app.py`, `pages/03_Modelos.py`, `pages/05_Sobre_Etica.py`, `README.md`, `docs/delivery_checklist.md`, `docs/model_card.md`, `models/model_card.md` e registros em `docs/methodology/`.
- Comandos executados: `git status --short`, `git pull --ff-only`, leitura da constituição e documentação, varreduras de linguagem proibida/mojibake/artefatos, `python -m pytest -q`, `pytest -q`, `pytest --cov=src`, `git diff --check`, `git diff --stat`.
- Testes: 86 testes passaram em `python -m pytest -q` e `pytest -q`.
- Cobertura: `pytest --cov=src` passou com cobertura total de 88%.
- Problemas: `pytest --cov=src` falhou inicialmente porque `pytest-cov` não estava instalado no ambiente atual; o plugin foi instalado localmente por já estar previsto no projeto. Persistem warnings não bloqueantes de versão do Scikit-learn ao carregar o artefato `.joblib`.
- Resultado: textos desatualizados foram corrigidos, a linguagem ética foi reforçada, checklist e model cards foram alinhados ao estado real.
- Commit relacionado: `d343d9f chore: revisa qualidade final da V1`.
- Tokens/custo: não disponível.
- Observações: não houve retreino, novo `.joblib`, novo JSON, CSV, notebook, API, banco, autenticação, dataset novo, troca de modelo ou alteração de artefatos.

## Rodada 12 — Reprodutibilidade do ambiente e quality gate

- Rodada: 12
- Data: 2026-06-27
- Objetivo: consolidar reprodutibilidade do ambiente e criar um quality gate automatizado para reduzir validações manuais repetitivas.
- Arquivos alterados: `requirements.txt`, `docs/environment_reproducibility.md`, `scripts/quality_gate.py`, `README.md`, `docs/delivery_checklist.md` e registros em `docs/methodology/`.
- Comandos executados: `git status --short`, `git pull --ff-only`, leitura da constituição e documentação, `python scripts/quality_gate.py`, testes e validações finais.
- Testes: `python scripts/quality_gate.py` passou; `python -m pytest -q` e `pytest -q` passaram com 86 testes; `pytest --cov=src` passou com cobertura total de 88%.
- Resultado: `scikit-learn==1.9.0` e `joblib==1.5.3` fixados para compatibilidade com o artefato persistido; quality gate local criado para checar mojibake, parâmetros depreciados de largura do Streamlit, artefatos, pins, JSONs, schema, carregamento do `.joblib` e linguagem crítica.
- Problemas: o primeiro teste do quality gate falhou porque o script executado diretamente não encontrava `src`; a raiz do repositório foi adicionada ao `sys.path` do script.
- Commit relacionado: pendente.
- Tokens/custo: não disponível.
- Observações: não houve retreino, novo `.joblib`, novo JSON de modelo, CSV, notebook, API, banco, autenticação, dataset novo ou alteração do split oficial.

## Rodada 13 — Declaração do modelo final acadêmico da V1

- Rodada: 13
- Data: 2026-06-27
- Objetivo: declarar formalmente que o modelo persistido recomendado passa a ser o modelo final acadêmico da V1/MVP.
- Arquivos alterados: `README.md`, `docs/delivery_checklist.md`, `docs/model_card.md`, `models/model_card.md`, `docs/methodology/decision_traceability.md` e registros em `docs/methodology/`.
- Decisão: a Regressão Logística persistida em `models/artifacts/recommended_model.joblib` é o modelo final acadêmico da V1.
- Critério: maior `recall_malignant`, seguido por `roc_auc_malignant` e `f1_malignant`.
- Testes: `python scripts/quality_gate.py` passou; `python -m pytest -q` e `pytest -q` passaram com 86 testes; `pytest --cov=src` passou com cobertura total de 88%.
- Resultado: decisão formal registrada sem alterar artefatos, métricas, feature names, split, dataset, predição ou explicabilidade.
- Problemas: nenhum até o momento.
- Commit relacionado: pendente.
- Tokens/custo: não disponível.
- Observações: não houve retreino, novo `.joblib`, novo JSON de modelo, CSV, notebook, API, banco, autenticação, React/Vite, FastAPI, dataset novo ou alteração de artefatos.

## Template

- Rodada:
- Data:
- Objetivo:
- Arquivos alterados:
- Comandos executados:
- Testes:
- Resultado:
- Problemas:
- Commit relacionado:
- Tokens/custo:
- Observações:
