# Registro de Uso de IA — FemHealth ML Triage

Este arquivo registra como ferramentas de IA foram usadas no projeto, com foco em transparência metodológica, revisão humana e rastreabilidade acadêmica.

---

## Princípios de uso

- IA é usada como apoio técnico, não como substituta da responsabilidade do estudante/desenvolvedor.
- Decisões finais são revisadas e aceitas pelo usuário antes de implementação ou commit.
- Alterações de código feitas pelo Codex são validadas com testes locais antes de commit.
- O ChatGPT pode apoiar planejamento, revisão, documentação, prompts e análise do repositório remoto.
- O uso de IA deve ser registrado quando influenciar decisões, arquitetura, implementação, testes ou documentação.

---

## Papéis assumidos pelo ChatGPT

| Papel | Como foi usado | Limite aplicado |
|---|---|---|
| Tutor técnico | Explicação do desafio, orientação de etapas e comandos | Usuário valida decisões e executa comandos locais |
| Arquiteto de software | Definição de stack, arquitetura, pastas, qualidade e testes | Escopo precisa respeitar o PDF oficial e a constituição |
| Revisor de projeto | Revisão de logs, testes, Git status, arquivos e GitHub remoto | Não substitui validação local do usuário |
| Planejador do Codex | Criação de prompts restritos por rodada | Codex não deve modificar fora do escopo definido |
| Revisor conectado ao GitHub | Consulta de commits e arquivos remotos após push | Alterações remotas devem ser sincronizadas localmente com cuidado |
| Apoio à documentação | Criação de constituição, metodologia, checklists e notas para relatório | Documentação deve permanecer factual e atualizada |

---

## Usos já registrados

| Data | Ferramenta | Uso | Resultado | Revisão humana |
|---|---|---|---|---|
| 2026-06-26 | ChatGPT | Análise do PDF e lista de aulas | Escopo inicial do Tech Challenge compreendido | Sim |
| 2026-06-26 | ChatGPT | Pesquisa e decisão estratégica | WDBC definido como dataset principal; Maternal Health Risk como reserva | Sim |
| 2026-06-26 | ChatGPT | Constituição do projeto | `PROJECT_CONSTITUTION.md` criado e enviado ao repositório | Sim |
| 2026-06-26 | ChatGPT | Prompt da Rodada 1 do Codex | Bootstrap estrutural orientado | Sim |
| 2026-06-26 | Codex | Criação da estrutura inicial | Estrutura Python/Streamlit criada | Sim |
| 2026-06-26 | ChatGPT | Revisão de erro do Pytest | Identificado problema de import e depois BOM no `pytest.ini` | Sim |
| 2026-06-26 | ChatGPT conectado ao GitHub | Revisão do remoto | Confirmação dos commits de bootstrap e dados | Sim |
| 2026-06-26 | Codex | Rodada 2 — WDBC e validação | 14 testes passaram; commit publicado | Sim |
| 2026-06-26 | Codex | Rodada 3 — pré-processamento e split | 25 testes passaram localmente; ainda sem commit remoto no momento deste registro | Pendente de revisão final |

---

## Pesquisas aprofundadas com apoio de IA

As pesquisas apoiaram as seguintes decisões:

- escolha do dataset principal;
- comparação entre WDBC, PCOS/SOP, Maternal Health Risk, Cervical Cancer, Contraceptive Method Choice, datasets textuais e datasets de imagem;
- decisão de manter CNN/Computer Vision como extra futuro;
- decisão de usar Streamlit em vez de Lovable/React/FastAPI na V1;
- definição de documentação profissional e testes desde o início.

---

## Limites e responsabilidade humana

- O usuário executa comandos localmente.
- O usuário revisa saídas do Codex antes de commit.
- O usuário decide aceitar ou rejeitar recomendações.
- O GitHub registra commits, mas o commit só deve ser feito após testes e revisão.
- Nenhuma decisão médica real é delegada ao sistema ou à IA.
