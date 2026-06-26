"""Unit tests for WDBC preprocessing and train/test splitting."""

import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.data.load_data import load_wdbc_data, load_wdbc_dataframe
from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_NAMES, TARGET_COLUMN
from src.features.preprocess import (
    build_passthrough_pipeline,
    build_scaling_pipeline,
    separate_features_and_target,
    split_train_test,
    validate_train_test_split,
)


@pytest.fixture
def wdbc_dataset() -> tuple[pd.DataFrame, pd.Series]:
    features, target, _ = load_wdbc_data()
    return features, target


@pytest.fixture
def wdbc_split(
    wdbc_dataset: tuple[pd.DataFrame, pd.Series],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    features, target = wdbc_dataset
    return split_train_test(features, target)


def test_separate_features_and_target_keeps_canonical_contract() -> None:
    dataframe = load_wdbc_dataframe()
    original_dataframe = dataframe.copy(deep=True)

    features, target = separate_features_and_target(dataframe)

    assert tuple(features.columns) == FEATURE_NAMES
    assert features.shape[1] == EXPECTED_FEATURE_COUNT
    assert target.name == TARGET_COLUMN
    pd.testing.assert_frame_equal(dataframe, original_dataframe)


def test_split_train_test_keeps_all_30_features_and_80_20_sizes(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, y_train, y_test = wdbc_split

    assert tuple(X_train.columns) == FEATURE_NAMES
    assert tuple(X_test.columns) == FEATURE_NAMES
    assert X_train.shape == (455, EXPECTED_FEATURE_COUNT)
    assert X_test.shape == (114, EXPECTED_FEATURE_COUNT)
    assert len(y_train) == 455
    assert len(y_test) == 114


def test_split_train_test_has_no_index_overlap(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, _, _ = wdbc_split

    assert X_train.index.intersection(X_test.index).empty


def test_split_train_test_keeps_both_classes_in_each_target_split(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    _, _, y_train, y_test = wdbc_split

    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}


def test_split_train_test_preserves_class_ratio_approximately(
    wdbc_dataset: tuple[pd.DataFrame, pd.Series],
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    _, target = wdbc_dataset
    _, _, y_train, y_test = wdbc_split

    full_ratio = target.value_counts(normalize=True).sort_index()
    train_ratio = y_train.value_counts(normalize=True).sort_index()
    test_ratio = y_test.value_counts(normalize=True).sort_index()

    assert ((train_ratio - full_ratio).abs() < 0.02).all()
    assert ((test_ratio - full_ratio).abs() < 0.02).all()


def test_split_train_test_reorders_shuffled_input_to_canonical_features(
    wdbc_dataset: tuple[pd.DataFrame, pd.Series],
) -> None:
    features, target = wdbc_dataset
    shuffled_features = features.loc[:, list(reversed(FEATURE_NAMES))]

    X_train, X_test, _, _ = split_train_test(shuffled_features, target)

    assert tuple(X_train.columns) == FEATURE_NAMES
    assert tuple(X_test.columns) == FEATURE_NAMES


def test_validate_train_test_split_accepts_valid_split(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, y_train, y_test = wdbc_split

    validate_train_test_split(X_train, X_test, y_train, y_test)


def test_scaling_pipeline_contains_standard_scaler() -> None:
    pipeline = build_scaling_pipeline()

    assert isinstance(pipeline.named_steps["scaler"], StandardScaler)


def test_scaling_pipeline_fit_transform_train_and_transform_test(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, _, _ = wdbc_split
    pipeline = build_scaling_pipeline()

    X_train_scaled = pipeline.fit_transform(X_train)
    X_test_scaled = pipeline.transform(X_test)

    assert X_train_scaled.shape == X_train.shape
    assert X_test_scaled.shape == X_test.shape
    assert pipeline.named_steps["scaler"].n_samples_seen_ == len(X_train)


def test_passthrough_pipeline_preserves_feature_count(
    wdbc_split: tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
) -> None:
    X_train, X_test, _, _ = wdbc_split
    pipeline = build_passthrough_pipeline()

    X_train_processed = pipeline.fit_transform(X_train)
    X_test_processed = pipeline.transform(X_test)

    assert X_train_processed.shape[1] == EXPECTED_FEATURE_COUNT
    assert X_test_processed.shape[1] == EXPECTED_FEATURE_COUNT


def test_preprocess_functions_do_not_mutate_original_dataset(
    wdbc_dataset: tuple[pd.DataFrame, pd.Series],
) -> None:
    features, target = wdbc_dataset
    original_features = features.copy(deep=True)
    original_target = target.copy(deep=True)

    split_train_test(features, target)
    separate_features_and_target(features.assign(**{TARGET_COLUMN: target}))

    pd.testing.assert_frame_equal(features, original_features)
    pd.testing.assert_series_equal(target, original_target)
