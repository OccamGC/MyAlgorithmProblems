"""Validate one input; checks remain enabled under python -O."""
from pathlib import Path
import sys
from generate import validate

validate(Path(sys.argv[1]).read_text(encoding="utf-8"))
