"""Helpers visuais leves para padronizar a experiência Streamlit."""

from __future__ import annotations

from collections.abc import Iterable

try:  # pragma: no cover - fallback used only outside the Streamlit runtime.
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover
    class _SidebarFallback:
        @staticmethod
        def selectbox(_label, options, index=0, **_kwargs):
            return list(options)[index]

    class _StreamlitFallback:
        sidebar = _SidebarFallback()

        @staticmethod
        def columns(count: int):
            return [_StreamlitFallback() for _ in range(count)]

        @staticmethod
        def markdown(*_args, **_kwargs) -> None:
            return None

        @staticmethod
        def warning(*_args, **_kwargs) -> None:
            return None

    st = _StreamlitFallback()

from src.ui.i18n import LANGUAGE_OPTIONS, get_language, set_language, t
from src.ui.theme import THEME_OPTIONS, apply_theme, get_theme, set_theme


ETHICS_NOTICE = (
    "O FemHealth ML Triage é uma plataforma demonstrativa acadêmica. "
    "A saída do modelo não substitui diagnóstico médico, laudo anatomopatológico, "
    "avaliação clínica ou decisão profissional. O médico sempre deve ter a palavra final."
)


def apply_global_style() -> None:
    """Apply small CSS refinements without changing Streamlit behavior."""
    apply_theme()


def render_sidebar_controls() -> None:
    """Render language and theme controls in the sidebar."""
    language = get_language()
    selected_language_label = st.sidebar.selectbox(
        t("language.label", language),
        list(LANGUAGE_OPTIONS.values()),
        index=list(LANGUAGE_OPTIONS).index(language),
        key="fh_language_selector",
    )
    selected_language = {
        label: code for code, label in LANGUAGE_OPTIONS.items()
    }[selected_language_label]
    set_language(selected_language)

    theme = get_theme()
    theme_labels = {
        "light": t("theme.light", selected_language),
        "dark": t("theme.dark", selected_language),
    }
    selected_theme_label = st.sidebar.selectbox(
        t("theme.label", selected_language),
        list(theme_labels.values()),
        index=list(THEME_OPTIONS).index(theme),
        key="fh_theme_selector",
    )
    selected_theme = {
        label: code for code, label in theme_labels.items()
    }[selected_theme_label]
    set_theme(selected_theme)
    apply_theme(selected_theme)


def render_page_intro(title: str, subtitle: str, description: str) -> None:
    """Render a consistent page opening block."""
    st.markdown(f'<div class="fh-kicker">{subtitle}</div>', unsafe_allow_html=True)
    st.title(title)
    st.write(description)


def render_card(title: str, body: str, target=st) -> None:
    """Render a compact explanatory card."""
    target.markdown(
        f"""
        <div class="fh-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card_grid(cards: Iterable[tuple[str, str]], columns: int = 3) -> None:
    """Render cards in a responsive Streamlit column grid."""
    cards = list(cards)
    for start in range(0, len(cards), columns):
        cols = st.columns(columns)
        for column, (title, body) in zip(cols, cards[start : start + columns]):
            if hasattr(column, "markdown"):
                render_card(title, body, target=column)
            else:
                render_card(title, body)


def render_ethics_notice(short: bool = False) -> None:
    """Render the mandatory ethical notice with consistent wording."""
    if short:
        st.warning(t("ethics.short"))
        return

    st.warning(t("ethics.full"))


def render_soft_divider() -> None:
    """Render a subtle divider without relying on Streamlit version-specific APIs."""
    st.markdown('<div class="fh-soft-divider"></div>', unsafe_allow_html=True)
