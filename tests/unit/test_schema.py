"""Unit tests for the canonical WDBC schema."""

from src.data.schema import (
    DATASET_NAME,
    EXPECTED_FEATURE_COUNT,
    FEATURE_GROUPS,
    FEATURE_NAMES,
    TARGET_COLUMN,
    TARGET_LABELS,
)


def test_schema_has_30_unique_features_in_three_groups() -> None:
    assert len(FEATURE_NAMES) == EXPECTED_FEATURE_COUNT == 30
    assert len(set(FEATURE_NAMES)) == EXPECTED_FEATURE_COUNT
    assert tuple(FEATURE_GROUPS) == ("mean", "error", "worst")
    assert all(len(group) == 10 for group in FEATURE_GROUPS.values())


def test_schema_declares_dataset_and_target_contract() -> None:
    assert DATASET_NAME == "Breast Cancer Wisconsin Diagnostic (WDBC)"
    assert TARGET_COLUMN == "target"
    assert TARGET_LABELS == {0: "malignant", 1: "benign"}
