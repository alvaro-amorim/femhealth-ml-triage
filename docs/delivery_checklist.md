# Checklist de entrega — Tech Challenge Fase 1

## Base do projeto

- [x] Constituição oficial lida e preservada.
- [x] Estrutura modular Python/Streamlit criada.
- [x] Schema canônico das 30 features definido.
- [x] README, ADRs, wireframes e model card iniciados.
- [x] Documento de reprodutibilidade do ambiente criado.
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
- [x] Curva ROC revisada com visualização didática, eixos 0–1, linha de referência e legenda com AUC.
- [x] Seleção acadêmica controlada do modelo final da V1 implementada.
- [x] Critérios de seleção do modelo final acadêmico documentados.
- [x] Modelo final acadêmico persistido para fins acadêmicos.
- [x] Métricas do modelo final acadêmico persistidas.
- [x] Feature names do modelo final acadêmico persistidos.
- [x] Modelo final acadêmico da V1 declarado e revisado com métricas e feature names existentes.
- [x] Feature importance inicial por coeficientes implementada.
- [x] SHAP opcional com fallback técnico implementado.

## Aplicação e qualidade

- [x] Páginas Streamlit principais funcionais.
- [x] Jornada guiada do MVP implementada na interface Streamlit.
- [x] Componentes visuais simples padronizados para hero, cards e aviso ético.
- [x] Seletor de tema claro/escuro implementado na sidebar.
- [x] Seletor de idioma Português/Inglês implementado na sidebar.
- [x] Dicionário didático das 30 features WDBC implementado para apresentação na UI.
- [x] Página de exploração parcialmente funcional com EDA real do WDBC.
- [x] Página de modelos parcialmente funcional com comparação acadêmica inicial.
- [x] Página de explicabilidade parcialmente funcional com importância global e explicação local.
- [x] Entrada individual validada.
- [x] Exemplos reais do WDBC usados para demonstração na página de predição.
- [x] Smoke tests de estrutura, schema e carregamento criados.
- [x] Testes de validação de schema e entrada criados.
- [x] Testes de pré-processamento implementados.
- [x] Testes de modelagem e avaliação inicial implementados.
- [x] Testes de predição implementados.
- [x] Testes de explicabilidade implementados.
- [x] `pytest` e `pytest --cov=src` passam no projeto completo.
- [x] Quality gate automatizado criado para checar ambiente, artefatos, schema, mojibake e linguagem crítica.

## Documentação e entrega

- [x] Aviso ético no README e model card.
- [x] Aviso ético nas páginas principais do app.
- [ ] Aviso ético no relatório final.
- [ ] README atualizado com treinamento, artefatos, exemplos, repositório e vídeo.
- [x] README atualizado com quality gate e reprodutibilidade do ambiente.
- [x] Model card operacional atualizado para o modelo final acadêmico persistido.
- [ ] Relatório técnico em PDF concluído.
- [ ] Vídeo de até 15 minutos publicado e referenciado.
- [ ] Revisão visual humana final.
- [ ] Revisão final de limpeza, segredos, testes e links.
- [ ] Futuro opcional: entrada assistida por arquivo/OCR experimental apenas para relatórios tabulares estruturados contendo as 30 features WDBC; fora do escopo para imagem médica real, mamografia ou ultrassom.
