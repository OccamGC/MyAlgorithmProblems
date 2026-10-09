"""Verify public forest fixtures with bitsets and an independent small-case oracle."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def read_case(path):
    words = path.read_text(encoding="utf8").split()
    n, m = map(int, words[:2])
    assert len(words) == 2 + n + m, path
    rows = words[2:2 + n]
    assert 1 <= n <= 1000 and all(len(row) == n and set(row) <= {"0", "1"} for row in rows)
    moves = list(map(int, words[2 + n:]))
    assert all(0 <= direction < 4 for direction in moves)
    roads = {(r, c) for r, row in enumerate(rows) for c, bit in enumerate(row) if bit == "1"}
    return n, roads, moves


def check_forest(roads):
    unseen = set(roads)
    while unseen:
        root = unseen.pop()
        stack = [(root, None)]
        visited = {root}
        while stack:
            point, parent = stack.pop()
            for dr, dc in DIRECTIONS:
                other = (point[0] + dr, point[1] + dc)
                if other not in roads or other == parent:
                    continue
                assert other not in visited, "Road graph contains a cycle"
                visited.add(other)
                unseen.remove(other)
                stack.append((other, point))


def count_with_bitsets(n, roads, moves):
    mask = sum(1 << (r * n + c) for r, c in roads)
    candidates = mask
    row_repeat = ((1 << (n * n)) - 1) // ((1 << n) - 1)
    seen = {(0, 0)}
    r = c = scans = 0
    answers = [len(roads)]
    for direction in moves:
        dr, dc = DIRECTIONS[direction]
        r, c = r + dr, c + dc
        if candidates and (r, c) not in seen:
            seen.add((r, c))
            if abs(r) >= n or abs(c) >= n:
                candidates = 0  # The program clears this case without scanning candidates.
            else:
                scans += candidates.bit_count()
                offset = r * n + c
                shifted = mask >> offset if offset >= 0 else mask << -offset
                lo, hi = max(0, -c), min(n, n - c)
                columns = (((1 << (hi - lo)) - 1) << lo) * row_repeat
                candidates &= shifted & columns
        answers.append(candidates.bit_count())
    return answers, scans


def small_oracle(roads, moves):
    prefix = {(0, 0)}
    r = c = 0
    answers = [len(roads)]
    for direction in moves:
        dr, dc = DIRECTIONS[direction]
        r, c = r + dr, c + dc
        prefix.add((r, c))
        answers.append(sum(all((a + x, b + y) in roads for x, y in prefix) for a, b in roads))
    return answers


def target_events(roads, moves, target):
    prefix = {(0, 0)}
    r = c = 0
    events = []
    for direction in moves:
        dr, dc = DIRECTIONS[direction]
        r, c = r + dr, c + dc
        if (r, c) in prefix:
            continue
        prefix.add((r, c))
        image = {(target[0] - r + x, target[1] - c + y) for x, y in prefix}
        if image <= roads:
            events.append(((r, c), direction, image))
    return events


def check_obstruction(name, roads, moves):
    if name == "unchanged-union.in":
        events = [event for event in target_events(roads, moves, (1, 8)) if event[0][0] == 1]
        assert [event[0][1] for event in events[:5]] == [0, 4, 2, 8, 6]
        union = set().union(*(event[2] for event in events[:4]))
        assert len(union) == 23 and events[4][2] <= union
    if name == "same-direction-parallelogram.in":
        selected = [(1, 0), (2, -2), (2, 0), (1, 2)]
        events = [event for event in target_events(roads, moves, (6, 5)) if event[0] in selected]
        assert [event[0] for event in events] == selected
        assert all(event[1] == 1 for event in events)
        a, b, c, d = selected
        assert (a[0] + c[0], a[1] + c[1]) == (b[0] + d[0], b[1] + d[1])
        assert (b[0] - a[0]) * (d[1] - a[1]) != (b[1] - a[1]) * (d[0] - a[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", type=Path, help="Compiled standard solution to compare")
    args = parser.parse_args()
    results = []
    for item in json.loads((HERE / "examples/inputs/manifest.json").read_text(encoding="utf8")):
        path = HERE / "examples/inputs" / item["file"]
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"], path
        n, roads, moves = read_case(path)
        assert (n, len(moves)) == (item["n"], item["moves"])
        check_forest(roads)
        answers, scans = count_with_bitsets(n, roads, moves)
        if item["expected_scans"] is not None:
            assert scans == item["expected_scans"], (path, scans)
        if len(roads) <= 200:
            assert answers == small_oracle(roads, moves), path
        check_obstruction(item["file"], roads, moves)
        if args.program:
            result = subprocess.run([str(args.program.resolve())], input=data, capture_output=True, check=True, timeout=30)
            assert list(map(int, result.stdout.split())) == answers, path
        results.append({"file": item["file"], "roads": len(roads), "moves": len(moves), "scans": scans})
    print(json.dumps({"verified": len(results), "program_compared": bool(args.program), "cases": results}, indent=2))


if __name__ == "__main__":
    main()
