"""Generate reproducible signed-weight Candy Brackets inputs (standard library)."""
import argparse
import json
import random
import subprocess
from pathlib import Path

LIMIT = 4_000_000_000


def generate(case):
    rng = random.Random(case["seed"])
    n, m = case["n"], case["m"]
    mode = case["mode"]
    weights = case.get("weights", "signed")

    def value(index):
        if weights == "positive":
            return rng.choice((0, 1, LIMIT, rng.randrange(LIMIT + 1)))
        if weights == "maximum":
            return LIMIT
        if weights == "negative":
            return -LIMIT
        if weights == "zero":
            return 0
        if weights == "alternating":
            return (-LIMIT, LIMIT, LIMIT, -LIMIT, -1, 0, 1)[index % 7]
        if weights == "extremes":
            return rng.choice((-LIMIT, -1, 0, 1, LIMIT))
        if weights == "signed":
            return rng.randrange(-LIMIT, LIMIT + 1)
        raise ValueError("unknown weight mode: " + weights)

    if mode == "manual":
        initial = case["initial"]
        operations = case["operations"]
        assert len(initial) == n and len(operations) == m
        types = [item[0] for item in initial]
        values = [item[1] for item in initial]
    else:
        if mode == "nested":
            types = [0] * (n // 2) + [1] * (n - n // 2)
        elif mode == "unmatched":
            types = [1] * (n // 2) + [0] * (n - n // 2)
        elif mode in ("candy", "wrap"):
            types = [2] * n
        elif mode == "close":
            types = [0] * n
        elif mode == "atoms":
            pattern = (2, 0, 2, 1, 0, 1, 2, 2)
            types = [pattern[i % len(pattern)] for i in range(n)]
        elif mode == "random":
            types = [rng.randrange(3) for _ in range(n)]
        else:
            raise ValueError("unknown mode: " + mode)
        values = [value(i) for i in range(n)]
        operations = None

    rows = [f"{n} {m}", " ".join(map(str, types)), " ".join(map(str, values))]
    for i in range(m):
        if operations is not None:
            side, kind, weight = operations[i]
        else:
            if mode == "close":
                side, kind = 1, 1
            elif mode == "candy":
                side, kind = i % 2, 2
            elif mode == "unmatched":
                side = i % 2
                kind = 1 - side
            elif mode in ("wrap", "nested"):
                side = i % 2
                kind = side
            elif mode == "atoms":
                side = (i // 8) % 2
                kind = (2, 0, 2, 1, 0, 1, 2, 2)[i % 8]
                if side == 0 and kind != 2:
                    kind = 1 - kind
            else:
                side, kind = rng.randrange(2), rng.randrange(3)
            weight = value(n + i)
        rows.append(f"{side} {kind} {weight}")
    return "\n".join(rows) + "\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    selected = set(args.case or [case['id'] for case in plan['cases']])
    unknown = selected - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if case['id'] not in selected:
            continue
        path = args.out_dir / (case['id'] + '.in')
        path.write_text(generate(case), encoding='ascii', newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())], stdin=source,
                                        stdout=subprocess.PIPE, check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n', b'\n'))

if __name__ == '__main__':
    main()
