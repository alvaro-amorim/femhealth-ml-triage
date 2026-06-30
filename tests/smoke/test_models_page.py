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
        metric=lambda *_args, **_kwargs: None,
        columns=lambda count: [
            SimpleNamespace(
                metric=lambda *_args, **_kwargs: None,
                markdown=lambda *_args, **_kwargs: None,
            )
            for _ in range(count)
        ],
        caption=lambda *_args, **_kwargs: None,
        markdown=lambda *_args, **_kwargs: None,
        dataframe=lambda *_args, **_kwargs: None,
        line_chart=lambda *_args, **_kwargs: None,
        plotly_chart=lambda *_args, **_kwargs: None,
        info=lambda *_args, **_kwargs: None,
        success=lambda *_args, **_kwargs: None,
        expander=lambda *_args, **_kwargs: nullcontext(),
        session_state={},
    )
    sys.modules["streamlit"] = fake_streamlit
    for module_name in list(sys.modules):
        if module_name == "src.ui" or module_name.startswith("src.ui."):
            sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location("models_page", MODELS_PAGE)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "render_page")


def test_models_page_contains_academic_and_ethical_text() -> None:
    page_source = MODELS_PAGE.read_text(encoding="utf-8")

    assert "Central de decisão do modelo acadêmico" in page_source
    assert "render_ethics_notice" in page_source
    assert "médico" in page_source
    assert "Modelo final acadêmico da V1" in page_source
    assert "modelo final acadêmico da V1" in page_source
    assert "não é diagnóstico" in page_source
    assert "Curva ROC" in page_source
    assert "_build_roc_figure" in page_source
    assert "plotly_layout[\"xaxis\"].update({\"range\": [0, 1]" in page_source
    assert "get_plotly_layout" in page_source
    assert "\"displayModeBar\": False" in page_source
    assert "linha diagonal de referência" in page_source
    assert "Artefatos persistidos" in page_source
    assert "persistência controlada" in page_source
    assert "Como interpretar as métricas" in page_source
    assert "Verdadeiros malignos" in page_source
