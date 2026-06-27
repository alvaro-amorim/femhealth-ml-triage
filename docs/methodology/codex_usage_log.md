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
| 8 | 2026-06-27 | Persistência controlada do candidato recomendado | 65 testes passaram | Artefatos acadêmicos gerados em `models/artifacts/` | Pendente |

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
- Comandos executados: `git status --short`, leitura da constituição e metodologia, `python -m src.models.persist`; validações finais completas serão registradas no resumo da rodada.
- Testes: 65 testes passaram em `python -m pytest -q` e `pytest -q`.
- Resultado: artefatos acadêmicos do candidato recomendado gerados em `models/artifacts/`, com model card operacional e testes de persistência; pendente de revisão humana.
- Problemas: nenhum bloqueio relevante até o momento.
- Commit relacionado: pendente.
- Tokens/custo: não disponível.
- Observações: não houve SHAP, explicabilidade final, predição individual final, API, banco, autenticação, dataset novo ou alteração do split oficial.

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
