"""Pré-processamento reproduzível para modelagem tabular do WDBC.

Este módulo mantém a preparação de dados separada do treino de modelos. O
``StandardScaler`` deve ser ajustado apenas no conjunto de treino, por meio de
um ``Pipeline`` do Scikit-learn, para evitar vazamento de dados do teste.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from src.data.schema import FEATURE_NAMES, TARGET_COLUMN, TARGET_LABELS
from src.data.validation import (
    DataValidationError,
    validate_feature_columns,
    validate_no_missing_values,
    validate_non_negative_features,
    validate_numeric_features,
)


DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42


def separate_features_and_target(
    dataframe: pd.DataFrame, *, target_column: str = TARGET_COLUMN
) -> tuple[pd.DataFrame, pd.Series]:
    """Return canonical feature matrix ``X`` and target vector ``y``.

    The backend keeps the original WDBC feature names. The returned feature
    matrix is always copied and ordered exactly as ``FEATURE_NAMES``.
    """
    _require_dataframe(dataframe)
    validate_feature_columns(dataframe, allow_extra_columns=True)

    if target_column not in dataframe.columns:
        raise DataValidationError(f"Coluna target obrigatória ausente: {target_column}.")

    allowed_columns = set(FEATURE_NAMES) | {target_column}
    extra_columns = sorted(set(dataframe.columns) - allowed_columns)
    if extra_columns:
        raise DataValidationError(
            "Colunas não esperadas para modelagem: " f"{', '.join(extra_columns)}."
        )

    features = dataframe.loc[:, list(FEATURE_NAMES)].copy()
    target = dataframe[target_column].rename(target_column).copy()
    _validate_feature_matrix(features)
    _validate_target(target)
    return features, target


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create a stratified, reproducible train/test split for the WDBC data.

    Defaults follow the project constitution: ``test_size=0.2``,
    ``random_state=42`` and ``stratify=y``. Feature columns are copied and
    reordered to the canonical ``FEATURE_NAMES`` order before splitting.
    """
    _validate_feature_matrix(X)
    target = _as_target_series(y)
    _validate_target(target)

    if len(X) != len(target):
        raise DataValidationError(
            "X e y devem possuir a mesma quantidade de amostras para o split."
        )

    X_ordered = X.loc[:, list(FEATURE_NAMES)].copy()
    y_ordered = target.copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X_ordered,
        y_ordered,
        test_size=test_size,
        random_state=random_state,
        stratify=y_ordered,
    )
    validate_train_test_split(X_train, X_test, y_train, y_test)
    return X_train, X_test, y_train, y_test


def build_scaling_pipeline() -> Pipeline:
    """Build a preprocessing pipeline with ``StandardScaler``.

    Scaling is recommended for Logistic Regression, KNN and SVM because these
    models are sensitive to feature scale. Fit this pipeline only on training
    data, then call ``transform`` on validation/test data.
    """
    return Pipeline(steps=[("scaler", StandardScaler())])


def build_passthrough_pipeline() -> Pipeline:
    """Build a preprocessing pipeline that keeps features unchanged.

    Tree-based models generally do not require scaling. This pipeline preserves
    the Scikit-learn interface without changing the feature matrix shape.
    """
    return Pipeline(steps=[("passthrough", FunctionTransformer(validate=False))])


def validate_train_test_split(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> None:
    """Validate the train/test split contract used by the modeling stage."""
    _validate_feature_matrix(X_train, require_canonical_order=True)
    _validate_feature_matrix(X_test, require_canonical_order=True)
    y_train = _as_target_series(y_train)
    y_test = _as_target_series(y_test)
    _validate_target(y_train)
    _validate_target(y_test)

    if len(X_train) != len(y_train):
        raise DataValidationError("X_train e y_train possuem tamanhos diferentes.")
    if len(X_test) != len(y_test):
        raise DataValidationError("X_test e y_test possuem tamanhos diferentes.")
    if not X_train.index.equals(y_train.index):
        raise DataValidationError("Os índices de X_train e y_train não estão alinhados.")
    if not X_test.index.equals(y_test.index):
        raise DataValidationError("Os índices de X_test e y_test não estão alinhados.")
    if len(X_train.index.intersection(X_test.index)) > 0:
        raise DataValidationError("X_train e X_test não devem compartilhar índices.")


def _validate_feature_matrix(
    dataframe: pd.DataFrame, *, require_canonical_order: bool = False
) -> None:
    _require_dataframe(dataframe)
    validate_feature_columns(dataframe)
    if require_canonical_order and tuple(dataframe.columns) != FEATURE_NAMES:
        raise DataValidationError("As features devem seguir a ordem canônica do WDBC.")

    features = dataframe.loc[:, list(FEATURE_NAMES)]
    validate_numeric_features(features)
    validate_no_missing_values(features)
    validate_non_negative_features(features)


def _validate_target(target: pd.Series) -> None:
    if not isinstance(target, pd.Series):
        raise TypeError("O target deve ser um pandas.Series.")
    if target.isna().any():
        raise DataValidationError("O target não deve conter valores ausentes.")

    expected_classes = set(TARGET_LABELS)
    observed_classes = set(target.unique())
    if observed_classes != expected_classes:
        raise DataValidationError(
            "O target deve conter exatamente as duas classes canônicas do WDBC: "
            f"{sorted(expected_classes)}."
        )


def _as_target_series(target: pd.Series) -> pd.Series:
    if not isinstance(target, pd.Series):
        raise TypeError("O target deve ser um pandas.Series.")
    return target.rename(TARGET_COLUMN)


def _require_dataframe(dataframe: pd.DataFrame) -> None:
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("A matriz de features deve ser um pandas.DataFrame.")
