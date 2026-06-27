"""Unit tests for academic explainability helpers."""

from pathlib import Path

import pandas as pd

from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_NAMES
from src.models.explain import (
    build_reference_sample_for_explanation,
    get_global_feature_importance,
    get_logistic_regression_coefficients,
    get_top_local_contributions,
    load_explainability_context,
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


def test_load_explainability_context_returns_expected_metadata() -> None:
    context = load_explainability_context()

    assert context["metadata"]["model_name"] == "Regressão Logística"
    assert context["metadata"]["priority_label"] == 0
    assert context["metadata"]["priority_class"] == "malignant"
    assert context["metadata"]["feature_count"] == EXPECTED_FEATURE_COUNT


def test_logistic_regression_coefficients_cover_canonical_features() -> None:
    coefficients = get_logistic_regression_coefficients()

    assert isinstance(coefficients, pd.DataFrame)
    assert len(coefficients) == EXPECTED_FEATURE_COUNT
    assert coefficients["feature"].tolist() == list(FEATURE_NAMES)
    assert {"coefficient", "coefficient_abs", "interpretive_direction"}.issubset(
        coefficients.columns
    )


def test_global_feature_importance_contains_all_features_sorted_by_abs_value() -> None:
    global_importance = get_global_feature_importance()

    assert len(global_importance) == EXPECTED_FEATURE_COUNT
    assert set(global_importance["feature"]) == set(FEATURE_NAMES)
    assert global_importance["coefficient_abs"].is_monotonic_decreasing


def test_reference_sample_for_explanation_returns_one_valid_row() -> None:
    sample = build_reference_sample_for_explanation(0)

    assert sample.shape == (1, EXPECTED_FEATURE_COUNT)
    assert sample.columns.tolist() == list(FEATURE_NAMES)


def test_top_local_contributions_respects_top_n() -> None:
    sample = build_reference_sample_for_explanation(1)
    top_contributions = get_top_local_contributions(sample, top_n=10)

    assert len(top_contributions) == 10
    assert set(top_contributions["feature"]).issubset(set(FEATURE_NAMES))
    assert top_contributions["contribution_abs"].is_monotonic_decreasing


def test_explainability_functions_do_not_create_artifacts() -> None:
    before = _tracked_model_artifacts()

    context = load_explainability_context()
    get_global_feature_importance(context)
    sample = build_reference_sample_for_explanation(0)
    get_top_local_contributions(sample, context=context)

    after = _tracked_model_artifacts()
    assert after == before
    assert ALLOWED_PERSISTED_ARTIFACTS.issubset(after)
