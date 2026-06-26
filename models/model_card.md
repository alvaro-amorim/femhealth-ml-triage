# Model Card — FemHealth ML Triage

## Estado

**Status:** modelo ainda não treinado. Nenhum artefato `.joblib` é fornecido nesta etapa de bootstrap.

## Identificação planejada

| Campo | Valor |
|---|---|
| Nome | A definir após comparação de modelos |
| Versão | Não treinada |
| Data de treinamento | Não aplicável |
| Comando de treinamento | A definir em `src/models/train.py` |

## Dataset e tarefa

- **Dataset:** Breast Cancer Wisconsin Diagnostic (WDBC), carregado via Scikit-learn.
- **Tarefa:** classificação tabular binária de amostras do dataset.
- **Target:** o mapeamento numérico e semântico será documentado junto ao treino.
- **Features:** 30 atributos numéricos canônicos, centralizados em `src/data/schema.py`.

## Modelagem planejada

- Modelos candidatos: Regressão Logística, KNN, Árvore de Decisão, Random Forest e SVM.
- Métrica prioritária: recall da classe maligna, analisado juntamente com precision, F1 e ROC AUC.
- Artefatos esperados após treino: pipeline/modelo, `feature_names.json` e `metrics.json`.

## Uso pretendido

Ferramenta acadêmica e demonstrativa para explorar um pipeline de Machine Learning tabular e sua explicabilidade no contexto do Tech Challenge.

## Usos não pretendidos e limitações

- Não é uma ferramenta clínica validada.
- Não usa dados privados nem prontuários reais.
- Não substitui avaliação médica, laudo anatomopatológico, exame clínico ou decisão profissional.
- O dataset é limitado, histórico e não possui validação externa na V1.
- Explicabilidade descreve o comportamento do modelo e não estabelece causalidade médica.

## Aviso ético

> O FemHealth ML Triage é uma ferramenta acadêmica de apoio à triagem analítica e não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.
