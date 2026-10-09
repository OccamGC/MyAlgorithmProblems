"""Reproduce and measure the signed Candy Brackets package."""
import importlib.util
import json
import math
from pathlib import Path
import platform
import statistics
import subprocess
import sys
from benchmark_reference import run, run_with_peak_memory, sha256
from check_candy_signed import candy_oracle, validate

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "topics/strings/candy-brackets"
WORK = ROOT / "build/candy-signed-20261001"


def main():
    program = WORK / "std.exe"
    data = WORK / "data"
    data.mkdir(parents=True, exist_ok=True)
    compiler = ROOT.parent / "Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe"
    flags = ["-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic"]
    subprocess.run([str(compiler), *flags, str(PACKAGE / "std.cpp"), "-o", str(program)], check=True)
    spec = importlib.util.spec_from_file_location("candy_generator", PACKAGE / "tests/generate.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    plan = json.loads((PACKAGE / "tests/plan.json").read_text(encoding="utf-8"))
    item = dict(source_sha256=sha256(PACKAGE / "std.cpp"), binary_sha256=sha256(program),
                generator_sha256=sha256(PACKAGE / "tests/generate.py"),
                plan_sha256=sha256(PACKAGE / "tests/plan.json"), cases=[])
    report = dict(date="2026-10-01", timezone="Asia/Shanghai",
                  cpu="Intel(R) Core(TM) Ultra 9 275HX", os=platform.platform(),
                  python=platform.python_version(),
                  compiler=subprocess.check_output([str(compiler), "--version"]).decode().splitlines()[0],
                  flags=flags, repeat=5, multiplier=2, resolution_seconds=0.5,
                  timing_scope="Startup and I/O included; generation and oracle validation excluded.",
                  memory_scope="Separately measured peak working set, including runtime overhead.",
                  oracle="Offline sibling-atom activation and maximum-subarray DSU; checked against brute force.",
                  problems={"candy-brackets": item})
    report_path = ROOT / "docs/benchmark-candy-signed.json"
    for case in plan["cases"]:
        print("Generating and independently checking", case["id"], flush=True)
        path = data / (case["id"] + ".in")
        source = generator.generate(case)
        dimensions = validate(source, case["group"])
        path.write_text(source, encoding="ascii", newline="\n")
        assert generator.generate(case) == source, ("not reproducible", case["id"])
        expected = candy_oracle(source).encode("ascii")
        del source
        target = data / (case["id"] + ".out")
        target.write_bytes(expected)
        output = WORK / "run.out"
        peak = run_with_peak_memory(program, path, output)
        assert output.read_bytes().replace(b"\r\n", b"\n") == expected, case["id"]
        times = []
        for _ in range(5):
            times.append(run(program, path, output))
            assert output.read_bytes().replace(b"\r\n", b"\n") == expected, case["id"]
        assert peak < 128 * 1024**2, (case["id"], peak)
        item["cases"].append(dict(id=case["id"], group=case["group"], dimensions=dimensions,
                                 input_sha256=sha256(path), output_sha256=sha256(target),
                                 seconds=times, median_seconds=statistics.median(times),
                                 peak_working_set_bytes=peak))
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("Passed", case["id"], "median", statistics.median(times), "peak", peak, flush=True)
    slowest = max(case["median_seconds"] for case in item["cases"])
    peak = max(case["peak_working_set_bytes"] for case in item["cases"])
    item["summary"] = dict(slowest_median_seconds=slowest, peak_working_set_bytes=peak)
    item["limit_seconds"] = math.ceil(2 * slowest / 0.5) * 0.5
    item["within_limits"] = slowest <= item["limit_seconds"] and peak < 128 * 1024**2
    cli = WORK / "cli"
    subprocess.run([sys.executable, str(PACKAGE / "tests/generate.py"), "--plan",
                    str(PACKAGE / "tests/plan.json"), "--out-dir", str(cli),
                    "--case", "02", "--case", "03", "--std", str(program)], check=True)
    for number in ("02", "03"):
        assert (cli / (number + ".in")).read_bytes() == (data / (number + ".in")).read_bytes()
        assert (cli / (number + ".out")).read_bytes() == (data / (number + ".out")).read_bytes()
    invalid = subprocess.run([sys.executable, str(PACKAGE / "tests/generate.py"), "--out-dir", str(cli),
                              "--case", "missing"], capture_output=True)
    assert invalid.returncode != 0 and b"unknown case" in invalid.stderr
    item["generator_cli_checks"] = ["custom plan", "multiple --case", "--std", "unknown case rejected"]
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(item["summary"]), "limit", item["limit_seconds"], flush=True)


if __name__ == "__main__":
    main()
