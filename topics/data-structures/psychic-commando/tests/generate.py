"""Generate deterministic test inputs; optionally run a locally compiled reference."""
import argparse
import json
import subprocess
from pathlib import Path

MASK = (1 << 64) - 1

class SplitMix64:
    def __init__(self, seed):
        self.state = seed & MASK

    def next(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK
        value = self.state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK
        return value ^ (value >> 31)

    def between(self, low, high):
        return low + self.next() % (high - low + 1)


def make_case(spec, output):
    rng = SplitMix64(spec['seed'])
    xmin, ymin = spec['origin']
    width, height = spec['span']
    xmax, ymax = xmin + width, ymin + height
    m = spec['m']
    updates = []
    queries = []
    operations = []
    for i in range(m):
        op = 0 if i % 3 == 0 or i + 1 == m else (1 if i % 3 == 1 else 2)
        if op == 1:
            x = rng.between(xmin - 10, xmax + 10)
            y = rng.between(ymin - 10, ymax + 10)
            radius = (1, 2, 3, 10**8, rng.between(1, 1000))[i % 5]
            power = rng.between(0, 10000)
            current = [1, x, y, radius, power]
        else:
            if i % 9 == 0:
                x1, y1, x2, y2 = xmin, ymin, xmax, ymax
            elif i % 9 == 3:
                x1 = x2 = rng.between(xmin, xmax)
                y1 = y2 = rng.between(ymin, ymax)
            else:
                x1, x2 = sorted((rng.between(xmin - 10, xmax + 10), rng.between(xmin - 10, xmax + 10)))
                y1, y2 = sorted((rng.between(ymin - 10, ymax + 10), rng.between(ymin - 10, ymax + 10)))
            current = [op, x1, y1, x2, y2]
            if op == 2:
                current.append(rng.between(0, 10000))
        operations.append(current)
        (queries if op == 0 else updates).append(current)
    if spec.get('offline'):
        operations = updates + queries
    if spec.get('outside'):
        operations[:5] = [[1, xmin - 100, ymin - 100, 1, 9999],
                          [0, xmin - 5, ymin - 5, xmin - 1, ymin - 1],
                          [2, xmin - 5, ymin - 5, xmax + 5, ymax + 5, 10000],
                          [1, xmin, ymin, 2, 3], [0, xmin, ymin, xmax, ymax]]
    output.write(f'{m} {xmin} {ymin} {xmax} {ymax}\n')
    for current in operations:
        output.write(' '.join(map(str, current)) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--std", type=Path)
    parser.add_argument("--case")
    args = parser.parse_args()
    plan = json.loads((Path(__file__).parent / "plan.json").read_text(encoding="utf-8"))
    cases = [spec for spec in plan["cases"] if args.case is None or spec["id"] == args.case]
    if not cases:
        parser.error("unknown case id")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in cases:
        input_path = args.out_dir / (spec["id"] + ".in")
        with input_path.open("w", encoding="utf-8", newline="\n") as output:
            make_case(spec, output)
        if args.std is not None:
            with input_path.open("rb") as source, input_path.with_suffix(".out").open("wb") as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(input_path)

if __name__ == "__main__":
    main()
