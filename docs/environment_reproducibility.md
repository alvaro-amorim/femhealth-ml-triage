# Reprodutibilidade do ambiente

Este documento consolida o ambiente recomendado para executar o FemHealth ML Triage de forma reprodutível.

O projeto é acadêmico e demonstrativo. Ele não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional.

## Versão recomendada do Python

Use Python 3.11.

```powershell
py -3.11 --version
```

## Criar ambiente virtual no Windows PowerShell

Na raiz do repositório:

```powershell
py -3.11 -m venv .venv
```

## Ativar ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, use apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Rodar o app

```powershell
streamlit run app.py
```

## Rodar testes

```powershell
python -m pytest -q
pytest -q
```

## Rodar cobertura

```powershell
pytest --cov=src
```

## Rodar o quality gate

Antes de commit ou push, execute:

```powershell
python scripts/quality_gate.py
```

O quality gate verifica mojibake comum, uso depreciado de Streamlit, artefatos indevidos, presença dos artefatos oficiais, consistência dos JSONs, schema das 30 features e carregamento do modelo persistido.

## Artefato `.joblib`

O modelo persistido fica em:

```text
models/artifacts/recommended_model.joblib
```

Esse arquivo é um artefato técnico pequeno, versionado para fins acadêmicos e usado pelas páginas de predição individual e explicabilidade. Ele não transforma o projeto em ferramenta clínica ou diagnóstica.

## Versões fixadas para reprodutibilidade

O artefato persistido foi criado com:

- `scikit-learn==1.9.0`
- `joblib==1.5.3`

Essas versões estão fixadas em `requirements.txt` para reduzir warnings de compatibilidade ao carregar o `.joblib` e tornar a execução local mais previsível.

