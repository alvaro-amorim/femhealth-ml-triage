# Architecture Decision Records

## ADR-001 — Escolha do WDBC como dataset principal

**Data:** 2026-06-26  
**Status:** Aceita

**Contexto:** O Tech Challenge exige um dataset público ligado à saúde e segurança da mulher, com uma solução de Machine Learning reproduzível.

**Decisão:** Usar o Breast Cancer Wisconsin Diagnostic (WDBC) como dataset principal, carregado preferencialmente por `sklearn.datasets.load_breast_cancer(as_frame=True)`.

**Justificativa:** A base é pública, estável, integrada ao Scikit-learn, possui 569 amostras, 30 features numéricas e não requer download externo. Ela reduz risco operacional e permite EDA, classificação, métricas e explicabilidade dentro do escopo V1.

**Consequências:** A interface de entrada futura terá um schema técnico de 30 features; a documentação deve explicar suas limitações e o mapeamento dos rótulos.

## ADR-002 — Uso de Streamlit multipage na V1

**Data:** 2026-06-26  
**Status:** Aceita

**Contexto:** A V1 precisa demonstrar EDA, predição, comparação de modelos, explicabilidade e ética sem criar camadas desnecessárias.

**Decisão:** Usar Streamlit multipage, com `app.py` como início e páginas separadas em `pages/`.

**Justificativa:** Streamlit mantém a solução no ecossistema Python, integra-se à stack oficial e permite uma demonstração clara sem backend separado.

**Consequências:** A UI deve apenas orquestrar módulos testáveis em `src/`; treinamento e regras de negócio não ficarão concentrados nas páginas.

## ADR-003 — Lovable, React e FastAPI fora da V1

**Data:** 2026-06-26  
**Status:** Aceita

**Contexto:** O objetivo da fase é demonstrar Machine Learning tabular, avaliação e explicabilidade de forma segura e reproduzível.

**Decisão:** Manter Lovable, React, Vite, FastAPI, APIs, banco de dados e autenticação fora da V1.

**Justificativa:** Essas tecnologias adicionariam integração, superfície de falha e tempo de implementação sem ganho proporcional para os critérios acadêmicos da fase.

**Consequências:** A V1 é uma aplicação Python/Streamlit autocontida. Qualquer evolução arquitetural futura requer nova decisão documentada e validação humana.
