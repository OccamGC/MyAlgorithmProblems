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


def expected_value(n, edges, damage, probabilities, cuts):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    best = 0.0
    for root in range(n):
        parent = [-1] * n
        order = [root]
        for u in order:
            for v in graph[u]:
                if v != parent[u]:
                    parent[v] = u
                    order.append(v)
        dp = [0.0] * n
        for u in reversed(order):
            children = sorted((dp[v] for v in graph[u] if v != parent[u]), reverse=True)
            prefix = 0.0
            gain = 0.0
            for count, value in enumerate(children, 1):
                prefix += value
                if cuts or count == len(children):
                    gain = max(gain, prefix * (probabilities[u] + (1 - probabilities[u]) / count))
            dp[u] = damage[u] + gain
        best = max(best, dp[root])
    return best


def make_case(spec, output):
    rng = SplitMix64(spec['seed'])
    n = spec['n']
    shape = spec['kind']
    edges = []
    for v in range(1, n):
        if shape == 'isolated' or (shape == 'forest' and v % 5 == 0):
            continue
        parent = 0 if shape == 'star' else (v - 1 if shape == 'chain' else rng.between(0, v - 1))
        edges.append((parent, v))
    block_limit = min(spec['block_limit'], len(edges))
    damage = [rng.between(0, 500000) / 100 for _ in range(n)]
    probabilities = [rng.between(0, 1000) / 1000 for _ in range(n)]
    if shape == 'star':
        probabilities[0] = 0
        # Two valuable leaves make blocking the zero-damage leaves beneficial,
        # even though the initial target can be chosen freely.
        damage = [0.0] + [5000.0 if i in (1, 2) else 0.0 for i in range(1, n)]
    if spec.get('zero'):
        damage = [0.0] * n
    value = expected_value(n, edges, damage, probabilities, block_limit > 0)
    # Choose a two-decimal offset well within the required rounding margin.
    cents = min(range(101), key=lambda x: abs(value + x / 100 - int(value + x / 100 + 0.5)))
    output.write(f'{n} {block_limit} {len(edges)} {cents / 100:.2f}\n')
    for u, v in edges:
        output.write(f'{u + 1} {v + 1}\n')
    output.write(' '.join(f'{x:.2f}' for x in damage) + '\n')
    output.write(' '.join(f'{x:.3f}' for x in probabilities) + '\n')

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
