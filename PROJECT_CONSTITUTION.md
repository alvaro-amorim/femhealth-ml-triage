# PROJECT_CONSTITUTION.md

# FemHealth ML Triage

**Nome público:** FemHealth ML Triage  
**Nome da pasta/repositório:** `femhealth-ml-triage`  
**Descrição do repositório GitHub:** Aplicação acadêmica de Machine Learning para apoio à triagem analítica em saúde da mulher, com classificação tabular, explicabilidade e interface em Streamlit.  
**Tech Challenge:** Fase 1 — Pós-graduação  
**Status do documento:** Fonte oficial da verdade do projeto  
**Versão do documento:** 1.0  
**Stack oficial da V1:** Python 3.11 + Pandas + NumPy + Scikit-learn + SHAP + Joblib + Matplotlib + Plotly + Streamlit + Pytest  
**Dataset principal:** Breast Cancer Wisconsin Diagnostic — WDBC  
**Dataset reserva:** Maternal Health Risk — UCI  
**Interface oficial da V1:** Streamlit multipage  
**Fora da V1:** Lovable, React/Vite, FastAPI, banco de dados, autenticação, CNN/Computer Vision como núcleo, NLP como núcleo, deploy complexo obrigatório.

---

## Sumário

1. [Finalidade deste documento](#1-finalidade-deste-documento)
2. [Identidade do projeto](#2-identidade-do-projeto)
3. [Contexto oficial do Tech Challenge](#3-contexto-oficial-do-tech-challenge)
4. [Decisão estratégica consolidada](#4-decisão-estratégica-consolidada)
5. [Dataset principal e dataset reserva](#5-dataset-principal-e-dataset-reserva)
6. [Arquitetura oficial da V1](#6-arquitetura-oficial-da-v1)
7. [Estrutura de pastas e arquivos](#7-estrutura-de-pastas-e-arquivos)
8. [Especificação do app Streamlit](#8-especificação-do-app-streamlit)
9. [Predição Individual — especificação detalhada](#9-predição-individual--especificação-detalhada)
10. [Modelagem](#10-modelagem)
11. [Métricas](#11-métricas)
12. [Explicabilidade](#12-explicabilidade)
13. [Testes](#13-testes)
14. [Documentação](#14-documentação)
15. [Regras para o Codex](#15-regras-para-o-codex)
16. [Setup local em Windows/PowerShell](#16-setup-local-em-windowspowershell)
17. [GitHub, branches e commits](#17-github-branches-e-commits)
18. [Plano de desenvolvimento](#18-plano-de-desenvolvimento)
19. [Definition of Ready e Definition of Done](#19-definition-of-ready-e-definition-of-done)
20. [Checklist final](#20-checklist-final)
21. [Apêndices](#21-apêndices)

---

# 1. Finalidade deste documento

Este arquivo é a **constituição oficial do projeto FemHealth ML Triage**.

Ele deve orientar:

- decisões de arquitetura;
- organização do repositório;
- escopo técnico;
- escopo acadêmico;
- implementação com apoio do Codex;
- documentação;
- testes;
- relatório técnico;
- vídeo de demonstração;
- revisão final antes da entrega.

Este documento deve ser considerado a **fonte primária de orientação do desenvolvimento**, abaixo apenas do PDF oficial do Tech Challenge.

Antes de qualquer implementação relevante, o Codex ou qualquer pessoa desenvolvedora deve ler este documento inteiro.

## 1.1 Objetivo da constituição

A constituição existe para evitar:

- desenvolvimento desalinhado com o PDF oficial;
- excesso de tecnologia sem ganho acadêmico;
- app bonito, mas fraco em Machine Learning;
- código improvisado;
- notebook solto sem estrutura;
- mocks esquecidos;
- dependências desnecessárias;
- documentação genérica;
- mudanças de dataset no meio do projeto;
- promessas médicas indevidas;
- uso do Codex de forma descontrolada.

## 1.2 Ordem de prioridade das decisões

Quando houver conflito entre fontes, seguir esta ordem:

1. PDF oficial do Tech Challenge da Fase 1.
2. Este arquivo `PROJECT_CONSTITUTION.md`.
3. Relatório de pesquisa aprofundada usado para decisão estratégica.
4. `README.md`.
5. `docs/decisions.md`.
6. Demais documentos do repositório.
7. Sugestões do Codex.
8. Preferências visuais ou ideias futuras.

O Codex **não tem autorização** para contrariar este documento sem registrar a divergência e pedir validação humana.

## 1.3 Princípio central

O projeto deve ser desenvolvido como um produto acadêmico-profissional:

> Simples o suficiente para ser entregue com segurança, mas completo o suficiente para demonstrar domínio real de Machine Learning, explicabilidade, responsabilidade ética, documentação e testes.

---

# 2. Identidade do projeto

## 2.1 Nome público

**FemHealth ML Triage**

## 2.2 Nome da pasta/repositório

```text
femhealth-ml-triage
```

## 2.3 Descrição curta

Aplicação acadêmica de Machine Learning para apoio à triagem analítica em saúde da mulher, com classificação tabular, explicabilidade e interface em Streamlit.

## 2.4 Descrição longa

O **FemHealth ML Triage** é uma aplicação acadêmica desenvolvida para o Tech Challenge da Fase 1 da pós-graduação. O sistema demonstra um pipeline de Machine Learning aplicado à saúde da mulher, com foco na classificação de amostras de massa mamária a partir de dados tabulares do dataset Breast Cancer Wisconsin Diagnostic.

A solução contempla análise exploratória de dados, pré-processamento, treinamento e comparação de modelos de classificação, avaliação por métricas adequadas ao contexto de triagem médica, explicabilidade global e local com feature importance e SHAP, além de uma interface interativa em Streamlit multipage para demonstração do fluxo.

O sistema é estritamente educacional e demonstrativo. Ele não substitui avaliação médica, laudo anatomopatológico, exame clínico ou decisão profissional.

## 2.5 Objetivo acadêmico

Construir uma solução alinhada ao Tech Challenge da Fase 1 que demonstre, de forma clara e completa:

- escolha justificada de dataset público relacionado à saúde da mulher;
- exploração e análise dos dados;
- pré-processamento com Python;
- classificação supervisionada com Machine Learning;
- uso de duas ou mais técnicas de classificação;
- separação treino/teste;
- avaliação com métricas adequadas;
- interpretação com feature importance e SHAP;
- discussão crítica sobre uso prático;
- documentação técnica;
- app demonstrável;
- testes automatizados;
- repositório limpo e reprodutível.

## 2.6 Objetivo técnico

Desenvolver uma aplicação Python modular, testável e documentada composta por:

- módulos Python organizados em `src/`;
- notebooks de análise em `notebooks/`;
- modelo final persistido em `models/`;
- dados de exemplo em `data/examples/`;
- app Streamlit multipage;
- testes smoke, unitários e, se viável, testes leves de app;
- documentação em `docs/`;
- README completo;
- model card;
- base para relatório técnico e vídeo.

## 2.7 Persona de uso

A aplicação é voltada para:

- avaliadores acadêmicos;
- professores da pós-graduação;
- colegas de equipe;
- pessoas interessadas em entender um pipeline de ML aplicado à saúde;
- profissionais técnicos avaliando a arquitetura e explicabilidade.

A V1 **não é direcionada a pacientes finais**.

## 2.8 Proposta de valor acadêmica

O projeto se destaca por unir:

- aderência direta ao enunciado;
- dataset estável e bem documentado;
- pipeline de ML reproduzível;
- comparação de modelos;
- foco em recall da classe maligna;
- explicabilidade global e local;
- interface profissional;
- testes;
- documentação forte;
- postura ética clara.

## 2.9 Escopo resumido da V1

A V1 deve entregar:

- dataset WDBC carregado via Scikit-learn;
- EDA;
- pré-processamento;
- comparação de modelos;
- modelo final;
- SHAP/feature importance;
- Streamlit multipage;
- predição individual;
- exemplos benigno/maligno;
- upload de CSV;
- preenchimento manual avançado;
- testes mínimos;
- documentação;
- base para relatório e vídeo.

## 2.10 Linguagem permitida por responsabilidade médica

Usar termos como:

- ferramenta acadêmica;
- aplicação demonstrativa;
- apoio à triagem analítica;
- apoio à decisão;
- classificação estatística;
- estimativa do modelo;
- risco estimado;
- probabilidade estimada;
- análise exploratória;
- interpretação do modelo;
- explicabilidade;
- uso educacional.

## 2.11 Linguagem proibida por responsabilidade médica

Não usar termos como:

- diagnóstico definitivo;
- diagnóstico automático;
- laudo automático;
- substitui o médico;
- detecta câncer com certeza;
- prevê câncer com segurança clínica;
- ferramenta clínica pronta;
- recomendação médica;
- decisão terapêutica;
- prevenção garantida;
- resultado confiável para paciente real;
- sistema hospitalar real.

## 2.12 Aviso ético obrigatório

Este texto, ou variação equivalente, deve aparecer no app, no README, no model card e no relatório:

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.

---

# 3. Contexto oficial do Tech Challenge

## 3.1 Resumo do desafio

O Tech Challenge da Fase 1 propõe a criação de uma solução inicial de Inteligência Artificial aplicada à saúde e segurança da mulher.

O contexto apresentado envolve uma rede de hospitais e centros de saúde especializados no atendimento à mulher, que busca implementar um sistema inteligente capaz de apoiar profissionais de saúde na identificação precoce de condições de risco.

O desafio pede uma base de sistema de IA focada em Machine Learning, capaz de analisar dados médicos automaticamente e identificar padrões de risco relacionados à saúde feminina.

## 3.2 Relação com saúde e segurança da mulher

O FemHealth ML Triage se relaciona ao desafio por abordar o câncer de mama, uma condição diretamente associada à saúde da mulher e citada como exemplo no enunciado oficial.

A aplicação não trata diretamente violência doméstica, prontuários ou imagens médicas na V1, porque a decisão estratégica prioriza uma entrega tabular robusta e alinhada ao núcleo obrigatório do desafio.

## 3.3 Relação com Machine Learning

O projeto usa Machine Learning supervisionado para classificação binária.

A tarefa principal é:

```text
Entrada: 30 atributos numéricos de uma amostra de massa mamária.
Saída: classificação estimada pelo modelo como benigna ou maligna.
```

A aplicação deve demonstrar:

- seleção de dataset;
- EDA;
- pré-processamento;
- treino de modelos;
- avaliação;
- comparação;
- escolha de modelo final;
- explicabilidade.

## 3.4 Relação com Visão Computacional

Embora o dataset WDBC tenha features derivadas de imagens digitalizadas de punção aspirativa por agulha fina, a V1 **não processa imagens diretamente**.

Visão Computacional fica como:

- contexto conceitual;
- possível extra futuro;
- não núcleo da V1.

## 3.5 Requisitos obrigatórios do PDF oficial

O projeto deve atender aos seguintes requisitos:

| Requisito do desafio | Como o FemHealth ML Triage atende |
|---|---|
| Dataset público relacionado à saúde e segurança da mulher | WDBC, relacionado a câncer de mama |
| Classificação de risco/diagnóstico via ML | Classificação binária benigno/maligno |
| Exploração dos dados | Página de EDA + notebooks |
| Estatísticas descritivas | Tabelas e gráficos |
| Visualização de distribuições | Histogramas/boxplots |
| Identificação de padrões | Discussão da EDA e correlações |
| Limpeza e pré-processamento | Pipeline Scikit-learn e validação |
| Conversão de variáveis | Dataset já numérico; validação documentada |
| Análise de correlação | Heatmap e discussão |
| Duas ou mais técnicas de classificação | Regressão Logística, KNN, Árvore, Random Forest |
| Separação treino/teste | Split estratificado e reprodutível |
| Métricas adequadas | Accuracy, precision, recall, F1, ROC AUC |
| Discussão da métrica | Recall maligno como prioridade |
| Explicabilidade | Feature importance e SHAP |
| Discussão crítica | Sobre/Ética, relatório e README |
| Código Python estruturado | `src/`, notebooks e app |
| README com execução | Obrigatório |
| Dataset ou link | README e docs |
| Resultados, prints e gráficos | App, notebooks e relatório |
| Relatório técnico em PDF | Etapa final |
| Vídeo até 15 minutos | Etapa final |

## 3.6 Entregáveis finais

O projeto deve preparar:

- repositório GitHub;
- código-fonte completo;
- README.md;
- dataset ou link para dataset;
- notebooks ou scripts demonstrativos;
- app Streamlit;
- prints e gráficos;
- relatório técnico em PDF;
- vídeo de demonstração até 15 minutos publicado no YouTube ou Vimeo;
- link do repositório no relatório;
- link do vídeo no relatório e README.

## 3.7 Riscos de reprovação ou perda de nota

| Risco | Por que é grave | Mitigação |
|---|---|---|
| Não usar dataset de saúde da mulher | Fere o contexto do desafio | Usar WDBC |
| Fazer app visual sem ML forte | Desvia do objetivo principal | Priorizar pipeline, métricas e SHAP |
| Usar apenas um modelo | PDF pede duas ou mais técnicas | Comparar pelo menos 3 modelos |
| Não separar treino/teste | Erro metodológico grave | Split documentado e testado |
| Usar apenas accuracy | Métrica insuficiente em saúde | Priorizar recall maligno |
| Não ter explicabilidade | PDF pede feature importance/SHAP | Implementar ambas se viável |
| Prometer diagnóstico real | Problema ético e acadêmico | Avisos em todo o projeto |
| Repositório bagunçado | Prejudica avaliação | Estrutura profissional e checklist |
| Vídeo superficial | Entregável obrigatório | Roteiro demonstrando app real |
| README fraco | Prejudica reprodutibilidade | README completo |

## 3.8 Pontos de destaque

O projeto pode se destacar por:

- interface Streamlit clara e profissional;
- explicabilidade local por caso;
- documentação forte;
- model card;
- testes;
- discussão honesta sobre falsos negativos;
- clareza ética;
- comparação visual de modelos;
- app demonstrando casos benigno e maligno rapidamente;
- organização de código superior a um notebook solto.

---

# 4. Decisão estratégica consolidada

## 4.1 Decisão central

A V1 seguirá com:

```text
WDBC + Python + Scikit-learn + SHAP + Streamlit multipage + testes + documentação profissional.
```

## 4.2 Por que usar WDBC

O WDBC foi escolhido porque:

- é um dataset público e reconhecido;
- é estável;
- está disponível na UCI;
- está integrado ao Scikit-learn;
- é diretamente relacionado a câncer de mama;
- é citado de forma alinhada ao desafio;
- tem problema de classificação binária claro;
- tem 569 amostras;
- tem 30 features numéricas;
- não possui valores ausentes;
- permite EDA robusta;
- permite análise de correlação;
- permite comparação de modelos;
- permite métricas de classificação;
- permite SHAP;
- reduz risco operacional;
- reduz dependência de Kaggle;
- facilita reprodutibilidade para avaliadores.

## 4.3 Por que não usar PCOS/SOP na V1

PCOS/SOP é tematicamente forte, mas foi deixado fora da V1 por motivos estratégicos:

- depende de Kaggle;
- pode exigir autenticação;
- pode ter variações de versão;
- pode ter schema menos previsível;
- pode ter metadados menos claros;
- pode gerar retrabalho no início;
- aumenta risco operacional;
- não é necessário para cumprir o obrigatório;
- pode ser considerado evolução futura.

A decisão não invalida PCOS. Ele pode ser revisitado após a V1 se tornar sólida.

## 4.4 Por que Maternal Health Risk fica como reserva

O Maternal Health Risk fica como plano B porque:

- é oficial;
- é limpo;
- tem poucas features;
- é ligado à saúde da mulher;
- tem interface mais intuitiva;
- pode manter a arquitetura geral;
- reduz risco caso o WDBC gere algum bloqueio inesperado.

Ele não será usado na V1 principal porque o WDBC tem conexão mais direta com o exemplo de câncer de mama e permite uma entrega mais forte no tema escolhido.

## 4.5 Por que Streamlit foi escolhido

Streamlit foi escolhido porque:

- permite criar app interativo rapidamente;
- mantém o projeto no ecossistema Python;
- reduz necessidade de backend separado;
- integra bem com Pandas, Scikit-learn, Plotly e SHAP;
- é adequado para demonstrações acadêmicas;
- facilita visualização de dados;
- facilita deploy futuro simples;
- permite app multipage;
- reduz risco de integração;
- prioriza o que a fase avalia: ML e explicabilidade.

## 4.6 Por que Lovable fica fora da V1

Lovable fica fora da V1 porque:

- geraria um frontend separado;
- poderia criar estrutura React/Vite;
- exigiria integração com backend Python;
- aumentaria dependências;
- aumentaria tempo;
- poderia criar UI bonita, mas desalinhada ao ML;
- não é exigido pelo desafio.

## 4.7 Por que React/Vite fica fora da V1

React/Vite fica fora da V1 porque:

- o desafio não exige frontend web tradicional;
- exigiria API;
- exigiria integração;
- exigiria tratamento de CORS;
- exigiria build separado;
- aumentaria complexidade de deploy;
- aumentaria pontos de falha;
- poderia consumir tempo que deve ir para ML, SHAP e relatório.

## 4.8 Por que FastAPI fica fora da V1

FastAPI fica fora da V1 porque:

- não há requisito de API;
- Streamlit pode consumir o modelo diretamente;
- API adicionaria camada extra;
- exigiria testes de endpoint;
- exigiria contrato JSON;
- exigiria execução de dois serviços;
- não traz ganho proporcional para a nota da V1.

FastAPI pode ser evolução futura se houver necessidade de desacoplar frontend e backend.

## 4.9 Por que CNN/Computer Vision fica como extra futuro

Computer Vision com CNN é explicitamente mais complexo e, para a V1, arriscado.

Fica fora do núcleo porque:

- exigiria dataset de imagem;
- exigiria pipeline diferente;
- exigiria pré-processamento de imagens;
- exigiria treino mais pesado;
- exigiria métricas e explicabilidade próprias;
- poderia atrasar o obrigatório.

Pode ser diferencial futuro apenas se a V1 estiver totalmente finalizada.

---

# 5. Dataset principal e dataset reserva

## 5.1 Dataset principal

### Nome completo

**Breast Cancer Wisconsin Diagnostic — WDBC**

### Fonte

Fonte preferencial de carregamento na V1:

```python
sklearn.datasets.load_breast_cancer
```

A documentação do README deve citar também a origem UCI.

### Forma de carregamento preferencial

A V1 deve carregar o dataset preferencialmente via Scikit-learn:

```text
sklearn.datasets.load_breast_cancer(as_frame=True)
```

O uso de `as_frame=True` é preferível porque facilita a integração com Pandas.

### Quantidade de amostras

O dataset possui:

```text
569 amostras
```

### Quantidade de features

O dataset possui:

```text
30 features numéricas
```

### Classes

O target representa duas classes:

- benigno;
- maligno.

A implementação deve documentar com clareza o mapeamento usado pelo Scikit-learn, evitando confusão entre rótulo numérico e nome da classe.

### Significado geral das features

As features são medidas numéricas extraídas de núcleos celulares em imagens digitalizadas de punção aspirativa por agulha fina.

Elas são agrupadas em:

- médias;
- erros padrão;
- piores valores observados.

Cada grupo possui medidas relacionadas a:

- radius;
- texture;
- perimeter;
- area;
- smoothness;
- compactness;
- concavity;
- concave points;
- symmetry;
- fractal dimension.

## 5.2 Lista oficial de features

### Grupo 1 — Médias

| Feature | Descrição geral |
|---|---|
| `mean radius` | Média do raio dos núcleos celulares |
| `mean texture` | Média da textura |
| `mean perimeter` | Média do perímetro |
| `mean area` | Média da área |
| `mean smoothness` | Média da suavidade |
| `mean compactness` | Média da compacidade |
| `mean concavity` | Média da concavidade |
| `mean concave points` | Média dos pontos côncavos |
| `mean symmetry` | Média da simetria |
| `mean fractal dimension` | Média da dimensão fractal |

### Grupo 2 — Erros padrão

| Feature | Descrição geral |
|---|---|
| `radius error` | Erro padrão do raio |
| `texture error` | Erro padrão da textura |
| `perimeter error` | Erro padrão do perímetro |
| `area error` | Erro padrão da área |
| `smoothness error` | Erro padrão da suavidade |
| `compactness error` | Erro padrão da compacidade |
| `concavity error` | Erro padrão da concavidade |
| `concave points error` | Erro padrão dos pontos côncavos |
| `symmetry error` | Erro padrão da simetria |
| `fractal dimension error` | Erro padrão da dimensão fractal |

### Grupo 3 — Piores valores observados

| Feature | Descrição geral |
|---|---|
| `worst radius` | Pior/maior valor observado do raio |
| `worst texture` | Pior/maior valor observado da textura |
| `worst perimeter` | Pior/maior valor observado do perímetro |
| `worst area` | Pior/maior valor observado da área |
| `worst smoothness` | Pior/maior valor observado da suavidade |
| `worst compactness` | Pior/maior valor observado da compacidade |
| `worst concavity` | Pior/maior valor observado da concavidade |
| `worst concave points` | Pior/maior valor observado dos pontos côncavos |
| `worst symmetry` | Pior/maior valor observado da simetria |
| `worst fractal dimension` | Pior/maior valor observado da dimensão fractal |

## 5.3 Cuidados de interpretação

O projeto deve explicar que:

- as features não são dados digitados por pacientes;
- as features derivam de análise de características celulares;
- as features podem ser correlacionadas entre si;
- correlação não implica causalidade;
- importância de variável não implica relação clínica causal;
- o dataset é público e acadêmico;
- o modelo treinado nele não é ferramenta clínica validada;
- resultados podem não generalizar para populações reais diversas.

## 5.4 Limitações do dataset

Limitações a documentar:

- dataset pequeno;
- base histórica;
- ausência de validação externa na V1;
- features derivadas de processo específico;
- possível falta de diversidade populacional;
- não contempla histórico clínico completo;
- não contempla exames laboratoriais adicionais;
- não contempla contexto médico;
- não contempla avaliação médica;
- não inclui imagem original na V1;
- não substitui biópsia, laudo ou consulta.

## 5.5 Como documentar o dataset no README

O README deve incluir:

- nome completo do dataset;
- fonte UCI;
- carregamento via Scikit-learn;
- número de amostras;
- número de features;
- classes;
- motivo da escolha;
- limitações;
- aviso de uso acadêmico;
- link para fonte oficial;
- explicação de que a V1 não usa dados privados.

## 5.6 Data examples

A pasta `data/examples/` deve conter:

```text
case_benign.csv
case_malignant.csv
```

Regras:

- usar amostras reais do WDBC;
- preferencialmente amostras do conjunto de teste;
- manter as 30 colunas;
- não incluir target se o objetivo for simular entrada do usuário;
- se incluir target em arquivo separado para teste, documentar claramente;
- garantir que os arquivos sejam pequenos;
- garantir que os arquivos sejam versionáveis;
- usar nos testes e na demonstração.

## 5.7 Dataset reserva

### Nome

**Maternal Health Risk — UCI**

### Quando usar

Apenas se houver bloqueio grave com o WDBC.

### Regra de troca

A troca deve ser registrada em `docs/decisions.md` com:

- motivo;
- impacto no escopo;
- impacto nas páginas;
- impacto nas métricas;
- impacto no relatório;
- data;
- aprovação humana.

---

# 6. Arquitetura oficial da V1

## 6.1 Visão geral

A arquitetura oficial é:

```text
Streamlit multipage
        ↓
Módulos Python em src/
        ↓
Carregamento e validação do WDBC
        ↓
Pipeline Scikit-learn
        ↓
Modelos de classificação
        ↓
Métricas e seleção do modelo final
        ↓
Modelo salvo com Joblib
        ↓
Predição individual
        ↓
Explicabilidade global/local com SHAP
        ↓
Visualização no app
```

## 6.2 Princípios arquiteturais

- Separar app de lógica de ML.
- Separar dados, features, modelos, plots e utilidades.
- Não colocar todo o código dentro do Streamlit.
- Não depender apenas de notebooks.
- Reutilizar funções testáveis.
- Salvar artefatos de modelo de forma previsível.
- Validar entradas antes de prever.
- Documentar decisões.
- Evitar dependências não usadas.
- Manter repositório limpo.

## 6.3 Fluxo de dados

```text
load_breast_cancer()
        ↓
DataFrame com 30 features + target
        ↓
Validação de schema
        ↓
EDA
        ↓
Split treino/teste
        ↓
Pipeline de pré-processamento
        ↓
Treinamento de modelos
        ↓
Métricas
        ↓
Persistência de artefatos
        ↓
App consome artefatos
```

## 6.4 Fluxo de treino

```text
1. Carregar dataset.
2. Validar colunas.
3. Separar X e y.
4. Criar split treino/teste estratificado.
5. Criar pipelines por modelo.
6. Aplicar feature scaling quando necessário.
7. Treinar modelos candidatos.
8. Avaliar no conjunto de teste.
9. Comparar métricas.
10. Escolher modelo final.
11. Salvar pipeline/modelo final.
12. Salvar métricas.
13. Salvar feature names.
14. Gerar model card.
```

## 6.5 Fluxo de predição

```text
1. Usuário escolhe modo de entrada.
2. App recebe os dados.
3. App valida schema.
4. App valida tipos e valores.
5. App carrega pipeline/modelo final.
6. App executa predição.
7. App calcula probabilidade.
8. App converte resultado para rótulo humano.
9. App calcula faixa de risco demonstrativa.
10. App exibe resultado.
11. App exibe aviso ético.
```

## 6.6 Fluxo de explicabilidade

```text
1. Modelo final é carregado.
2. Dados de referência são carregados.
3. Explicabilidade global é calculada ou carregada.
4. Para caso individual, entrada validada é transformada.
5. SHAP local é calculado.
6. Top features são extraídas.
7. App exibe gráfico e texto interpretativo.
8. App reforça que explicabilidade não é causalidade médica.
```

## 6.7 Responsabilidade por camada

| Camada | Responsabilidade | Não deve fazer |
|---|---|---|
| `app.py` e `pages/` | UI, navegação, chamada de funções | Treinar modelo pesado diretamente |
| `src/data/` | Carregar e validar dados | Gerar gráficos complexos |
| `src/features/` | Pré-processamento e pipelines | Exibir Streamlit |
| `src/models/` | Treino, avaliação, predição, explicação | Misturar UI |
| `src/plots/` | Gráficos reutilizáveis | Carregar modelo |
| `tests/` | Garantia de qualidade | Depender de app manual |
| `docs/` | Documentação | Código executável crítico |

## 6.8 Arquivos que o Codex deve criar

O Codex deve criar ou manter:

- `app.py`;
- arquivos em `pages/`;
- módulos em `src/`;
- notebooks em `notebooks/`;
- testes em `tests/`;
- docs em `docs/`;
- `README.md`;
- `requirements.txt`;
- `.gitignore`;
- `models/model_card.md`;
- artefatos leves em `models/`;
- exemplos pequenos em `data/examples/`.

## 6.9 Arquivos que o Codex não deve criar

O Codex não deve criar:

- `package.json`;
- `vite.config.*`;
- `src/App.jsx`;
- `src/main.jsx`;
- frontend React;
- backend FastAPI;
- `api/`;
- `server.py` para API;
- banco SQLite/Postgres;
- autenticação;
- `node_modules/`;
- `.env` com segredos;
- arquivos temporários;
- relatórios locais de debug;
- mocks genéricos sem uso;
- dados inventados;
- notebooks duplicados;
- modelos pesados não justificados.

---

# 7. Estrutura de pastas e arquivos

## 7.1 Estrutura-base recomendada

```text
femhealth-ml-triage/
├── app.py
├── pages/
│   ├── 01_Exploracao.py
│   ├── 02_Predicao.py
│   ├── 03_Modelos.py
│   ├── 04_Explicabilidade.py
│   └── 05_Sobre_Etica.py
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   ├── schema.py
│   │   └── validation.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── preprocess.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   └── explain.py
│   ├── plots/
│   │   ├── __init__.py
│   │   └── charts.py
│   └── utils/
│       ├── __init__.py
│       └── io.py
├── models/
│   ├── final_model.joblib
│   ├── preprocessing_pipeline.joblib
│   ├── feature_names.json
│   ├── metrics.json
│   └── model_card.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── examples/
│       ├── case_benign.csv
│       └── case_malignant.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   └── 03_explainability.ipynb
├── tests/
│   ├── unit/
│   │   ├── test_schema.py
│   │   ├── test_validation.py
│   │   ├── test_preprocess.py
│   │   └── test_predict.py
│   ├── smoke/
│   │   ├── test_dataset_loads.py
│   │   ├── test_model_artifacts.py
│   │   └── test_examples.py
│   └── e2e/
│       └── test_app_flow.py
├── docs/
│   ├── decisions.md
│   ├── wireframes.md
│   └── delivery_checklist.md
├── README.md
├── requirements.txt
├── .gitignore
└── PROJECT_CONSTITUTION.md
```

## 7.2 `app.py`

Página inicial do Streamlit.

Responsabilidades:

- configurar página;
- apresentar identidade do projeto;
- apresentar objetivo;
- apresentar cards;
- mostrar aviso ético;
- orientar navegação;
- não concentrar lógica de ML pesada.

## 7.3 `pages/01_Exploracao.py`

Responsabilidades:

- carregar dataset;
- exibir dimensões;
- exibir distribuição de classes;
- exibir estatísticas;
- exibir gráficos;
- exibir análise de correlação;
- explicar padrões encontrados;
- não treinar modelo.

## 7.4 `pages/02_Predicao.py`

Responsabilidades:

- permitir entrada por exemplo benigno;
- permitir entrada por exemplo maligno;
- permitir upload CSV;
- permitir preenchimento manual;
- validar dados;
- chamar função de predição;
- mostrar resultado;
- mostrar probabilidade;
- mostrar faixa de risco;
- mostrar top fatores explicativos;
- mostrar aviso ético.

## 7.5 `pages/03_Modelos.py`

Responsabilidades:

- exibir comparação de modelos;
- exibir métricas;
- exibir matriz de confusão;
- exibir curva ROC;
- explicar escolha do modelo final;
- destacar recall da classe maligna.

## 7.6 `pages/04_Explicabilidade.py`

Responsabilidades:

- exibir feature importance;
- exibir permutation importance, se disponível;
- exibir SHAP global;
- exibir SHAP local do último caso avaliado, se disponível;
- explicar limites da interpretação.

## 7.7 `pages/05_Sobre_Etica.py`

Responsabilidades:

- explicar escopo;
- listar fontes;
- explicar limitações;
- reforçar aviso médico;
- apresentar relação com Tech Challenge;
- apresentar relação com aulas;
- apresentar próximos passos possíveis.

## 7.8 `src/data/load_data.py`

Responsabilidades esperadas:

- carregar WDBC via Scikit-learn;
- retornar DataFrame de features;
- retornar target;
- retornar nomes das classes;
- retornar metadata;
- não depender de Streamlit.

## 7.9 `src/data/schema.py`

Responsabilidades esperadas:

- definir lista oficial de features;
- definir grupos de features;
- definir nomes esperados;
- definir mapeamento target;
- definir ranges observados, se gerados dinamicamente;
- centralizar schema.

## 7.10 `src/data/validation.py`

Responsabilidades esperadas:

- validar presença de colunas;
- validar tipos numéricos;
- validar valores ausentes;
- validar valores negativos;
- validar CSV de uma linha;
- retornar mensagens de erro claras;
- não corrigir silenciosamente dados inválidos.

## 7.11 `src/features/preprocess.py`

Responsabilidades esperadas:

- criar pipeline de pré-processamento;
- aplicar scaler quando necessário;
- separar X/y;
- preparar dados para treino;
- preparar dados para inferência;
- evitar vazamento de dados.

## 7.12 `src/models/train.py`

Responsabilidades esperadas:

- criar modelos candidatos;
- executar treino;
- executar validação cruzada, se aplicável;
- selecionar modelo final;
- salvar artefatos;
- salvar métricas.

## 7.13 `src/models/evaluate.py`

Responsabilidades esperadas:

- calcular métricas;
- gerar classification report;
- gerar matriz de confusão;
- gerar ROC AUC;
- organizar tabela comparativa;
- salvar resultados em JSON.

## 7.14 `src/models/predict.py`

Responsabilidades esperadas:

- carregar modelo;
- validar entrada;
- executar predição;
- retornar rótulo;
- retornar probabilidade;
- retornar faixa de risco;
- retornar payload adequado para UI.

## 7.15 `src/models/explain.py`

Responsabilidades esperadas:

- calcular feature importance;
- calcular permutation importance, se implementada;
- calcular SHAP global;
- calcular SHAP local;
- extrair top features;
- retornar explicações em formato utilizável pelo app.

## 7.16 `src/plots/charts.py`

Responsabilidades esperadas:

- gerar gráficos reutilizáveis;
- não conter regra de negócio;
- não treinar modelo;
- manter visual consistente.

## 7.17 `src/utils/io.py`

Responsabilidades esperadas:

- salvar JSON;
- carregar JSON;
- salvar Joblib;
- carregar Joblib;
- resolver caminhos;
- evitar caminhos hardcoded frágeis.

## 7.18 `models/`

Conteúdo esperado:

- `final_model.joblib`;
- `preprocessing_pipeline.joblib`, se separado;
- `feature_names.json`;
- `metrics.json`;
- `model_card.md`.

Se o modelo e pré-processamento estiverem unidos em um único pipeline, o nome do artefato pode ser documentado como `final_pipeline.joblib`.

## 7.19 `data/`

Regras:

- `data/raw/`: dados brutos, se houver necessidade de exportar;
- `data/processed/`: dados tratados pequenos, se necessário;
- `data/examples/`: exemplos benigno/maligno para demonstração.

Não versionar arquivos grandes desnecessários.

## 7.20 `notebooks/`

Notebooks esperados:

- `01_eda.ipynb`;
- `02_modeling.ipynb`;
- `03_explainability.ipynb`.

Os notebooks devem ser limpos, objetivos e conectados aos módulos em `src/`.

## 7.21 `tests/`

Organização:

- `tests/unit/`: funções isoladas;
- `tests/smoke/`: saúde geral do projeto;
- `tests/e2e/`: fluxo de app, se viável.

## 7.22 `docs/`

Documentos esperados:

- `decisions.md`;
- `wireframes.md`;
- `delivery_checklist.md`.

---

# 8. Especificação do app Streamlit

## 8.1 Identidade visual

A interface deve ser:

- limpa;
- moderna;
- sóbria;
- clínica;
- acadêmica;
- profissional;
- sem aparência de app genérico;
- sem excesso de cores;
- sem promessas médicas.

## 8.2 Direção visual recomendada

Sugestão de identidade:

| Elemento | Direção |
|---|---|
| Tom | Clínico, acadêmico, confiável |
| Cores | Azul escuro, verde/teal, branco, cinza claro |
| Destaques | Usar cor de atenção apenas para alertas |
| Tipografia | Padrão limpa do Streamlit |
| Cards | Métricas e informações-chave |
| Gráficos | Legíveis, sem poluição |
| Emojis | Evitar excesso; usar poucos ou nenhum |
| Imagens | Não usar imagens médicas reais sem necessidade |

## 8.3 Princípios de UX

- O usuário deve entender o objetivo em menos de 30 segundos.
- O aviso ético deve estar visível.
- O usuário deve conseguir testar um caso sem preencher 30 campos.
- A predição manual deve ser possível, mas não o caminho principal.
- Erros devem ser explicados em linguagem clara.
- Gráficos devem ter título e interpretação.
- O app deve guiar o avaliador pelo fluxo do projeto.
- A navegação deve ser simples.
- O resultado não deve parecer laudo médico.

## 8.4 Navegação

Páginas obrigatórias:

1. Início;
2. Exploração dos Dados;
3. Predição Individual;
4. Comparação de Modelos;
5. Explicabilidade;
6. Sobre e Ética.

## 8.5 Layout da Home

A Home deve conter:

- título;
- subtítulo;
- descrição curta;
- cards:
  - Dataset;
  - Modelos;
  - Métricas;
  - Explicabilidade;
- chamada para acessar Predição Individual;
- aviso ético;
- breve instrução de navegação.

Texto sugerido:

> O FemHealth ML Triage demonstra um pipeline acadêmico de Machine Learning para classificação de amostras de massa mamária usando dados públicos, métricas de classificação e explicabilidade.

Aviso obrigatório:

> Esta aplicação é educacional e não substitui avaliação médica.

## 8.6 Página Exploração dos Dados

Componentes:

- dimensão do dataset;
- número de features;
- distribuição benigno/maligno;
- tabela de estatísticas;
- histogramas;
- boxplots;
- heatmap de correlação;
- interpretação textual;
- link interno/indicação para Comparação de Modelos.

Texto interpretativo deve explicar:

- balanceamento das classes;
- variáveis com maior separação visual;
- correlações fortes;
- motivo para usar feature scaling;
- cuidado com multicolinearidade.

## 8.7 Página Predição Individual

Ver seção 9 para especificação detalhada.

## 8.8 Página Comparação de Modelos

Componentes:

- tabela de modelos;
- accuracy;
- precision;
- recall;
- F1;
- ROC AUC;
- matriz de confusão;
- curva ROC;
- observação sobre falso negativo;
- destaque do modelo final.

Texto obrigatório:

> Em triagem médica, o recall da classe maligna é especialmente importante, pois falsos negativos podem atrasar investigação clínica. A métrica, porém, não deve ser interpretada isoladamente.

## 8.9 Página Explicabilidade

Componentes:

- explicação do que é interpretabilidade;
- feature importance;
- permutation importance, se implementada;
- SHAP global;
- SHAP local;
- top fatores por caso;
- limitações.

Texto obrigatório:

> As explicações apresentadas descrevem o comportamento do modelo, não relações causais médicas.

## 8.10 Página Sobre e Ética

Componentes:

- objetivo acadêmico;
- dataset;
- stack;
- limitações;
- usos pretendidos;
- usos não pretendidos;
- aviso médico;
- relação com Tech Challenge;
- relação com aulas;
- fontes.

Texto obrigatório:

> O médico sempre deve ter a palavra final.

## 8.11 Estados de erro

O app deve tratar:

| Situação | Comportamento esperado |
|---|---|
| Modelo não encontrado | Exibir mensagem orientando treinar/gerar artefatos |
| CSV vazio | Informar que o arquivo não contém dados |
| CSV com mais de uma linha | Informar que a V1 aceita uma linha por vez |
| Colunas faltantes | Listar colunas faltantes |
| Colunas extras | Informar colunas extras ou ignorar somente se documentado |
| Valor não numérico | Informar coluna e valor inválido |
| Campo manual vazio | Solicitar preenchimento de todos os campos |
| Valor negativo | Informar que features devem ser não negativas |
| Erro SHAP | Exibir resultado da predição e avisar que explicação não pôde ser gerada |

## 8.12 Fluxo completo do usuário

```text
1. Usuário abre o app.
2. Usuário lê o objetivo.
3. Usuário vê aviso ético.
4. Usuário acessa Exploração dos Dados.
5. Usuário entende o dataset.
6. Usuário acessa Predição Individual.
7. Usuário escolhe caso exemplo ou envia CSV.
8. App valida dados.
9. App executa modelo.
10. App mostra classe prevista.
11. App mostra probabilidade.
12. App mostra faixa de risco.
13. App mostra top fatores explicativos.
14. Usuário acessa Comparação de Modelos.
15. Usuário entende métricas.
16. Usuário acessa Explicabilidade.
17. Usuário entende fatores globais e locais.
18. Usuário acessa Sobre e Ética.
19. Usuário entende limitações.
```

---

# 9. Predição Individual — especificação detalhada

## 9.1 Objetivo da página

Permitir que o avaliador veja o modelo funcionando em um caso individual, de forma rápida, clara e responsável.

## 9.2 Modos de entrada

A página deve oferecer quatro modos:

1. Carregar caso benigno.
2. Carregar caso maligno.
3. Upload de CSV.
4. Preenchimento manual avançado.

## 9.3 Carregar caso benigno

Comportamento:

- carregar `data/examples/case_benign.csv`;
- validar schema;
- exibir resumo dos dados;
- permitir executar análise;
- exibir resultado esperado do modelo;
- não prometer certeza.

## 9.4 Carregar caso maligno

Comportamento:

- carregar `data/examples/case_malignant.csv`;
- validar schema;
- exibir resumo dos dados;
- permitir executar análise;
- exibir resultado esperado do modelo;
- não prometer certeza.

## 9.5 Upload de CSV

Requisitos:

- aceitar `.csv`;
- exigir uma linha;
- exigir as 30 colunas;
- validar nomes;
- validar tipos;
- validar valores ausentes;
- validar valores numéricos;
- informar erros claramente.

### Mensagem para CSV com colunas faltantes

Texto sugerido:

> O arquivo enviado não possui todas as colunas necessárias para a predição. Colunas faltantes: `...`. Baixe ou consulte o schema esperado no README.

### Mensagem para CSV com colunas extras

Texto sugerido:

> O arquivo enviado possui colunas não esperadas: `...`. A V1 espera exatamente as 30 features do dataset WDBC.

### Mensagem para CSV com mais de uma linha

Texto sugerido:

> A predição individual da V1 aceita apenas uma amostra por vez. Envie um CSV com exatamente uma linha.

### Mensagem para valor inválido

Texto sugerido:

> A coluna `NOME_DA_COLUNA` contém valor inválido. Todas as features devem ser numéricas e não vazias.

## 9.6 Preenchimento manual avançado

O formulário deve ser organizado em três grupos:

- Médias;
- Erros padrão;
- Piores valores observados.

Cada campo deve:

- aceitar número;
- ter rótulo claro;
- mostrar nome técnico original;
- mostrar faixa observada, se disponível;
- impedir ou alertar sobre valores negativos;
- não usar nomes inventados no backend.

## 9.7 Validação de schema

A validação deve conferir:

- todas as 30 features;
- ausência de colunas faltantes;
- ausência de tipos inválidos;
- uma linha por predição;
- ausência de valores nulos;
- valores numéricos;
- valores não negativos.

## 9.8 Resultado esperado

Após a análise, exibir:

- classe prevista;
- probabilidade estimada para classe maligna;
- faixa de risco demonstrativa;
- top variáveis que influenciaram a predição;
- gráfico ou tabela SHAP local, se disponível;
- aviso de não diagnóstico.

## 9.9 Probabilidade

A probabilidade deve ser apresentada como:

```text
Probabilidade estimada pelo modelo
```

Nunca como:

```text
Chance real de câncer
```

## 9.10 Faixa de risco demonstrativa

Sugestão inicial:

| Probabilidade estimada de maligno | Faixa |
|---:|---|
| Menor que 0.35 | Baixa |
| 0.35 a 0.70 | Intermediária |
| Maior que 0.70 | Alta |

Esses limites são demonstrativos e devem ser documentados.

## 9.11 Interpretação

Texto sugerido:

> A classificação apresentada é uma estimativa estatística baseada no padrão aprendido pelo modelo a partir do dataset público. Ela deve ser interpretada apenas como demonstração acadêmica.

## 9.12 Principais fatores explicativos

O app deve listar, por exemplo:

```text
Principais fatores que mais influenciaram a estimativa neste caso:
1. worst concave points
2. worst perimeter
3. mean concavity
```

Esses fatores devem vir do cálculo real de explicabilidade, não de texto fixo inventado.

## 9.13 Aviso de não diagnóstico

Texto obrigatório:

> Resultado demonstrativo. Não utilize esta estimativa como diagnóstico médico. A avaliação clínica deve ser feita por profissional habilitado.

---

# 10. Modelagem

## 10.1 Objetivo da modelagem

Criar e avaliar modelos supervisionados de classificação capazes de distinguir, no contexto do dataset WDBC, amostras benignas e malignas.

## 10.2 Modelos candidatos

Modelos candidatos:

- Regressão Logística;
- KNN;
- Árvore de Decisão;
- Random Forest;
- SVM.

## 10.3 Modelos obrigatórios mínimos

A V1 deve treinar e comparar pelo menos dois modelos.

Recomendação mínima:

- Regressão Logística;
- Random Forest.

Recomendação ideal:

- Regressão Logística;
- KNN;
- Árvore de Decisão;
- Random Forest;
- SVM, se não aumentar risco.

## 10.4 Separação treino/teste

Regras:

- usar `train_test_split`;
- usar `random_state` fixo;
- usar estratificação;
- documentar proporção;
- garantir que scaler é ajustado apenas no treino;
- evitar vazamento de dados.

Sugestão:

```text
test_size = 0.2
random_state = 42
stratify = y
```

## 10.5 Validação cruzada

A validação cruzada deve ser usada se não comprometer prazo.

Objetivo:

- comparar estabilidade dos modelos;
- evitar escolha baseada em um único split;
- registrar média e desvio padrão.

Sugestão:

```text
StratifiedKFold com 5 folds
```

## 10.6 Pipeline Scikit-learn

Usar pipeline para modelos que precisam de scaling.

Exemplo conceitual:

```text
StandardScaler → Modelo
```

Modelos que se beneficiam de scaling:

- Regressão Logística;
- KNN;
- SVM.

Modelos baseados em árvore geralmente não exigem scaling, mas podem ser colocados em pipeline para padronização da interface de treino.

## 10.7 Feature scaling

Feature scaling é necessário porque as features têm escalas diferentes.

Deve ser explicado na documentação:

- algumas features representam área;
- outras representam suavidade;
- KNN e Regressão Logística são sensíveis à escala;
- scaler deve ser ajustado apenas no treino.

## 10.8 Escolha do modelo final

O modelo final deve ser escolhido considerando:

- recall da classe maligna;
- F1-score;
- ROC AUC;
- estabilidade;
- interpretabilidade;
- simplicidade;
- risco de overfitting;
- qualidade para demonstração.

A escolha deve ser documentada em:

- `models/model_card.md`;
- `docs/decisions.md`;
- relatório técnico;
- página Comparação de Modelos.

## 10.9 Critérios de comparação

Tabela comparativa deve conter:

| Modelo | Accuracy | Precision maligno | Recall maligno | F1 maligno | ROC AUC | Observações |
|---|---:|---:|---:|---:|---:|---|

## 10.10 Persistência com Joblib

Artefatos esperados:

- `models/final_model.joblib` ou `models/final_pipeline.joblib`;
- `models/feature_names.json`;
- `models/metrics.json`.

Regras:

- o app deve consumir artefatos salvos;
- o modelo não deve ser retreinado a cada carregamento do app;
- se artefatos não existirem, app deve mostrar mensagem clara.

## 10.11 Salvamento de métricas

Salvar métricas em JSON para consumo pelo app.

Exemplo conceitual de estrutura:

```json
{
  "selected_model": "RandomForestClassifier",
  "priority_metric": "recall_malignant",
  "models": {
    "LogisticRegression": {
      "accuracy": 0.0,
      "precision_malignant": 0.0,
      "recall_malignant": 0.0,
      "f1_malignant": 0.0,
      "roc_auc": 0.0
    }
  }
}
```

## 10.12 Salvamento de nomes de features

Salvar em:

```text
models/feature_names.json
```

Objetivo:

- validar entrada;
- garantir ordem correta;
- evitar divergência entre treino e inferência.

---

# 11. Métricas

## 11.1 Métricas obrigatórias

A V1 deve apresentar:

- accuracy;
- precision;
- recall;
- F1-score;
- ROC AUC;
- matriz de confusão;
- curva ROC.

## 11.2 Accuracy

Accuracy mede proporção geral de acertos.

Limite:

- pode ser enganosa se classes forem desbalanceadas;
- não deve ser métrica principal.

## 11.3 Precision

Precision responde:

> Entre os casos previstos como malignos, quantos eram realmente malignos?

Importante para entender falso positivo.

## 11.4 Recall

Recall responde:

> Entre os casos realmente malignos, quantos o modelo conseguiu identificar?

Será a métrica prioritária.

## 11.5 F1-score

F1-score combina precision e recall.

Deve ser usado como métrica de equilíbrio.

## 11.6 ROC AUC

ROC AUC avalia capacidade de separação do modelo em diferentes limiares.

Deve ser apresentada como métrica complementar.

## 11.7 Matriz de confusão

A matriz de confusão deve ser exibida e explicada.

Ela deve permitir discutir:

- verdadeiro benigno;
- falso benigno;
- verdadeiro maligno;
- falso maligno.

## 11.8 Curva ROC

A curva ROC deve ser exibida para modelo final e, se viável, para comparação entre modelos.

## 11.9 Justificativa do recall da classe maligna

O recall da classe maligna é prioritário porque, em uma ferramenta de triagem, deixar de sinalizar um caso maligno pode atrasar investigação clínica.

Texto recomendado para relatório:

> Em um contexto de apoio à triagem, falsos negativos merecem atenção especial, pois representam casos malignos que o modelo classificou como benignos. Embora o sistema não seja uma ferramenta clínica real, essa discussão ajuda a justificar a escolha do recall da classe maligna como métrica prioritária.

## 11.10 Como explicar falso positivo

Falso positivo no contexto do projeto:

> Uma amostra benigna classificada pelo modelo como maligna.

Discussão:

- pode gerar alerta desnecessário;
- em contexto real, poderia levar a investigação adicional;
- ainda assim, no contexto de triagem, pode ser menos crítico do que falso negativo;
- não deve ser minimizado sem análise.

## 11.11 Como explicar falso negativo

Falso negativo no contexto do projeto:

> Uma amostra maligna classificada pelo modelo como benigna.

Discussão:

- é o erro mais sensível;
- poderia atrasar investigação;
- justifica foco em recall;
- deve ser claramente discutido no relatório.

---

# 12. Explicabilidade

## 12.1 Objetivo

A explicabilidade deve tornar o modelo mais compreensível para avaliadores, sem criar falsa sensação de causalidade médica.

## 12.2 Feature importance

Para modelos baseados em árvores, usar `feature_importances_` quando disponível.

Deve mostrar:

- ranking das features;
- importância relativa;
- interpretação textual.

## 12.3 Permutation importance

Permutation importance pode ser usada se for útil para comparar importância de features em qualquer modelo.

Vantagens:

- mais agnóstica ao modelo;
- útil para comparação;
- pode ser explicada no relatório.

Limite:

- pode ser afetada por correlação entre variáveis;
- pode ser mais lenta;
- deve ser usada com cuidado.

## 12.4 SHAP global

SHAP global deve explicar comportamento geral do modelo.

Possíveis visualizações:

- summary plot;
- bar plot de importância média;
- ranking global.

## 12.5 SHAP local

SHAP local deve explicar caso individual.

Possíveis visualizações:

- waterfall;
- force plot;
- bar plot local;
- tabela de top features.

## 12.6 Limites da explicabilidade

O projeto deve declarar:

- SHAP explica o comportamento do modelo;
- SHAP não prova causalidade médica;
- SHAP depende do modelo treinado;
- SHAP pode ser influenciado por correlação;
- explicabilidade não valida uso clínico;
- explicabilidade não substitui especialista.

## 12.7 Texto obrigatório

> As explicações apresentadas descrevem quais variáveis influenciaram a estimativa do modelo. Elas não devem ser interpretadas como relações causais médicas nem como justificativa clínica definitiva.

---

# 13. Testes

## 13.1 Objetivo dos testes

Garantir que o projeto permaneça saudável, reprodutível e seguro contra regressões.

## 13.2 Ferramentas

Ferramentas oficiais:

- Pytest;
- Pytest-cov.

Opcionais:

- Streamlit testing;
- Playwright;
- pytest-playwright.

## 13.3 Smoke tests

Smoke tests devem validar:

- dataset carrega;
- schema existe;
- features esperadas existem;
- exemplos existem;
- modelo carrega, quando treinado;
- função de predição retorna estrutura esperada;
- app não possui erro básico de import.

## 13.4 Testes unitários

Testes unitários devem validar:

- lista de features;
- grupos de features;
- validação de CSV;
- validação de tipos;
- validação de valores;
- pré-processamento;
- predição;
- conversão de resultado;
- cálculo de faixa de risco.

## 13.5 Testes de validação de dados

Casos obrigatórios:

- CSV com coluna faltante;
- CSV com coluna extra;
- CSV com valor nulo;
- CSV com texto em campo numérico;
- CSV com duas linhas;
- CSV correto.

## 13.6 Testes de predição

Validar:

- entrada correta retorna classe;
- entrada correta retorna probabilidade;
- probabilidade está entre 0 e 1;
- faixa de risco é válida;
- erro é claro quando modelo não existe.

## 13.7 Testes de carregamento do modelo

Validar:

- artefato existe;
- artefato carrega;
- artefato possui método de predição;
- feature names são compatíveis;
- metrics JSON é legível.

## 13.8 Testes leves de app

Se viável, validar:

- Home carrega;
- página Predição carrega;
- caso exemplo carrega;
- resultado aparece após análise;
- aviso ético aparece.

## 13.9 Comandos para rodar testes

```powershell
pytest
pytest tests/smoke
pytest tests/unit
pytest --cov=src
```

Se E2E existir:

```powershell
pytest tests/e2e
```

## 13.10 Critérios mínimos de saúde do projeto

O projeto é considerado saudável quando:

- `pytest` passa;
- app roda localmente;
- modelo carrega;
- predição funciona;
- exemplos funcionam;
- README está atualizado;
- não há arquivos temporários no Git.

---

# 14. Documentação

## 14.1 Documentos obrigatórios

- `README.md`;
- `PROJECT_CONSTITUTION.md`;
- `docs/decisions.md`;
- `docs/wireframes.md`;
- `docs/delivery_checklist.md`;
- `models/model_card.md`;
- relatório técnico final;
- roteiro de vídeo.

## 14.2 README.md

Deve conter:

- nome do projeto;
- descrição;
- contexto acadêmico;
- objetivo;
- dataset;
- stack;
- estrutura de pastas;
- instalação;
- execução do app;
- execução de testes;
- como treinar modelo;
- como gerar artefatos;
- como usar exemplos;
- limitações;
- aviso ético;
- link do repositório;
- link do vídeo, quando pronto;
- link do relatório, quando pronto.

## 14.3 `docs/decisions.md`

Deve registrar decisões no formato ADR.

Modelo:

```markdown
## ADR-001 — Escolha do WDBC como dataset principal

**Data:** YYYY-MM-DD  
**Status:** Aceita  
**Contexto:** O Tech Challenge exige dataset público relacionado à saúde da mulher.  
**Decisão:** Usar Breast Cancer Wisconsin Diagnostic como dataset principal.  
**Justificativa:** Base pública, estável, sem missing values, integrada ao Scikit-learn e alinhada ao tema.  
**Consequências:** App terá formulário técnico com 30 features; UX deve ser organizada.
```

## 14.4 `docs/wireframes.md`

Deve conter:

- fluxograma do usuário;
- wireframes textuais;
- componentes por tela;
- mensagens de erro;
- textos éticos;
- comportamento esperado.

## 14.5 `docs/delivery_checklist.md`

Deve conter checklist final com:

- requisitos obrigatórios;
- código;
- app;
- testes;
- relatório;
- vídeo;
- GitHub;
- limpeza;
- ética.

## 14.6 `models/model_card.md`

Deve conter:

- nome do modelo;
- versão;
- dataset;
- target;
- features;
- modelos comparados;
- métrica prioritária;
- métricas finais;
- limitações;
- uso pretendido;
- usos não pretendidos;
- aviso ético;
- data de treinamento;
- comando de treinamento.

## 14.7 Relatório técnico final

Estrutura recomendada:

1. Capa;
2. Introdução;
3. Contexto do Tech Challenge;
4. Problema escolhido;
5. Dataset;
6. Análise exploratória;
7. Pré-processamento;
8. Modelagem;
9. Métricas;
10. Comparação;
11. Explicabilidade;
12. App;
13. Discussão crítica;
14. Limitações;
15. Ética;
16. Conclusão;
17. Link do GitHub;
18. Link do vídeo;
19. Referências.

## 14.8 Roteiro de vídeo

Roteiro sugerido:

1. Apresentação do projeto;
2. Desafio da fase;
3. Dataset;
4. Pipeline;
5. App Home;
6. EDA;
7. Predição benigno;
8. Predição maligno;
9. Comparação de modelos;
10. Explicabilidade;
11. Limitações;
12. Como rodar;
13. Encerramento.

## 14.9 Como manter documentação atualizada

Sempre que mudar:

- dataset;
- modelo;
- métrica;
- fluxo do app;
- dependências;
- comandos;
- estrutura de pastas;
- mensagens éticas;

Atualizar:

- README;
- decisions;
- model card;
- checklist;
- este documento, se a decisão for estrutural.

---

# 15. Regras para o Codex

## 15.1 Regra principal

O Codex deve ler este documento inteiro antes de alterar arquivos.

## 15.2 O Codex deve fazer

- respeitar escopo V1;
- usar WDBC;
- usar Python;
- usar Scikit-learn;
- usar Streamlit;
- usar SHAP;
- organizar projeto em módulos;
- criar testes junto com features;
- atualizar documentação;
- documentar alterações;
- manter repositório limpo;
- priorizar simplicidade;
- priorizar manutenção;
- priorizar alinhamento acadêmico;
- explicar decisões relevantes.

## 15.3 O Codex não deve fazer

- criar Lovable;
- criar React;
- criar Vite;
- criar FastAPI;
- criar backend separado;
- criar banco de dados;
- criar autenticação;
- trocar dataset;
- inventar features;
- criar mocks genéricos;
- deixar arquivos temporários;
- instalar dependências sem justificativa;
- criar código morto;
- esconder erros;
- apagar testes para passar build;
- prometer diagnóstico médico;
- renomear features no backend sem mapeamento documentado.

## 15.4 Regra sobre dependências

Antes de adicionar dependência, o Codex deve justificar:

- por que ela é necessária;
- onde será usada;
- se já não existe alternativa na stack;
- impacto no `requirements.txt`.

## 15.5 Regra sobre testes

Toda feature nova deve vir com:

- teste unitário, se houver lógica;
- smoke test, se afetar saúde do projeto;
- teste de validação, se afetar entrada;
- atualização de documentação, se afetar uso.

## 15.6 Regra sobre documentação

Toda mudança relevante deve atualizar documentação.

Exemplos:

- novo comando;
- nova página;
- nova métrica;
- novo modelo;
- novo arquivo;
- mudança de fluxo.

## 15.7 Regra sobre alterações em massa

Se o Codex precisar alterar muitos arquivos, deve:

1. explicar plano;
2. executar em etapas;
3. preservar funcionamento;
4. rodar testes;
5. listar arquivos alterados;
6. registrar pendências.

---

# 16. Setup local em Windows/PowerShell

## 16.1 Versão recomendada de Python

Usar:

```text
Python 3.11
```

## 16.2 Verificar Python

```powershell
python --version
py --version
py -0p
```

## 16.3 Criar ambiente virtual

Executar na raiz do repositório:

```powershell
py -3.11 -m venv .venv
```

## 16.4 Ativar ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

Se houver bloqueio de execução no PowerShell, usar com cuidado:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 16.5 Atualizar pip

```powershell
python -m pip install --upgrade pip
```

## 16.6 Instalar dependências

```powershell
pip install pandas numpy scikit-learn matplotlib plotly shap joblib streamlit jupyterlab pytest pytest-cov
```

## 16.7 Gerar requirements

```powershell
pip freeze > requirements.txt
```

## 16.8 Instalar a partir do requirements

```powershell
pip install -r requirements.txt
```

## 16.9 Rodar app

```powershell
streamlit run app.py
```

## 16.10 Rodar testes

```powershell
pytest
```

Com cobertura:

```powershell
pytest --cov=src
```

## 16.11 Rodar notebooks

```powershell
jupyter lab
```

## 16.12 Comandos de verificação

```powershell
git status
python --version
pip list
pytest
streamlit run app.py
```

## 16.13 Comandos Git básicos

```powershell
git init
git status
git add .
git commit -m "docs: adiciona constituição do projeto"
git branch -M main
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

---

# 17. GitHub, branches e commits

## 17.1 Nome do repositório

```text
femhealth-ml-triage
```

## 17.2 Descrição do GitHub

```text
Aplicação acadêmica de Machine Learning para apoio à triagem analítica em saúde da mulher, com classificação tabular, explicabilidade e interface em Streamlit.
```

## 17.3 Visibilidade

Preferencialmente público, se permitido pela pós.

Se privado, garantir que avaliadores tenham acesso.

## 17.4 Estratégia de branches

Para projeto individual ou curto:

- `main`: versão estável;
- `dev`: opcional;
- branches curtas opcionais.

Se usar branches:

```text
feature/eda
feature/modeling
feature/streamlit-app
feature/tests
docs/report
```

## 17.5 Padrão de commits

Formato:

```text
tipo: descrição curta
```

Tipos:

- `docs`;
- `feat`;
- `fix`;
- `test`;
- `refactor`;
- `chore`;
- `model`;
- `app`;
- `data`.

Exemplos:

```text
docs: adiciona constituição oficial do projeto
data: implementa carregamento do dataset WDBC
feat: cria validação de schema
model: adiciona treinamento baseline
app: cria página de predição individual
test: adiciona smoke tests dos exemplos
```

## 17.6 O que não subir

Não subir:

- `.venv/`;
- `__pycache__/`;
- `.pytest_cache/`;
- arquivos `.log`;
- arquivos temporários;
- dados sensíveis;
- segredos;
- `.env`;
- arquivos grandes sem justificativa;
- outputs locais pesados;
- `node_modules/`;
- builds desnecessários.

## 17.7 Checklist antes de commit

- [ ] `git status` conferido.
- [ ] Arquivos alterados fazem sentido.
- [ ] Testes rodam ou pendência foi documentada.
- [ ] README/docs atualizados, se necessário.
- [ ] Nenhum arquivo temporário.
- [ ] Nenhum segredo.
- [ ] Nenhuma dependência inútil.
- [ ] Nenhum código morto óbvio.
- [ ] Mensagem de commit clara.

## 17.8 Checklist antes de push

- [ ] App roda.
- [ ] Testes principais passam.
- [ ] README está coerente.
- [ ] Git remoto está correto.
- [ ] Branch correta.
- [ ] Último commit revisado.
- [ ] Repositório limpo.

---

# 18. Plano de desenvolvimento

## 18.1 Etapa 0 — Constituição e setup

Objetivo:

- congelar decisões;
- criar repositório;
- criar ambiente.

Entregáveis:

- `PROJECT_CONSTITUTION.md`;
- `.gitignore`;
- `README.md` inicial;
- ambiente virtual;
- `requirements.txt`.

## 18.2 Etapa 1 — Estrutura inicial

Objetivo:

- criar estrutura de pastas e arquivos base.

Entregáveis:

- `src/`;
- `pages/`;
- `tests/`;
- `docs/`;
- `models/`;
- `data/examples/`;
- notebooks vazios/planejados.

## 18.3 Etapa 2 — Dataset e EDA

Objetivo:

- carregar WDBC;
- entender dados.

Entregáveis:

- `src/data/load_data.py`;
- `src/data/schema.py`;
- notebook `01_eda.ipynb`;
- gráficos;
- estatísticas;
- distribuição de classes;
- correlação.

## 18.4 Etapa 3 — Modelagem

Objetivo:

- treinar e comparar modelos.

Entregáveis:

- `src/features/preprocess.py`;
- `src/models/train.py`;
- `src/models/evaluate.py`;
- notebook `02_modeling.ipynb`;
- métricas;
- modelo final salvo.

## 18.5 Etapa 4 — Explicabilidade

Objetivo:

- explicar modelo global e localmente.

Entregáveis:

- `src/models/explain.py`;
- notebook `03_explainability.ipynb`;
- feature importance;
- SHAP global;
- SHAP local.

## 18.6 Etapa 5 — Streamlit

Objetivo:

- criar app demonstrável.

Entregáveis:

- `app.py`;
- páginas obrigatórias;
- fluxo de predição;
- visualizações;
- avisos éticos.

## 18.7 Etapa 6 — Testes

Objetivo:

- garantir saúde do projeto.

Entregáveis:

- smoke tests;
- unit tests;
- testes de validação;
- testes de predição;
- testes leves de app, se viável.

## 18.8 Etapa 7 — Documentação

Objetivo:

- tornar projeto reprodutível.

Entregáveis:

- README completo;
- decisions;
- wireframes;
- delivery checklist;
- model card.

## 18.9 Etapa 8 — Relatório

Objetivo:

- preparar PDF final.

Entregáveis:

- relatório técnico;
- prints;
- tabelas;
- gráficos;
- discussão crítica;
- links.

## 18.10 Etapa 9 — Vídeo

Objetivo:

- demonstrar app em funcionamento.

Entregáveis:

- roteiro;
- gravação;
- upload;
- link no README e relatório.

## 18.11 Etapa 10 — Revisão final

Objetivo:

- limpar e validar entrega.

Entregáveis:

- checklist completo;
- repositório limpo;
- testes passando;
- relatório revisado;
- vídeo conferido.

---

# 19. Definition of Ready e Definition of Done

## 19.1 Definition of Ready

Uma tarefa pode começar quando:

- objetivo está claro;
- entrada necessária está disponível;
- impacto no projeto é compreendido;
- arquivos afetados são conhecidos;
- critérios de aceite estão definidos;
- relação com Tech Challenge está clara;
- riscos principais foram considerados.

## 19.2 Definition of Done

Uma tarefa está pronta quando:

- implementação foi concluída;
- testes relacionados passam;
- app não quebrou;
- documentação foi atualizada;
- não há arquivos inúteis;
- não há código morto;
- comportamento foi validado;
- commit está claro;
- solução respeita este documento.

## 19.3 Critérios de aceite por feature

Toda feature deve atender:

- utilidade clara;
- alinhamento com V1;
- teste quando aplicável;
- documentação quando aplicável;
- ausência de gambiarra;
- ausência de dependência desnecessária.

## 19.4 Critérios de aceite do projeto final

O projeto final será aceito internamente quando:

- todos os requisitos do PDF estiverem cobertos;
- app rodar localmente;
- modelo final estiver salvo;
- predição funcionar;
- explicabilidade funcionar;
- testes mínimos passarem;
- README estiver completo;
- relatório estiver completo;
- vídeo estiver gravado;
- repositório estiver limpo;
- ética médica estiver clara.

---

# 20. Checklist final

## 20.1 Requisitos obrigatórios

- [ ] Dataset público relacionado à saúde da mulher.
- [ ] Problema discutido.
- [ ] EDA realizada.
- [ ] Estatísticas descritivas.
- [ ] Visualizações.
- [ ] Padrões identificados.
- [ ] Pré-processamento.
- [ ] Análise de correlação.
- [ ] Pelo menos dois modelos.
- [ ] Separação treino/teste.
- [ ] Treinamento.
- [ ] Avaliação.
- [ ] Accuracy.
- [ ] Precision.
- [ ] Recall.
- [ ] F1-score.
- [ ] ROC AUC.
- [ ] Matriz de confusão.
- [ ] Curva ROC.
- [ ] Feature importance ou SHAP.
- [ ] Discussão crítica.
- [ ] Código Python estruturado.
- [ ] README.
- [ ] Link do dataset.
- [ ] Relatório PDF.
- [ ] Vídeo até 15 minutos.

## 20.2 Qualidade técnica

- [ ] Código modular.
- [ ] Funções reutilizáveis.
- [ ] Baixa duplicação.
- [ ] Pipeline reprodutível.
- [ ] Schema centralizado.
- [ ] Modelo salvo.
- [ ] Métricas salvas.
- [ ] Feature names salvos.
- [ ] App consome artefatos.
- [ ] Erros tratados.
- [ ] Dependências justificadas.

## 20.3 Documentação

- [ ] README completo.
- [ ] Constituição atualizada.
- [ ] Decisions atualizado.
- [ ] Wireframes atualizado.
- [ ] Delivery checklist atualizado.
- [ ] Model card atualizado.
- [ ] Relatório técnico final.
- [ ] Roteiro de vídeo.

## 20.4 Testes

- [ ] Smoke tests.
- [ ] Unit tests.
- [ ] Testes de schema.
- [ ] Testes de validação.
- [ ] Testes de predição.
- [ ] Testes de modelo.
- [ ] Testes de app, se viável.
- [ ] `pytest` passa.

## 20.5 Relatório

- [ ] Contexto.
- [ ] Dataset.
- [ ] EDA.
- [ ] Pré-processamento.
- [ ] Modelos.
- [ ] Métricas.
- [ ] Explicabilidade.
- [ ] Discussão crítica.
- [ ] Limitações.
- [ ] Ética.
- [ ] Link GitHub.
- [ ] Link vídeo.

## 20.6 Vídeo

- [ ] Menos de 15 minutos.
- [ ] Mostra app rodando.
- [ ] Mostra EDA.
- [ ] Mostra predição.
- [ ] Mostra modelos.
- [ ] Mostra explicabilidade.
- [ ] Explica limitações.
- [ ] Link funciona.

## 20.7 Repositório limpo

- [ ] Sem `.venv`.
- [ ] Sem `__pycache__`.
- [ ] Sem `.pytest_cache`.
- [ ] Sem logs.
- [ ] Sem arquivos temporários.
- [ ] Sem dados sensíveis.
- [ ] Sem segredos.
- [ ] Sem node_modules.
- [ ] Sem mocks inúteis.
- [ ] Sem código morto.

## 20.8 Ética médica

- [ ] App tem aviso.
- [ ] README tem aviso.
- [ ] Relatório tem aviso.
- [ ] Model card tem aviso.
- [ ] Não há promessa de diagnóstico.
- [ ] Médico tem palavra final.
- [ ] Limitações são claras.

---

# 21. Apêndices

## 21.1 Glossário técnico

| Termo | Significado |
|---|---|
| Machine Learning | Área da IA em que modelos aprendem padrões a partir de dados |
| Classificação | Tarefa de prever uma classe/categoria |
| Dataset | Conjunto de dados usado no projeto |
| Feature | Variável de entrada do modelo |
| Target | Variável que o modelo tenta prever |
| EDA | Análise exploratória dos dados |
| Pipeline | Sequência organizada de transformações e modelo |
| Feature scaling | Padronização/normalização de variáveis |
| Accuracy | Proporção geral de acertos |
| Precision | Proporção de previsões positivas corretas |
| Recall | Capacidade de encontrar casos positivos reais |
| F1-score | Média harmônica entre precision e recall |
| ROC AUC | Métrica de separação entre classes |
| Matriz de confusão | Tabela de acertos e erros por classe |
| SHAP | Técnica de explicabilidade para modelos |
| Feature importance | Ranking de importância das variáveis |
| Falso positivo | Caso benigno previsto como maligno |
| Falso negativo | Caso maligno previsto como benigno |
| Streamlit | Framework Python para apps de dados |
| Joblib | Biblioteca para salvar/carregar modelos |
| Model card | Documento que descreve modelo, uso e limitações |

## 21.2 Relação com aulas da fase

### Fundamentos de Inteligência Artificial

| Aula | Relação com o projeto |
|---|---|
| Introdução e História | Contextualização de IA em saúde |
| Dados e Machine Learning | Dataset, classificação e pipeline |
| Deep Learning | Extra futuro de visão computacional |
| IA Generative | Apoio documental, não núcleo do modelo |

### Fundamentos de IA e Machine Learning

| Aula | Relação com o projeto |
|---|---|
| Python para ML | Pandas, NumPy, manipulação de dados |
| Fundamentos de Python | Funções, módulos e scripts |
| Criação de Módulos e Bibliotecas | Organização em `src/` |
| Criação de APIs com Python | Fora da V1; possível evolução |
| Frameworks de ML em Python | Scikit-learn, SHAP, Streamlit |
| Publicação de Modelo no Hugging Face | Referência para evolução futura |

### Machine Learning

| Aula | Relação com o projeto |
|---|---|
| Conceitos Básicos e Aplicações | Problema supervisionado |
| Regressão Linear e Métricas | Base conceitual de avaliação |
| Redução de Dimensionalidade | Possível discussão de correlação/PCA |
| Feature Scaling | StandardScaler e pipelines |

### Machine Learning Avançado

| Aula | Relação com o projeto |
|---|---|
| Modelos de Classificação | Núcleo da modelagem |
| KNN, SVM | Modelos candidatos |
| KMeans | Fora do escopo por ser não supervisionado |
| Modelos Baseados em Árvores | Decision Tree e Random Forest |
| Validação Cruzada e Pipeline no Sklearn | Estrutura de treino |
| Classification Report e Métricas | Precision, recall, F1 |
| AUC Score e ROC Curve | Avaliação complementar |

### Computer Vision

| Aula | Relação com o projeto |
|---|---|
| Introdução à Visão Computacional | Contexto das features derivadas de imagem |
| OCR | Fora da V1 |
| Detecção e Rastreamento | Fora da V1 |
| CNN | Extra futuro |
| YOLO | Fora da V1 |
| GAN | Fora da V1 |

## 21.3 Riscos técnicos

| Risco | Impacto | Mitigação |
|---|---:|---|
| SHAP lento | Médio | Cache e simplificação |
| Formulário de 30 features confuso | Médio | Exemplos e agrupamento |
| Dependências quebrando | Médio | Requirements estável |
| Modelo não salvo corretamente | Alto | Smoke test de artefatos |
| Feature order incorreta | Alto | `feature_names.json` e validação |
| App retreinar sempre | Médio | Carregar artefatos salvos |
| Métrica mal calculada | Alto | Testar avaliação |
| Codex criar estrutura errada | Alto | Usar prompt restritivo |

## 21.4 Riscos acadêmicos

| Risco | Impacto | Mitigação |
|---|---:|---|
| Não atender requisito | Alto | Checklist |
| Relatório superficial | Alto | Documentar desde o início |
| Vídeo fraco | Alto | Roteiro objetivo |
| Ética insuficiente | Alto | Avisos em todas as camadas |
| Pouca explicabilidade | Alto | SHAP + feature importance |
| App visual sem técnica | Médio | Priorizar ML |
| Falta de relação com aulas | Médio | Seção específica |

## 21.5 Decisões futuras possíveis

Somente após V1:

- deploy Streamlit Community Cloud;
- Dockerfile;
- Hugging Face Space;
- FastAPI;
- React;
- Lovable;
- visão computacional;
- PCOS;
- Maternal Health Risk como versão alternativa;
- calibração de threshold;
- análise de fairness;
- relatório interativo;
- testes E2E completos.

## 21.6 Itens fora de escopo

Fora de escopo da V1:

- diagnóstico real;
- uso clínico;
- prontuários reais;
- dados privados;
- autenticação;
- banco de dados;
- API externa;
- imagens médicas como input;
- treinamento deep learning;
- LLM;
- chatbot;
- prescrição;
- recomendação terapêutica;
- deploy obrigatório;
- mobile app;
- multiusuário.

## 21.7 Mensagem final de governança

Este documento congela oficialmente a direção do projeto:

```text
Nome: FemHealth ML Triage
Repo: femhealth-ml-triage
Dataset: Breast Cancer Wisconsin Diagnostic
Stack: Python + Scikit-learn + SHAP + Streamlit
Escopo: Machine Learning tabular explicável
Postura: acadêmica, ética e não diagnóstica
```

Qualquer mudança estrutural deve ser registrada, justificada e aprovada antes de implementação.

