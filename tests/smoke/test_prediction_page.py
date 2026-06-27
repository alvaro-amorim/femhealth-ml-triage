"""Smoke checks for the Streamlit individual-prediction page."""

import importlib.util
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PREDICTION_PAGE = PROJECT_ROOT / "pages" / "02_Predicao.py"


def test_prediction_page_imports_without_error() -> None:
    def _fake_columns(count: int):
        return [
            SimpleNamespace(
                metric=lambda *_args, **_kwargs: None,
                number_input=lambda *_args, **kwargs: kwargs.get("value", 0.0),
            )
            for _ in range(count)
        ]

    fake_streamlit = SimpleNamespace(
        title=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        write=lambda *_args, **_kwargs: None,
        subheader=lambda *_args, **_kwargs: None,
        columns=_fake_columns,
        metric=lambda *_args, **_kwargs: None,
        caption=lambda *_args, **_kwargs: None,
        dataframe=lambda *_args, **_kwargs: None,
        markdown=lambda *_args, **_kwargs: None,
        selectbox=lambda _label, options, **_kwargs: options[0],
        button=lambda *_args, **_kwargs: False,
        info=lambda *_args, **_kwargs: None,
        error=lambda *_args, **_kwargs: None,
        success=lambda *_args, **_kwargs: None,
        expander=lambda *_args, **_kwargs: nullcontext(),
        session_state={},
    )
    sys.modules["streamlit"] = fake_streamlit
    spec = importlib.util.spec_from_file_location("prediction_page", PREDICTION_PAGE)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "render_page")


def test_prediction_page_contains_academic_and_non_diagnostic_text() -> None:
    page_source = PREDICTION_PAGE.read_text(encoding="utf-8")

    assert "Predição Individual" in page_source
    assert "estimativa acadêmica" in page_source
    assert "Não é diagnóstico médico" in page_source
    assert "laudo anatomopatológico" in page_source
    assert "médico sempre deve ter a palavra final" in page_source
    assert "Executar estimativa acadêmica" in page_source
    assert "Exemplo real WDBC" in page_source
    assert "Resultado da estimativa acadêmica" in page_source
    assert "Classe estimada pelo modelo" in page_source
    assert "Classe estimada" in page_source
    assert "Ver valores usados na estimativa" in page_source
    assert "Features do grupo" in page_source
    assert "Probabilidade estimada de malignant" in page_source
    assert "Probabilidade estimada de benign" in page_source
