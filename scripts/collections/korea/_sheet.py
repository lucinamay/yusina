"""Korea collection: Hangul fallback font, Gowun Batang titles, ko before en."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheet import *
from sheet import configure

configure("korea", langs=("ko", "en"), serif=["Gowun Batang", "Apple SD Gothic Neo"], fallback="Apple SD Gothic Neo",
          references=("korea", "korea_pigments"))

