"""Unit tests for strict WDBC prediction-input validation."""

import pandas as pd
import pytest

from src.data.schema import FEATURE_NAMES
from src.data.validation import DataValidationError, validate_prediction_input


@pytest.fixture
def valid_prediction_input() -> pd.DataFrame:
    return pd.DataFrame([{feature: 1.0 for feature in FEATURE_NAMES}])


def test_validation_accepts_a_complete_single_numeric_row(
    valid_prediction_input: pd.DataFrame,
) -> None:
    validate_prediction_input(valid_prediction_input)


def test_validation_rejects_missing_columns(valid_prediction_input: pd.DataFrame) -> None:
    invalid_input = valid_prediction_input.drop(columns=[FEATURE_NAMES[0]])

    with pytest.raises(DataValidationError, match="Colunas obrigatórias ausentes"):
        validate_prediction_input(invalid_input)


def test_validation_rejects_extra_columns(valid_prediction_input: pd.DataFrame) -> None:
    invalid_input = valid_prediction_input.assign(unexpected_feature=1.0)

    with pytest.raises(DataValidationError, match="Colunas não esperadas"):
        validate_prediction_input(invalid_input)


def test_validation_rejects_non_numeric_values(valid_prediction_input: pd.DataFrame) -> None:
    invalid_input = valid_prediction_input.astype({FEATURE_NAMES[0]: "object"})
    invalid_input.loc[0, FEATURE_NAMES[0]] = "invalid"

    with pytest.raises(DataValidationError, match="features devem ser numéricas"):
        validate_prediction_input(invalid_input)


def test_validation_rejects_missing_values(valid_prediction_input: pd.DataFrame) -> None:
    invalid_input = valid_prediction_input.copy()
    invalid_input.loc[0, FEATURE_NAMES[0]] = None

    with pytest.raises(DataValidationError, match="Valores ausentes"):
        validate_prediction_input(invalid_input)


def test_validation_rejects_negative_values(valid_prediction_input: pd.DataFrame) -> None:
    invalid_input = valid_prediction_input.copy()
    invalid_input.loc[0, FEATURE_NAMES[0]] = -1.0

    with pytest.raises(DataValidationError, match="Valores negativos"):
        validate_prediction_input(invalid_input)


def test_validation_rejects_multiple_prediction_rows(
    valid_prediction_input: pd.DataFrame,
) -> None:
    invalid_input = pd.concat([valid_prediction_input, valid_prediction_input])

    with pytest.raises(DataValidationError, match="exatamente uma linha"):
        validate_prediction_input(invalid_input)
