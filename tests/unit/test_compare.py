"""Unit tests for controlled in-memory model comparison."""

from pathlib import Path

from src.models.compare import run_model_comparison


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


def test_run_model_comparison_returns_expected_contract() -> None:
    payload = run_model_comparison()

    assert set(payload) == {"results", "ranking", "metadata"}
    assert len(payload["results"]) >= 2
    assert payload["ranking"]
    assert payload["metadata"]["priority_label"] == 0
    assert payload["metadata"]["priority_class"] == "malignant"
    assert payload["metadata"]["priority_metric"] == "recall_malignant"


def test_run_model_comparison_ranking_prioritizes_malignant_recall() -> None:
    payload = run_model_comparison()
    ranking = payload["ranking"]

    recall_values = [row["recall_malignant"] for row in ranking]

    assert recall_values == sorted(recall_values, reverse=True)


def test_run_model_comparison_metadata_documents_reproducible_split() -> None:
    metadata = run_model_comparison()["metadata"]

    assert metadata["test_size"] == 0.2
    assert metadata["random_state"] == 42
    assert metadata["ranking_criteria"] == [
        "recall_malignant",
        "roc_auc_malignant",
        "f1_malignant",
    ]


def test_run_model_comparison_does_not_create_final_artifacts() -> None:
    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)

    run_model_comparison()

    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)
