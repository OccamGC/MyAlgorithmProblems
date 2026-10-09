"""Deterministic input recipes and optional reference-output generation (Python 3)."""
import argparse
import json
import math
from pathlib import Path
import random
import subprocess

SCALE = 10**6
MOD = 998244353
MAX_K = 10**18
SMALL_K = 2 * 10**7
PRIMES = [x for x in range(2, 300)
          if all(x % d for d in range(2, math.isqrt(x) + 1))]


def encode(games):
    lines = [str(len(games))]
    for items, queries in games:
        lines.append(f"{len(items)} {len(queries)}")
        lines.extend(f"{p} {m}" for p, m in items)
        lines.extend(map(str, queries))
    return "\n".join(lines) + "\n"


def parse(text):
    tokens = list(map(int, text.split()))
    pos = 1
    assert tokens and 1 <= tokens[0] <= 8, "T out of range"
    games = []
    for _ in range(tokens[0]):
        assert pos + 2 <= len(tokens), "missing n,q"
        n, q = tokens[pos:pos + 2]
        pos += 2
        assert 1 <= n <= 2000 and 1 <= q <= 5600, "n,q out of range"
        assert pos + 2 * n + q <= len(tokens), "truncated case"
        items = [tuple(tokens[pos + 2 * i:pos + 2 * i + 2]) for i in range(n)]
        pos += 2 * n
        queries = tokens[pos:pos + q]
        pos += q
        assert all(0 <= p <= SCALE and 1 <= m <= 10**9 for p, m in items)
        assert all(1 <= k <= MAX_K for k in queries)
        assert n <= 44 or max(queries) <= SMALL_K, "neither size regime holds"
        games.append((items, queries))
    assert pos == len(tokens), "extra tokens"
    return games


def validate(text, group=None):
    games = parse(text)
    small_work = 0
    large_work = 0
    for items, queries in games:
        n, q = len(items), len(queries)
        if max(queries) <= SMALL_K:
            small_work += n * q
        else:
            large_work += (q + 4) * 2**((n + 1) // 2)
        if group == 1:
            assert n <= 18
        if group == 2:
            assert max(queries) <= SMALL_K
        if group == 3:
            assert n <= 34
    assert small_work <= 2000, "small-threshold budget exceeded"
    assert large_work <= 7 * 2**24, "large-threshold budget exceeded"
    assert sum(len(qs) for _, qs in games) <= 5600, "query budget exceeded"
    return games


def prime_game(rng, n, q, offset=0, narrow=False, distinct=False, query_cap=MAX_K):
    if distinct:
        multipliers = PRIMES[offset:offset + n]
        assert len(multipliers) == n and len(set(multipliers)) == n
    else:
        half = PRIMES[offset:offset + (n + 1) // 2]
        multipliers = (half * 2)[:n]
    rng.shuffle(multipliers)
    items = [(rng.randrange(1, SCALE), m) for m in multipliers]
    center = min(math.isqrt(math.prod(multipliers)), query_cap // 2)
    if q == 1:
        queries = [center + rng.choice([-1, 0, 1])]
    else:
        queries = [max(1, min(MAX_K, center * rng.randrange(70000, 140000) // 100000 + i))
                   for i in range(q)]
        if not narrow:
            queries[0] = center
            queries[1] = center + 1
    return items, queries


def distinct_game(rng, n, q, integers=False, offset=0):
    multipliers = list(range(2, n + 2)) if integers else PRIMES[offset:offset + n]
    assert len(multipliers) == len(set(multipliers)) == n
    rng.shuffle(multipliers)
    items = [(rng.randrange(1, SCALE), m) for m in multipliers]
    queries = [MAX_K * rng.randrange(500000, 999000) // 1000000 + j for j in range(q)]
    return items, queries


def make_case(case):
    rng = random.Random(case["seed"])
    mode = case["mode"]
    if mode == "boundaries":
        games = [
            ([(0, 10**9)], [1, 2, MAX_K - 1, MAX_K]),
            ([(SCALE, 10**9)] * 3, [MAX_K - 1, MAX_K]),
            ([(SCALE // 2, 2), (SCALE // 4, 3), (SCALE, 5)], [1, 5, 10, 15, 30, 31]),
            ([(500000, 1)] * 18, [1, 2, MAX_K]),
            ([(999999, 999999937), (1, 999999929)], [999999937, 999999937 * 999999929]),
            ([(500000, 2)] * 18, [2**9 - 1, 2**9, 2**9 + 1, 2**18, 2**18 + 1]),
            ([(1000000, 3), (500000, 5)], [5, 6, 15, 16]),
            ([(500000, 10**9)] * 8, [2**31 - 1, 2**31, 2**31 + 1, MAX_K]),
        ]
    elif mode == "small-random":
        games = []
        for _ in range(8):
            items = [(rng.randrange(SCALE + 1), rng.choice([1, 2, 3, 17, 10**9])) for _ in range(18)]
            product = math.prod(m for _, m in items[:9])
            games.append((items, [max(1, min(MAX_K, product + d)) for d in [-1, 0, 1]]))
    elif mode == "dp-max":
        items = [(rng.randrange(1, SCALE), rng.randrange(2, 1001)) for _ in range(2000)]
        games = [(items, [SMALL_K])]
    elif mode == "dp-squares":
        items = [(rng.choice([0, 1, 123456, 999999]), rng.choice([1, 2, 3, 7, 997, 1000, 1000000000]))
                 for _ in range(80)]
        queries = [s * s + d for s in [11, 101, 317, 701, 4201, 4301, 4401, 4472] for d in [-1, 0, 1]]
        games = [(items, queries)]
    elif mode == "dp-low-factors":
        items = [(rng.randrange(1, SCALE), rng.choice([2, 3, 5, 7, 11, 13])) for _ in range(2000)]
        games = [(items, [SMALL_K])]
    elif mode == "mitm-medium":
        games = [prime_game(rng, 30, 8, i % 3) for i in range(8)]
    elif mode == "integer-boundaries":
        games = []
        for _ in range(8):
            items = [(rng.randrange(1, SCALE), rng.choice([2, 999999929, 999999937, 10**9])) for _ in range(30)]
            queries = [2**31 - 1, 2**31, 2**31 + 1, 10**12 - 1, 10**12, 10**12 + 1, MAX_K - 1, MAX_K]
            games.append((items, queries))
    elif mode == "anti-sort":
        games = [distinct_game(rng, 44, 1, integers=True) for _ in range(5)]
    elif mode == "anti-binary":
        games = [distinct_game(rng, 28, 5600)]
    elif mode == "mixed-budget":
        games = [distinct_game(rng, 30, 1700, offset=i) for i in range(2)]
        games.append(([(rng.randrange(1, SCALE), rng.randrange(2, 1001)) for _ in range(2000)], [SMALL_K]))
    else:
        raise ValueError(f"unknown mode: {mode}")
    text = encode(games)
    validate(text, case["group"])
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=Path(__file__).with_name("plan.json"))
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--std", type=Path)
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    chosen = set(args.case or [c["id"] for c in plan["cases"]])
    known = {c["id"] for c in plan["cases"]}
    if not chosen <= known:
        parser.error("unknown case id")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan["cases"]:
        if case["id"] not in chosen:
            continue
        text = make_case(case)
        target = args.out_dir / (case["id"] + ".in")
        target.write_text(text, encoding="utf-8", newline="\n")
        if args.std:
            output = subprocess.check_output([str(args.std.resolve())], input=text.encode())
            target.with_suffix(".out").write_bytes(output.replace(b"\r\n", b"\n"))
        print(case["id"], flush=True)


if __name__ == "__main__":
    main()
