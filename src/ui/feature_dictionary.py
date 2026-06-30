"""Dicionário didático de exibição das features WDBC."""

from __future__ import annotations

from src.data.schema import FEATURE_GROUPS, FEATURE_NAMES
from src.ui.i18n import get_language


_BASE_DESCRIPTIONS_PT = {
    "radius": "raio calculado nas medições celulares",
    "texture": "variação de intensidade dos pixels na amostra tabular",
    "perimeter": "perímetro calculado nas medições celulares",
    "area": "área calculada nas medições celulares",
    "smoothness": "suavidade estimada do contorno nas medições",
    "compactness": "compactação estimada a partir de perímetro e área",
    "concavity": "concavidade estimada do contorno",
    "concave points": "pontos côncavos identificados no contorno",
    "symmetry": "simetria estimada nas medições",
    "fractal dimension": "dimensão fractal estimada do contorno",
}

_BASE_DESCRIPTIONS_EN = {
    "radius": "radius calculated from the tabular cell measurements",
    "texture": "pixel-intensity variation in the tabular sample",
    "perimeter": "perimeter calculated from the cell measurements",
    "area": "area calculated from the cell measurements",
    "smoothness": "estimated contour smoothness in the measurements",
    "compactness": "compactness estimated from perimeter and area",
    "concavity": "estimated contour concavity",
    "concave points": "concave points identified in the contour",
    "symmetry": "estimated symmetry in the measurements",
    "fractal dimension": "estimated fractal dimension of the contour",
}

_BASE_LABELS_PT = {
    "radius": "Raio",
    "texture": "Textura",
    "perimeter": "Perímetro",
    "area": "Área",
    "smoothness": "Suavidade",
    "compactness": "Compactação",
    "concavity": "Concavidade",
    "concave points": "Pontos côncavos",
    "symmetry": "Simetria",
    "fractal dimension": "Dimensão fractal",
}

_MEAN_LABELS_PT = {
    "radius": "Raio médio",
    "texture": "Textura média",
    "perimeter": "Perímetro médio",
    "area": "Área média",
    "smoothness": "Suavidade média",
    "compactness": "Compactação média",
    "concavity": "Concavidade média",
    "concave points": "Pontos côncavos médios",
    "symmetry": "Simetria média",
    "fractal dimension": "Dimensão fractal média",
}

_ERROR_LABELS_PT = {
    "radius": "Variação do raio",
    "texture": "Variação da textura",
    "perimeter": "Variação do perímetro",
    "area": "Variação da área",
    "smoothness": "Variação da suavidade",
    "compactness": "Variação da compactação",
    "concavity": "Variação da concavidade",
    "concave points": "Variação dos pontos côncavos",
    "symmetry": "Variação da simetria",
    "fractal dimension": "Variação da dimensão fractal",
}

_WORST_LABELS_PT = {
    "radius": "Maior raio observado",
    "texture": "Maior textura observada",
    "perimeter": "Maior perímetro observado",
    "area": "Maior área observada",
    "smoothness": "Maior suavidade observada",
    "compactness": "Maior compactação observada",
    "concavity": "Maior concavidade observada",
    "concave points": "Maior número de pontos côncavos",
    "symmetry": "Maior simetria observada",
    "fractal dimension": "Maior dimensão fractal observada",
}

_BASE_LABELS_EN = {
    "radius": "Radius",
    "texture": "Texture",
    "perimeter": "Perimeter",
    "area": "Area",
    "smoothness": "Smoothness",
    "compactness": "Compactness",
    "concavity": "Concavity",
    "concave points": "Concave points",
    "symmetry": "Symmetry",
    "fractal dimension": "Fractal dimension",
}


def _split_feature(feature_name: str) -> tuple[str, str]:
    if feature_name.startswith("mean "):
        return "mean", feature_name.removeprefix("mean ")
    if feature_name.endswith(" error"):
        return "error", feature_name.removesuffix(" error")
    if feature_name.startswith("worst "):
        return "worst", feature_name.removeprefix("worst ")
    raise ValueError(f"Unsupported WDBC feature: {feature_name}")


def _group_for_feature(feature_name: str) -> str:
    for group_name, features in FEATURE_GROUPS.items():
        if feature_name in features:
            return group_name
    raise ValueError(f"Feature not found in canonical WDBC groups: {feature_name}")


def _label_pt(feature_name: str) -> str:
    prefix, base = _split_feature(feature_name)
    if prefix == "mean":
        return _MEAN_LABELS_PT[base]
    if prefix == "error":
        return _ERROR_LABELS_PT[base]
    return _WORST_LABELS_PT[base]


def _label_en(feature_name: str) -> str:
    prefix, base = _split_feature(feature_name)
    base_label = _BASE_LABELS_EN[base]
    if prefix == "mean":
        return f"Mean {base_label.lower()}"
    if prefix == "error":
        return f"{base_label} variation"
    return f"Largest observed {base_label.lower()}"


def _description_pt(feature_name: str) -> str:
    prefix, base = _split_feature(feature_name)
    base_description = _BASE_DESCRIPTIONS_PT[base]
    if prefix == "mean":
        return f"Média do {base_description}."
    if prefix == "error":
        return f"Variação estimada do {base_description}."
    return f"Maior valor observado para {base_description}."


def _description_en(feature_name: str) -> str:
    prefix, base = _split_feature(feature_name)
    base_description = _BASE_DESCRIPTIONS_EN[base]
    if prefix == "mean":
        return f"Mean value of the {base_description}."
    if prefix == "error":
        return f"Estimated variation of the {base_description}."
    return f"Largest observed value for the {base_description}."


FEATURE_DICTIONARY: dict[str, dict[str, str]] = {
    feature_name: {
        "technical_name": feature_name,
        "display_name_pt": _label_pt(feature_name),
        "display_name_en": _label_en(feature_name),
        "group": _group_for_feature(feature_name),
        "description_pt": _description_pt(feature_name),
        "description_en": _description_en(feature_name),
    }
    for feature_name in FEATURE_NAMES
}


def get_feature_entry(feature_name: str) -> dict[str, str]:
    """Return the didactic dictionary entry for a canonical WDBC feature."""
    try:
        return FEATURE_DICTIONARY[feature_name]
    except KeyError as exc:
        raise ValueError(f"Unknown WDBC feature: {feature_name}") from exc


def translate_feature_name(feature_name: str, language: str | None = None) -> str:
    """Return a friendly feature label in the selected language."""
    entry = get_feature_entry(feature_name)
    selected_language = language or get_language()
    if selected_language == "en":
        return entry["display_name_en"]
    return entry["display_name_pt"]


def get_feature_help(feature_name: str, language: str | None = None) -> str:
    """Return a concise tooltip/description while preserving the technical name."""
    entry = get_feature_entry(feature_name)
    selected_language = language or get_language()
    description = entry["description_en"] if selected_language == "en" else entry["description_pt"]
    return f"{description} Technical WDBC name: {entry['technical_name']}"


def build_feature_dictionary_table(language: str | None = None) -> list[dict[str, str]]:
    """Return a serializable table with friendly and technical feature names."""
    selected_language = language or get_language()
    return [
        {
            "Atributo" if selected_language == "pt" else "Attribute": translate_feature_name(
                feature_name, selected_language
            ),
            "Nome técnico" if selected_language == "pt" else "Technical name": feature_name,
            "Grupo" if selected_language == "pt" else "Group": entry["group"],
            "Descrição" if selected_language == "pt" else "Description": (
                entry["description_en"] if selected_language == "en" else entry["description_pt"]
            ),
        }
        for feature_name, entry in FEATURE_DICTIONARY.items()
    ]
