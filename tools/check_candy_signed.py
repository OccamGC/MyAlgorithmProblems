"""Independent signed Candy Brackets oracle and focused regression checks."""
from array import array
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "topics/strings/candy-brackets"
WORK = ROOT / "build/candy-signed-20261001"
spec = importlib.util.spec_from_file_location("candy_validator", PACKAGE / "tests/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validate = validator.validate


def candy_oracle(text):
    """Offline parse into sibling atoms, then activate by insertion time.

    A matching substring is a consecutive run of complete atoms at one bracket
    level. An atom is a candy or an entire matched pair, with its raw total.
    Substrings inside an atom are covered independently at deeper levels.
    DSU joins only active adjacent siblings, never children with their parent.
    This does not use endpoint reductions or the wrapping-summary formula.
    """
    rows = text.splitlines()
    n, m = map(int, rows[0].split())
    length = n + m
    start = sum(int(row.split()[0]) == 0 for row in rows[3:])
    types = bytearray(length)
    weights = array("q", [0]) * length
    times = array("i", [0]) * length
    types[start:start+n] = bytearray(map(int, rows[1].split()))
    weights[start:start+n] = array("q", map(int, rows[2].split()))
    left, right = start, start + n
    for time, row in enumerate(rows[3:], 1):
        side, kind, weight = map(int, row.split())
        if side == 0:
            left -= 1
            index = left
        else:
            index = right
            right += 1
        types[index], weights[index], times[index] = kind, weight, time
    del rows

    previous = array("i")
    following = array("i")
    sums = array("q")
    event_next = array("i")
    event_head = array("i", [-1]) * (m + 1)
    openings = array("i")
    before = array("q")
    last = array("i", [-1])
    total = 0

    def atom(weight, time):
        index = len(sums)
        sums.append(weight)
        previous.append(last[-1])
        following.append(-1)
        if last[-1] != -1:
            following[last[-1]] = index
        last[-1] = index
        event_next.append(event_head[time])
        event_head[time] = index

    for index, kind in enumerate(types):
        prior = total
        total += weights[index]
        if kind == 0:
            openings.append(index)
            before.append(prior)
            last.append(-1)
        elif kind == 2:
            atom(weights[index], times[index])
        elif openings:
            opening = openings.pop()
            weight = total - before.pop()
            last.pop()
            atom(weight, max(times[opening], times[index]))
        else:
            # An unmatched closing bracket is a barrier between root atoms.
            last[-1] = -1
    del types, weights, times, openings, before, last

    count = len(sums)
    parent = array("i", [-1]) * count
    size = array("i", [1]) * count
    prefix = array("q", [0]) * count
    suffix = array("q", [0]) * count
    best = 0

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def join(a, b):
        nonlocal best
        a, b = find(a), find(b)
        if a == b:
            return
        best = max(best, suffix[a] + prefix[b])
        full = sums[a] + sums[b]
        pref = max(prefix[a], sums[a] + prefix[b])
        suff = max(suffix[b], sums[b] + suffix[a])
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        sums[a], prefix[a], suffix[a] = full, pref, suff

    answers = []
    for time in range(m + 1):
        index = event_head[time]
        while index != -1:
            parent[index] = index
            prefix[index] = suffix[index] = max(0, sums[index])
            best = max(best, prefix[index])
            if previous[index] != -1 and parent[previous[index]] != -1:
                join(previous[index], index)
            if following[index] != -1 and parent[following[index]] != -1:
                join(index, following[index])
            index = event_next[index]
        answers.append(str(best))
    return "\n".join(answers) + "\n"


def candy_brute(text):
    rows = text.splitlines()
    sequence = list(zip(map(int, rows[1].split()), map(int, rows[2].split())))

    def solve():
        best = 0
        for left in range(len(sequence)):
            balance = weight = 0
            for kind, value in sequence[left:]:
                balance += (1 if kind == 0 else -1 if kind == 1 else 0)
                weight += value
                if balance < 0:
                    break
                if balance == 0:
                    best = max(best, weight)
        return best

    answers = [solve()]
    for row in rows[3:]:
        side, kind, value = map(int, row.split())
        if side == 0:
            sequence.insert(0, (kind, value))
        else:
            sequence.append((kind, value))
        answers.append(solve())
    return "\n".join(map(str, answers)) + "\n"


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    alphabet = list(itertools.product(range(3), (-2, 0, 3)))
    exhaustive = 0
    for n in range(5):
        for sequence in itertools.product(alphabet, repeat=n):
            text = f"{n} 0\n" + " ".join(str(t) for t, _ in sequence) + "\n" + " ".join(str(w) for _, w in sequence) + "\n"
            assert candy_oracle(text) == candy_brute(text), text
            exhaustive += 1
    rng = random.Random(2026100201)
    for iteration in range(500):
        n, m = rng.randrange(15), 40
        values = (-4_000_000_000, -10, -1, 0, 1, 10, 4_000_000_000)
        text = f"{n} {m}\n" + " ".join(str(rng.randrange(3)) for _ in range(n)) + "\n" + " ".join(str(rng.choice(values)) for _ in range(n)) + "\n"
        text += "".join(f"{rng.randrange(2)} {rng.randrange(3)} {rng.choice(values)}\n" for _ in range(m))
        validate(text)
        expected = candy_brute(text)
        assert candy_oracle(text) == expected, (iteration, text)
        actual = subprocess.check_output([str(WORK / "std.exe")], input=text.encode("ascii")).decode().replace("\r\n", "\n")
        assert actual == expected, (iteration, text, actual, expected)
    samples = []
    for path in sorted((PACKAGE / "tests/samples").glob("*.in")):
        text = path.read_text(encoding="ascii")
        validate(text)
        expected = path.with_suffix(".out").read_text(encoding="ascii")
        assert candy_brute(text) == candy_oracle(text) == expected
        actual = subprocess.check_output([str(WORK / "std.exe")], input=text.encode("ascii")).decode().replace("\r\n", "\n")
        assert actual == expected
        samples.append(path.stem)
    for invalid in ["1 0\n2\n-4000000001\n", "1 0\n2\n4000000001\n", "0 1\n\n\n2 2 0\n", "1 0\n3\n0\n", "0 0\n"]:
        try:
            validate(invalid)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError(("accepted invalid input", invalid))
    for text, group in [("1 0\n2\n-1\n", 2), ("1 0\n0\n0\n", 3)]:
        try:
            validate(text, group)
        except AssertionError:
            pass
        else:
            raise AssertionError(("accepted invalid group", text, group))
    report = dict(offline_oracle_exhaustive_strings=exhaustive,
                  random_cpp_and_oracle_batches=500, random_updates=20_000,
                  samples=samples, invalid_input_checks=7)
    (WORK / "checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
