"""Persistência controlada do modelo candidato recomendado.

Os artefatos gerados por este módulo são técnicos e acadêmicos. Eles servem
para tornar as próximas etapas do projeto reprodutíveis; não representam uma
ferramenta para uso real em saúde.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
from sklearn.base import BaseEstimator

from src.data.load_data import load_wdbc_data
from src.data.schema import FEATURE_NAMES, TARGET_LABELS
from src.features.preprocess import DEFAULT_RANDOM_STATE, DEFAULT_TEST_SIZE, split_train_test
from src.models.compare import run_model_comparison
from src.models.evaluate import MALIGNANT_LABEL, evaluate_classifier
from src.models.train import build_candidate_models, train_model


DEFAULT_ARTIFACT_DIR = Path("models") / "artifacts"
RECOMMENDED_MODEL_FILENAME = "recommended_model.joblib"
RECOMMENDED_METRICS_FILENAME = "recommended_model_metrics.json"
RECOMMENDED_FEATURE_NAMES_FILENAME = "recommended_model_feature_names.json"

ACADEMIC_WARNING = (
    "Este modelo é um artefato acadêmico para demonstração de Machine Learning "
    "e não deve ser usado para diagnóstico médico."
)


def get_recommended_artifact_paths(
    output_dir: Path | str = DEFAULT_ARTIFACT_DIR,
) -> dict[str, Path]:
    """Return canonical paths for the recommended-model artifacts."""
    artifact_dir = Path(output_dir)
    return {
        "model": artifact_dir / RECOMMENDED_MODEL_FILENAME,
        "metrics": artifact_dir / RECOMMENDED_METRICS_FILENAME,
        "feature_names": artifact_dir / RECOMMENDED_FEATURE_NAMES_FILENAME,
    }


def recommended_artifacts_exist(
    output_dir: Path | str = DEFAULT_ARTIFACT_DIR,
) -> dict[str, bool]:
    """Return existence flags for each recommended-model artifact."""
    return {
        artifact_name: artifact_path.exists()
        for artifact_name, artifact_path in get_recommended_artifact_paths(output_dir).items()
    }


def build_recommended_model_artifacts() -> dict[str, Any]:
    """Train and evaluate the recommended candidate using the official split.

    The recommended candidate comes from the same controlled comparison used by
    the app. The persisted estimator is the full Scikit-learn pipeline, so the
    scaler is included when the selected algorithm requires scaling.
    """
    comparison_payload = run_model_comparison()
    recommended_candidate = comparison_payload["recommended_candidate"]
    selected_model_key = recommended_candidate["selected_model_key"]

    features, target, dataset_metadata = load_wdbc_data()
    X_train, X_test, y_train, y_test = split_train_test(features, target)
    candidate_models = build_candidate_models()
    if selected_model_key not in candidate_models:
        raise ValueError(f"Modelo candidato desconhecido: {selected_model_key}")

    trained_model = train_model(candidate_models[selected_model_key], X_train, y_train)
    metrics = evaluate_classifier(trained_model, X_test, y_test)
    metadata = {
        "dataset": dataset_metadata["name"],
        "dataset_source": dataset_metadata["source"],
        "dataset_loader": dataset_metadata["loader"],
        "sample_count": dataset_metadata["sample_count"],
        "feature_count": dataset_metadata["feature_count"],
        "classes": {str(label): name for label, name in TARGET_LABELS.items()},
        "target_mapping": {str(label): name for label, name in TARGET_LABELS.items()},
        "priority_label": MALIGNANT_LABEL,
        "priority_class": "malignant",
        "selection_criteria": recommended_candidate["selection_criteria"],
        "test_size": DEFAULT_TEST_SIZE,
        "random_state": DEFAULT_RANDOM_STATE,
        "selected_model_key": selected_model_key,
        "selected_model_name": recommended_candidate["selected_model_name"],
        "created_by": "Codex Rodada 8",
        "academic_warning": ACADEMIC_WARNING,
    }

    return {
        "model": trained_model,
        "metrics": {
            "selected_model_key": selected_model_key,
            "selected_model_name": recommended_candidate["selected_model_name"],
            "metrics": metrics,
            "metadata": metadata,
        },
        "feature_names": {
            "feature_names": list(FEATURE_NAMES),
            "feature_count": len(FEATURE_NAMES),
            "source": "src.data.schema.FEATURE_NAMES",
        },
        "metadata": metadata,
    }


def save_recommended_model_artifacts(
    output_dir: Path | str = DEFAULT_ARTIFACT_DIR,
) -> dict[str, Path]:
    """Build and persist the recommended-model artifacts.

    Returns:
        Paths of the saved model, metrics and feature-name files.
    """
    artifact_paths = get_recommended_artifact_paths(output_dir)
    artifact_paths["model"].parent.mkdir(parents=True, exist_ok=True)
    artifacts = build_recommended_model_artifacts()

    joblib.dump(artifacts["model"], artifact_paths["model"])
    artifact_paths["metrics"].write_text(
        json.dumps(artifacts["metrics"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    artifact_paths["feature_names"].write_text(
        json.dumps(artifacts["feature_names"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return artifact_paths


def load_recommended_model_artifacts(
    model_path: Path | str = DEFAULT_ARTIFACT_DIR / RECOMMENDED_MODEL_FILENAME,
) -> BaseEstimator:
    """Load a persisted recommended-model pipeline."""
    return joblib.load(Path(model_path))


if __name__ == "__main__":
    saved_paths = save_recommended_model_artifacts()
    for artifact_name, artifact_path in saved_paths.items():
        print(f"{artifact_name}: {artifact_path}")
