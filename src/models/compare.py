"""Orquestração em memória da comparação inicial de modelos WDBC."""

from typing import Any

from src.data.load_data import load_wdbc_data
from src.features.preprocess import (
    DEFAULT_RANDOM_STATE,
    DEFAULT_TEST_SIZE,
    split_train_test,
)
from src.models.evaluate import (
    MALIGNANT_LABEL,
    calculate_roc_curve_points,
    evaluate_candidate_models,
    rank_models_by_recall_then_auc,
)
from src.models.select import select_recommended_candidate
from src.models.train import build_candidate_models, train_candidate_models


PRIORITY_CLASS = "malignant"
PRIORITY_METRIC = "recall_malignant"


def run_model_comparison() -> dict[str, Any]:
    """Run the complete initial model-comparison flow in memory.

    The flow loads the local WDBC dataset, creates the canonical stratified
    train/test split, trains candidate models in memory, evaluates them and
    returns a ranking for academic analysis. It does not save models, metrics,
    feature names, CSVs or any other final artifact.
    """
    features, target, dataset_metadata = load_wdbc_data()
    X_train, X_test, y_train, y_test = split_train_test(features, target)
    candidates = build_candidate_models()
    trained_models = train_candidate_models(candidates, X_train, y_train)
    results = evaluate_candidate_models(trained_models, X_test, y_test)
    roc_curves = {
        model_name: calculate_roc_curve_points(model, X_test, y_test)
        for model_name, model in trained_models.items()
    }
    ranked_results = rank_models_by_recall_then_auc(results)
    ranking = [
        {"model_name": model_name, **metrics}
        for model_name, metrics in ranked_results
    ]
    metadata = {
        "dataset_name": dataset_metadata["name"],
        "sample_count": dataset_metadata["sample_count"],
        "feature_count": dataset_metadata["feature_count"],
        "train_size": len(X_train),
        "test_size": DEFAULT_TEST_SIZE,
        "test_sample_count": len(X_test),
        "random_state": DEFAULT_RANDOM_STATE,
        "priority_metric": PRIORITY_METRIC,
        "priority_class": PRIORITY_CLASS,
        "priority_label": MALIGNANT_LABEL,
        "ranking_criteria": [
            "recall_malignant",
            "roc_auc_malignant",
            "f1_malignant",
        ],
    }

    payload = {
        "results": results,
        "ranking": ranking,
        "roc_curves": roc_curves,
        "metadata": metadata,
    }
    payload["recommended_candidate"] = select_recommended_candidate(payload)

    return payload
