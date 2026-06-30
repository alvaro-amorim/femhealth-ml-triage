"""Camada simples de internacionalização para a interface Streamlit."""

from __future__ import annotations

try:  # pragma: no cover - fallback used only outside the Streamlit runtime.
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover
    class _StreamlitFallback:
        session_state: dict[str, str] = {}

    st = _StreamlitFallback()


LANGUAGE_KEY = "fh_language"
DEFAULT_LANGUAGE = "pt"
LANGUAGE_OPTIONS = {
    "pt": "Português",
    "en": "English",
}


TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt": {
        "nav.home": "Início",
        "nav.exploration": "Exploração",
        "nav.prediction": "Predição",
        "nav.models": "Modelos",
        "nav.explainability": "Explicabilidade",
        "nav.about": "Sobre e Ética",
        "language.label": "Idioma",
        "theme.label": "Tema",
        "theme.light": "Claro",
        "theme.dark": "Escuro",
        "class.malignant": "Maligno",
        "class.benign": "Benigno",
        "class.priority": "Maligno (0)",
        "group.mean": "Medidas médias",
        "group.error": "Variações das medidas",
        "group.worst": "Maiores valores observados",
        "ethics.short": "Uso acadêmico e demonstrativo: a saída do modelo não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional.",
        "ethics.full": "O FemHealth ML Triage é uma plataforma demonstrativa acadêmica. A saída do modelo não substitui diagnóstico médico, laudo anatomopatológico, avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final.",
    },
    "en": {
        "nav.home": "Home",
        "nav.exploration": "Exploration",
        "nav.prediction": "Prediction",
        "nav.models": "Models",
        "nav.explainability": "Explainability",
        "nav.about": "About and Ethics",
        "language.label": "Language",
        "theme.label": "Theme",
        "theme.light": "Light",
        "theme.dark": "Dark",
        "class.malignant": "Malignant",
        "class.benign": "Benign",
        "class.priority": "Malignant (0)",
        "group.mean": "Mean measurements",
        "group.error": "Measurement variations",
        "group.worst": "Largest observed values",
        "ethics.short": "Academic and demonstrative use: the model output does not replace medical diagnosis, pathology reports, clinical evaluation, or professional decisions.",
        "ethics.full": "FemHealth ML Triage is an academic demonstrative platform. The model output does not replace medical diagnosis, pathology reports, clinical evaluation, or professional decisions. A physician must always have the final say.",
    },
}


def get_language() -> str:
    """Return the current interface language."""
    session_state = getattr(st, "session_state", {})
    language = session_state.get(LANGUAGE_KEY, DEFAULT_LANGUAGE)
    return language if language in LANGUAGE_OPTIONS else DEFAULT_LANGUAGE


def set_language(language: str) -> None:
    """Persist the selected interface language in Streamlit session state."""
    if language not in LANGUAGE_OPTIONS:
        raise ValueError(f"Unsupported language: {language}")
    if hasattr(st, "session_state"):
        st.session_state[LANGUAGE_KEY] = language


def t(key: str, language: str | None = None) -> str:
    """Translate a UI key, falling back to Portuguese and then to the key."""
    selected_language = language or get_language()
    return (
        TRANSLATIONS.get(selected_language, {}).get(key)
        or TRANSLATIONS[DEFAULT_LANGUAGE].get(key)
        or key
    )


def translate_target_label(label: int | str, language: str | None = None) -> str:
    """Return the display label for a WDBC target value."""
    selected_language = language or get_language()
    numeric_label = int(label)
    if numeric_label == 0:
        return f"{t('class.malignant', selected_language)} (0)"
    if numeric_label == 1:
        return f"{t('class.benign', selected_language)} (1)"
    raise ValueError(f"Unsupported target label: {label}")


def translate_group_name(group_name: str, language: str | None = None) -> str:
    """Return the display label for a canonical WDBC feature group."""
    return t(f"group.{group_name}", language)
