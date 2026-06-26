"""Funções de análise exploratória para o dataset WDBC.

Todas as funções carregam o WDBC pela camada oficial do projeto, não baixam
dados, não persistem arquivos e não alteram o dataset original in-place.
"""

from typing import Any

import pandas as pd

from src.data.load_data import load_wdbc_data
from src.data.schema import FEATURE_GROUPS, FEATURE_NAMES, TARGET_LABELS


PRIORITY_LABEL = 0
PRIORITY_CLASS = TARGET_LABELS[PRIORITY_LABEL]


def get_dataset_overview() -> dict[str, Any]:
    """Return core WDBC metadata and missing-value information."""
    features, target, metadata = load_wdbc_data()

    return {
        "dataset_name": metadata["name"],
        "dataset_source": metadata["source"],
        "sample_count": len(features),
        "feature_count": len(FEATURE_NAMES),
        "class_count": int(target.nunique()),
        "target_labels": dict(TARGET_LABELS),
        "priority_label": PRIORITY_LABEL,
        "priority_class": PRIORITY_CLASS,
        "missing_values_total": int(features.isna().sum().sum() + target.isna().sum()),
    }


def get_target_distribution() -> pd.DataFrame:
    """Return count and percentage by WDBC target class.

    Scikit-learn exposes the target as ``0 = malignant`` and ``1 = benign``.
    """
    _, target, _ = load_wdbc_data()
    counts = target.value_counts().sort_index()

    return pd.DataFrame(
        {
            "target": counts.index.astype(int),
            "class_name": [TARGET_LABELS[int(label)] for label in counts.index],
            "count": counts.to_numpy(dtype=int),
            "percentage": (counts / len(target) * 100).to_numpy(dtype=float),
        }
    )


def get_feature_group_summary() -> pd.DataFrame:
    """Return the canonical WDBC feature groups and their sizes."""
    return pd.DataFrame(
        [
            {
                "group": group_name,
                "feature_count": len(features),
                "features": ", ".join(features),
            }
            for group_name, features in FEATURE_GROUPS.items()
        ]
    )


def get_descriptive_statistics(group: str | None = None) -> pd.DataFrame:
    """Return descriptive statistics for WDBC features.

    Args:
        group: Optional canonical feature group: ``mean``, ``error`` or
            ``worst``. When omitted, all 30 features are summarized.
    """
    features, _, _ = load_wdbc_data()
    selected_features = FEATURE_GROUPS[group] if group else FEATURE_NAMES
    statistics = features.loc[:, list(selected_features)].describe().T

    return statistics.rename_axis("feature").reset_index()


def get_missing_values_summary() -> pd.DataFrame:
    """Return missing-value counts and percentages by feature."""
    features, _, _ = load_wdbc_data()
    missing_counts = features.isna().sum()

    return pd.DataFrame(
        {
            "feature": missing_counts.index,
            "missing_count": missing_counts.to_numpy(dtype=int),
            "missing_percentage": (
                missing_counts / len(features) * 100
            ).to_numpy(dtype=float),
        }
    )


def get_top_target_correlations(top_n: int = 10) -> pd.DataFrame:
    """Return features most correlated with the numeric target.

    The sign must be interpreted carefully because the WDBC target uses
    ``0 = malignant`` and ``1 = benign``. Correlation is exploratory and does
    not imply medical causality.
    """
    features, target, metadata = load_wdbc_data()
    dataframe = features.assign(**{metadata["target_column"]: target})
    correlations = (
        dataframe.corr(numeric_only=True)[metadata["target_column"]]
        .drop(metadata["target_column"])
        .loc[list(FEATURE_NAMES)]
    )

    return (
        pd.DataFrame(
            {
                "feature": correlations.index,
                "correlation_with_target": correlations.to_numpy(dtype=float),
                "absolute_correlation": correlations.abs().to_numpy(dtype=float),
            }
        )
        .sort_values("absolute_correlation", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
