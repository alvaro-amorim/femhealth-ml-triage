"""Smoke checks for the Streamlit model-comparison page."""

import importlib.util
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_PAGE = PROJECT_ROOT / "pages" / "03_Modelos.py"


def test_models_page_imports_without_error() -> None:
    fake_streamlit = SimpleNamespace(
        cache_data=lambda **_: lambda function: function,
        title=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        spinner=lambda *_args, **_kwargs: nullcontext(),
        subheader=lambda *_args, **_kwargs: None,
        write=lambda *_args, **_kwargs: None,
        columns=lambda count: [SimpleNamespace(metric=lambda *_args, **_kwargs: None) for _ in range(count)],
        caption=lambda *_args, **_kwargs: None,
        markdown=lambda *_args, **_kwargs: None,
        dataframe=lambda *_args, **_kwargs: None,
        line_chart=lambda *_args, **_kwargs: None,
        info=lambda *_args, **_kwargs: None,
    )
    sys.modules["streamlit"] = fake_streamlit
    spec = importlib.util.spec_from_file_location("models_page", MODELS_PAGE)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "render_page")


def test_models_page_contains_academic_and_ethical_text() -> None:
    page_source = MODELS_PAGE.read_text(encoding="utf-8")

    assert "Comparação acadêmica inicial" in page_source
    assert "não realiza diagnóstico" in page_source
    assert "médico" in page_source
    assert "Curva ROC" in page_source
    assert "probabilidade da classe maligna" in page_source
    assert "modelo final" in page_source
