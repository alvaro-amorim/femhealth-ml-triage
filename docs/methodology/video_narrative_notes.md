# Notas para Narrativa do Vídeo — FemHealth ML Triage

Este arquivo acumula pontos para o roteiro final de demonstração.

## Narrativa do problema

- Aplicação acadêmica de Machine Learning em saúde da mulher.
- Classificação tabular de amostras de massa mamária com WDBC.
- Uso demonstrativo, sem substituir avaliação médica.

Frase possível:

> O FemHealth ML Triage mostra como um pipeline de Machine Learning pode apoiar uma triagem analítica de forma educacional e responsável.

## Narrativa da solução

- Dataset público WDBC carregado via Scikit-learn.
- Projeto modular em Python.
- Pré-processamento com split treino/teste estratificado e reproduzível.
- Pipelines base com `StandardScaler` para modelos sensíveis à escala e passthrough para modelos baseados em árvore.
- Modelagem inicial em memória com Regressão Logística, Árvore de Decisão e KNN.
- Avaliação com foco em recall da classe maligna, respeitando `0 = malignant` no WDBC.
- Página de modelos com comparação acadêmica inicial, ranking e matriz de confusão.
- Interface Streamlit multipage.
- Testes desde o início.
- Explicabilidade planejada com feature importance e SHAP.

## Metodologia de desenvolvimento

Mostrar:

- `PROJECT_CONSTITUTION.md`.
- `docs/methodology/`.
- Commits no GitHub.
- Terminal com testes passando.
- Rodada 3 com 25 testes passando após pré-processamento e split.
- Rodada 4 com 37 testes passando após modelagem inicial e avaliação.
- Rodada 5 com 43 testes passando após integração da comparação inicial na página de modelos.
- App Streamlit rodando.

## Uso responsável de IA

- ChatGPT apoiou planejamento, revisão e arquitetura.
- Codex foi usado em rodadas pequenas.
- O usuário revisou testes antes dos commits.

## Pontos para mostrar na tela

- Home do Streamlit.
- Página de comparação inicial de modelos.
- Testes com `pytest`.
- GitHub com commits.
- Futuras páginas de EDA, predição, modelos e explicabilidade.

## Estrutura provável

1. Problema.
2. Dataset.
3. Metodologia.
4. App.
5. Testes.
6. Modelos.
7. Explicabilidade.
8. Ética e limitações.
