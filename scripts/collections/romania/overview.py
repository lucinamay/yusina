"""One row per Romania palette: the object it was sampled from, its swatches, and plots.

    python scripts/collections/romania/overview.py   # -> gallery/collections/romania/overview.png
"""

from _sheet import overview

ROWS = [  # palette, asset, crop (l, t, r, b) or None, credit
    ("Bucovina", "voronet_last_judgement_ccbysa20.jpg", (0, 0.12, 1, 1), "Voroneț. Alastair Rae, Wikimedia Commons, CC BY-SA 2.0"),
    ("Horezu", "horezu_plates_ccbysa30.jpg", (0, 0, 1, 0.55), "Bogdan29roman, Wikimedia Commons, CC BY-SA 3.0"),
    ("Maramures", "maramures_zgardan_ccbysa40.jpg", None, "CEllen, Wikimedia Commons, CC BY-SA 4.0"),
    ("Oltenia", "oltenia_carpet_detail_ccbysa40.jpg", None, "Joe Mabel, Wikimedia Commons, CC BY-SA 4.0"),
    ("Sapanta", "sapanta_crosses_ccbysa30.jpg", (0.55, 0.38, 0.85, 0.95), "Andrei Stroe, Wikimedia Commons, CC BY-SA 3.0"),
    ("Zagar", "zagar_saxon_dresser_ccbysa30ro.jpg", (0.3, 0.1, 0.85, 0.95), "Țetcu Mircea Rareș, Wikimedia Commons, CC BY-SA 3.0 ro"),
]

if __name__ == "__main__":
    overview(ROWS, "Romania · the six palettes and the objects they were sampled from")
