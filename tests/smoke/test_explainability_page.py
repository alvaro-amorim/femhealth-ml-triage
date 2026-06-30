"""Smoke checks for the Streamlit explainability page."""

import importlib.util
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPLAINABILITY_PAGE = PROJECT_ROOT / "pages" / "04_Explicabilidade.py"


def test_explainability_page_imports_without_error() -> None:
    def _fake_columns(count: int):
        return [
            SimpleNamespace(
                metric=lambda *_args, **_kwargs: None,
                markdown=lambda *_args, **_kwargs: None,
            )
            for _ in range(count)
        ]

    fake_streamlit = SimpleNamespace(
        markdown=lambda *_args, **_kwargs: None,
        title=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        info=lambda *_args, **_kwargs: None,
        error=lambda *_args, **_kwargs: None,
        success=lambda *_args, **_kwargs: None,
        subheader=lambda *_args, **_kwargs: None,
        write=lambda *_args, **_kwargs: None,
        caption=lambda *_args, **_kwargs: None,
        columns=_fake_columns,
        metric=lambda *_args, **_kwargs: None,
        dataframe=lambda *_args, **_kwargs: None,
        bar_chart=lambda *_args, **_kwargs: None,
        plotly_chart=lambda *_args, **_kwargs: None,
        selectbox=lambda _label, options, **_kwargs: options[0],
        expander=lambda *_args, **_kwargs: nullcontext(),
        session_state={},
    )
    sys.modules["streamlit"] = fake_streamlit
    for module_name in list(sys.modules):
        if module_name == "src.ui" or module_name.startswith("src.ui."):
            sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(
        "explainability_page", EXPLAINABILITY_PAGE
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "render_page")


def test_explainability_page_contains_required_texts() -> None:
    page_source = EXPLAINABILITY_PAGE.read_text(encoding="utf-8")

    assert "Explicabilidade" in page_source
    assert "Quais atributos mais influenciaram o modelo?" in page_source
    assert "Como os atributos influenciaram este exemplo?" in page_source
    assert "translate_feature_name" in page_source
    assert "render_ethics_notice" in page_source
    assert "não implica causalidade médica" in page_source
