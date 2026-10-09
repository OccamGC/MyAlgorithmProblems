"""Validate one input file."""
from pathlib import Path
import sys
from generate import validate
validate(Path(sys.argv[1]).read_text("utf-8"))
