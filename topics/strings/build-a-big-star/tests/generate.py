"""Regenerate big-star cases; optionally run a compiled std.cpp."""

import argparse
import json
import subprocess
from pathlib import Path

MASK = (1 << 64) - 1
MARKS = "<>*"


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
    n, m = spec["n"], spec["m"]
    if not (0 <= n <= 1_000_000 and 0 <= m <= 1_000_000):
        raise ValueError("case exceeds the statement bounds")
    rng = SplitMix64(spec["seed"])
    output.write(f"{n} {m}\n")
    for index in range(n):
        mark = MARKS[rng.between(0, 2)]
        if spec["kind"] == "blocks":
            mark = MARKS[(index // 1000) % 3]
        output.write(mark + ("\n" if index + 1 == n else " "))
    if n == 0:
        output.write("\n")

    for index in range(m):
        if spec["kind"] == "alternating":
            side = 1 + index % 2
            mark = MARKS[(index // 2) % 3]
        elif spec["kind"] == "blocks":
            side = 1 + (index // 1000) % 2
            mark = MARKS[(index // 1000) % 3]
        else:
            side = rng.between(1, 2)
            mark = MARKS[rng.between(0, 2)]
        output.write(f"{side} {mark}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--std", type=Path, help="path to a locally compiled reference program")
    parser.add_argument("--case", help="generate only the named case")
    args = parser.parse_args()

    plan = json.loads((Path(__file__).parent / "plan.json").read_text(encoding="utf-8"))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in plan["cases"]:
        if args.case and spec["id"] != args.case:
            continue
        input_path = args.out_dir / (spec["id"] + ".in")
        with input_path.open("w", encoding="ascii", newline="\n") as output:
            make_case(spec, output)
        if args.std is not None:
            with input_path.open("rb") as source, (args.out_dir / (spec["id"] + ".out")).open("wb") as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(input_path)


if __name__ == "__main__":
    main()
