"""Smoke tests for the local Scikit-learn WDBC loader."""

from src.data.load_data import load_wdbc_data, load_wdbc_dataframe
from src.data.schema import (
    EXPECTED_FEATURE_COUNT,
    EXPECTED_SAMPLE_COUNT,
    FEATURE_NAMES,
    TARGET_COLUMN,
    TARGET_LABELS,
)


def test_wdbc_loads_with_the_canonical_shape_and_features() -> None:
    features, target, metadata = load_wdbc_data()

    assert features.shape == (EXPECTED_SAMPLE_COUNT, EXPECTED_FEATURE_COUNT)
    assert tuple(features.columns) == FEATURE_NAMES
    assert not features.isna().any().any()
    assert target.name == TARGET_COLUMN
    assert not target.isna().any()
    assert set(target.unique()) == set(TARGET_LABELS)
    assert target.nunique() == 2
    assert metadata["sample_count"] == EXPECTED_SAMPLE_COUNT
    assert metadata["feature_count"] == EXPECTED_FEATURE_COUNT
    assert metadata["feature_names"] == FEATURE_NAMES
    assert metadata["target_labels"] == dict(TARGET_LABELS)


def test_wdbc_dataframe_optionally_includes_target() -> None:
    dataframe_with_target = load_wdbc_dataframe()
    features_only = load_wdbc_dataframe(include_target=False)

    assert dataframe_with_target.shape == (EXPECTED_SAMPLE_COUNT, EXPECTED_FEATURE_COUNT + 1)
    assert list(dataframe_with_target.columns) == [*FEATURE_NAMES, TARGET_COLUMN]
    assert features_only.shape == (EXPECTED_SAMPLE_COUNT, EXPECTED_FEATURE_COUNT)
