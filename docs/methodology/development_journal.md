# Diário de Desenvolvimento — FemHealth ML Triage

Este arquivo registra a evolução cronológica do projeto para apoiar o relatório técnico final, a rastreabilidade acadêmica e o roteiro do vídeo de demonstração.

## Template de entrada

| Campo | Conteúdo esperado |
|---|---|
| Data | Data da atividade |
| Etapa | Fase ou rodada do projeto |
| Objetivo | O que se pretendia realizar |
| Ações realizadas | Resumo das ações |
| Comandos executados | Comandos relevantes |
| Ferramentas usadas | ChatGPT, GitHub, Codex, PowerShell, VS Code, Streamlit, Pytest etc. |
| Problemas encontrados | Erros, riscos ou bloqueios |
| Soluções aplicadas | Como o problema foi resolvido |
| Testes executados | Testes e validações |
| Resultado | Resultado da etapa |
| Commit relacionado | SHA ou mensagem do commit |
| Próximo passo | Próxima ação planejada |

---

## 2026-06-26 — Constituição do projeto

| Campo | Registro |
|---|---|
| Etapa | Planejamento e constituição |
| Objetivo | Definir a fonte oficial da verdade do projeto |
| Ações realizadas | Criação do `PROJECT_CONSTITUTION.md` com escopo, stack, dataset, arquitetura, testes, regras do Codex e critérios de entrega |
| Ferramentas usadas | ChatGPT como tutor técnico e arquiteto; GitHub; PowerShell |
| Problemas encontrados | Necessidade de evitar escopo amplo demais e tecnologias fora da V1 |
| Soluções aplicadas | Congelamento do escopo em WDBC + Python + Scikit-learn + SHAP + Streamlit |
| Testes executados | Não aplicável nesta etapa documental |
| Resultado | Constituição criada e adicionada à raiz do repositório |
| Commit relacionado | Commit inicial anterior ao bootstrap estrutural |
| Próximo passo | Bootstrap estrutural do projeto |

## 2026-06-26 — Bootstrap estrutural

| Campo | Registro |
|---|---|
| Etapa | Rodada 1 do Codex |
| Objetivo | Criar estrutura inicial do repositório sem implementar a aplicação completa |
| Ações realizadas | Criação de `app.py`, `pages/`, `src/`, `data/`, `models/`, `notebooks/`, `tests/`, `docs/`, `requirements.txt`, `pytest.ini` e documentação inicial |
| Ferramentas usadas | Codex no VS Code; ChatGPT como planejador/revisor; PowerShell; Pytest; Streamlit |
| Problemas encontrados | `pytest` inicialmente não encontrava o pacote `src` quando executado diretamente |
| Soluções aplicadas | Criação de `pytest.ini` com `pythonpath = .` e `testpaths = tests` |
| Testes executados | `python -m pytest -q`; `pytest -q`; `streamlit run app.py` |
| Resultado | 3 testes passaram e app Streamlit inicial abriu em `localhost:8501` |
| Commit relacionado | `556ce05 chore: bootstrap inicial do projeto` |
| Próximo passo | Implementar carregamento real do WDBC e validação de schema |

## 2026-06-26 — Correção do `pytest.ini` para UTF-8 sem BOM

| Campo | Registro |
|---|---|
| Etapa | Validação local pós-bootstrap |
| Objetivo | Garantir que `pytest` e `python -m pytest` funcionassem de forma equivalente |
| Ações realizadas | Recriação do `pytest.ini` usando `System.Text.UTF8Encoding($false)` no PowerShell |
| Ferramentas usadas | PowerShell; Pytest; ChatGPT como revisor |
| Problemas encontrados | Pytest acusou `unexpected line: '\ufeff[pytest]'` devido a BOM no arquivo |
| Soluções aplicadas | Remoção e recriação do arquivo em UTF-8 sem BOM |
| Testes executados | `python -m pytest -q`; `pytest -q` |
| Resultado | 3 testes passaram nos dois comandos |
| Commit relacionado | Incluído no commit `556ce05` |
| Próximo passo | Validar Streamlit e commitar bootstrap |

## 2026-06-26 — Validação local com Python 3.11 e Streamlit

| Campo | Registro |
|---|---|
| Etapa | Validação de ambiente |
| Objetivo | Confirmar que o projeto roda no ambiente oficial da V1 |
| Ações realizadas | Ativação da `.venv`, verificação de Python 3.11.9, instalação de dependências, execução de testes e app |
| Ferramentas usadas | PowerShell; Python 3.11.9; Pytest; Streamlit |
| Problemas encontrados | Avisos LF/CRLF normais do Git no Windows |
| Soluções aplicadas | Avisos mantidos como não bloqueantes |
| Testes executados | `python -m pytest -q`; `pytest -q`; `streamlit run app.py` |
| Resultado | App inicial carregou corretamente no navegador |
| Commit relacionado | `556ce05 chore: bootstrap inicial do projeto` |
| Próximo passo | Rodada 2 do Codex |

## 2026-06-26 — Carregamento real do WDBC e validação de schema

| Campo | Registro |
|---|---|
| Etapa | Rodada 2 do Codex |
| Objetivo | Implementar carregamento real do dataset e validações de entrada |
| Ações realizadas | Implementação de `load_wdbc_data()`, `load_wdbc_dataframe()`, constantes de schema e validações estritas |
| Ferramentas usadas | Codex; ChatGPT; GitHub; Pytest; Scikit-learn |
| Problemas encontrados | Comando manual assumiu retorno com atributos `.features` e `.target`, mas a função retorna tupla `(features, target, metadata)` |
| Soluções aplicadas | Interface confirmada por teste manual usando desempacotamento da tupla |
| Testes executados | `python -m pytest -q`; `pytest -q`; validação direta do shape `(569, 30)` e duas classes |
| Resultado | 14 testes passaram; carregamento local confirmado |
| Commit relacionado | `ba2aa27 data: implementa carregamento e validação do WDBC` |
| Próximo passo | Pré-processamento e split treino/teste |

## 2026-06-26 — Pré-processamento e split treino/teste

| Campo | Registro |
|---|---|
| Etapa | Rodada 3 do Codex |
| Objetivo | Criar funções de pré-processamento, split estratificado e pipelines base |
| Ações realizadas | Criação local de `separate_features_and_target`, `split_train_test`, `build_scaling_pipeline`, `build_passthrough_pipeline` e `validate_train_test_split` |
| Ferramentas usadas | Codex; ChatGPT; Pytest; Scikit-learn |
| Problemas encontrados | Nenhum problema reportado pelo Codex |
| Soluções aplicadas | Não aplicável |
| Testes executados | `git diff --check`; `python -m pytest -q`; `pytest -q` |
| Resultado | 25 testes passaram localmente; alterações ainda sem commit remoto no momento da criação desta trilha metodológica |
| Commit relacionado | Não disponível — status local sem commit remoto |
| Próximo passo | Sincronizar documentação metodológica via `git pull` antes de continuar |

## 2026-06-26 — Validação pós-pull da Rodada 3

| Campo | Registro |
|---|---|
| Etapa | Sincronização metodológica e revisão local |
| Objetivo | Sincronizar a documentação metodológica remota e validar a Rodada 3 local sem sobrescrever alterações |
| Ações realizadas | Execução de `git status --short`, `git pull --ff-only`, leitura do `PROJECT_CONSTITUTION.md`, leitura do adendo metodológico e revisão do diff local da Rodada 3 |
| Ferramentas usadas | Codex; PowerShell; Git; Pytest |
| Problemas encontrados | Nenhum conflito no pull; apenas avisos LF/CRLF normais do Git no Windows |
| Soluções aplicadas | Pull fast-forward preservou as alterações locais; nenhuma ação destrutiva foi usada |
| Testes executados | `python -m pytest -q`; `pytest -q`; `git diff --check` |
| Resultado | 25 testes passaram nos dois comandos; Rodada 3 segue pronta para revisão humana e commit |
| Commit relacionado | Não disponível — alterações locais ainda sem commit |
| Próximo passo | Revisar e commitar a Rodada 3 quando aprovado |
