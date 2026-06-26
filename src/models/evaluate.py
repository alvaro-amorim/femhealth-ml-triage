"""Métricas e comparação de classificadores para o WDBC."""

from collections.abc import Mapping
from typing import Any

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


MALIGNANT_LABEL = 0
BENIGN_LABEL = 1
CONFUSION_MATRIX_LABELS = [MALIGNANT_LABEL, BENIGN_LABEL]


def get_malignant_probability(model: BaseEstimator, X_test: pd.DataFrame) -> list[float]:
    """Return the predicted probability for the malignant class.

    In Scikit-learn's WDBC target, ``0 = malignant`` and ``1 = benign``. ROC AUC
    for the project's priority class must therefore use the probability column
    associated with class ``0``; using the benign column would invert the
    interpretation.
    """
    if not hasattr(model, "predict_proba"):
        raise TypeError("O modelo precisa expor predict_proba para calcular ROC AUC.")

    classes = list(getattr(model, "classes_", []))
    if MALIGNANT_LABEL not in classes:
        raise ValueError("O modelo treinado não expõe a classe maligna esperada: 0.")

    malignant_index = classes.index(MALIGNANT_LABEL)
    probabilities = np.asarray(model.predict_proba(X_test))
    return probabilities[:, malignant_index].tolist()


def evaluate_classifier(
    model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, Any]:
    """Calculate core classification metrics for a trained WDBC classifier."""
    y_pred = model.predict(X_test)
    malignant_probability = get_malignant_probability(model, X_test)
    y_true_malignant = (y_test == MALIGNANT_LABEL).astype(int)

    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision_malignant": float(
            precision_score(
                y_test, y_pred, pos_label=MALIGNANT_LABEL, zero_division=0
            )
        ),
        "recall_malignant": float(
            recall_score(y_test, y_pred, pos_label=MALIGNANT_LABEL, zero_division=0)
        ),
        "f1_malignant": float(
            f1_score(y_test, y_pred, pos_label=MALIGNANT_LABEL, zero_division=0)
        ),
        "roc_auc_malignant": float(
            roc_auc_score(y_true_malignant, malignant_probability)
        ),
        "confusion_matrix": confusion_matrix(
            y_test, y_pred, labels=CONFUSION_MATRIX_LABELS
        ).tolist(),
    }


def evaluate_candidate_models(
    trained_models: Mapping[str, BaseEstimator],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, dict[str, Any]]:
    """Evaluate trained candidate models and return metrics by model name."""
    return {
        model_name: evaluate_classifier(model, X_test, y_test)
        for model_name, model in trained_models.items()
    }


def rank_models_by_recall_then_auc(
    results: Mapping[str, Mapping[str, Any]]
) -> list[tuple[str, Mapping[str, Any]]]:
    """Rank models by malignant recall, then malignant ROC AUC, then F1.

    This ranking is only an analytical ordering for comparison. It does not
    select or persist a final production model.
    """
    return sorted(
        results.items(),
        key=lambda item: (
            item[1]["recall_malignant"],
            item[1]["roc_auc_malignant"],
            item[1]["f1_malignant"],
        ),
        reverse=True,
    )
