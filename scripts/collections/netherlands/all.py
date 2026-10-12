"""All Netherlands sheets stacked into one image per language.

    python scripts/collections/netherlands/all.py   # -> gallery/collections/netherlands/netherlands[_<lang>].png (renders the sheets first)
"""

import subprocess
import sys
from pathlib import Path

from _sheet import combine

STEMS = ['vangogh', 'nuenen', 'vermeer', 'destijl', 'delft']

if __name__ == "__main__":
    here = Path(__file__).parent
    for stem in STEMS:
        subprocess.run([sys.executable, str(here / f"{stem}.py"), "all"], check=True)
    combine(STEMS, "netherlands")
