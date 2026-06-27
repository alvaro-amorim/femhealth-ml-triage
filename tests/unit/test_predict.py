"""Unit tests for academic individual prediction."""

from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_NAMES
from src.data.validation import DataValidationError
from src.models.predict import (
    build_reference_sample,
    load_prediction_artifacts,
    predict_single_sample,
)


ALLOWED_PERSISTED_ARTIFACTS = {
    Path("models/artifacts/recommended_model.joblib"),
    Path("models/artifacts/recommended_model_metrics.json"),
    Path("models/artifacts/recommended_model_feature_names.json"),
}


def _tracked_model_artifacts() -> set[Path]:
    return {
        path
        for path in Path(".").rglob("*")
        if path.is_file()
        and ".venv" not in path.parts
        and (
            path.suffix in {".joblib", ".csv"}
            or path.name
            in {
                "metrics.json",
                "feature_names.json",
                "recommended_model_metrics.json",
                "recommended_model_feature_names.json",
            }
        )
    }


def test_prediction_artifacts_load_correctly() -> None:
    artifacts = load_prediction_artifacts()
    model = artifacts["model"]

    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")
    assert len(artifacts["feature_names"]) == EXPECTED_FEATURE_COUNT
    assert artifacts["feature_names"] == list(FEATURE_NAMES)


def test_build_reference_sample_returns_valid_malignant_row() -> None:
    sample = build_reference_sample(0)

    assert isinstance(sample, pd.DataFrame)
    assert sample.shape == (1, EXPECTED_FEATURE_COUNT)
    assert list(sample.columns) == list(FEATURE_NAMES)


def test_build_reference_sample_returns_valid_benign_row() -> None:
    sample = build_reference_sample(1)

    assert isinstance(sample, pd.DataFrame)
    assert sample.shape == (1, EXPECTED_FEATURE_COUNT)
    assert list(sample.columns) == list(FEATURE_NAMES)


def test_predict_single_sample_returns_expected_payload() -> None:
    sample = build_reference_sample(0)
    result = predict_single_sample(sample)

    assert {
        "predicted_label",
        "predicted_class",
        "probability_malignant",
        "probability_benign",
        "model_name",
        "priority_label",
        "priority_class",
        "academic_warning",
    }.issubset(result)
    assert result["predicted_label"] in {0, 1}
    assert result["predicted_class"] in {"malignant", "benign"}
    assert result["priority_label"] == 0
    assert result["priority_class"] == "malignant"


def test_predict_single_sample_probabilities_are_valid() -> None:
    result = predict_single_sample(build_reference_sample(1))

    assert 0.0 <= result["probability_malignant"] <= 1.0
    assert 0.0 <= result["probability_benign"] <= 1.0
    assert result["probability_malignant"] + result["probability_benign"] == pytest.approx(
        1.0
    )


def test_predict_single_sample_rejects_missing_column() -> None:
    invalid_sample = build_reference_sample(0).drop(columns=[FEATURE_NAMES[0]])

    with pytest.raises(DataValidationError):
        predict_single_sample(invalid_sample)


def test_predict_single_sample_rejects_extra_column() -> None:
    invalid_sample = build_reference_sample(0).assign(unexpected_feature=1.0)

    with pytest.raises(DataValidationError):
        predict_single_sample(invalid_sample)


def test_predict_single_sample_rejects_null_value() -> None:
    invalid_sample = build_reference_sample(0)
    invalid_sample.loc[invalid_sample.index[0], FEATURE_NAMES[0]] = None

    with pytest.raises(DataValidationError):
        predict_single_sample(invalid_sample)


def test_predict_single_sample_rejects_wrong_feature_order() -> None:
    invalid_sample = build_reference_sample(0)
    reversed_columns = list(reversed(FEATURE_NAMES))
    invalid_sample = invalid_sample.loc[:, reversed_columns]

    with pytest.raises(DataValidationError, match="ordem canônica"):
        predict_single_sample(invalid_sample)


def test_predict_single_sample_does_not_mutate_input() -> None:
    sample = build_reference_sample(0)
    original = sample.copy(deep=True)

    predict_single_sample(sample)

    assert_frame_equal(sample, original)


def test_prediction_functions_do_not_create_new_artifacts() -> None:
    before = _tracked_model_artifacts()

    predict_single_sample(build_reference_sample(0))

    after = _tracked_model_artifacts()
    assert after == before
    assert ALLOWED_PERSISTED_ARTIFACTS.issubset(after)
