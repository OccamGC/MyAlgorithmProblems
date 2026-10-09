"""Validate one input and optionally its scoring-group constraints."""
import argparse
from pathlib import Path
from generate import validate

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("input", type=Path)
parser.add_argument("--group", type=int, choices=[1, 2, 3, 4])
args = parser.parse_args()
try:
    games = validate(args.input.read_text(encoding="utf-8"), args.group)
except (AssertionError, ValueError, IndexError) as error:
    parser.error(str(error))
print(f"valid: {len(games)} games")
