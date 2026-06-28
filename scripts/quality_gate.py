"""Quality gate local para o projeto FemHealth ML Triage.

O script executa checagens rápidas de higiene técnica e reprodutibilidade sem
treinar modelos, sem gerar artefatos e sem depender de internet.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path
from typing import Callable

import joblib


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.schema import FEATURE_NAMES

ALLOWED_MODEL_ARTIFACTS = {
    ROOT / "models" / "artifacts" / "recommended_model.joblib",
    ROOT / "models" / "artifacts" / "recommended_model_metrics.json",
    ROOT / "models" / "artifacts" / "recommended_model_feature_names.json",
}

TEXT_ROOTS = [
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "models" / "model_card.md",
    ROOT / "pages",
    ROOT / "src",
    ROOT / "tests",
]

IGNORED_DIRS = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".codex",
    ".agents",
    "__pycache__",
    "htmlcov",
}

MOJIBAKE_MARKERS = ("Ã", "Â", "â€")
PROHIBITED_LANGUAGE = (
    "diagnóstico automático",
    "substitui médico",
    "decisão clínica automática",
    "uso clínico",
    "laudo automático",
    "garantia",
    "100% seguro",
    "detecção definitiva",
)


def iter_text_files() -> list[Path]:
    """Return project text files relevant to repository hygiene checks."""
    files: list[Path] = []
    for root in TEXT_ROOTS:
        if root.is_file():
            files.append(root)
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in IGNORED_DIRS for part in path.parts):
                continue
            if path.suffix.lower() in {".md", ".py", ".txt"}:
                files.append(path)

    return files


def pass_check(message: str) -> None:
    """Print a successful check line."""
    print(f"[OK] {message}")


def fail_check(message: str) -> None:
    """Print a failed check line."""
    print(f"[ERRO] {message}")


def check(name: str, fn: Callable[[], None]) -> bool:
    """Run a named check and convert exceptions into terminal failures."""
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - CLI gate should report all check failures.
        fail_check(f"{name}: {exc}")
        return False

    pass_check(name)
    return True


def check_no_mojibake() -> None:
    """Fail when common mojibake markers or C1 controls are present."""
    offenders: list[str] = []
    for path in iter_text_files():
        content = path.read_text(encoding="utf-8-sig")
        has_marker = any(marker in content for marker in MOJIBAKE_MARKERS)
        has_c1_control = any(128 <= ord(char) <= 159 for char in content)
        if has_marker or has_c1_control:
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise ValueError("mojibake detectado em: " + ", ".join(offenders))


def check_no_deprecated_streamlit_width() -> None:
    """Fail when deprecated Streamlit width parameter remains in text files."""
    offenders: list[str] = []
    for path in iter_text_files():
        if "use_container_width" in path.read_text(encoding="utf-8-sig"):
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise ValueError("uso de use_container_width em: " + ", ".join(offenders))


def check_no_unwanted_artifacts() -> None:
    """Fail when model/data artifacts exist outside the allowed artifact set."""
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path in ALLOWED_MODEL_ARTIFACTS:
            continue
        if path.suffix.lower() in {".joblib", ".csv"} or path.name in {
            "metrics.json",
            "feature_names.json",
        }:
            offenders.append(str(path.relative_to(ROOT)))

    if offenders:
        raise ValueError("artefatos indevidos encontrados: " + ", ".join(offenders))


def check_required_artifacts_exist() -> None:
    """Fail when the canonical persisted artifacts are missing."""
    missing = [
        str(path.relative_to(ROOT)) for path in ALLOWED_MODEL_ARTIFACTS if not path.exists()
    ]
    if missing:
        raise ValueError("artefatos obrigatórios ausentes: " + ", ".join(missing))


def check_requirements_pins() -> None:
    """Fail when reproducibility pins are missing from requirements.txt."""
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8-sig").splitlines()
    required = {"scikit-learn==1.9.0", "joblib==1.5.3", "pytest-cov"}
    missing = sorted(required.difference(line.strip() for line in requirements))
    if missing:
        raise ValueError("dependências obrigatórias ausentes: " + ", ".join(missing))


def load_json(path: Path) -> object:
    """Load a JSON file with a clear error if invalid."""
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def check_json_artifacts() -> None:
    """Fail when metrics or feature-name JSON artifacts are invalid."""
    metrics = load_json(ROOT / "models" / "artifacts" / "recommended_model_metrics.json")
    feature_payload = load_json(
        ROOT / "models" / "artifacts" / "recommended_model_feature_names.json"
    )

    if not isinstance(metrics, dict):
        raise ValueError("recommended_model_metrics.json não contém objeto JSON")
    if not isinstance(feature_payload, dict):
        raise ValueError("recommended_model_feature_names.json não contém objeto JSON")

    saved_features = feature_payload.get("feature_names")
    if saved_features != list(FEATURE_NAMES):
        raise ValueError("features persistidas não batem com o schema canônico")
    if feature_payload.get("feature_count") != len(FEATURE_NAMES):
        raise ValueError("feature_count persistido não é 30")

    metrics_block = metrics.get("metrics")
    if not isinstance(metrics_block, dict):
        raise ValueError("bloco metrics ausente ou inválido")
    for metric_name in (
        "accuracy",
        "precision_malignant",
        "recall_malignant",
        "f1_malignant",
        "roc_auc_malignant",
    ):
        if metric_name not in metrics_block:
            raise ValueError(f"métrica ausente: {metric_name}")


def check_model_loads_and_classes() -> None:
    """Fail when the persisted pipeline cannot be loaded or class labels differ."""
    model_path = ROOT / "models" / "artifacts" / "recommended_model.joblib"
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        model = joblib.load(model_path)

    if not hasattr(model, "predict"):
        raise ValueError("modelo carregado não expõe predict")
    if not hasattr(model, "predict_proba"):
        raise ValueError("modelo carregado não expõe predict_proba")

    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        final_estimator = list(model.named_steps.values())[-1]
        classes = getattr(final_estimator, "classes_", None)

    if classes is None:
        raise ValueError("classes_ não encontrado no pipeline ou estimador final")
    if list(classes) != [0, 1]:
        raise ValueError(f"classes esperadas [0, 1], obtido {list(classes)}")


def check_no_prohibited_language() -> None:
    """Fail when critical unsafe medical claims appear in project text files."""
    offenders: list[str] = []
    for path in iter_text_files():
        content = path.read_text(encoding="utf-8-sig").lower()
        for term in PROHIBITED_LANGUAGE:
            if term in content:
                offenders.append(f"{path.relative_to(ROOT)}: {term}")

    if offenders:
        raise ValueError("linguagem proibida encontrada: " + ", ".join(offenders))


def main() -> int:
    """Run all quality checks and return a process exit code."""
    checks: tuple[tuple[str, Callable[[], None]], ...] = (
        ("arquivos principais sem mojibake comum", check_no_mojibake),
        ("sem use_container_width", check_no_deprecated_streamlit_width),
        ("sem artefatos indevidos fora dos permitidos", check_no_unwanted_artifacts),
        ("artefatos permitidos existem", check_required_artifacts_exist),
        ("requirements com versões reprodutíveis", check_requirements_pins),
        ("JSONs de métricas e features válidos", check_json_artifacts),
        ("modelo persistido carrega e expõe classes [0, 1]", check_model_loads_and_classes),
        ("sem linguagem proibida crítica", check_no_prohibited_language),
    )

    results = [check(name, fn) for name, fn in checks]
    if all(results):
        pass_check("quality gate concluído")
        return 0

    fail_check("quality gate falhou")
    return 1


if __name__ == "__main__":
    sys.exit(main())
