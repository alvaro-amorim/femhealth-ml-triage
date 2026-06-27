# Checklist de entrega — Tech Challenge Fase 1

## Base do projeto

- [x] Constituição oficial lida e preservada.
- [x] Estrutura modular Python/Streamlit criada.
- [x] Schema canônico das 30 features definido.
- [x] README, ADRs, wireframes e model card iniciados.
- [x] Dataset WDBC carregado via Scikit-learn.
- [x] EDA inicial do WDBC implementada na página de exploração.
- [x] Distribuição de classes, estatísticas descritivas, missing values e correlações exploratórias apresentados.
- [ ] Notebooks de EDA concluídos.

## Modelagem e explicabilidade

- [x] Separação treino/teste estratificada e reproduzível.
- [x] Pelo menos dois classificadores candidatos treináveis em memória.
- [x] Accuracy, precision, recall, F1 e ROC AUC calculados para candidatos.
- [x] Matriz de confusão calculada para candidatos.
- [x] Comparação inicial de candidatos exibida na página de modelos.
- [x] Ranking inicial por recall maligno, ROC AUC e F1 exibido.
- [x] Matriz de confusão exibida na página de modelos.
- [x] Curva ROC apresentada.
- [x] Seleção acadêmica de modelo candidato recomendado implementada.
- [x] Critérios de seleção do candidato recomendado documentados.
- [x] Modelo candidato recomendado persistido para fins acadêmicos.
- [x] Métricas do modelo candidato recomendado persistidas.
- [x] Feature names do modelo candidato recomendado persistidos.
- [ ] Modelo final definitivo para entrega, métricas e feature names revisados.
- [ ] Feature importance e SHAP implementados.

## Aplicação e qualidade

- [ ] Páginas Streamlit funcionais.
- [x] Página de exploração parcialmente funcional com EDA real do WDBC.
- [x] Página de modelos parcialmente funcional com comparação acadêmica inicial.
- [ ] Entrada individual e CSV validados.
- [ ] Exemplos reais e pequenos do WDBC disponibilizados.
- [x] Smoke tests de estrutura, schema e carregamento criados.
- [x] Testes de validação de schema e entrada criados.
- [x] Testes de pré-processamento implementados.
- [x] Testes de modelagem e avaliação inicial implementados.
- [ ] Testes de predição implementados.
- [ ] `pytest` e `pytest --cov=src` passam no projeto completo.

## Documentação e entrega

- [x] Aviso ético no README e model card.
- [ ] Aviso ético em todas as páginas e no relatório.
- [ ] README atualizado com treinamento, artefatos, exemplos, repositório e vídeo.
- [x] Model card operacional atualizado para o candidato persistido.
- [ ] Relatório técnico em PDF concluído.
- [ ] Vídeo de até 15 minutos publicado e referenciado.
- [ ] Revisão final de limpeza, segredos, testes e links.
