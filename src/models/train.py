"""Treinamento em memória de modelos candidatos para o WDBC.

Esta rodada não persiste artefatos. Os pipelines retornados aqui servem para
comparação controlada e futura integração com a página de modelos.
"""

from collections.abc import Mapping

import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from src.features.preprocess import build_passthrough_pipeline, build_scaling_pipeline


RANDOM_STATE = 42


def build_candidate_models() -> dict[str, Pipeline]:
    """Build simple, reproducible candidate classifiers.

    Logistic Regression and KNN use ``StandardScaler`` because they are
    sensitive to feature scale. Decision Tree uses a passthrough preprocessing
    step because tree-based models generally do not require scaling.
    """
    return {
        "logistic_regression": Pipeline(
            steps=[
                *build_scaling_pipeline().steps,
                (
                    "classifier",
                    LogisticRegression(max_iter=5000, random_state=RANDOM_STATE),
                ),
            ]
        ),
        "decision_tree": Pipeline(
            steps=[
                *build_passthrough_pipeline().steps,
                (
                    "classifier",
                    DecisionTreeClassifier(random_state=RANDOM_STATE),
                ),
            ]
        ),
        "knn": Pipeline(
            steps=[
                *build_scaling_pipeline().steps,
                ("classifier", KNeighborsClassifier(n_neighbors=5)),
            ]
        ),
    }


def train_model(
    model: BaseEstimator, X_train: pd.DataFrame, y_train: pd.Series
) -> BaseEstimator:
    """Fit a cloned model in memory and return the trained estimator.

    The input estimator and tabular data are not modified in place. No model,
    metric or feature-name artifact is saved by this function.
    """
    trained_model = clone(model)
    trained_model.fit(X_train.copy(deep=True), y_train.copy(deep=True))
    return trained_model


def train_candidate_models(
    models: Mapping[str, BaseEstimator],
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, BaseEstimator]:
    """Train every candidate model in memory and return trained estimators."""
    return {
        model_name: train_model(model, X_train, y_train)
        for model_name, model in models.items()
    }
