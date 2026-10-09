"""Build and measure the Swords and Critical Hits reference and slow witnesses."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import platform
import statistics
import subprocess
import sys

from benchmark_reference import run, run_with_peak_memory, sha256

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "topics/probability/swords-and-crits"
BUILD = ROOT / "build/swords-and-crits"
RECORD = ROOT / "docs/benchmark-swords-and-crits.json"
FLAGS = ["-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic"]


def load_generator():
    spec = importlib.util.spec_from_file_location("sword_generator", PROBLEM / "tests/generate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    variants = {
        "std": ("std.cpp", []),
        "slow-sort": ("tests/slow-sort.cpp", []),
        "slow-binary": ("tests/slow-binary.cpp", []),
    }
    programs = {}
    for name, (source, extra) in variants.items():
        programs[name] = BUILD / (name + ".exe")
        subprocess.run([args.cxx, *FLAGS, *extra, str(PROBLEM / source), "-o", str(programs[name])], check=True)
    generator = load_generator()
    plan = json.loads((PROBLEM / "tests/plan.json").read_text(encoding="utf-8"))
    record = {
        "platform": platform.platform(), "processor": platform.processor(),
        "python": sys.version, "compiler": subprocess.check_output([args.cxx, "--version"]).decode().splitlines()[0],
        "flags": FLAGS, "record_id": "SC2",
        "repeat": args.repeat, "multiplier": 2, "resolution_seconds": 0.5,
        "sources": {str(p.relative_to(PROBLEM)): sha256(p) for p in PROBLEM.rglob("*") if p.suffix in {".cpp", ".hpp", ".py"}},
        "plan_sha256": sha256(PROBLEM / "tests/plan.json"),
        "binary_sha256": {name: sha256(path) for name, path in programs.items()}, "cases": [],
    }
    if args.case and RECORD.exists():
        old = json.loads(RECORD.read_text(encoding="utf-8"))
        record["cases"] = [c for c in old["cases"] if c["id"] not in args.case]
    data_dir = ROOT / "build/data/swords-and-crits"
    data_dir.mkdir(parents=True, exist_ok=True)
    for case in plan["cases"]:
        if args.case and case["id"] not in args.case:
            continue
        print("case", case["id"], case["mode"], flush=True)
        text = generator.make_case(case)
        assert text == generator.make_case(case)
        games = generator.validate(text, case["group"])
        inp = data_dir / (case["id"] + ".in")
        inp.write_text(text, encoding="utf-8", newline="\n")
        item = {"id": case["id"], "input_sha256": sha256(inp), "programs": {}}
        expected = None
        for name, program in programs.items():
            output = BUILD / (name + ".out")
            peak = run_with_peak_memory(program, inp, output)
            data = output.read_bytes().replace(b"\r\n", b"\n")
            assert len(data.split()) == sum(len(queries) for _, queries in games)
            assert all(0 <= int(x) < generator.MOD for x in data.split())
            if expected is None:
                expected = data
            assert data == expected, (case["id"], name)
            assert peak is None or peak <= 256 * 2**20
            item["programs"][name] = {"seconds": [], "peak_working_set_bytes": peak}
        for repeat in range(args.repeat):
            names = list(programs) if repeat % 2 == 0 else list(programs)[::-1]
            for name in names:
                output = BUILD / (name + ".out")
                elapsed = run(programs[name], inp, output)
                assert output.read_bytes().replace(b"\r\n", b"\n") == expected
                item["programs"][name]["seconds"].append(elapsed)
            print(" repeat", repeat + 1, flush=True)
        for stats in item["programs"].values():
            stats["median_seconds"] = statistics.median(stats["seconds"])
        inp.with_suffix(".out").write_bytes(expected)
        item["output_sha256"] = sha256(inp.with_suffix(".out"))
        record["cases"].append(item)
        record["cases"].sort(key=lambda x: x["id"])
        RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print({k: round(v["median_seconds"], 4) for k, v in item["programs"].items()}, flush=True)
    record["summary"] = {}
    for name in programs:
        stats = [c["programs"][name] for c in record["cases"]]
        record["summary"][name] = {
            "slowest_median_seconds": max(x["median_seconds"] for x in stats),
            "peak_working_set_bytes": max((x["peak_working_set_bytes"] or 0) for x in stats),
        }
    limit = max(0.5, math.ceil(record["summary"]["std"]["slowest_median_seconds"] * 4) / 2)
    record["limit_seconds"] = limit
    record["separation_ratios"] = {
        name: value["slowest_median_seconds"] / limit for name, value in record["summary"].items() if name != "std"
    }
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("SUMMARY", record["summary"], "LIMIT", limit, "SEPARATION", record["separation_ratios"], flush=True)


if __name__ == "__main__":
    main()
