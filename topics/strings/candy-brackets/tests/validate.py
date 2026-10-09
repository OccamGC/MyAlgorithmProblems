"""Validate one Candy Brackets input and its optional scoring group."""
import argparse
import json
from pathlib import Path


def validate(text, group=None):
    rows = text.splitlines()
    assert len(rows) >= 3, "missing initial type/value lines"
    n, m = map(int, rows[0].split())
    assert 0 <= n <= 10**6 and 0 <= m <= 10**6 and len(rows) == m + 3
    types = list(map(int, rows[1].split()))
    weights = list(map(int, rows[2].split()))
    assert len(types) == len(weights) == n
    assert all(kind in (0, 1, 2) for kind in types)
    assert all(-4 * 10**9 <= w <= 4 * 10**9 for w in weights)
    minimum = min(weights, default=0)
    maximum = max(weights, default=0)
    negative = sum(w < 0 for w in weights)
    brackets = sum(kind != 2 for kind in types)
    for row in rows[3:]:
        side, kind, weight = map(int, row.split())
        assert side in (0, 1) and kind in (0, 1, 2)
        assert -4 * 10**9 <= weight <= 4 * 10**9
        minimum = min(minimum, weight)
        maximum = max(maximum, weight)
        negative += weight < 0
        brackets += kind != 2
    assert group in (None, 1, 2, 3, 4)
    if group == 1:
        assert n + m <= 100
    if group == 2:
        assert minimum >= 0
    if group == 3:
        assert brackets == 0
    return dict(N=n, M=m, minimum_weight=minimum, maximum_weight=maximum,
                negative_elements=negative, bracket_elements=brackets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--group", type=int, choices=(1, 2, 3, 4))
    args = parser.parse_args()
    print(json.dumps(validate(args.input.read_text(encoding="ascii"), args.group)))
