# Model Card — FemHealth ML Triage

## Status

**Status:** modelo candidato persistido para fins acadêmicos na Rodada 8, consumido pela predição individual acadêmica na Rodada 9 e pela explicabilidade inicial na Rodada 10.

Este modelo é um artefato acadêmico para demonstração de Machine Learning e não deve ser usado para diagnóstico médico.

## Identificação

| Campo | Valor |
|---|---|
| Nome | Modelo candidato recomendado — Regressão Logística |
| Versão | Rodada 8 |
| Data de geração | 2026-06-27 |
| Comando de geração | `python -m src.models.persist` |
| Caminho do modelo | `models/artifacts/recommended_model.joblib` |
| Caminho das métricas | `models/artifacts/recommended_model_metrics.json` |
| Caminho das features | `models/artifacts/recommended_model_feature_names.json` |

## Objetivo acadêmico

Persistir o modelo candidato recomendado nesta comparação controlada para permitir que etapas futuras, como predição individual e explicabilidade, usem um artefato técnico reproduzível.

O artefato não representa ferramenta validada para uso real em saúde, laudo ou recomendação profissional.

## Dataset e tarefa

- **Dataset:** Breast Cancer Wisconsin Diagnostic (WDBC).
- **Carregamento:** `sklearn.datasets.load_breast_cancer(as_frame=True)`.
- **Amostras:** 569.
- **Features:** 30 atributos numéricos canônicos.
- **Tarefa:** classificação tabular binária.
- **Target Scikit-learn:** `0 = malignant`, `1 = benign`.
- **Classe prioritária para análise:** `malignant (0)`.

## Features

As 30 features são mantidas na ordem canônica de `src.data.schema.FEATURE_NAMES` e persistidas em:

```text
models/artifacts/recommended_model_feature_names.json
```

As features são agrupadas em `mean`, `error` e `worst`, cada grupo com 10 variáveis.

## Pré-processamento e algoritmo

- **Algoritmo:** Regressão Logística.
- **Pipeline persistido:** `StandardScaler` + `LogisticRegression`.
- **Motivo do scaling:** Regressão Logística é sensível à escala das variáveis.
- **Controle de vazamento:** o scaler é ajustado apenas no conjunto de treino dentro do pipeline Scikit-learn.

## Split e seleção

- **Split:** treino/teste estratificado.
- **test_size:** 0.2.
- **random_state:** 42.
- **Critérios de seleção:**
  1. maior `recall_malignant`;
  2. empate: maior `roc_auc_malignant`;
  3. empate: maior `f1_malignant`.

## Métricas no conjunto de teste

| Métrica | Valor |
|---|---:|
| accuracy | 0.9824561403508771 |
| precision_malignant | 0.9761904761904762 |
| recall_malignant | 0.9761904761904762 |
| f1_malignant | 0.9761904761904762 |
| roc_auc_malignant | 0.9953703703703705 |

Matriz de confusão, na ordem `0 = malignant`, `1 = benign`:

```text
[[41, 1],
 [1, 71]]
```

## Uso pretendido

- Demonstração acadêmica de pipeline de Machine Learning tabular.
- Base técnica para próximas etapas do projeto.
- Apoio à apresentação de comparação de modelos, predição individual acadêmica demonstrativa e explicabilidade inicial.

## Uso na predição individual acadêmica

Na Rodada 9, este artefato passou a ser consumido pela página `pages/02_Predicao.py` para executar estimativas acadêmicas de uma única amostra no formato WDBC.

A entrada é validada contra as 30 features canônicas, na ordem esperada, sem colunas extras, sem colunas ausentes e sem valores nulos. A página usa exemplos reais do WDBC apenas como demonstração educacional.

## Uso na explicabilidade inicial

Na Rodada 10, este artefato passou a ser consumido pela página `pages/04_Explicabilidade.py` para explicar o comportamento do pipeline persistido.

A importância global usa coeficientes da Regressão Logística e SHAP é calculado em memória quando disponível no ambiente. Quando SHAP falha por incompatibilidade local, a aplicação mantém fallback por coeficientes. As explicações locais usam exemplos reais do WDBC e não devem ser interpretadas como causalidade médica.

## Usos não pretendidos

- Diagnóstico médico.
- Laudo anatomopatológico.
- Avaliação clínica.
- Decisão profissional em saúde.
- Uso por pacientes finais.
- Uso hospitalar ou operacional real.

## Limitações e riscos

- Dataset pequeno, histórico e sem validação externa nesta V1.
- Features derivadas de um processo específico de análise celular.
- Possível limitação de diversidade populacional.
- Métricas são calculadas em um único split estratificado.
- Correlações e coeficientes não devem ser interpretados como causalidade médica.
- Explicabilidade descreve comportamento do modelo, não prova causalidade nem decisão clínica.
- Alto desempenho em WDBC não implica validade clínica real.

## Aviso ético

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.
