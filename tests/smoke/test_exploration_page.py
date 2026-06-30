"""Smoke checks for the Streamlit exploration page."""

import importlib.util
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPLORATION_PAGE = PROJECT_ROOT / "pages" / "01_Exploracao.py"


def test_exploration_page_imports_without_error() -> None:
    fake_streamlit = SimpleNamespace(
        cache_data=lambda **_: lambda function: function,
        markdown=lambda *_args, **_kwargs: None,
        title=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        write=lambda *_args, **_kwargs: None,
        subheader=lambda *_args, **_kwargs: None,
        columns=lambda count: [
            SimpleNamespace(
                metric=lambda *_args, **_kwargs: None,
                markdown=lambda *_args, **_kwargs: None,
            )
            for _ in range(count)
        ],
        caption=lambda *_args, **_kwargs: None,
        dataframe=lambda *_args, **_kwargs: None,
        bar_chart=lambda *_args, **_kwargs: None,
        info=lambda *_args, **_kwargs: None,
        expander=lambda *_args, **_kwargs: nullcontext(),
        session_state={},
    )
    sys.modules["streamlit"] = fake_streamlit
    for module_name in list(sys.modules):
        if module_name == "src.ui" or module_name.startswith("src.ui."):
            sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location("exploration_page", EXPLORATION_PAGE)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "render_page")


def test_exploration_page_contains_academic_and_ethical_text() -> None:
    page_source = EXPLORATION_PAGE.read_text(encoding="utf-8")

    assert "Conheça os dados" in page_source
    assert "Dados do WDBC" in page_source
    assert "render_ethics_notice" in page_source
    assert "0 = Maligno" in page_source
    assert "translate_feature_name" in page_source
    assert "Relações exploratórias com a classe do registro" in page_source
    assert "Correlação não implica causalidade médica" in page_source
