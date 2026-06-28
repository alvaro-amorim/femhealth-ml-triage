# Rastreabilidade de Decisões — FemHealth ML Triage

Este arquivo conecta decisões técnicas e acadêmicas ao contexto, justificativa, evidências e arquivos relacionados.

---

## Matriz de decisões

| ID | Decisão | Contexto | Justificativa | Evidência | Impacto | Status | Arquivos relacionados |
|---|---|---|---|---|---|---|---|
| DEC-001 | Usar WDBC como dataset principal | O Tech Challenge exige dataset público relacionado à saúde da mulher e classificação com ML | Dataset oficial, estável, sem missing values, binário, integrado ao Scikit-learn e alinhado ao tema câncer de mama | Pesquisa comparativa e constituição do projeto | Reduz risco e viabiliza EDA, modelagem, métricas e explicabilidade | Aceita | `PROJECT_CONSTITUTION.md`, `src/data/schema.py`, `src/data/load_data.py` |
| DEC-002 | Usar Maternal Health Risk como dataset reserva | Necessidade de plano B caso o WDBC tenha bloqueio | Dataset oficial, limpo, com poucas features e aderente à saúde da mulher | Pesquisa comparativa | Mantém alternativa segura sem mudar a arquitetura geral | Aceita | `PROJECT_CONSTITUTION.md`, `docs/methodology/research_log.md` |
| DEC-003 | Usar Streamlit multipage na V1 | O projeto precisa de demonstração funcional sem excesso de integração | Streamlit mantém o fluxo em Python e reduz complexidade de API/frontend | Constituição e pesquisa de stack | App mais simples, integrado ao pipeline de ML e adequado à apresentação acadêmica | Aceita | `app.py`, `pages/`, `PROJECT_CONSTITUTION.md` |
| DEC-004 | Deixar Lovable, React/Vite e FastAPI fora da V1 | Tecnologias web tradicionais poderiam aumentar escopo | O desafio avalia ML, métricas e explicabilidade, não front-end sofisticado | Constituição e decisão estratégica | Reduz risco e tempo de integração | Aceita | `PROJECT_CONSTITUTION.md`, `docs/methodology/research_log.md` |
| DEC-005 | Manter CNN/Computer Vision como extra futuro | Computer Vision é possível, mas complexo | PDF trata visão computacional como extra; V1 deve cumprir o obrigatório primeiro | Análise do desafio e pesquisa de datasets | Evita atraso e complexidade prematura | Aceita | `PROJECT_CONSTITUTION.md`, `docs/methodology/research_log.md` |
| DEC-006 | Priorizar recall da classe maligna | Contexto de triagem exige atenção a falsos negativos | Falso negativo pode atrasar investigação em um cenário real; no projeto, isso justifica análise crítica | Constituição e planejamento de métricas | Orienta comparação de modelos e relatório | Aceita | `PROJECT_CONSTITUTION.md`, futura modelagem |
| DEC-007 | Usar Codex por rodadas pequenas e controladas | O usuário quer economizar créditos e evitar mudanças amplas | Rodadas menores facilitam revisão, testes e commits limpos | Fluxo de desenvolvimento adotado | Reduz risco de gambiarras e arquivos fora de escopo | Aceita | `docs/methodology/codex_usage_log.md`, commits do Git |
| DEC-008 | Criar trilha metodológica de desenvolvimento assistido por IA | O projeto usou ChatGPT, GitHub conectado, pesquisas e Codex | Registrar o processo ajuda relatório, vídeo e rastreabilidade acadêmica | Nova decisão metodológica de 2026-06-26 | Cria documentação contínua em `docs/methodology/` | Aceita | `docs/PROJECT_CONSTITUTION_ADDENDUM_01_METHODOLOGY.md`, `docs/methodology/` |
| DEC-009 | Validar localmente antes de commit | O Codex pode alterar múltiplos arquivos | Testes e execução local reduzem risco de publicar erro | Rodadas 1 e 2 | Commits só entram após validação | Aceita | `tests/`, logs do usuário, Git history |
| DEC-010 | Selecionar candidato recomendado por ranking acadêmico controlado | A comparação inicial já produz ranking por recall maligno, ROC AUC e F1 | Formalizar um candidato recomendado ajuda a continuidade do projeto sem antecipar modelo final clínico ou persistido | Rodada 7 e testes locais | Página de modelos passa a indicar candidato recomendado, mantendo aviso ético e sem salvar artefatos | Aceita | `src/models/select.py`, `src/models/compare.py`, `pages/03_Modelos.py`, `tests/unit/test_select.py` |
| DEC-011 | Versionar artefatos pequenos do candidato recomendado em `models/artifacts/` | As próximas etapas precisam carregar o mesmo pipeline sem retreinar a cada execução | O `.joblib` é pequeno, determinístico, documentado e restrito ao candidato recomendado acadêmico | Rodada 8, model card e testes de persistência | Permite predição/explicabilidade futuras com artefato reproduzível, sem criar ferramenta diagnóstica | Aceita | `src/models/persist.py`, `models/artifacts/`, `models/model_card.md`, `docs/model_card.md` |
| DEC-012 | Usar o artefato persistido para predição individual acadêmica sem retreino | A Rodada 9 precisava executar predição demonstrativa com o candidato recomendado já persistido | Consumir o `.joblib` e os JSONs da Rodada 8 garante reprodutibilidade, preserva o split oficial e evita artefatos novos desnecessários | Rodada 9, testes de predição e página Streamlit | A página de predição passa a validar uma amostra WDBC e exibir estimativa acadêmica sem transformar o projeto em ferramenta diagnóstica | Aceita | `src/models/predict.py`, `pages/02_Predicao.py`, `tests/unit/test_predict.py`, `tests/smoke/test_prediction_page.py` |
| DEC-013 | Usar coeficientes como fallback estável para explicabilidade e SHAP apenas quando disponível | A Rodada 10 precisava ativar explicabilidade sem quebrar em ambientes com incompatibilidade de SHAP | O modelo persistido é Regressão Logística com `StandardScaler`; coeficientes são explicáveis e testáveis, enquanto SHAP pode variar por ambiente | Rodada 10 e testes de explicabilidade | Página de explicabilidade funciona com importância global e local mesmo se SHAP falhar, preservando linguagem acadêmica e não causal | Aceita | `src/models/explain.py`, `pages/04_Explicabilidade.py`, `tests/unit/test_explain.py`, `tests/smoke/test_explainability_page.py` |
| DEC-014 | Declarar a Regressão Logística persistida como modelo final acadêmico da V1/MVP | Após comparação, seleção controlada, persistência, predição e explicabilidade, restava ambiguidade entre candidato recomendado e modelo final acadêmico | O artefato já persistido foi selecionado por `recall_malignant`, `roc_auc_malignant` e `f1_malignant`, usa WDBC, mantém split oficial e já é consumido pelo app sem retreino | Rodada 13, model cards, README e checklist | Fecha a decisão de modelo da V1 sem alterar artefatos, métricas, dataset ou lógica; mantém caráter acadêmico, educacional e não diagnóstico | Aceita | `README.md`, `docs/model_card.md`, `models/model_card.md`, `docs/delivery_checklist.md`, `models/artifacts/` |

---

## Como adicionar novas decisões

Use o próximo ID sequencial e registre:

- decisão;
- contexto;
- justificativa;
- evidência;
- impacto;
- status;
- arquivos relacionados.

Status recomendados:

- Proposta;
- Aceita;
- Substituída;
- Rejeitada;
- Em revisão.
