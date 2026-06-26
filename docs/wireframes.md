# Wireframes textuais

## Fluxo do avaliador

```text
Início → Exploração dos Dados → Predição Individual
      → Comparação de Modelos → Explicabilidade → Sobre e Ética
```

## Início (`app.py`)

- Título e descrição acadêmica do projeto.
- Resumo do WDBC, pipeline e escopo da V1.
- Aviso ético visível.
- Orientação para navegar pelas páginas.

## Exploração dos Dados

- Dimensões, classes e estatísticas descritivas do WDBC.
- Distribuições, boxplots e heatmap de correlação.
- Interpretação acadêmica e limites de correlação.

## Predição Individual

- Modos: exemplo benigno, exemplo maligno, upload de CSV e preenchimento manual avançado.
- Validação explícita de 30 colunas, tipos numéricos, valores ausentes, valores negativos e uma linha por arquivo.
- Resultado como estimativa do modelo, probabilidade estimada, faixa demonstrativa e fatores explicativos reais quando disponíveis.
- Mensagens planejadas: modelo não encontrado; CSV vazio; número incorreto de linhas; colunas faltantes ou extras; valores inválidos.
- Aviso de que o resultado é demonstrativo e não é diagnóstico médico.

## Comparação de Modelos

- Tabela de métricas: accuracy, precision, recall, F1 e ROC AUC.
- Matriz de confusão e curva ROC.
- Justificativa da priorização do recall da classe maligna, sem interpretar a métrica isoladamente.

## Explicabilidade

- Feature importance e SHAP global/local, quando o modelo estiver treinado.
- Explicação de que os fatores descrevem o comportamento do modelo e não causalidade médica.

## Sobre e Ética

- Objetivo acadêmico, dataset, stack, limitações e fontes.
- Usos pretendidos e não pretendidos.
- Relação com o Tech Challenge e reforço de que o médico tem a palavra final.
