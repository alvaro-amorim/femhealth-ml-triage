# Controle de Custos e Tokens — FemHealth ML Triage

Este arquivo registra custos, tokens e ferramentas utilizadas no desenvolvimento, quando essa informação estiver disponível.

---

## Regra principal

Não inventar custos ou tokens.

Quando a ferramenta não informar o valor exato, registrar:

```text
não disponível
```

Os valores devem ser preenchidos manualmente pelo usuário quando a ferramenta exibir consumo, custo ou créditos utilizados.

---

## Tabela de custos e tokens

| Data | Ferramenta | Modelo/plano | Rodada | Objetivo | Tokens de entrada | Tokens de saída | Custo informado | Custo estimado | Fonte da informação | Observações |
|---|---|---|---|---|---:|---:|---:|---:|---|---|
| 2026-06-26 | ChatGPT | não disponível | Planejamento inicial | Análise do desafio, dataset, stack e constituição | não disponível | não disponível | não disponível | não disponível | Interface ChatGPT | Uso como tutor, arquiteto e revisor |
| 2026-06-26 | Codex | não disponível | Rodada 1 | Bootstrap estrutural | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 3 testes passaram; commit `556ce05` |
| 2026-06-26 | Codex | não disponível | Rodada 2 | Carregamento e validação do WDBC | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 14 testes passaram; commit `ba2aa27` |
| 2026-06-26 | Codex | não disponível | Rodada 3 | Pré-processamento e split treino/teste | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 25 testes passaram; commit `a6b8f9f` |
| 2026-06-26 | Codex | não disponível | Rodada 3 — validação pós-pull | Sincronização metodológica, revisão local e validação da Rodada 3 | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 25 testes passaram; alterações publicadas no commit `a6b8f9f` |
| 2026-06-26 | Codex | não disponível | Rodada 4 | Modelagem inicial e avaliação controlada | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 37 testes passaram; commit `7180bda` |
| 2026-06-26 | Codex | não disponível | Rodada 5 | Integração da comparação inicial na página de modelos | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 43 testes passaram; commit `7b142dd` |
| 2026-06-26 | Codex | não disponível | Rodada 6A | Curva ROC na comparação inicial de modelos | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 45 testes passaram; commit `d7e3a48` |
| 2026-06-26 | Codex | não disponível | Rodada 6B | EDA real do WDBC na página de exploração | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 54 testes passaram; commit `4e8b9bc` |
| 2026-06-26 | Codex | não disponível | Rodada 7 | Seleção controlada do modelo candidato recomendado | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 60 testes passaram; commit `a483031` |
| 2026-06-27 | Codex | não disponível | Rodada 8 | Persistência controlada do modelo candidato recomendado | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 65 testes passaram; commit `6769ead` |
| 2026-06-27 | Codex | não disponível | Rodada 9 | Predição individual acadêmica com artefato persistido | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 78 testes passaram; commit `3efa07f` |
| 2026-06-27 | Codex | não disponível | Rodada 10 | Explicabilidade inicial do modelo persistido | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | 86 testes passaram; commit `af1bfc1` |
| 2026-06-26 | GitHub conectado ao ChatGPT | não disponível | Revisões remotas | Conferência de commits e arquivos no GitHub | não disponível | não disponível | não disponível | não disponível | Não informado pela ferramenta | Usado para revisar estado remoto |

---

## Ferramentas utilizadas

| Ferramenta | Uso no projeto | Custo/tokens disponíveis? | Observações |
|---|---|---|---|
| ChatGPT | Tutor técnico, arquitetura, planejamento, revisão, documentação e GitHub conectado | não disponível | Registrar manualmente se a interface informar |
| Codex no VS Code | Implementação por rodadas controladas | não disponível | Registrar tokens/custo se aparecerem no VS Code |
| GitHub | Versionamento, commits e revisão remota | não disponível | Repositório público |
| PowerShell | Execução de comandos locais | não aplicável | Sem custo direto |
| Streamlit | Interface local | não aplicável | Sem deploy pago na V1 atual |
| Pytest | Testes automatizados | não aplicável | Sem custo direto |

---

## Como preencher em próximas rodadas

1. Registrar a data.
2. Registrar ferramenta e modelo/plano, se aparecer.
3. Registrar a rodada ou etapa.
4. Registrar objetivo.
5. Copiar tokens/custos exatamente como exibidos.
6. Quando não houver número, preencher `não disponível`.
7. Não estimar custo sem base.
8. Manter observações curtas e factuais.

---

## Observação para relatório final

No relatório técnico, esta seção pode ser resumida como:

> O projeto foi desenvolvido com apoio de ferramentas de IA e Codex em rodadas controladas. Quando informações exatas de custo ou tokens não estavam disponíveis na interface, elas foram registradas como não disponíveis, sem estimativas inventadas.
