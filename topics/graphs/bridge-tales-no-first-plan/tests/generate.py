"""Regenerate connected graphs; optionally run a locally compiled std.cpp."""

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
    if spec["kind"] == "second-distinct":
        output.write("3 3\n1 2 1\n2 3 2\n1 3 2\n")
        return
    if spec["kind"] == "equal-cycle":
        output.write("3 4\n1 2 1\n2 3 1\n1 3 1\n1 2 3\n")
        return

    n, m = spec["n"], spec["m"]
    if not (2 <= n <= 100_000 and n <= m <= 200_000):
        raise ValueError("case exceeds the statement bounds")
    rng = SplitMix64(spec["seed"])
    output.write(f"{n} {m}\n")
    for vertex in range(2, n + 1):
        parent = vertex - 1 if spec["kind"] == "chain" else rng.between(1, vertex - 1)
        weight = 1 if spec["kind"] == "chain" else rng.between(1, 1000)
        output.write(f"{parent} {vertex} {weight}\n")

    # Vertex 2 is connected to 1 by a cheaper tree edge. This extra edge
    # guarantees a spanning tree strictly heavier than the minimum.
    output.write("1 2 5000\n")
    # In the chain case every extra edge must cost more than a chain edge.
    minimum_weight = 2 if spec["kind"] == "chain" else 1
    for _ in range(m - n):
        u = rng.between(1, n)
        v = rng.between(1, n - 1)
        if v >= u:
            v += 1
        output.write(f"{u} {v} {rng.between(minimum_weight, 5000)}\n")


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
