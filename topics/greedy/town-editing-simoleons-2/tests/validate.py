"""Validate one input file; exits unsuccessfully on an invalid input."""
from pathlib import Path
import sys
from generate import validate

validate(Path(sys.argv[1]).read_text(encoding='utf-8'))
