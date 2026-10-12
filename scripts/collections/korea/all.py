"""All Korea sheets stacked into one image per language.

    python scripts/collections/korea/all.py   # -> gallery/collections/korea/korea[_<lang>].png (renders the sheets first)
"""

import subprocess
import sys
from pathlib import Path

from _sheet import combine

STEMS = ['dancheong', 'irworobongdo', 'minhwa', 'embroidery']

if __name__ == "__main__":
    here = Path(__file__).parent
    for stem in STEMS:
        subprocess.run([sys.executable, str(here / f"{stem}.py"), "all"], check=True)
    combine(STEMS, "korea")
