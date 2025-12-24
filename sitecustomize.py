#The goal of this file is to set a custom location for Python's __pycache__ directory, so it doesn't clutter the source directories.

import sys
import os
from pathlib import Path

try:
    prefix = Path(__file__).resolve().parent / "out_pycache"
    prefix.mkdir(parents=True, exist_ok=True)
    sys.pycache_prefix = str(prefix)
except Exception:
    pass