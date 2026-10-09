"""Independent Python integer oracle, forced branches, wide arithmetic, samples, and CLI checks."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import re
import subprocess
import sys

import generate

PROBLEM = Path(__file__).resolve().parents[1]
ROOT = PROBLEM.parents[2]
BUILD = ROOT / "build/swords-and-crits"
FLAGS = ["-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic"]


def oracle(items, queries):
    # Exact, unbounded integer products; unnormalized integer probability numerators.
    distribution = {1: 1}
    for p, m in items:
        following = {}
        for value, weight in distribution.items():
            following[value] = (following.get(value, 0) + weight * (generate.SCALE - p)) % generate.MOD
            following[value * m] = (following.get(value * m, 0) + weight * p) % generate.MOD
        distribution = following
    inverse = pow(pow(generate.SCALE, len(items), generate.MOD), -1, generate.MOD)
    return [sum(weight for product, weight in distribution.items() if product >= k) * inverse % generate.MOD
            for k in queries]


def execute(program, text, timeout=30):
    try:
        return list(map(int, subprocess.check_output([str(program)], input=text.encode(), timeout=timeout).split()))
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        (BUILD / ("failure-" + program.stem + ".in")).write_text(text, encoding="utf-8")
        raise


def check_arithmetic(program, rng):
    lines, answers = [], []
    bound = 2**63 - 1
    special = [1, 2, 10**9, 10**18 - 1, 10**18, 3037000499, 3037000500, bound]
    for a in special:
        for b in special:
            product = a * b
            for k in [1, 10**18, bound, max(1, min(bound, product))]:
                lines.append(f"0 {a} {b} {k}")
                answers.append(str(min(product, k)))
                lines.append(f"1 {a} {b} {k}")
                answers.append(str(int(product >= k)))
    for _ in range(10000):
        a, b, k = [rng.randrange(1, bound + 1) for _ in range(3)]
        lines.append(f"0 {a} {b} {k}")
        answers.append(str(min(a * b, k)))
        lines.append(f"1 {a} {b} {k}")
        answers.append(str(int(a * b >= k)))
        lines.append(f"2 {a} {b}")
        answers.append(str((a + b - 1) // b))
        value = rng.randrange(bound + 1)
        lines.append(f"3 {value}")
        answers.append(str(math.isqrt(value)))
    for value in [0, *special]:
        lines.append(f"3 {value}")
        answers.append(str(math.isqrt(value)))
    text = str(len(lines)) + "\n" + "\n".join(lines) + "\n"
    answers.append("100000")  # 100000 products of (P-1)^2 exercise all batching boundaries.
    actual = subprocess.check_output([str(program)], input=text.encode()).decode().splitlines()
    assert actual == answers
    return len(lines) + 100000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cxx", default="g++")
    args = parser.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    sources = {
        "std": "std.cpp", "brute": "brute.cpp", "streaming": "alternative-streaming.cpp",
        "branches": "tests/verify-branches.cpp", "arithmetic": "tests/verify-arithmetic.cpp",
        "slow-sort": "tests/slow-sort.cpp", "slow-binary": "tests/slow-binary.cpp",
        "slow-dense": "tests/slow-dense.cpp",
    }
    programs = {}
    for name, source in sources.items():
        programs[name] = BUILD / (name + ".exe")
        subprocess.run([args.cxx, *FLAGS, str(PROBLEM / source), "-o", str(programs[name])], check=True)
    rng = random.Random(2026100419)
    report = {"seed": 2026100419, "arithmetic_operations": check_arithmetic(programs["arithmetic"], rng)}
    variants = ["std", "brute", "streaming", "branches", "slow-sort", "slow-binary", "slow-dense"]
    games = []
    for index in range(640):
        n = rng.randrange(1, 15)
        if index < 320:
            items = [(rng.choice([0, 1, 500000, 999999, 1000000, rng.randrange(1000001)]), rng.randrange(1, 31))
                     for _ in range(n)]
            k = rng.randrange(1, 100000)
            queries = [max(1, k - 1), k, k + 1, 1]
        else:
            items = [(rng.choice([0, 1, 123456, 999999, 1000000, rng.randrange(1000001)]),
                      rng.choice([1, 2, 3, 999999929, 999999937, 10**9, rng.randrange(1, 10**9 + 1)]))
                     for _ in range(n)]
            product = math.prod(m for _, m in items[:rng.randrange(n + 1)])
            queries = [max(1, min(generate.MAX_K, product + d)) for d in [-1, 0, 1]]
            queries += [rng.choice([2**31 - 1, 2**31, 2**31 + 1, generate.MAX_K])]
        games.append((items, queries))
    # Include the formal small instances, including sample-sized probability boundaries.
    plan = json.loads((PROBLEM / "tests/plan.json").read_text(encoding="utf-8"))
    for case in plan["cases"][:2]:
        games.extend(generate.validate(generate.make_case(case), case["group"]))
    query_count = 0
    for begin in range(0, len(games), 8):
        if begin % 64 == 0:
            print("oracle games", begin, "/", len(games), flush=True)
        batch = games[begin:begin + 8]
        text = generate.encode(batch)
        generate.validate(text)
        expected = [answer for items, queries in batch for answer in oracle(items, queries)]
        query_count += len(expected)
        for variant in variants:
            assert execute(programs[variant], text) == expected, (begin, variant)
    report.update({"oracle_games": len(games), "oracle_queries": query_count, "verified_variants": variants})
    samples = sorted((PROBLEM / "tests/samples").glob("*.in"))
    for inp in samples:
        text = inp.read_text(encoding="utf-8")
        cases = generate.validate(text)
        expected = list(map(int, inp.with_suffix(".out").read_text().split()))
        assert expected == [x for items, queries in cases for x in oracle(items, queries)]
        for variant in variants:
            assert execute(programs[variant], text) == expected, (inp, variant)
    for language in ["zh", "en"]:
        blocks = re.findall(r"```text\n(.*?)```", (PROBLEM / f"statement.{language}.md").read_text(encoding="utf-8"), re.S)
        assert len(blocks) == 2 * len(samples)
        for i, inp in enumerate(samples):
            assert blocks[2 * i] == inp.read_text(encoding="utf-8")
            assert blocks[2 * i + 1] == inp.with_suffix(".out").read_text(encoding="utf-8")
    report["samples"] = len(samples)
    bad = ["0\n", "9\n", "1\n1 1\n0 0\n1\n", "1\n1 1\n1000001 2\n1\n",
           "1\n1 1\n1 2\n0\n", f"1\n1 1\n1 2\n{generate.MAX_K + 1}\n",
           generate.encode([([(1, 2)] * 45, [10**9])]),
           generate.encode([([(1, 2)] * 2000, [generate.SMALL_K] * 2)]),
           generate.encode([([(1, 2)] * 44, [generate.MAX_K] * 32)] * 2)]
    bad.append(generate.encode([([(1, 2)], [generate.MAX_K] * 3201)] * 2))
    for text in bad:
        try:
            generate.validate(text)
        except (AssertionError, ValueError, IndexError):
            continue
        raise AssertionError("validator accepted invalid input")
    report["rejected_invalid_inputs"] = len(bad)
    cli = BUILD / "cli"
    command = [sys.executable, str(PROBLEM / "tests/generate.py"), "--out-dir", str(cli),
               "--case", "01", "--case", "02", "--std", str(programs["std"])]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    for case in plan["cases"][:2]:
        text = generate.make_case(case)
        assert text == (cli / (case["id"] + ".in")).read_text(encoding="utf-8")
        assert execute(programs["brute"], text) == list(map(int, (cli / (case["id"] + ".out")).read_text().split()))
    assert subprocess.run([sys.executable, str(PROBLEM / "tests/generate.py"), "--out-dir", str(cli), "--case", "missing"],
                          capture_output=True).returncode != 0
    report["cli_and_deterministic_generation"] = True
    source = (PROBLEM / "std.cpp").read_text(encoding="utf-8")
    assert not re.search(r'#include\s*"|__int128|FWide|std::uint64_t|long double', source)
    isolated = BUILD / "standalone"
    isolated.mkdir(exist_ok=True)
    (isolated / "std.cpp").write_text(source, encoding="utf-8", newline="\n")
    standalone = isolated / "std.exe"
    subprocess.run([args.cxx, *FLAGS, str(isolated / "std.cpp"), "-o", str(standalone)], check=True)
    for inp in samples:
        assert execute(standalone, inp.read_text(encoding="utf-8")) == list(map(int, inp.with_suffix(".out").read_text().split()))
    report["standalone_std"] = True
    report["sources"] = {
        str(path.relative_to(PROBLEM)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PROBLEM.rglob("*") if path.suffix in {".cpp", ".hpp", ".py"}
    }
    target = ROOT / "docs/verification-swords-and-crits.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
