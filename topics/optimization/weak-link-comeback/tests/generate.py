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
    n, kind = spec["n"], spec["kind"]
    assert 1 <= n <= 1_000_000
    rng = SplitMix64(spec["seed"])
    def values(is_a):
        for i in range(n):
            if kind == "single":
                yield 2 if is_a else -3
            elif kind == "product":
                yield -1_000_000
            elif kind == "ties":
                yield -7 if is_a else (100 if i % 2 else -101)
            elif kind == "zeros" and is_a:
                yield 0
            elif kind == "monotone" and is_a:
                yield i - n // 2
            else:
                yield rng.between(-1_000_000, 1_000_000)
    output.write(str(n) + "\n")
    for is_a in (True, False):
        # Bounded batches avoid holding a million formatted integers at once.
        chunk = []
        for i, value in enumerate(values(is_a)):
            chunk.append(str(value))
            if len(chunk) == 4096 or i + 1 == n:
                output.write(" ".join(chunk) + ("\n" if i + 1 == n else " "))
                chunk.clear()

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
        with input_path.open("w", encoding="ascii", newline="\n") as output:
            make_case(spec, output)
        if args.std is not None:
            with input_path.open("rb") as source, input_path.with_suffix(".out").open("wb") as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(input_path)

if __name__ == "__main__":
    main()
