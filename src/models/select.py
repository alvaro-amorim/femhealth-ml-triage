"""Seleção controlada de modelo candidato para continuidade acadêmica."""

from typing import Any


SELECTION_CRITERIA = [
    "recall_malignant",
    "roc_auc_malignant",
    "f1_malignant",
]

CANDIDATE_MODEL_NAMES = {
    "logistic_regression": "Regressão Logística",
    "decision_tree": "Árvore de Decisão",
    "knn": "KNN",
}


def select_recommended_candidate(comparison_payload: dict[str, Any]) -> dict[str, Any]:
    """Select the recommended candidate from an existing comparison payload.

    The function intentionally follows the ranking already produced by the
    project: first malignant recall, then malignant ROC AUC, then malignant F1.
    It does not train models, persist artifacts or define a clinical model.
    """
    ranking = comparison_payload.get("ranking", [])
    metadata = comparison_payload.get("metadata", {})
    if not ranking:
        raise ValueError("Payload de comparação não contém ranking de modelos.")

    selected = ranking[0]
    selected_model_key = selected["model_name"]
    selection_criteria = metadata.get("ranking_criteria", SELECTION_CRITERIA)

    return {
        "selected_model_key": selected_model_key,
        "selected_model_name": CANDIDATE_MODEL_NAMES.get(
            selected_model_key, selected_model_key
        ),
        "selection_criteria": list(selection_criteria),
        "priority_class": metadata.get("priority_class", "malignant"),
        "priority_label": metadata.get("priority_label", 0),
        "metrics": {
            "accuracy": selected["accuracy"],
            "precision_malignant": selected["precision_malignant"],
            "recall_malignant": selected["recall_malignant"],
            "f1_malignant": selected["f1_malignant"],
            "roc_auc_malignant": selected["roc_auc_malignant"],
        },
        "reason": (
            "Modelo candidato melhor ranqueado nesta comparação acadêmica "
            "inicial, seguindo recall da classe maligna como critério primário, "
            "ROC AUC maligno como primeiro desempate e F1 maligno como segundo "
            "desempate."
        ),
        "limitations": (
            "Seleção técnica e inicial para continuidade do projeto. Não é "
            "modelo clínico, não representa diagnóstico médico e ainda não há "
            "artefato final persistido."
        ),
    }
