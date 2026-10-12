"""Netherlands collection: nl before en."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheet import *
from sheet import configure

configure("netherlands", langs=("nl", "en"), references=("korea_pigments", "netherlands_pigments"))
