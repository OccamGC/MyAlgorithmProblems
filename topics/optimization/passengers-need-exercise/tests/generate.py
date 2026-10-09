"""Regenerate passengers-need-exercise inputs; optionally run a compiled reference program."""

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
    L, M, N = spec["L"], spec["M"], spec["N"]
    if not (1 <= L <= 1_000_000_000 and 1 <= M <= 300 and 1 <= N <= min(300, L + 1)):
        raise ValueError("case exceeds the statement bounds")
    rng = SplitMix64(spec["seed"])
    if spec["kind"] == "tie":
        passengers = [0, 2, 5, 8, 10]
        doors = [0, 2, 4]
    elif spec["kind"] == "half-integer":
        assert L == M == N == 300
        passengers = list(range(M))
        doors = list(range(N))
    else:
        passengers = sorted(rng.between(0, L) for _ in range(M))
        door_set = {0}
        while len(door_set) < N:
            if spec["kind"] == "uneven" and len(door_set) < N // 2:
                door_set.add(rng.between(1, min(L, 10_000)))
            else:
                door_set.add(rng.between(1, L))
        doors = sorted(door_set)
    assert len(passengers) == M and len(doors) == N
    output.write(f"{L}\n{M}\n")
    output.write(" ".join(map(str, passengers)) + "\n")
    output.write(f"{N}\n")
    if N > 1:
        output.write(" ".join(map(str, doors[1:])) + "\n")


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
