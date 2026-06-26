"""Smoke tests do contrato estrutural inicial do projeto."""

from pathlib import Path

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
