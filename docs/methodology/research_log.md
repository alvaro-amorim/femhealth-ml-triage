# Registro de Pesquisas — FemHealth ML Triage

Este arquivo registra pesquisas e análises que fundamentaram decisões do projeto.

---

## Template de pesquisa

| Campo | Conteúdo esperado |
|---|---|
| Data | Data da pesquisa |
| Tema | Assunto pesquisado |
| Objetivo | Por que a pesquisa foi feita |
| Alternativas avaliadas | Opções consideradas |
| Fontes | Fontes consultadas ou tipo de fonte |
| Síntese | O que foi encontrado |
| Decisão derivada | Decisão tomada com base na pesquisa |
| Impacto no projeto | Como a decisão afeta arquitetura, escopo ou entrega |
| Relação com o Tech Challenge | Como se conecta ao desafio oficial |

---

## 2026-06-26 — Seleção do dataset principal

| Campo | Registro |
|---|---|
| Tema | Escolha do dataset público para saúde da mulher |
| Objetivo | Selecionar um dataset seguro, reproduzível e adequado para classificação tabular com explicabilidade |
| Alternativas avaliadas | WDBC, Maternal Health Risk, PCOS/SOP, Cervical Cancer Risk Factors, Contraceptive Method Choice, datasets textuais de misoginia/violência e datasets de imagem de câncer de mama |
| Fontes | PDF oficial do Tech Challenge, documentação de datasets públicos, documentação Scikit-learn, pesquisa técnica comparativa |
| Síntese | O WDBC é oficial, estável, pequeno, sem missing values, binário, integrado ao Scikit-learn e diretamente relacionado a câncer de mama |
| Decisão derivada | Usar Breast Cancer Wisconsin Diagnostic como dataset principal |
| Impacto no projeto | Reduz risco operacional, facilita testes, EDA, modelagem, métricas e SHAP |
| Relação com o Tech Challenge | Atende ao requisito de dataset público relacionado à saúde da mulher e classificação com Machine Learning |

---

## 2026-06-26 — Dataset reserva

| Campo | Registro |
|---|---|
| Tema | Definição de plano B para dataset |
| Objetivo | Evitar bloqueio caso o WDBC se tornasse inviável |
| Alternativas avaliadas | Maternal Health Risk, PCOS/SOP, Cervical Cancer Risk Factors |
| Síntese | Maternal Health Risk é oficial, limpo, com poucas features e aderente à saúde da mulher |
| Decisão derivada | Definir Maternal Health Risk como dataset reserva |
| Impacto no projeto | Mantém uma alternativa tabular simples sem mudar toda a arquitetura |
| Relação com o Tech Challenge | Preserva aderência ao tema de saúde da mulher |

---

## 2026-06-26 — Por que PCOS/SOP não entrou na V1

| Campo | Registro |
|---|---|
| Tema | Avaliação do dataset PCOS/SOP |
| Objetivo | Considerar uma base tematicamente forte para saúde feminina |
| Síntese | PCOS/SOP é muito aderente ao tema, mas depende de Kaggle, pode ter variações de versão/schema/licença e aumenta risco operacional |
| Decisão derivada | Não usar PCOS/SOP na V1 |
| Impacto no projeto | Evita retrabalho e mantém foco no obrigatório |
| Relação com o Tech Challenge | Garante entrega mais segura da fase atual |

---

## 2026-06-26 — Decisão sobre Computer Vision

| Campo | Registro |
|---|---|
| Tema | Uso de CNN/imagens médicas |
| Objetivo | Avaliar se visão computacional deveria ser núcleo da V1 |
| Síntese | O PDF trata visão computacional como extra. Implementar CNN exigiria dataset, pipeline e explicabilidade próprios, aumentando risco |
| Decisão derivada | Manter CNN/Computer Vision como extra futuro |
| Impacto no projeto | Foco permanece em Machine Learning tabular e explicabilidade |
| Relação com o Tech Challenge | Cumpre o obrigatório antes de diferenciais complexos |

---

## 2026-06-26 — Decisão de stack e interface

| Campo | Registro |
|---|---|
| Tema | Escolha entre Streamlit, Lovable, React/Vite e FastAPI |
| Objetivo | Selecionar a stack mais segura para a Fase 1 |
| Síntese | Streamlit mantém app, gráficos, predição e explicabilidade no ecossistema Python. React/Vite/FastAPI adicionariam integração, API, CORS, build e deploy mais complexos sem ganho proporcional na V1 |
| Decisão derivada | Usar Streamlit multipage; deixar Lovable, React/Vite e FastAPI fora da V1 |
| Impacto no projeto | Reduz risco, acelera entrega e alinha com as aulas de Python/ML |
| Relação com o Tech Challenge | Prioriza Machine Learning, métricas, explicabilidade e demonstração funcional |
