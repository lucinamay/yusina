"""One row per Netherlands palette: the object it was sampled from, its swatches, and plots.

    python scripts/collections/netherlands/overview.py   # -> gallery/collections/netherlands/overview.png
"""

from _sheet import overview

ROWS = [  # palette, asset, crop (l, t, r, b) or None, credit
    ("VanGogh", "vangogh_bedroom_pd.jpg", None, "De slaapkamer, 1888. Van Gogh Museum; Wikimedia Commons, public domain"),
    ("Nuenen", "vangogh_potato_eaters_pd.jpg", None, "De aardappeleters, 1885. Van Gogh Museum; Wikimedia Commons, public domain"),
    ("DeStijl", "mondrian_composition_ii_1930_pd.jpg", None, "Mondriaan, Compositie II, 1930. Wikimedia Commons, public domain"),
    ("Vermeer", "vermeer_milkmaid_pd.jpg", (0.25, 0.2, 0.9, 0.9), "Het melkmeisje, c. 1660. Rijksmuseum; Wikimedia Commons, public domain"),
]

if __name__ == "__main__":
    overview(ROWS, "Netherlands · the four palettes and the objects they were sampled from")
