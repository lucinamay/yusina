"""All Romania sheets stacked into one image per language.

    python scripts/collections/romania/all.py   # -> gallery/collections/romania/romania[_<lang>].png (renders the sheets first)
"""

import subprocess
import sys
from pathlib import Path

from _sheet import combine

STEMS = ['frescoes', 'horezu', 'maramures', 'oltenia', 'sapanta', 'zagar']

if __name__ == "__main__":
    here = Path(__file__).parent
    for stem in STEMS:
        subprocess.run([sys.executable, str(here / f"{stem}.py"), "all"], check=True)
    combine(STEMS, "romania")
