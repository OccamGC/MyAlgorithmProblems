"""Validate a two-household input, also under python -O."""
from pathlib import Path
import sys
from generate import validate

validate(Path(sys.argv[1]).read_text(encoding='utf-8'))
