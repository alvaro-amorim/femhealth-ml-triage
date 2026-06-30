"""Tests for lightweight UI presentation helpers."""

import pytest

from src.data.schema import FEATURE_NAMES
from src.ui.feature_dictionary import (
    FEATURE_DICTIONARY,
    get_feature_entry,
    get_feature_help,
    translate_feature_name,
)
from src.ui.i18n import t, translate_group_name, translate_target_label
from src.ui import theme
from src.ui.theme import DARK_THEME, LIGHT_THEME, THEME_OPTIONS, get_plotly_layout, get_theme_tokens, set_theme


def test_i18n_translates_navigation_and_targets() -> None:
    assert t("nav.home", "pt") == "Início"
    assert t("nav.home", "en") == "Home"
    assert translate_target_label(0, "pt") == "Maligno (0)"
    assert translate_target_label(1, "en") == "Benign (1)"


def test_i18n_translates_feature_groups() -> None:
    assert translate_group_name("mean", "pt") == "Medidas médias"
    assert translate_group_name("error", "pt") == "Variações das medidas"
    assert translate_group_name("worst", "en") == "Largest observed values"


def test_feature_dictionary_covers_all_canonical_features() -> None:
    assert set(FEATURE_DICTIONARY) == set(FEATURE_NAMES)
    assert len(FEATURE_DICTIONARY) == 30


def test_feature_dictionary_preserves_technical_name_and_adds_friendly_labels() -> None:
    entry = get_feature_entry("mean radius")

    assert entry["technical_name"] == "mean radius"
    assert translate_feature_name("mean radius", "pt") == "Raio médio"
    assert translate_feature_name("worst texture", "pt") == "Maior textura observada"
    assert translate_feature_name("radius error", "en") == "Radius variation"
    assert "Technical WDBC name: mean radius" in get_feature_help("mean radius", "en")


def test_theme_rejects_invalid_values() -> None:
    assert set(THEME_OPTIONS) == {"light", "dark"}
    with pytest.raises(ValueError):
        set_theme("contrast")


def test_theme_tokens_cover_light_and_dark_modes() -> None:
    required_tokens = {
        "background",
        "surface",
        "card",
        "card_hover",
        "border",
        "text",
        "muted",
        "accent",
        "accent_2",
        "warning_bg",
        "warning_text",
        "info_bg",
        "success_bg",
    }

    assert required_tokens.issubset(LIGHT_THEME)
    assert required_tokens.issubset(DARK_THEME)
    assert get_theme_tokens("dark")["card"] != "#FFFFFF"
    assert get_theme_tokens("dark")["text"] != get_theme_tokens("dark")["background"]


def test_plotly_layout_uses_theme_tokens() -> None:
    layout = get_plotly_layout("dark")

    assert layout["paper_bgcolor"] == DARK_THEME["card"]
    assert layout["plot_bgcolor"] == DARK_THEME["card"]
    assert layout["font"]["color"] == DARK_THEME["text"]
    assert "xaxis" in layout
    assert "yaxis" in layout


def test_apply_theme_outputs_core_dark_mode_selectors(monkeypatch) -> None:
    rendered_css = {}

    def _capture_markdown(content: str, **_kwargs) -> None:
        rendered_css["content"] = content

    monkeypatch.setattr(theme.st, "markdown", _capture_markdown)

    theme.apply_theme("dark")

    css = rendered_css["content"]
    assert 'html, body' in css
    assert '[data-testid="stAppViewContainer"]' in css
    assert 'header[data-testid="stHeader"]' in css
    assert 'section[data-testid="stSidebar"]' in css
    assert 'div[data-baseweb="select"]' in css
    assert 'div[data-baseweb="popover"]' in css
    assert 'div[data-baseweb="menu"]' in css
    assert '[role="option"]' in css
    assert '[data-testid="stNumberInput"]' in css
    assert 'div[data-testid="stMetric"]' in css
    assert '[data-testid="stExpanderDetails"]' in css
    assert '[data-testid="stPlotlyChart"]' in css
    assert '.js-plotly-plot' not in css
    assert '.plot-container' not in css
    assert '.svg-container' not in css
    assert '.main-svg' not in css
    assert 'rect.bg' not in css
    assert DARK_THEME["background"] in css
