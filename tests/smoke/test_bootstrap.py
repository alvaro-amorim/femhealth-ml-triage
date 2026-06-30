"""Smoke tests do contrato estrutural inicial do projeto."""

import ast
import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

from src.data.schema import FEATURE_GROUPS, FEATURE_NAMES, TARGET_LABELS


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_wdbc_schema_has_the_canonical_feature_contract() -> None:
    """Impede alterações acidentais no schema de entrada antes da modelagem."""
    assert len(FEATURE_NAMES) == 30
    assert len(set(FEATURE_NAMES)) == 30
    assert tuple(FEATURE_GROUPS) == ("mean", "error", "worst")
    assert all(len(group) == 10 for group in FEATURE_GROUPS.values())
    assert set(TARGET_LABELS) == {0, 1}


def test_bootstrap_essential_files_exist() -> None:
    """Garante que a base navegável e documentada não seja removida por engano."""
    expected_files = (
        "app.py",
        "requirements.txt",
        "pages/01_Exploracao.py",
        "pages/02_Predicao.py",
        "pages/03_Modelos.py",
        "pages/04_Explicabilidade.py",
        "pages/05_Sobre_Etica.py",
        "docs/decisions.md",
        "docs/wireframes.md",
        "docs/delivery_checklist.md",
        "models/model_card.md",
    )

    assert all((PROJECT_ROOT / path).is_file() for path in expected_files)


def test_bootstrap_required_directories_exist() -> None:
    """Mantém a estrutura V1 disponível também em um clone limpo do Git."""
    expected_directories = (
        "pages",
        "src/data",
        "src/features",
        "src/models",
        "src/plots",
        "src/ui",
        "src/utils",
        "models",
        "data/raw",
        "data/processed",
        "data/examples",
        "notebooks",
        "tests/unit",
        "tests/smoke",
        "tests/e2e",
        "docs",
    )

    assert all((PROJECT_ROOT / path).is_dir() for path in expected_directories)


def test_app_uses_accented_streamlit_navigation_labels() -> None:
    """Garante que a sidebar use navegação amigável e traduzível."""
    app_source = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")
    i18n_source = (PROJECT_ROOT / "src" / "ui" / "i18n.py").read_text(
        encoding="utf-8"
    )

    assert "st.navigation" in app_source
    assert 'title=t("nav.home")' in app_source
    assert 'title=t("nav.exploration")' in app_source
    assert 'title=t("nav.prediction")' in app_source
    assert 'title=t("nav.about")' in app_source
    assert '"nav.home": "Início"' in i18n_source
    assert '"nav.exploration": "Exploração"' in i18n_source
    assert '"nav.prediction": "Predição"' in i18n_source
    assert '"nav.about": "Sobre e Ética"' in i18n_source


def test_app_component_imports_exist(monkeypatch) -> None:
    """Falha se app.py importar helper inexistente da camada visual."""
    app_source = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")
    tree = ast.parse(app_source)
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "src.ui.components"
        for alias in node.names
    }
    fake_streamlit = SimpleNamespace(
        sidebar=SimpleNamespace(selectbox=lambda _label, options, **_kwargs: options[0]),
        markdown=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        columns=lambda count: [SimpleNamespace(markdown=lambda *_args, **_kwargs: None) for _ in range(count)],
        session_state={},
    )
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    sys.modules.pop("src.ui.components", None)

    try:
        components = import_module("src.ui.components")

        assert "render_sidebar_controls" in imported_names
        assert imported_names
        assert all(hasattr(components, name) for name in imported_names)
    finally:
        sys.modules.pop("src.ui.components", None)
