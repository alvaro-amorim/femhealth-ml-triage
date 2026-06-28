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
- EDA real no Streamlit com visão geral, distribuição de classes, estatísticas descritivas e correlações.
- Projeto modular em Python.
- Pré-processamento com split treino/teste estratificado e reproduzível.
- Pipelines base com `StandardScaler` para modelos sensíveis à escala e passthrough para modelos baseados em árvore.
- Modelagem inicial em memória com Regressão Logística, Árvore de Decisão e KNN.
- Avaliação com foco em recall da classe maligna, respeitando `0 = malignant` no WDBC.
- Página de modelos com comparação acadêmica, ranking, modelo final acadêmico da V1, Curva ROC e matriz de confusão.
- Persistência controlada do modelo final acadêmico como artefato acadêmico em `models/artifacts/`.
- Declaração da Regressão Logística persistida como modelo final acadêmico da V1/MVP, sem uso diagnóstico.
- Predição individual acadêmica usando o artefato persistido, com exemplos reais do WDBC e formulário manual validado.
- Explicabilidade inicial com importância global por coeficientes, SHAP opcional com fallback e explicação local de exemplos reais WDBC.
- Interface Streamlit multipage.
- Testes desde o início.
- Polimento visual inicial do Streamlit para melhorar clareza, consistência e apresentação em vídeo.

## Metodologia de desenvolvimento

Mostrar:

- `PROJECT_CONSTITUTION.md`.
- `docs/methodology/`.
- Commits no GitHub.
- Terminal com testes passando.
- Rodada 3 com 25 testes passando após pré-processamento e split.
- Rodada 4 com 37 testes passando após modelagem inicial e avaliação.
- Rodada 5 com 43 testes passando após integração da comparação inicial na página de modelos.
- Rodada 6A com 45 testes passando após inclusão da Curva ROC na comparação inicial.
- Rodada 6B com 54 testes passando após implementação da EDA real do WDBC.
- Rodada 7 com 60 testes passando após seleção controlada do candidato recomendado.
- Rodada 8 com 65 testes passando após persistência controlada do candidato recomendado e model card operacional.
- Rodada 9 com 78 testes passando após predição individual acadêmica usando o artefato persistido.
- Rodada 10 com 86 testes passando após explicabilidade inicial do modelo persistido.
- Rodada 11 com revisão final de qualidade, 86 testes passando e cobertura total de 88% em `src`.
- Rodada 12 com ambiente reprodutível documentado, versões críticas fixadas e quality gate local antes de commit/push.
- Rodada 13 com declaração formal do modelo final acadêmico da V1 sem retreino nem alteração de artefatos.
- Rodada 14 com polimento visual assistido por inspeção visual real do app Streamlit.
- App Streamlit rodando.

## Uso responsável de IA

- ChatGPT apoiou planejamento, revisão e arquitetura.
- Codex foi usado em rodadas pequenas.
- O usuário revisou testes antes dos commits.

## Pontos para mostrar na tela

- Home do Streamlit.
- Página de exploração com distribuição das classes, grupos de features, estatísticas e correlações.
- Página de comparação de modelos.
- Seção de modelo final acadêmico da V1, com aviso de que o artefato persistido é acadêmico e não serve para uso real em saúde.
- Artefatos em `models/artifacts/` e model card operacional.
- Página de predição individual com exemplos reais WDBC, probabilidades estimadas e aviso não diagnóstico.
- Página de explicabilidade com importância global das features e explicação local de uma amostra.
- Curva ROC usando probabilidade da classe maligna.
- Testes com `pytest`.
- GitHub com commits.
- Página Sobre e Ética com escopo, limitações e uso responsável de IA.

## Estrutura provável

1. Problema.
2. Dataset.
3. Metodologia.
4. App.
5. Testes.
6. Modelos.
7. Explicabilidade.
8. Ética e limitações.
