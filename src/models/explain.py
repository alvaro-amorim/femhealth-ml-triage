"""Explicabilidade acadêmica do modelo persistido.

As funções deste módulo carregam o pipeline persistido da Rodada 8 e calculam
interpretações globais e locais em memória. Nenhum artefato é salvo.
"""

from __future__ import annotations

import warnings
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data.load_data import load_wdbc_data
from src.data.schema import EXPECTED_FEATURE_COUNT, FEATURE_NAMES, TARGET_LABELS
from src.data.validation import DataValidationError, validate_prediction_input
from src.models.evaluate import BENIGN_LABEL, MALIGNANT_LABEL
from src.models.predict import build_reference_sample, load_prediction_artifacts


EXPLAINABILITY_WARNING = (
    "Explicabilidade descreve o comportamento estatístico do modelo neste "
    "projeto acadêmico. Ela não substitui diagnóstico médico, não implica "
    "causalidade médica e não deve ser usada como recomendação profissional."
)


def load_explainability_context() -> dict[str, Any]:
    """Load model, dataset and metadata needed for explainability."""
    artifacts = load_prediction_artifacts()
    model = artifacts["model"]
    scaler, classifier = _extract_linear_pipeline_parts(model)
    features, target, dataset_metadata = load_wdbc_data()

    return {
        "model": model,
        "scaler": scaler,
        "classifier": classifier,
        "features": features.loc[:, list(FEATURE_NAMES)].copy(),
        "target": target.copy(),
        "metadata": {
            **dataset_metadata,
            "model_name": artifacts["metrics"].get(
                "selected_model_name", "Regressão Logística"
            ),
            "priority_label": MALIGNANT_LABEL,
            "priority_class": TARGET_LABELS[MALIGNANT_LABEL],
            "feature_count": EXPECTED_FEATURE_COUNT,
        },
        "artifact_paths": artifacts["paths"],
    }


def get_logistic_regression_coefficients(
    context: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Return coefficients mapped to canonical WDBC feature names.

    In this persisted binary classifier, Scikit-learn exposes classes as
    ``[0, 1]``. The single coefficient vector is oriented toward ``classes_[1]``,
    which is ``benign (1)``. Therefore, positive coefficients favor the benign
    class in the model's log-odds, while negative coefficients favor the
    malignant class. This is a model-behavior interpretation, not medical
    causality.
    """
    context = context or load_explainability_context()
    classifier: LogisticRegression = context["classifier"]
    coefficients = np.asarray(classifier.coef_[0], dtype=float)

    return pd.DataFrame(
        {
            "feature": list(FEATURE_NAMES),
            "coefficient": coefficients,
            "coefficient_abs": np.abs(coefficients),
            "interpretive_direction": [
                _coefficient_direction(coefficient) for coefficient in coefficients
            ],
        }
    )


def get_global_feature_importance(
    context: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Return global feature importance sorted by absolute coefficient."""
    coefficients = get_logistic_regression_coefficients(context)
    return coefficients.sort_values("coefficient_abs", ascending=False).reset_index(
        drop=True
    )


def build_reference_sample_for_explanation(target_label: int) -> pd.DataFrame:
    """Return one real WDBC sample for local explainability."""
    return build_reference_sample(target_label)


def get_local_feature_contributions(
    input_data: pd.DataFrame,
    context: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Calculate local linear contributions for one WDBC sample.

    Contributions are computed after applying the persisted ``StandardScaler``:
    ``standardized_value * logistic_regression_coefficient``. Positive values
    favor ``benign (1)`` in the model, and negative values favor
    ``malignant (0)``. They explain model behavior for one tabular sample only.
    """
    context = context or load_explainability_context()
    sample = _validate_single_sample(input_data)
    scaler: StandardScaler = context["scaler"]
    classifier: LogisticRegression = context["classifier"]

    standardized_values = np.asarray(scaler.transform(sample))[0]
    coefficients = np.asarray(classifier.coef_[0], dtype=float)
    contributions = standardized_values * coefficients

    return pd.DataFrame(
        {
            "feature": list(FEATURE_NAMES),
            "value": sample.iloc[0].to_numpy(dtype=float),
            "standardized_value": standardized_values,
            "coefficient": coefficients,
            "contribution": contributions,
            "contribution_abs": np.abs(contributions),
            "interpretive_direction": [
                _contribution_direction(contribution)
                for contribution in contributions
            ],
        }
    )


def get_top_local_contributions(
    input_data: pd.DataFrame,
    top_n: int = 10,
    context: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Return the largest local contributions by absolute magnitude."""
    if top_n <= 0:
        raise ValueError("top_n deve ser maior que zero.")

    contributions = get_local_feature_contributions(input_data, context)
    return contributions.sort_values("contribution_abs", ascending=False).head(
        top_n
    ).reset_index(drop=True)


def get_shap_global_feature_importance(
    context: dict[str, Any] | None = None,
    sample_size: int = 100,
) -> dict[str, Any]:
    """Try to calculate SHAP global importance for the linear model.

    SHAP is optional at runtime. If import or calculation fails because of local
    compatibility, the caller receives ``available=False`` and can display the
    coefficient fallback without breaking the app.
    """
    context = context or load_explainability_context()
    try:
        scaler: StandardScaler = context["scaler"]
        classifier: LogisticRegression = context["classifier"]
        features: pd.DataFrame = context["features"].head(sample_size)

        # SHAP is optional and may emit dependency deprecation warnings during
        # import in some environments. Keep the filter local to this optional
        # path so project warnings and real SHAP errors remain visible.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=PendingDeprecationWarning,
                module=r"shap(\.|$)",
            )
            import shap  # type: ignore

            transformed_features = scaler.transform(features)
            explainer = shap.LinearExplainer(classifier, transformed_features)
            shap_values = np.asarray(explainer.shap_values(transformed_features))

        if shap_values.ndim == 3:
            shap_values = shap_values[0]
        if shap_values.ndim != 2:
            raise ValueError("Formato inesperado de valores SHAP.")

        shap_importance = pd.DataFrame(
            {
                "feature": list(FEATURE_NAMES),
                "mean_abs_shap": np.abs(shap_values).mean(axis=0),
            }
        ).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)

        return {
            "available": True,
            "method": "shap.LinearExplainer",
            "message": "SHAP calculado em memória para o modelo linear persistido.",
            "data": shap_importance,
        }
    except Exception as error:  # pragma: no cover - depends on optional runtime
        return {
            "available": False,
            "method": "fallback_coefficients",
            "message": (
                "SHAP não ficou disponível neste ambiente; usando fallback "
                f"por coeficientes. Detalhe técnico: {error}"
            ),
            "data": get_global_feature_importance(context),
        }


def _extract_linear_pipeline_parts(
    model: Pipeline,
) -> tuple[StandardScaler, LogisticRegression]:
    if not isinstance(model, Pipeline):
        raise TypeError("O modelo persistido deve ser um Pipeline Scikit-learn.")

    scaler = model.named_steps.get("scaler")
    classifier = model.named_steps.get("classifier")
    if not isinstance(scaler, StandardScaler):
        raise TypeError("O pipeline persistido deve conter StandardScaler.")
    if not isinstance(classifier, LogisticRegression):
        raise TypeError("O pipeline persistido deve conter LogisticRegression.")

    classes = list(getattr(classifier, "classes_", []))
    if classes != [MALIGNANT_LABEL, BENIGN_LABEL]:
        raise ValueError("O classificador deve expor classes [0, 1] para WDBC.")

    return scaler, classifier


def _validate_single_sample(input_data: pd.DataFrame) -> pd.DataFrame:
    sample = input_data.copy(deep=True)
    validate_prediction_input(sample)
    if list(sample.columns) != list(FEATURE_NAMES):
        raise DataValidationError(
            "As features devem seguir exatamente a ordem canônica do WDBC."
        )
    return sample.loc[:, list(FEATURE_NAMES)].copy(deep=True)


def _coefficient_direction(coefficient: float) -> str:
    if coefficient > 0:
        return "favorece benign (1) no comportamento do modelo"
    if coefficient < 0:
        return "favorece malignant (0) no comportamento do modelo"
    return "efeito linear neutro no comportamento do modelo"


def _contribution_direction(contribution: float) -> str:
    if contribution > 0:
        return "contribui para benign (1) neste exemplo"
    if contribution < 0:
        return "contribui para malignant (0) neste exemplo"
    return "contribuição local neutra neste exemplo"
