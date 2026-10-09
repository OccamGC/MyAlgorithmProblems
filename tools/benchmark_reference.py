"""Validate generated inputs and benchmark locally compiled reference programs.

Generate inputs with each problem's tests/generate.py before running this script.
Build std.cpp files into build/bin/<problem-slug>.exe with a common configuration.
Outputs and timing details are written under build/ and are not versioned.
"""

import argparse
import ctypes
import hashlib
import json
import math
import os
import platform
import re
import statistics
import subprocess
import time
from pathlib import Path

import validate_ra1
import validate_ra2
import validate_r6
import validate_r7
import validate_r8
import validate_r9
import validate_r10
import validate_r11
import validate_r12
import validate_r13
import validate_r14


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_R1 = (
    ("strings", "eating-candy"),
    ("graphs", "bridge-tales-no-first-plan"),
    ("strings", "build-a-big-star"),
)
PROBLEMS_R2 = (
    ("graphs", "two-color-badges"),
    ("optimization", "passengers-need-exercise"),
    ("trees", "forest-ranger"),
)
PROBLEMS_R3 = (
    ("strings", "just-a-little-more"),
    ("optimization", "weak-link-comeback"),
    ("data-structures", "cookie-swap"),
)
PROBLEMS_R4 = (
    ("trees", "prism-tank"),
    ("data-structures", "psychic-commando"),
    ("dynamic-programming", "elite-combatant"),
)
PROBLEMS_R5 = (
    ("graphs", "terror-drone"),
    ("linear-algebra", "virus-sniper"),
    ("graphs", "chrono-legion"),
)
PROBLEMS_R6 = (
    ("graphs", "chaos-drone"),
    ("optimization", "force-shield"),
    ("data-structures", "vacuum-imploder"),
    ("dynamic-programming", "upgrade-toolkit"),
    ("data-structures", "nano-computer"),
    ("strings", "cloning-vat"),
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_candy(path):
    with path.open("rb") as stream:
        n = int(stream.readline())
        text = stream.readline().rstrip(b"\n")
        assert 0 <= n <= 100_000
        assert 1 <= len(text) <= 5_000_000 and set(text) <= {48, 49}
        total = 0
        max_pattern_length = 0
        first_pattern_length = None
        all_patterns_equal_length = True
        for _ in range(n):
            pattern = stream.readline().rstrip(b"\n")
            assert pattern and set(pattern) <= {48, 49}
            total += len(pattern)
            max_pattern_length = max(max_pattern_length, len(pattern))
            if first_pattern_length is None:
                first_pattern_length = len(pattern)
            elif len(pattern) != first_pattern_length:
                all_patterns_equal_length = False
        assert total <= 5_000_000
        assert not stream.read(1)
    return {
        "n": n,
        "text_length": len(text),
        "total_pattern_length": total,
        "max_pattern_length": max_pattern_length,
        "all_patterns_equal_length": all_patterns_equal_length,
    }


def validate_graph(path):
    with path.open("r", encoding="ascii") as stream:
        n, m = map(int, stream.readline().split())
        assert 2 <= n <= 100_000 and n <= m <= 200_000
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for index in range(m):
            u, v, w = map(int, stream.readline().split())
            assert 1 <= u <= n and 1 <= v <= n and u != v
            assert 1 <= w <= 5_000
            if path.stem == "long-chain":
                if index < n - 1:
                    assert (u, v, w) == (index + 1, index + 2, 1)
                else:
                    assert w >= 2
            a = find(u)
            b = find(v)
            if a != b:
                parent[a] = b
                components -= 1
        assert components == 1
        assert not stream.read(1)
    return {"n": n, "m": m}


def validate_star(path):
    with path.open("rb") as stream:
        n, m = map(int, stream.readline().split())
        assert 0 <= n <= 1_000_000 and 0 <= m <= 1_000_000
        marks = stream.readline().split()
        assert len(marks) == n and set(marks) <= {b"<", b">", b"*"}
        for _ in range(m):
            side, mark = stream.readline().split()
            assert side in {b"1", b"2"} and mark in {b"<", b">", b"*"}
        assert not stream.read(1)
    return {"n": n, "m": m}


def validate_badges(path):
    with path.open("r", encoding="ascii") as stream:
        n, m = map(int, stream.readline().split())
        assert 1 <= n <= 500_000 and 1 <= m <= 500_000
        for _ in range(m):
            u, v = map(int, stream.readline().split())
            assert 1 <= u <= n and 1 <= v <= n
        assert not stream.read(1)
    return {"n": n, "m": m}


def validate_platform(path):
    with path.open("r", encoding="ascii") as stream:
        L = int(stream.readline())
        M = int(stream.readline())
        passengers = list(map(int, stream.readline().split()))
        N = int(stream.readline())
        doors = [0] + (list(map(int, stream.readline().split())) if N > 1 else [])
        assert 1 <= L <= 1_000_000_000
        assert 1 <= M <= 300 and len(passengers) == M
        assert 1 <= N <= min(300, L + 1) and len(doors) == N
        assert passengers == sorted(passengers) and all(0 <= p <= L for p in passengers)
        assert doors == sorted(set(doors)) and doors[-1] <= L
        assert not stream.read(1)
    return {"L": L, "M": M, "N": N, "last_door": doors[-1]}


def validate_trail(path):
    with path.open("r", encoding="ascii") as stream:
        n = int(stream.readline())
        assert 2 <= n <= 1_000_000
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for _ in range(n - 1):
            u, v = map(int, stream.readline().split())
            assert 1 <= u <= n and 1 <= v <= n and u != v
            a, b = find(u), find(v)
            assert a != b
            parent[a] = b
        assert not stream.read(1)
    return {"n": n}


def validate_encore(path):
    with path.open("r", encoding="ascii") as stream:
        initial = stream.readline().strip()
        Q = int(stream.readline())
        queries = [int(stream.readline()) for _ in range(Q)]
        assert 1 <= len(initial) <= 10 and all("a" <= ch <= "z" for ch in initial)
        assert 1 <= Q <= 10 and all(1 <= x <= 70 for x in queries)
        assert not stream.read(1)
    return {"initial": initial, "Q": Q, "queries": queries, "max_version": max(queries)}


def validate_weak_link(path):
    with path.open("r", encoding="ascii") as stream:
        n = int(stream.readline())
        assert 1 <= n <= 1_000_000
        for _ in range(2):
            values = list(map(int, stream.readline().split()))
            assert len(values) == n
            assert all(-1_000_000 <= value <= 1_000_000 for value in values)
        assert not stream.read(1)
    return {"n": n}


def validate_cookies(path):
    with path.open("r", encoding="ascii") as stream:
        n, m = map(int, stream.readline().split())
        assert 1 <= n <= 300_000 and 1 <= m <= 300_000
        quantities = list(map(int, stream.readline().split()))
        assert len(quantities) == 2 * n
        assert all(0 <= value <= 1_000_000_000 for value in quantities)
        maximum = max(quantities)
        queries = 0
        for _ in range(m):
            operation, x, y = map(int, stream.readline().split())
            if operation == 3:
                assert 1 <= x <= y <= n
                queries += 1
            else:
                assert operation in (1, 2) and 1 <= x <= n
                assert 0 <= y <= 1_000_000_000
                maximum = max(maximum, y)
        assert not stream.read(1)
    return {"n": n, "m": m, "query_count": queries, "max_quantity": maximum}


VALIDATORS = {
    "eating-candy": validate_candy,
    "bridge-tales-no-first-plan": validate_graph,
    "build-a-big-star": validate_star,
    "two-color-badges": validate_badges,
    "passengers-need-exercise": validate_platform,
    "forest-ranger": validate_trail,
    "just-a-little-more": validate_encore,
    "weak-link-comeback": validate_weak_link,
    "cookie-swap": validate_cookies,
}

GROUP_SHARES = {
    "eating-candy": (30, 20, 20, 30),
    "bridge-tales-no-first-plan": (20, 30, 50),
    "build-a-big-star": (20, 20, 30, 30),
    "two-color-badges": (30, 30, 40),
    "passengers-need-exercise": (30, 70),
    "forest-ranger": (30, 30, 40),
    "just-a-little-more": (30, 20, 50),
    "weak-link-comeback": (20, 20, 20, 40),
    "cookie-swap": (10, 10, 20, 20, 20, 20),
}


def validate_groups(slug, plan):
    shares = [0] * len(GROUP_SHARES[slug])
    ids = set()
    for spec in plan["cases"]:
        assert spec["id"] not in ids, (slug, spec["id"])
        ids.add(spec["id"])
        group = spec["group"]
        score = spec["score_percent"]
        assert 1 <= group <= len(shares) and isinstance(score, int) and score > 0
        shares[group - 1] += score
    assert tuple(shares) == GROUP_SHARES[slug], (slug, shares)


def validate_group_case(slug, spec, dimensions):
    if slug in validate_r14.VALIDATORS:
        validate_r14.validate_group_case(slug, spec, dimensions)
        return
    if slug in validate_r13.VALIDATORS:
        validate_r13.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r12.VALIDATORS:
        validate_r12.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r11.VALIDATORS:
        validate_r11.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r10.VALIDATORS:
        validate_r10.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r9.VALIDATORS:
        validate_r9.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r8.VALIDATORS:
        validate_r8.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r7.VALIDATORS:
        validate_r7.validate_group(slug, spec, dimensions)
        return
    if slug in validate_r6.VALIDATORS:
        validate_r6.validate_group(slug, spec, dimensions)
        return
    if slug in validate_ra2.VALIDATORS:
        validate_ra2.validate_group(slug, spec, dimensions)
        return
    if slug in validate_ra1.VALIDATORS:
        validate_ra1.validate_group(slug, spec, dimensions)
        return
    group = spec["group"]
    if slug == "eating-candy":
        if group == 1:
            assert dimensions["text_length"] <= 1_000
            assert dimensions["total_pattern_length"] <= 10_000
        elif group == 2:
            assert dimensions["text_length"] <= 100_000
            assert dimensions["n"] <= 500
            assert dimensions["max_pattern_length"] <= 30
        elif group == 3:
            assert dimensions["all_patterns_equal_length"]
    elif slug == "bridge-tales-no-first-plan":
        if group == 1:
            assert dimensions["n"] <= 10 and dimensions["m"] <= 20
        elif group == 2:
            assert dimensions["n"] <= 5_000 and dimensions["m"] <= 10_000
    elif slug == "build-a-big-star":
        if group == 1:
            assert dimensions["n"] <= 25 and dimensions["m"] == 0
        elif group == 2:
            assert dimensions["n"] <= 5_000 and dimensions["m"] == 0
        elif group == 3:
            assert dimensions["n"] <= 5_000 and dimensions["m"] <= 5_000
    elif slug == "two-color-badges":
        if group == 1:
            assert dimensions["n"] <= 15 and dimensions["m"] <= 15
        elif group == 2:
            assert dimensions["n"] <= 5_000 and dimensions["m"] <= 5_000
    elif slug == "passengers-need-exercise":
        if group == 1:
            assert dimensions["L"] <= 100 and dimensions["M"] <= 50 and dimensions["N"] <= 50
    elif slug == "forest-ranger":
        if group == 1:
            assert dimensions["n"] <= 10
        elif group == 2:
            assert dimensions["n"] <= 5_000
    elif slug == "just-a-little-more":
        if group <= 2:
            assert dimensions["max_version"] <= (30, 50)[group - 1]
    elif slug == "weak-link-comeback":
        if group <= 3:
            assert dimensions["n"] <= (300, 2_000, 10_000)[group - 1]
    elif slug == "cookie-swap":
        limit = (10, 100, 300, 3_000, 50_000, 300_000)[group - 1]
        assert dimensions["n"] <= limit and dimensions["m"] <= limit
        if group == 1:
            assert dimensions["max_quantity"] <= 50


def check_samples(problem_dir, program):
    count = 0
    for sample in sorted((problem_dir / "tests" / "samples").glob("*.in")):
        expected = sample.with_suffix(".out").read_bytes().split()
        result = subprocess.run(
            [str(program)], input=sample.read_bytes(), capture_output=True, check=True
        )
        if problem_dir.name == "auto-wiring":
            validate_r11.check_wiring_tokens(sample, result.stdout.split(), expected)
        elif problem_dir.name in validate_r8.VALIDATORS:
            validate_r8.check_sample(sample, problem_dir.name, result.stdout.split(), expected)
        elif problem_dir.name == "redstone-computer":
            validate_r7.check_computer(sample, result.stdout.split(), expected)
        elif problem_dir.name == "vacuum-imploder":
            actual = result.stdout.split()
            assert len(actual) == len(expected) and all(
                math.isfinite(float(a)) and abs(float(a) - float(b)) <= 0.050001
                for a, b in zip(actual, expected)
            ), f"sample mismatch: {sample}"
        else:
            assert result.stdout.split() == expected, f"sample mismatch: {sample}"
        count += 1
    return count


def check_output(slug, output_path, dimensions):
    if slug in validate_r14.VALIDATORS:
        validate_r14.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r13.VALIDATORS:
        validate_r13.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r12.VALIDATORS:
        validate_r12.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r11.VALIDATORS:
        validate_r11.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r10.VALIDATORS:
        validate_r10.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r9.VALIDATORS:
        validate_r9.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r8.VALIDATORS:
        validate_r8.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r7.VALIDATORS:
        validate_r7.check_output(slug, output_path, dimensions)
        return
    if slug in validate_r6.VALIDATORS:
        validate_r6.check_output(slug, output_path, dimensions)
        return
    if slug in validate_ra2.VALIDATORS:
        validate_ra2.check_output(slug, output_path, dimensions)
        return
    if slug in validate_ra1.VALIDATORS:
        validate_ra1.check_output(slug, output_path, dimensions)
        return
    tokens = output_path.read_bytes().split()
    if slug == "just-a-little-more":
        current = dimensions["initial"].encode("ascii")
        lengths = [len(current)]
        for _ in range(1, dimensions["max_version"]):
            current += current[:(len(current) + 4) // 5]
            lengths.append(len(current))
        assert len(tokens) == dimensions["Q"]
        assert all(token == current[:lengths[x - 1]]
                   for token, x in zip(tokens, dimensions["queries"])), output_path
        return
    if slug == "weak-link-comeback":
        assert len(tokens) == 1 and re.fullmatch(rb"-?\d+", tokens[0])
        assert abs(int(tokens[0])) <= 10**18
        known = {"single-negative": -6, "maximum-product": 10**18, "zero-minima": 0}
        if output_path.stem in known:
            assert int(tokens[0]) == known[output_path.stem]
        return
    if slug == "cookie-swap":
        assert len(tokens) == dimensions["query_count"]
        assert all(token.isdigit() and int(token) <= dimensions["n"] * 10**9 for token in tokens)
        if output_path.stem == "dominant-participant":
            assert all(token == b"0" for token in tokens)
        return
    if slug == "two-color-badges":
        assert len(tokens) == 2 * dimensions["m"], (slug, output_path)
        assert all(tokens[i] in (b"0", b"1") and 1 <= int(tokens[i + 1]) <= dimensions["n"]
                   for i in range(0, len(tokens), 2))
        return
    if slug == "passengers-need-exercise":
        assert len(tokens) == 2 and all(re.fullmatch(rb"\d+\.[05]", token) for token in tokens)
        assert int(tokens[0].replace(b".", b"")) <= 10 * (dimensions["L"] - dimensions["last_door"])
        assert int(tokens[1].replace(b".", b"")) <= 10 * dimensions["M"] * dimensions["L"]
        if output_path.stem == "half-integer":
            assert tokens == [b"0.5", b"150.0"], output_path
        return
    if slug == "forest-ranger":
        assert 2 <= len(tokens) <= dimensions["n"]
        assert all(token.isdigit() for token in tokens)
        days = int(tokens[0])
        gains = [int(token) for token in tokens[1:]]
        assert days == len(gains) and gains[-1] == dimensions["n"] - 1
        increments = [gains[0], *(b - a for a, b in zip(gains, gains[1:]))]
        assert all(a >= b >= 1 for a, b in zip(increments, increments[1:]))
        return
    expected_count = dimensions["m"] + 1 if slug == "build-a-big-star" else 1
    assert len(tokens) == expected_count, (slug, output_path, len(tokens), expected_count)
    assert all(token.isdigit() for token in tokens), output_path
    if slug == "eating-candy":
        assert int(tokens[0]) <= dimensions["text_length"]
        if output_path.stem == "suffix-match":
            assert tokens == [b"30"]
    elif slug == "bridge-tales-no-first-plan":
        if output_path.stem == "second-distinct":
            assert tokens == [b"4"]
    elif slug == "build-a-big-star":
        assert all(int(token) <= dimensions["n"] + index for index, token in enumerate(tokens))


def run(program, input_path, output_path):
    with input_path.open("rb") as source, output_path.open("wb") as output:
        start = time.perf_counter()
        subprocess.run([str(program)], stdin=source, stdout=output, check=True)
        return time.perf_counter() - start


def run_with_peak_memory(program, input_path, output_path):
    with input_path.open("rb") as source, output_path.open("wb") as output:
        with subprocess.Popen([str(program)], stdin=source, stdout=output) as process:
            if process.wait() != 0:
                raise subprocess.CalledProcessError(process.returncode, [str(program)])
            if os.name != "nt":
                return None

            class MemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", ctypes.c_ulong),
                    ("PageFaultCount", ctypes.c_ulong),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                    ("PrivateUsage", ctypes.c_size_t),
                ]

            counters = MemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            if not ctypes.windll.psapi.GetProcessMemoryInfo(
                int(process._handle), ctypes.byref(counters), counters.cb
            ):
                raise ctypes.WinError()
            return counters.PeakWorkingSetSize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14"), default="R1")
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--multiplier", type=float, default=2)
    parser.add_argument("--resolution", type=float, default=0.5)
    args = parser.parse_args()
    assert args.repeat >= 3 and args.multiplier > 0 and args.resolution > 0

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "repeats": args.repeat,
        "time_resolution_seconds": args.resolution,
        "multiplier": args.multiplier,
        "timing": "wall clock, one input file per process; first run used to produce output, then repeated timed runs; median per case",
        "problems": {},
    }
    VALIDATORS.update(validate_ra1.VALIDATORS)
    GROUP_SHARES.update(validate_ra1.GROUP_SHARES)
    VALIDATORS.update(validate_ra2.VALIDATORS)
    GROUP_SHARES.update(validate_ra2.GROUP_SHARES)
    VALIDATORS.update(validate_r6.VALIDATORS)
    GROUP_SHARES.update(validate_r6.GROUP_SHARES)
    VALIDATORS.update(validate_r7.VALIDATORS)
    GROUP_SHARES.update(validate_r7.GROUP_SHARES)
    VALIDATORS.update(validate_r9.VALIDATORS)
    GROUP_SHARES.update(validate_r9.GROUP_SHARES)
    VALIDATORS.update(validate_r8.VALIDATORS)
    GROUP_SHARES.update(validate_r8.GROUP_SHARES)
    VALIDATORS.update(validate_r11.VALIDATORS)
    GROUP_SHARES.update(validate_r11.GROUP_SHARES)
    VALIDATORS.update(validate_r10.VALIDATORS)
    GROUP_SHARES.update(validate_r10.GROUP_SHARES)
    VALIDATORS.update(validate_r12.VALIDATORS)
    GROUP_SHARES.update(validate_r12.GROUP_SHARES)
    VALIDATORS.update(validate_r13.VALIDATORS)
    GROUP_SHARES.update(validate_r13.GROUP_SHARES)
    VALIDATORS.update(validate_r14.VALIDATORS)
    GROUP_SHARES.update(validate_r14.GROUP_SHARES)
    problems = {"R1": PROBLEMS_R1, "R2": PROBLEMS_R2, "R3": PROBLEMS_R3, "R4": PROBLEMS_R4, "R5": PROBLEMS_R5, "R6": PROBLEMS_R6, "R7": validate_r7.PROBLEMS, "R8": validate_r8.PROBLEMS, "R9": validate_r9.PROBLEMS, "R10": validate_r10.PROBLEMS, "R11": validate_r11.PROBLEMS, "R12": validate_r12.PROBLEMS, "R13": validate_r13.PROBLEMS, "R14": validate_r14.PROBLEMS}[args.batch]
    for topic, slug in problems:
        problem_dir = ROOT / "topics" / topic / slug
        program = ROOT / "build" / "bin" / (slug + (".exe" if os.name == "nt" else ""))
        data_dir = ROOT / "build" / "data" / slug
        assert program.is_file(), program
        samples = check_samples(problem_dir, program)
        plan = json.loads((problem_dir / "tests" / "plan.json").read_text(encoding="utf-8"))
        validate_groups(slug, plan)
        cases = []
        for spec in plan["cases"]:
            input_path = data_dir / (spec["id"] + ".in")
            output_path = data_dir / (spec["id"] + ".out")
            sink_path = data_dir / (spec["id"] + ".benchmark-out")
            dimensions = VALIDATORS[slug](input_path)
            validate_group_case(slug, spec, dimensions)
            peak_memory = run_with_peak_memory(program, input_path, output_path)
            check_output(slug, output_path, dimensions)
            elapsed = [run(program, input_path, sink_path) for _ in range(args.repeat)]
            median = statistics.median(elapsed)
            cases.append({
                "id": spec["id"],
                "group": spec["group"],
                "score_percent": spec["score_percent"],
                "purpose": spec["purpose"],
                "dimensions": dimensions,
                "input_bytes": input_path.stat().st_size,
                "input_sha256": sha256(input_path),
                "output_sha256": sha256(output_path),
                "peak_working_set_bytes": peak_memory,
                "times_seconds": elapsed,
                "median_seconds": median,
            })
            sink_path.unlink()
            print(f"{slug}/{spec['id']}: {median:.6f} s median", flush=True)
        standard_time = max(case["median_seconds"] for case in cases)
        indicative_limit = math.ceil((args.multiplier * standard_time) / args.resolution) * args.resolution
        report["problems"][slug] = {
            "sample_count": samples,
            "std_sha256": sha256(problem_dir / "std.cpp"),
            "cpp_sources_sha256": {
                str(path.relative_to(problem_dir)).replace("\\", "/"): sha256(path)
                for path in sorted(problem_dir.rglob("*")) if path.suffix in {".cpp", ".hpp"}
            },
            "generator_sha256": sha256(problem_dir / "tests" / "generate.py"),
            "plan_sha256": sha256(problem_dir / "tests" / "plan.json"),
            "program_sha256": sha256(program),
            "standard_time_seconds": standard_time,
            "peak_working_set_bytes": max(case["peak_working_set_bytes"] for case in cases) if os.name == "nt" else None,
            "indicative_limit_seconds": indicative_limit,
            "cases": cases,
        }
        print(f"{slug}: T_std={standard_time:.6f} s, L={indicative_limit:.1f} s", flush=True)

    output_path = ROOT / "build" / f"reference-benchmark-{args.batch}.json"
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Report: {output_path}")


if __name__ == "__main__":
    main()
