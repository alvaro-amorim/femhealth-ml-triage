"""Predição individual acadêmica usando artefatos persistidos.

Este módulo não treina modelos e não salva novos arquivos. Ele apenas carrega o
pipeline persistido na Rodada 8, valida uma única amostra no schema WDBC e
retorna uma saída estruturada para uso demonstrativo no Streamlit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from src.data.load_data import load_wdbc_data
from src.data.schema import (
    EXPECTED_FEATURE_COUNT,
    FEATURE_GROUPS,
    FEATURE_NAMES,
    TARGET_LABELS,
)
from src.data.validation import DataValidationError, validate_prediction_input
from src.models.evaluate import BENIGN_LABEL, MALIGNANT_LABEL
from src.models.persist import (
    DEFAULT_ARTIFACT_DIR,
    get_recommended_artifact_paths,
    load_recommended_model_artifacts,
)


PRIORITY_LABEL = MALIGNANT_LABEL
PRIORITY_CLASS = TARGET_LABELS[PRIORITY_LABEL]
ACADEMIC_PREDICTION_WARNING = (
    "Esta saída representa apenas a estimativa acadêmica do modelo para uma "
    "amostra tabular no formato WDBC. Ela não deve ser usada para diagnóstico "
    "médico, decisão clínica, substituição de avaliação profissional ou laudo "
    "anatomopatológico. O médico sempre deve ter a palavra final."
)


def load_prediction_artifacts(
    artifact_dir: Path | str = DEFAULT_ARTIFACT_DIR,
) -> dict[str, Any]:
    """Load the persisted model, metrics and canonical feature names.

    Args:
        artifact_dir: Directory containing the Rodada 8 artifacts.

    Returns:
        Dictionary with model, metrics payload, feature-name payload and paths.

    Raises:
        FileNotFoundError: If any required artifact is absent.
        ValueError: If persisted feature names diverge from the canonical schema.
        TypeError: If the loaded estimator cannot predict probabilities.
    """
    artifact_paths = get_recommended_artifact_paths(artifact_dir)
    missing_artifacts = [
        str(path) for path in artifact_paths.values() if not path.exists()
    ]
    if missing_artifacts:
        raise FileNotFoundError(
            "Artefatos de predição ausentes: " + ", ".join(missing_artifacts)
        )

    model = load_recommended_model_artifacts(artifact_paths["model"])
    feature_payload = _read_json(artifact_paths["feature_names"])
    metrics_payload = _read_json(artifact_paths["metrics"])
    feature_names = feature_payload.get("feature_names")

    if feature_names != list(FEATURE_NAMES):
        raise ValueError(
            "As features persistidas não correspondem à ordem canônica do WDBC."
        )
    if not hasattr(model, "predict"):
        raise TypeError("O artefato carregado precisa expor predict.")
    if not hasattr(model, "predict_proba"):
        raise TypeError("O artefato carregado precisa expor predict_proba.")

    return {
        "model": model,
        "feature_names": feature_names,
        "feature_payload": feature_payload,
        "metrics": metrics_payload,
        "paths": artifact_paths,
    }


def get_prediction_input_schema() -> dict[str, Any]:
    """Return the strict schema expected by individual prediction."""
    return {
        "feature_names": list(FEATURE_NAMES),
        "feature_count": EXPECTED_FEATURE_COUNT,
        "feature_groups": {
            group_name: list(group_features)
            for group_name, group_features in FEATURE_GROUPS.items()
        },
        "target_labels": dict(TARGET_LABELS),
        "priority_label": PRIORITY_LABEL,
        "priority_class": PRIORITY_CLASS,
    }


def build_reference_sample(target_label: int) -> pd.DataFrame:
    """Return one real WDBC sample for the requested target label.

    The returned sample is copied from the local Scikit-learn WDBC dataset and
    contains exactly one row with the 30 canonical feature columns. It is only a
    public dataset example for demonstration; it is not a clinical case.
    """
    if target_label not in TARGET_LABELS:
        raise ValueError(
            "target_label deve ser 0 (malignant) ou 1 (benign) no WDBC."
        )

    features, target, _metadata = load_wdbc_data()
    matching_indexes = target[target == target_label].index
    if matching_indexes.empty:
        raise ValueError(f"Nenhuma amostra WDBC encontrada para target {target_label}.")

    return features.loc[[matching_indexes[0]], list(FEATURE_NAMES)].copy()


def predict_single_sample(
    input_data: pd.DataFrame | pd.Series | dict[str, Any],
    artifact_dir: Path | str = DEFAULT_ARTIFACT_DIR,
) -> dict[str, Any]:
    """Predict one WDBC-formatted sample with the persisted academic model.

    The input must contain exactly one row and the 30 WDBC features in canonical
    order. Validation is strict: missing columns, extra columns, wrong order,
    non-numeric values, nulls and invalid negative values are rejected instead
    of being silently corrected.
    """
    sample = _normalize_single_sample(input_data)
    artifacts = load_prediction_artifacts(artifact_dir)
    model = artifacts["model"]
    metrics_payload = artifacts["metrics"]

    predicted_label = int(model.predict(sample)[0])
    probabilities = np.asarray(model.predict_proba(sample))[0]
    probability_by_label = _probability_by_label(model, probabilities)

    probability_malignant = float(probability_by_label[MALIGNANT_LABEL])
    probability_benign = float(probability_by_label[BENIGN_LABEL])

    return {
        "predicted_label": predicted_label,
        "predicted_class": TARGET_LABELS[predicted_label],
        "probability_malignant": probability_malignant,
        "probability_benign": probability_benign,
        "model_name": metrics_payload.get("selected_model_name", "Modelo persistido"),
        "model_key": metrics_payload.get("selected_model_key"),
        "priority_label": PRIORITY_LABEL,
        "priority_class": PRIORITY_CLASS,
        "academic_warning": ACADEMIC_PREDICTION_WARNING,
    }


def _normalize_single_sample(
    input_data: pd.DataFrame | pd.Series | dict[str, Any],
) -> pd.DataFrame:
    """Convert accepted input forms into a validated one-row DataFrame."""
    if isinstance(input_data, pd.DataFrame):
        sample = input_data.copy(deep=True)
    elif isinstance(input_data, pd.Series):
        sample = input_data.to_frame().T.copy(deep=True)
    elif isinstance(input_data, dict):
        sample = pd.DataFrame([input_data]).copy(deep=True)
    else:
        raise TypeError("A entrada deve ser DataFrame, Series ou dict.")

    validate_prediction_input(sample)
    if list(sample.columns) != list(FEATURE_NAMES):
        raise DataValidationError(
            "As features devem seguir exatamente a ordem canônica do WDBC."
        )

    return sample.loc[:, list(FEATURE_NAMES)].copy(deep=True)


def _probability_by_label(
    model: BaseEstimator, probabilities: np.ndarray
) -> dict[int, float]:
    """Map predict_proba output to WDBC labels using estimator classes."""
    classes = list(getattr(model, "classes_", []))
    if not classes and hasattr(model, "named_steps"):
        final_estimator = list(model.named_steps.values())[-1]
        classes = list(getattr(final_estimator, "classes_", []))

    expected_labels = {MALIGNANT_LABEL, BENIGN_LABEL}
    if set(classes) != expected_labels:
        raise ValueError(
            "O modelo carregado não expõe as classes WDBC esperadas: 0 e 1."
        )

    return {
        int(label): float(probabilities[index])
        for index, label in enumerate(classes)
        if int(label) in expected_labels
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
