"""Romania collection: ro before en, Open Sans covers the diacritics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheet import *
from sheet import configure

configure("romania", langs=("ro", "en"), references=("korea_pigments", "romania_pigments"))

