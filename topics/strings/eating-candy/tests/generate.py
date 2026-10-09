"""Regenerate inputs from plan.json; optionally run a locally compiled std.cpp."""

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


def bits(length, rng):
    result = bytearray(length)
    for index in range(length):
        result[index] = 48 + (rng.next() & 1)
    return result


def make_case(spec, output):
    rng = SplitMix64(spec["seed"])
    kind = spec["kind"]
    length = spec["length"]
    if kind == "empty":
        patterns = []
        text = b"0" * length
    elif kind == "repeat":
        patterns = [b"0", b"00", b"01", b"0"]
        text = b"0" * length
    elif kind == "suffix":
        assert length % 4 == 0
        patterns = [b"1101", b"10", b"10"]
        text = b"1100" * (length // 4)
    elif kind == "prefix":
        patterns = [b"0" * index + b"1" for index in range(1, spec["count"] + 1)]
        text = b"0" * length
    elif kind == "random":
        patterns = []
        total = 0
        for _ in range(spec["count"]):
            size = rng.between(spec["min_pattern"], spec["max_pattern"])
            total += size
            if total > 5_000_000:
                raise ValueError("total pattern length exceeds the statement bound")
            patterns.append(bits(size, rng))
        text = bits(length, rng)
    else:
        raise ValueError(f"unknown case kind: {kind}")

    if not (1 <= length <= 5_000_000 and len(patterns) <= 100_000):
        raise ValueError("case exceeds the statement bounds")
    output.write(f"{len(patterns)}\n".encode("ascii"))
    output.write(text)
    output.write(b"\n")
    for pattern in patterns:
        output.write(pattern)
        output.write(b"\n")


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
        with input_path.open("wb") as output:
            make_case(spec, output)
        if args.std is not None:
            with input_path.open("rb") as source, (args.out_dir / (spec["id"] + ".out")).open("wb") as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(input_path)


if __name__ == "__main__":
    main()
