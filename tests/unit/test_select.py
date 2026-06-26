"""Unit tests for controlled candidate-model selection."""

from pathlib import Path

import pytest

from src.models.select import select_recommended_candidate


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_ARTIFACTS = (
    PROJECT_ROOT / "models" / "final_model.joblib",
    PROJECT_ROOT / "models" / "final_pipeline.joblib",
    PROJECT_ROOT / "models" / "preprocessing_pipeline.joblib",
    PROJECT_ROOT / "models" / "metrics.json",
    PROJECT_ROOT / "models" / "feature_names.json",
    PROJECT_ROOT / "data" / "examples" / "case_benign.csv",
    PROJECT_ROOT / "data" / "examples" / "case_malignant.csv",
)


def _comparison_payload() -> dict:
    return {
        "ranking": [
            {
                "model_name": "knn",
                "accuracy": 0.80,
                "precision_malignant": 0.82,
                "recall_malignant": 0.95,
                "f1_malignant": 0.88,
                "roc_auc_malignant": 0.91,
            },
            {
                "model_name": "logistic_regression",
                "accuracy": 0.99,
                "precision_malignant": 0.98,
                "recall_malignant": 0.70,
                "f1_malignant": 0.82,
                "roc_auc_malignant": 0.99,
            },
        ],
        "metadata": {
            "priority_class": "malignant",
            "priority_label": 0,
            "ranking_criteria": [
                "recall_malignant",
                "roc_auc_malignant",
                "f1_malignant",
            ],
        },
    }


def test_select_recommended_candidate_returns_expected_fields() -> None:
    selected = select_recommended_candidate(_comparison_payload())

    assert set(selected) == {
        "selected_model_key",
        "selected_model_name",
        "selection_criteria",
        "priority_class",
        "priority_label",
        "metrics",
        "reason",
        "limitations",
    }
    assert selected["priority_label"] == 0
    assert selected["priority_class"] == "malignant"
    assert selected["selection_criteria"] == [
        "recall_malignant",
        "roc_auc_malignant",
        "f1_malignant",
    ]


def test_select_recommended_candidate_respects_ranking_order() -> None:
    selected = select_recommended_candidate(_comparison_payload())

    assert selected["selected_model_key"] == "knn"
    assert selected["selected_model_name"] == "KNN"


def test_selection_prioritizes_malignant_recall_before_accuracy() -> None:
    selected = select_recommended_candidate(_comparison_payload())

    assert selected["selected_model_key"] == "knn"
    assert selected["metrics"]["recall_malignant"] == 0.95
    assert selected["metrics"]["accuracy"] < 0.99


def test_select_recommended_candidate_rejects_empty_ranking() -> None:
    with pytest.raises(ValueError, match="ranking"):
        select_recommended_candidate({"ranking": [], "metadata": {}})


def test_select_recommended_candidate_does_not_create_final_artifacts() -> None:
    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)

    select_recommended_candidate(_comparison_payload())

    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)
