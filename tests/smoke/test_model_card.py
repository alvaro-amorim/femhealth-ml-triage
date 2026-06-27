"""Smoke checks for the operational model card."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_MODEL_CARD = PROJECT_ROOT / "docs" / "model_card.md"
MODELS_MODEL_CARD = PROJECT_ROOT / "models" / "model_card.md"


def test_operational_model_cards_contain_academic_warning() -> None:
    for model_card_path in (DOCS_MODEL_CARD, MODELS_MODEL_CARD):
        content = model_card_path.read_text(encoding="utf-8")

        assert "artefato acadêmico" in content
        assert "não deve ser usado para diagnóstico médico" in content
        assert "não substitui diagnóstico médico" in content
        assert "models/artifacts/recommended_model.joblib" in content
        assert "python -m src.models.persist" in content
