"""Validações estritas para entradas tabulares do schema WDBC."""

import pandas as pd

from src.data.schema import FEATURE_NAMES


class DataValidationError(ValueError):
    """Raised when input data violates the canonical WDBC contract."""


def validate_feature_columns(
    dataframe: pd.DataFrame, *, allow_extra_columns: bool = False
) -> None:
    """Validate required WDBC columns and reject duplicates or extras by default."""
    _require_dataframe(dataframe)
    expected_columns = set(FEATURE_NAMES)
    received_columns = set(dataframe.columns)
    missing_columns = sorted(expected_columns - received_columns)
    duplicate_columns = dataframe.columns[dataframe.columns.duplicated()].tolist()

    if missing_columns:
        raise DataValidationError(
            f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}."
        )
    if duplicate_columns:
        formatted_columns = ", ".join(map(str, duplicate_columns))
        raise DataValidationError(f"Colunas duplicadas não são permitidas: {formatted_columns}.")

    if not allow_extra_columns:
        extra_columns = sorted(received_columns - expected_columns)
        if extra_columns:
            raise DataValidationError(
                f"Colunas não esperadas: {', '.join(extra_columns)}. "
                "A entrada deve conter exatamente as 30 features do WDBC."
            )


def validate_numeric_features(dataframe: pd.DataFrame) -> None:
    """Reject columns whose dtype is not numeric without coercing values."""
    _require_dataframe(dataframe)
    invalid_columns = [
        str(column)
        for column in dataframe.columns
        if not pd.api.types.is_numeric_dtype(dataframe[column])
    ]
    if invalid_columns:
        raise DataValidationError(
            "As features devem ser numéricas. Colunas inválidas: "
            f"{', '.join(invalid_columns)}."
        )


def validate_no_missing_values(dataframe: pd.DataFrame) -> None:
    """Reject null values and identify every affected column."""
    _require_dataframe(dataframe)
    missing_columns = [
        str(column) for column in dataframe.columns if dataframe[column].isna().any()
    ]
    if missing_columns:
        raise DataValidationError(
            f"Valores ausentes não são permitidos: {', '.join(missing_columns)}."
        )


def validate_non_negative_features(dataframe: pd.DataFrame) -> None:
    """Reject negative values, which are invalid for the WDBC feature contract."""
    _require_dataframe(dataframe)
    validate_numeric_features(dataframe)
    negative_columns = [
        str(column) for column in dataframe.columns if (dataframe[column] < 0).any()
    ]
    if negative_columns:
        raise DataValidationError(
            "Valores negativos não são permitidos nas features WDBC: "
            f"{', '.join(negative_columns)}."
        )


def validate_single_prediction_row(dataframe: pd.DataFrame) -> None:
    """Require exactly one row for an individual prediction request."""
    _require_dataframe(dataframe)
    if len(dataframe) != 1:
        raise DataValidationError(
            "A predição individual aceita exatamente uma linha; "
            f"foram recebidas {len(dataframe)}."
        )


def validate_prediction_input(dataframe: pd.DataFrame) -> None:
    """Run the complete strict validation sequence for one prediction input."""
    validate_feature_columns(dataframe)
    validate_numeric_features(dataframe)
    validate_no_missing_values(dataframe)
    validate_non_negative_features(dataframe)
    validate_single_prediction_row(dataframe)


def _require_dataframe(dataframe: pd.DataFrame) -> None:
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("A entrada deve ser um pandas.DataFrame.")
