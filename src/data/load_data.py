"""Carregamento local e reproduzível do dataset WDBC via Scikit-learn."""

from typing import Any

import pandas as pd
from sklearn.datasets import load_breast_cancer

from src.data.schema import (
    DATASET_LOADER,
    DATASET_NAME,
    DATASET_SOURCE,
    EXPECTED_FEATURE_COUNT,
    EXPECTED_SAMPLE_COUNT,
    FEATURE_NAMES,
    TARGET_COLUMN,
    TARGET_LABELS,
)


def load_wdbc_data() -> tuple[pd.DataFrame, pd.Series, dict[str, Any]]:
    """Return the WDBC features, target and stable dataset metadata.

    The Scikit-learn copy is bundled with the installed package, so this
    function does not download data or require network access. A runtime
    contract check prevents a changed upstream schema from being used silently.
    """
    dataset = load_breast_cancer(as_frame=True)
    loaded_feature_names = tuple(dataset.feature_names)
    loaded_target_labels = {
        index: label for index, label in enumerate(dataset.target_names.tolist())
    }

    if loaded_feature_names != FEATURE_NAMES:
        raise RuntimeError(
            "O schema retornado pelo Scikit-learn não corresponde ao schema "
            "canônico do WDBC definido pelo projeto."
        )
    if loaded_target_labels != dict(TARGET_LABELS):
        raise RuntimeError(
            "O mapeamento de target retornado pelo Scikit-learn não corresponde "
            "ao mapeamento canônico do projeto."
        )

    features = dataset.data.loc[:, list(FEATURE_NAMES)].copy()
    target = dataset.target.rename(TARGET_COLUMN).astype("int64").copy()
    metadata: dict[str, Any] = {
        "name": DATASET_NAME,
        "source": DATASET_SOURCE,
        "loader": DATASET_LOADER,
        "sample_count": len(features),
        "feature_count": len(FEATURE_NAMES),
        "feature_names": FEATURE_NAMES,
        "target_column": TARGET_COLUMN,
        "target_labels": dict(TARGET_LABELS),
    }

    if metadata["sample_count"] != EXPECTED_SAMPLE_COUNT:
        raise RuntimeError(
            "O WDBC carregado não possui a quantidade de amostras esperada: "
            f"{EXPECTED_SAMPLE_COUNT}."
        )
    if metadata["feature_count"] != EXPECTED_FEATURE_COUNT:
        raise RuntimeError(
            "O WDBC carregado não possui a quantidade de features esperada: "
            f"{EXPECTED_FEATURE_COUNT}."
        )

    return features, target, metadata


def load_wdbc_dataframe(*, include_target: bool = True) -> pd.DataFrame:
    """Return a copy of the WDBC data as a DataFrame.

    Args:
        include_target: Include the canonical ``target`` column when ``True``.

    Returns:
        A DataFrame with the 30 canonical WDBC features and, by default, the
        target column. The feature order always matches ``FEATURE_NAMES``.
    """
    features, target, _ = load_wdbc_data()
    if not include_target:
        return features

    return features.assign(**{TARGET_COLUMN: target})
