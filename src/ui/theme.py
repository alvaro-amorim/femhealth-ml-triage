"""Tema visual leve para a interface Streamlit."""

from __future__ import annotations

try:  # pragma: no cover - fallback used only outside the Streamlit runtime.
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover
    class _StreamlitFallback:
        session_state: dict[str, str] = {}

        @staticmethod
        def markdown(*_args, **_kwargs) -> None:
            return None

    st = _StreamlitFallback()


THEME_KEY = "fh_theme"
DEFAULT_THEME = "light"
THEME_OPTIONS = {
    "light": "Claro",
    "dark": "Escuro",
}

LIGHT_THEME = {
    "background": "#F8FAFC",
    "surface": "#F1F5F9",
    "surface_alt": "#E2E8F0",
    "card": "#FFFFFF",
    "card_hover": "#F8FAFC",
    "border": "rgba(15, 23, 42, 0.12)",
    "text": "#111827",
    "muted": "#475569",
    "subtle": "#64748B",
    "accent": "#6D28D9",
    "accent_2": "#0284C7",
    "warning_bg": "rgba(245, 158, 11, 0.12)",
    "warning_text": "#92400E",
    "warning_border": "rgba(245, 158, 11, 0.35)",
    "info_bg": "rgba(14, 165, 233, 0.10)",
    "info_text": "#075985",
    "success_bg": "rgba(34, 197, 94, 0.10)",
    "success_text": "#166534",
    "shadow": "0 10px 24px rgba(15, 23, 42, 0.07)",
}

DARK_THEME = {
    "background": "#0B1020",
    "surface": "#111827",
    "surface_alt": "#172033",
    "card": "#121A2B",
    "card_hover": "#182235",
    "border": "rgba(148, 163, 184, 0.28)",
    "text": "#F8FAFC",
    "muted": "#CBD5E1",
    "subtle": "#94A3B8",
    "accent": "#A78BFA",
    "accent_2": "#38BDF8",
    "warning_bg": "rgba(245, 158, 11, 0.14)",
    "warning_text": "#FCD34D",
    "warning_border": "rgba(245, 158, 11, 0.34)",
    "info_bg": "rgba(56, 189, 248, 0.12)",
    "info_text": "#BAE6FD",
    "success_bg": "rgba(34, 197, 94, 0.12)",
    "success_text": "#BBF7D0",
    "shadow": "0 18px 44px rgba(0, 0, 0, 0.24)",
}


def get_theme() -> str:
    """Return the current UI theme."""
    session_state = getattr(st, "session_state", {})
    theme = session_state.get(THEME_KEY, DEFAULT_THEME)
    return theme if theme in THEME_OPTIONS else DEFAULT_THEME


def set_theme(theme: str) -> None:
    """Persist the selected UI theme in Streamlit session state."""
    if theme not in THEME_OPTIONS:
        raise ValueError(f"Unsupported theme: {theme}")
    if hasattr(st, "session_state"):
        st.session_state[THEME_KEY] = theme


def get_theme_tokens(theme: str | None = None) -> dict[str, str]:
    """Return CSS tokens for the selected UI theme."""
    selected_theme = theme or get_theme()
    if selected_theme == "dark":
        return DARK_THEME
    if selected_theme == "light":
        return LIGHT_THEME
    raise ValueError(f"Unsupported theme: {selected_theme}")


def get_plotly_layout(theme: str | None = None) -> dict:
    """Return Plotly layout defaults that match the selected Streamlit theme."""
    tokens = get_theme_tokens(theme)
    return {
        "paper_bgcolor": tokens["card"],
        "plot_bgcolor": tokens["card"],
        "font": {"color": tokens["text"]},
        "legend": {
            "bgcolor": tokens["card"],
            "font": {"color": tokens["text"]},
        },
        "xaxis": {
            "gridcolor": tokens["border"],
            "linecolor": tokens["border"],
            "zerolinecolor": tokens["border"],
            "tickfont": {"color": tokens["muted"]},
            "title_font": {"color": tokens["text"]},
        },
        "yaxis": {
            "gridcolor": tokens["border"],
            "linecolor": tokens["border"],
            "zerolinecolor": tokens["border"],
            "tickfont": {"color": tokens["muted"]},
            "title_font": {"color": tokens["text"]},
        },
    }


def apply_theme(theme: str | None = None) -> None:
    """Apply safe CSS tokens for light/dark presentation without app logic changes."""
    selected_theme = theme or get_theme()
    tokens = get_theme_tokens(selected_theme)

    st.markdown(
        f"""
        <style>
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main {{
            background: {tokens["background"]};
            color: {tokens["text"]};
        }}
        .stApp {{
            background:
                radial-gradient(circle at top left, {tokens["surface_alt"]} 0, transparent 34rem),
                {tokens["background"]};
            color: {tokens["text"]};
        }}
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stAppToolbar"] {{
            background: {tokens["background"]};
            color: {tokens["text"]};
        }}
        header[data-testid="stHeader"] * {{
            color: {tokens["text"]};
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp p, .stApp li, .stApp label, .stApp span {{
            color: {tokens["text"]};
        }}
        .stApp [data-testid="stCaptionContainer"],
        .stApp .caption,
        .stApp small {{
            color: {tokens["muted"]};
        }}
        .block-container {{
            padding-top: 3rem;
            padding-bottom: 3rem;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {tokens["surface"]}, {tokens["background"]});
            border-right: 1px solid {tokens["border"]};
        }}
        section[data-testid="stSidebar"] * {{
            color: {tokens["muted"]};
        }}
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{
            color: {tokens["muted"]};
        }}
        section[data-testid="stSidebar"] a {{
            color: {tokens["muted"]};
            border-radius: 0.72rem;
            margin: 0.08rem 0;
            transition: background 120ms ease, color 120ms ease;
        }}
        section[data-testid="stSidebar"] a:hover {{
            background: {tokens["card_hover"]};
            color: {tokens["text"]};
        }}
        section[data-testid="stSidebar"] a[aria-current="page"] {{
            background: linear-gradient(90deg, rgba(167, 139, 250, 0.22), rgba(56, 189, 248, 0.08));
            color: {tokens["text"]};
            border: 1px solid {tokens["border"]};
        }}
        .fh-card {{
            border: 1px solid {tokens["border"]};
            border-radius: 0.85rem;
            padding: 1rem 1.1rem;
            background: linear-gradient(180deg, {tokens["card"]}, {tokens["surface"]});
            min-height: 128px;
            box-shadow: {tokens["shadow"]};
            transition: border-color 120ms ease, transform 120ms ease, background 120ms ease;
        }}
        .fh-card:hover {{
            background: {tokens["card_hover"]};
            border-color: {tokens["accent"]};
            transform: translateY(-1px);
        }}
        .fh-card h3 {{
            color: {tokens["text"]};
            font-size: 1.05rem;
            margin: 0 0 0.35rem 0;
        }}
        .fh-card p {{
            margin: 0;
            color: {tokens["muted"]};
            line-height: 1.45;
        }}
        .fh-kicker {{
            color: {tokens["accent"]};
            font-weight: 700;
            letter-spacing: .04em;
            text-transform: uppercase;
            font-size: .78rem;
            margin-bottom: .25rem;
        }}
        .fh-soft-divider {{
            margin: 1.2rem 0;
            border-top: 1px solid {tokens["border"]};
        }}
        div[data-testid="stMetric"] {{
            background: linear-gradient(180deg, {tokens["card"]}, {tokens["surface"]});
            border: 1px solid {tokens["border"]};
            border-radius: 0.85rem;
            padding: 0.85rem 1rem;
            box-shadow: {tokens["shadow"]};
        }}
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {{
            color: {tokens["muted"]};
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetric"] [data-testid="stMetricValue"] div {{
            color: {tokens["text"]};
            font-weight: 750;
        }}
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] input,
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"],
        [data-testid="stNumberInput"] div[data-baseweb="input"] > div,
        [data-testid="stNumberInput"] div[data-baseweb="base-input"],
        [data-testid="stNumberInput"] input,
        textarea,
        input {{
            background: {tokens["card"]} !important;
            color: {tokens["text"]} !important;
            border-color: {tokens["border"]} !important;
            caret-color: {tokens["accent_2"]};
        }}
        [data-testid="stNumberInput"] button,
        [data-testid="stNumberInput"] button svg,
        [data-baseweb="select"] svg {{
            color: {tokens["muted"]} !important;
            fill: {tokens["muted"]} !important;
        }}
        [data-testid="stNumberInput"] button:hover {{
            background: {tokens["card_hover"]} !important;
            border-color: {tokens["accent_2"]} !important;
        }}
        [data-baseweb="select"] > div:hover,
        div[data-baseweb="input"] > div:hover,
        div[data-baseweb="base-input"]:hover {{
            border-color: {tokens["accent_2"]} !important;
        }}
        [data-baseweb="select"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="base-input"]:focus-within {{
            border-color: {tokens["accent"]} !important;
            box-shadow: 0 0 0 1px {tokens["accent"]} !important;
        }}
        input::placeholder,
        textarea::placeholder {{
            color: {tokens["subtle"]} !important;
        }}
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        div[data-baseweb="menu"] ul,
        ul[role="listbox"],
        div[role="listbox"] {{
            background: {tokens["card"]} !important;
            border: 1px solid {tokens["border"]} !important;
            color: {tokens["text"]} !important;
            box-shadow: {tokens["shadow"]} !important;
        }}
        [role="option"],
        li[role="option"],
        div[role="option"],
        div[data-baseweb="menu"] li,
        div[data-baseweb="menu"] [role="option"] {{
            background: {tokens["card"]} !important;
            color: {tokens["text"]} !important;
        }}
        [role="option"] *,
        div[data-baseweb="menu"] * {{
            color: {tokens["text"]} !important;
        }}
        [role="option"][aria-selected="true"],
        [role="option"]:hover,
        [role="option"][data-highlighted="true"],
        div[data-baseweb="menu"] li:hover,
        div[data-baseweb="menu"] [role="option"]:hover {{
            background: {tokens["card_hover"]} !important;
            color: {tokens["text"]} !important;
        }}
        [data-testid="stExpander"] {{
            background: {tokens["card"]} !important;
            border: 1px solid {tokens["border"]} !important;
            border-radius: 0.85rem !important;
            overflow: hidden;
        }}
        [data-testid="stExpander"] > details,
        [data-testid="stExpander"] details,
        [data-testid="stExpander"] div,
        [data-testid="stExpanderDetails"],
        [data-testid="stExpander"] [data-testid="stVerticalBlock"],
        [data-testid="stExpander"] [data-testid="stHorizontalBlock"] {{
            background-color: transparent;
        }}
        [data-testid="stExpander"] summary {{
            background: linear-gradient(180deg, {tokens["card"]}, {tokens["surface"]}) !important;
            border-bottom: 1px solid {tokens["border"]} !important;
        }}
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary svg {{
            color: {tokens["text"]} !important;
            fill: {tokens["text"]} !important;
        }}
        [data-testid="stExpanderDetails"] {{
            background: {tokens["card"]} !important;
            color: {tokens["text"]} !important;
            border-top: 0 !important;
        }}
        [data-testid="stDataFrame"] {{
            border: 1px solid {tokens["border"]};
            border-radius: 0.85rem;
            overflow: hidden;
        }}
        [data-testid="stPlotlyChart"] {{
            background: {tokens["card"]};
            border: 1px solid {tokens["border"]};
            border-radius: 0.85rem;
            overflow: hidden;
        }}
        div[data-testid="stAlert"] {{
            border-radius: 0.85rem;
            border-color: {tokens["warning_border"]};
            background: {tokens["warning_bg"]};
        }}
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {{
            color: {tokens["warning_text"]};
        }}
        button[kind="primary"], div[data-testid="stButton"] button {{
            border-radius: 0.7rem;
            background: linear-gradient(90deg, {tokens["accent"]}, {tokens["accent_2"]});
            border: 1px solid {tokens["border"]};
            color: #FFFFFF;
        }}
        div[data-testid="stButton"] button:hover {{
            border-color: {tokens["accent_2"]};
            filter: brightness(1.05);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
