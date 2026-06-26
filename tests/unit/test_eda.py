"""Unit tests for WDBC exploratory-data-analysis helpers."""

from pathlib import Path

from src.analysis.eda import (
    get_dataset_overview,
    get_descriptive_statistics,
    get_feature_group_summary,
    get_missing_values_summary,
    get_target_distribution,
    get_top_target_correlations,
)
from src.data.schema import EXPECTED_FEATURE_COUNT, EXPECTED_SAMPLE_COUNT, FEATURE_NAMES


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


def test_dataset_overview_returns_canonical_counts() -> None:
    overview = get_dataset_overview()

    assert overview["sample_count"] == EXPECTED_SAMPLE_COUNT == 569
    assert overview["feature_count"] == EXPECTED_FEATURE_COUNT == 30
    assert overview["class_count"] == 2
    assert overview["priority_label"] == 0
    assert overview["priority_class"] == "malignant"


def test_target_distribution_matches_wdbc_samples_and_labels() -> None:
    distribution = get_target_distribution()

    assert set(distribution["target"]) == {0, 1}
    assert set(distribution["class_name"]) == {"malignant", "benign"}
    assert distribution["count"].sum() == EXPECTED_SAMPLE_COUNT
    assert round(distribution["percentage"].sum(), 10) == 100.0


def test_missing_values_summary_confirms_no_missing_values() -> None:
    missing_summary = get_missing_values_summary()

    assert len(missing_summary) == EXPECTED_FEATURE_COUNT
    assert missing_summary["missing_count"].sum() == 0
    assert missing_summary["missing_percentage"].sum() == 0.0


def test_feature_group_summary_has_three_groups_with_ten_features_each() -> None:
    group_summary = get_feature_group_summary()

    assert list(group_summary["group"]) == ["mean", "error", "worst"]
    assert group_summary["feature_count"].tolist() == [10, 10, 10]


def test_descriptive_statistics_returns_all_30_features() -> None:
    statistics = get_descriptive_statistics()

    assert len(statistics) == EXPECTED_FEATURE_COUNT
    assert set(statistics["feature"]) == set(FEATURE_NAMES)
    assert {"mean", "std", "min", "25%", "50%", "75%", "max"}.issubset(
        statistics.columns
    )


def test_target_correlations_return_only_valid_features() -> None:
    correlations = get_top_target_correlations(top_n=10)

    assert len(correlations) == 10
    assert set(correlations["feature"]).issubset(set(FEATURE_NAMES))
    assert correlations["absolute_correlation"].is_monotonic_decreasing
    assert correlations["absolute_correlation"].between(0.0, 1.0).all()


def test_eda_helpers_do_not_create_persisted_artifacts() -> None:
    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)

    get_dataset_overview()
    get_target_distribution()
    get_feature_group_summary()
    get_descriptive_statistics()
    get_missing_values_summary()
    get_top_target_correlations()

    assert not any(path.exists() for path in FORBIDDEN_ARTIFACTS)
