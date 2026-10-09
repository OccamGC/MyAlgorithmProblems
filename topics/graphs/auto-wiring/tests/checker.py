"""Check a vertex cover against the trusted optimum: input answer output."""
import argparse
from pathlib import Path
import re
import sys


def check(input_path, answer_path, output_path):
    values = list(map(int, input_path.read_bytes().split()))
    n, m = values[:2]
    assert len(values) == 2+n+2*m, 'invalid judge input'
    tokens = output_path.read_bytes().split()
    if not tokens or any(re.fullmatch(rb'[0-9]+', t) is None for t in tokens):
        return False, 'Expected nonnegative integers.'
    count = int(tokens[0])
    if count > n or len(tokens) != count+1:
        return False, 'Wrong number of vertex IDs.'
    chosen = list(map(int, tokens[1:]))
    if len(set(chosen)) != count or any(v < 1 or v > n for v in chosen):
        return False, 'IDs must be distinct and in range.'
    optimum = int(answer_path.read_bytes().split()[0])
    if count != optimum:
        return False, 'The cover size is not optimal.'
    chosen = set(chosen)
    edges = values[2+n:]
    if any(u not in chosen and v not in chosen for u, v in zip(edges[::2], edges[1::2])):
        return False, 'An edge is uncovered.'
    return True, 'Accepted.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('answer', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    accepted, message = check(args.input, args.answer, args.output)
    print(message)
    return 0 if accepted else 1


if __name__ == '__main__':
    sys.exit(main())
