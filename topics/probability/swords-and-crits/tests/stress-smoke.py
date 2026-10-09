"""Bounded stress checks for dense DP and the space-oriented streaming implementation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import generate

PROBLEM = Path(__file__).resolve().parents[1]
ROOT = PROBLEM.parents[2]
BUILD = ROOT / "build/swords-and-crits"
sys.path.insert(0, str(ROOT / "tools"))
from benchmark_reference import run_with_peak_memory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()
    plan = json.loads((PROBLEM / "tests/plan.json").read_text(encoding="utf-8"))
    cases = {c["id"]: c for c in plan["cases"]}
    record = {"timeout_seconds": args.timeout, "stress": []}
    for variant, case_id in [("slow-dense", "05"), ("streaming", "09")]:
        program = BUILD / (variant + ".exe")
        if not program.exists():
            parser.error("run tests/verify.py first to build the programs")
        text = generate.make_case(cases[case_id])
        start = time.perf_counter()
        try:
            output = subprocess.check_output([str(program)], input=text.encode(), timeout=args.timeout)
            elapsed = time.perf_counter() - start
            expected = subprocess.check_output([str(BUILD / "std.exe")], input=text.encode())
            assert output == expected
            result = {"completed": True, "seconds": elapsed}
        except subprocess.TimeoutExpired:
            result = {"completed": False, "exceeded_seconds": args.timeout}
        result.update({"program": variant, "case": case_id, "input_sha256": hashlib.sha256(text.encode()).hexdigest()})
        record["stress"].append(result)
        print(result, flush=True)
    # A smaller, explicitly identified workload for reproducible memory comparison.
    game = generate.parse(generate.make_case(cases["08"]))[0]
    game = (game[0][:40], game[1][:1])
    text = generate.encode([game])
    inp = BUILD / "streaming-memory.in"
    inp.write_text(text, encoding="utf-8", newline="\n")
    record["memory_example"] = {"n": len(game[0]), "q": 1, "input_sha256": hashlib.sha256(text.encode()).hexdigest(), "programs": {}}
    expected = None
    for variant in ["std", "streaming"]:
        output = BUILD / (variant + "-memory.out")
        peak = run_with_peak_memory(BUILD / (variant + ".exe"), inp, output)
        actual = output.read_bytes()
        if expected is None:
            expected = actual
        assert actual == expected
        record["memory_example"]["programs"][variant] = {"peak_working_set_bytes": peak}
    record["sources"] = {str(p.relative_to(PROBLEM)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in PROBLEM.rglob("*") if p.suffix in {".cpp", ".hpp"}}
    (ROOT / "docs/stress-swords-and-crits.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
