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
    n, m, kind = spec['n'], spec['m'], spec['kind']
    if kind == 'sample':
        output.write((Path(__file__).parent / 'samples' / (spec['sample'] + '.in')).read_text(encoding='ascii'))
        return
    grid = []
    for x in range(n):
        row = []
        for y in range(m):
            if kind == 'checkerboard':
                value = 'B' if (x+y)%2 else 'S'
            elif kind == 'corridor':
                value = 'E'
            elif kind == 'open':
                value = 'S'
            elif kind == 'no-start':
                value = 'B' if rng.between(0, 2)==0 else 'E'
            elif kind == 'no-trap':
                value = 'B' if rng.between(0, 2)==0 else 'S'
            else:
                value = 'B' if rng.between(0, 99)<spec.get('obstacle_percent', 40) else 'S'
            row.append(value)
        grid.append(row)
    if kind not in ('no-trap',):
        grid[-1][-1] = 'T'
    if spec.get('single_start'):
        grid = [['E' if c=='S' else c for c in row] for row in grid]
    if kind != 'no-start':
        grid[0][0] = 'S'
    if spec.get('many_traps'):
        for _ in range(20):
            grid[rng.between(0,n-1)][rng.between(0,m-1)] = 'T'
    output.write(f'{n} {m}\n' + '\n'.join(''.join(row) for row in grid) + '\n')

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
