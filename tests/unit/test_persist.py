"""Unit tests for controlled recommended-model persistence."""

import json

from src.data.load_data import load_wdbc_data
from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_NAMES
from src.models.persist import (
    RECOMMENDED_FEATURE_NAMES_FILENAME,
    RECOMMENDED_METRICS_FILENAME,
    RECOMMENDED_MODEL_FILENAME,
    load_recommended_model_artifacts,
    save_recommended_model_artifacts,
)


def test_save_recommended_model_artifacts_creates_expected_files(tmp_path) -> None:
    artifact_paths = save_recommended_model_artifacts(tmp_path)

    assert artifact_paths["model"].name == RECOMMENDED_MODEL_FILENAME
    assert artifact_paths["metrics"].name == RECOMMENDED_METRICS_FILENAME
    assert artifact_paths["feature_names"].name == RECOMMENDED_FEATURE_NAMES_FILENAME
    assert all(path.exists() for path in artifact_paths.values())
    assert {path.name for path in tmp_path.iterdir()} == {
        RECOMMENDED_MODEL_FILENAME,
        RECOMMENDED_METRICS_FILENAME,
        RECOMMENDED_FEATURE_NAMES_FILENAME,
    }


def test_persisted_model_loads_and_predicts(tmp_path) -> None:
    artifact_paths = save_recommended_model_artifacts(tmp_path)
    model = load_recommended_model_artifacts(artifact_paths["model"])
    features, _, _ = load_wdbc_data()
    sample = features.head(3)

    predictions = model.predict(sample)
    probabilities = model.predict_proba(sample)

    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")
    assert len(predictions) == len(sample)
    assert probabilities.shape == (len(sample), 2)


def test_saved_metrics_and_metadata_follow_project_contract(tmp_path) -> None:
    artifact_paths = save_recommended_model_artifacts(tmp_path)
    payload = json.loads(artifact_paths["metrics"].read_text(encoding="utf-8"))
    metrics = payload["metrics"]
    metadata = payload["metadata"]

    assert {
        "accuracy",
        "precision_malignant",
        "recall_malignant",
        "f1_malignant",
        "roc_auc_malignant",
    }.issubset(metrics)
    assert metadata["priority_label"] == 0
    assert metadata["priority_class"] == "malignant"
    assert metadata["selection_criteria"] == [
        "recall_malignant",
        "roc_auc_malignant",
        "f1_malignant",
    ]
    assert metadata["test_size"] == 0.2
    assert metadata["random_state"] == 42
    assert metadata["academic_warning"]


def test_saved_feature_names_match_canonical_order(tmp_path) -> None:
    artifact_paths = save_recommended_model_artifacts(tmp_path)
    payload = json.loads(artifact_paths["feature_names"].read_text(encoding="utf-8"))

    assert payload["feature_count"] == EXPECTED_FEATURE_COUNT
    assert payload["feature_names"] == list(FEATURE_NAMES)
