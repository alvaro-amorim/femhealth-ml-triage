"""Unit tests for in-memory model training and evaluation."""

from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data.load_data import load_wdbc_data
from src.features.preprocess import split_train_test
from src.models.evaluate import (
    evaluate_candidate_models,
    evaluate_classifier,
    get_malignant_probability,
    rank_models_by_recall_then_auc,
)
from src.models.train import build_candidate_models, train_candidate_models, train_model


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


class FixedProbabilityModel:
    """Small deterministic classifier for metric-contract tests."""

    classes_ = [1, 0]

    def __init__(self, predictions: list[int], probabilities: list[list[float]]) -> None:
        self._predictions = predictions
        self._probabilities = probabilities

    def predict(self, X: pd.DataFrame) -> list[int]:
        return self._predictions[: len(X)]

    def predict_proba(self, X: pd.DataFrame) -> list[list[float]]:
        return self._probabilities[: len(X)]


@pytest.fixture
def wdbc_split() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    features, target, _ = load_wdbc_data()
    return split_train_test(features, target)


@pytest.fixture
def candidate_models() -> dict[str, Pipeline]:
    return build_candidate_models()


def test_build_candidate_models_returns_expected_models(
    candidate_models: dict[str, Pipeline],
) -> None:
    assert len(candidate_models) >= 2
    assert {"logistic_regression", "decision_tree"}.issubset(candidate_models)
    assert "knn" in candidate_models


def test_scaled_candidate_models_use_standard_scaler(
    candidate_models: dict[str, Pipeline],
) -> None:
    assert isinstance(candidate_models["logistic_regression"].named_steps["scaler"], StandardScaler)
    assert isinstance(candidate_models["knn"].named_steps["scaler"], StandardScaler)


def test_decision_tree_uses_passthrough_without_scaler(
    candidate_models: dict[str, Pipeline],
) -> None:
    decision_tree = candidate_models["decision_tree"]

    assert "passthrough" in decision_tree.named_steps
    assert "scaler" not in decision_tree.named_steps


def test_train_model_fits_in_memory_without_mutating_data(
    candidate_models: dict[str, Pipeline],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, _, y_train, _ = wdbc_split
    original_X_train = X_train.copy(deep=True)
    original_y_train = y_train.copy(deep=True)

    trained_model = train_model(candidate_models["logistic_regression"], X_train, y_train)

    assert hasattr(trained_model, "classes_")
    pd.testing.assert_frame_equal(X_train, original_X_train)
    pd.testing.assert_series_equal(y_train, original_y_train)


def test_train_candidate_models_fits_all_candidates_in_memory(
    candidate_models: dict[str, Pipeline],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, _, y_train, _ = wdbc_split

    trained_models = train_candidate_models(candidate_models, X_train, y_train)

    assert set(trained_models) == set(candidate_models)
    assert all(hasattr(model, "classes_") for model in trained_models.values())


def test_evaluate_classifier_returns_required_metrics(
    candidate_models: dict[str, Pipeline],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, y_train, y_test = wdbc_split
    trained_model = train_model(candidate_models["logistic_regression"], X_train, y_train)

    metrics = evaluate_classifier(trained_model, X_test, y_test)

    assert set(metrics) == {
        "accuracy",
        "precision_malignant",
        "recall_malignant",
        "f1_malignant",
        "roc_auc_malignant",
        "confusion_matrix",
    }
    assert len(metrics["confusion_matrix"]) == 2
    assert all(len(row) == 2 for row in metrics["confusion_matrix"])


def test_evaluate_candidate_models_returns_metrics_between_zero_and_one(
    candidate_models: dict[str, Pipeline],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, y_train, y_test = wdbc_split
    trained_models = train_candidate_models(candidate_models, X_train, y_train)

    results = evaluate_candidate_models(trained_models, X_test, y_test)

    assert set(results) == set(candidate_models)
    for metrics in results.values():
        for metric_name in (
            "accuracy",
            "precision_malignant",
            "recall_malignant",
            "f1_malignant",
            "roc_auc_malignant",
        ):
            assert 0.0 <= metrics[metric_name] <= 1.0


def test_recall_malignant_uses_pos_label_zero() -> None:
    X_test = pd.DataFrame({"feature": [1.0, 2.0, 3.0, 4.0]})
    y_test = pd.Series([0, 0, 1, 1])
    model = FixedProbabilityModel(
        predictions=[0, 1, 1, 1],
        probabilities=[
            [0.10, 0.90],
            [0.80, 0.20],
            [0.90, 0.10],
            [0.60, 0.40],
        ],
    )

    metrics = evaluate_classifier(model, X_test, y_test)

    assert metrics["recall_malignant"] == 0.5


def test_roc_auc_malignant_uses_probability_for_class_zero() -> None:
    X_test = pd.DataFrame({"feature": [1.0, 2.0, 3.0, 4.0]})
    y_test = pd.Series([0, 0, 1, 1])
    malignant_probabilities = [0.90, 0.20, 0.10, 0.40]
    model = FixedProbabilityModel(
        predictions=[0, 1, 1, 1],
        probabilities=[
            [0.10, 0.90],
            [0.80, 0.20],
            [0.90, 0.10],
            [0.60, 0.40],
        ],
    )

    extracted_probabilities = get_malignant_probability(model, X_test)
    metrics = evaluate_classifier(model, X_test, y_test)

    assert extracted_probabilities == malignant_probabilities
    assert metrics["roc_auc_malignant"] == roc_auc_score(
        (y_test == 0).astype(int), malignant_probabilities
    )


def test_ranking_prioritizes_malignant_recall_before_accuracy() -> None:
    results = {
        "high_accuracy_low_recall": {
            "accuracy": 0.99,
            "recall_malignant": 0.50,
            "roc_auc_malignant": 0.99,
            "f1_malignant": 0.90,
        },
        "lower_accuracy_high_recall": {
            "accuracy": 0.80,
            "recall_malignant": 0.95,
            "roc_auc_malignant": 0.80,
            "f1_malignant": 0.70,
        },
    }

    ranked_results = rank_models_by_recall_then_auc(results)

    assert ranked_results[0][0] == "lower_accuracy_high_recall"


def test_ranking_uses_auc_then_f1_as_tiebreakers() -> None:
    results = {
        "lower_auc": {
            "recall_malignant": 0.90,
            "roc_auc_malignant": 0.80,
            "f1_malignant": 0.99,
        },
        "higher_auc": {
            "recall_malignant": 0.90,
            "roc_auc_malignant": 0.95,
            "f1_malignant": 0.70,
        },
        "same_auc_higher_f1": {
            "recall_malignant": 0.90,
            "roc_auc_malignant": 0.95,
            "f1_malignant": 0.80,
        },
    }

    ranked_results = rank_models_by_recall_then_auc(results)

    assert [name for name, _ in ranked_results] == [
        "same_auc_higher_f1",
        "higher_auc",
        "lower_auc",
    ]


def test_training_and_evaluation_do_not_create_persisted_artifacts(
    candidate_models: dict[str, Pipeline],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)
    X_train, X_test, y_train, y_test = wdbc_split

    trained_models = train_candidate_models(candidate_models, X_train, y_train)
    evaluate_candidate_models(trained_models, X_test, y_test)

    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)
