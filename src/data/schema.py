"""Schema canônico do Breast Cancer Wisconsin Diagnostic (WDBC)."""

from collections.abc import Mapping


FEATURE_NAMES: tuple[str, ...] = (
    "mean radius",
    "mean texture",
    "mean perimeter",
    "mean area",
    "mean smoothness",
    "mean compactness",
    "mean concavity",
    "mean concave points",
    "mean symmetry",
    "mean fractal dimension",
    "radius error",
    "texture error",
    "perimeter error",
    "area error",
    "smoothness error",
    "compactness error",
    "concavity error",
    "concave points error",
    "symmetry error",
    "fractal dimension error",
    "worst radius",
    "worst texture",
    "worst perimeter",
    "worst area",
    "worst smoothness",
    "worst compactness",
    "worst concavity",
    "worst concave points",
    "worst symmetry",
    "worst fractal dimension",
)

FEATURE_GROUPS: Mapping[str, tuple[str, ...]] = {
    "mean": FEATURE_NAMES[:10],
    "error": FEATURE_NAMES[10:20],
    "worst": FEATURE_NAMES[20:],
}

# Scikit-learn expõe os targets do WDBC nesta ordem: malignant, benign.
TARGET_LABELS: Mapping[int, str] = {0: "malignant", 1: "benign"}
