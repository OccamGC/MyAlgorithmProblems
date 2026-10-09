"""Small independent differential checks for compiled reference programs."""

import itertools
import argparse
import os
import random
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "build" / "bin"
RNG = random.Random(20190709)


def run(slug, data):
    program = BIN / (slug + (".exe" if os.name == "nt" else ""))
    result = subprocess.run(
        [str(program)], input=data.encode("ascii"), capture_output=True, check=True
    )
    return [int(token) for token in result.stdout.split()]


def check_candy():
    for _ in range(250):
        text = "".join(RNG.choices("01", k=RNG.randint(1, 16)))
        patterns = [
            "".join(RNG.choices("01", k=RNG.randint(1, 6)))
            for _ in range(RNG.randint(0, 8))
        ]
        dp = [0] * (len(text) + 1)
        for i in range(len(text) - 1, -1, -1):
            dp[i] = dp[i + 1]
            for pattern in patterns:
                if text.startswith(pattern, i):
                    dp[i] = max(dp[i], 1 + dp[i + len(pattern)])
        data = "\n".join([str(len(patterns)), text, *patterns]) + "\n"
        assert run("eating-candy", data) == [dp[0]], data
    return 250


def all_tree_costs(n, edges):
    costs = []
    for chosen in itertools.combinations(edges, n - 1):
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for u, v, _ in chosen:
            a, b = find(u), find(v)
            if a == b:
                break
            parent[a] = b
        else:
            costs.append(sum(w for _, _, w in chosen))
    return sorted(set(costs))


def check_graph():
    checked = 0
    while checked < 250:
        n = RNG.randint(2, 6)
        m = RNG.randint(n, min(10, n + 5))
        edges = []
        for v in range(2, n + 1):
            edges.append((RNG.randint(1, v - 1), v, RNG.randint(1, 7)))
        while len(edges) < m:
            u, v = RNG.sample(range(1, n + 1), 2)
            edges.append((u, v, RNG.randint(1, 7)))
        costs = all_tree_costs(n, edges)
        if len(costs) < 2:
            continue
        data = f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
        assert run("bridge-tales-no-first-plan", data) == [costs[1]], data
        checked += 1
    return checked


def longest_star_segment(sequence):
    best = 0
    for left in range(len(sequence)):
        balance = 0
        for right in range(left, len(sequence)):
            balance += (sequence[right] == "<") - (sequence[right] == ">")
            if balance < 0:
                break
            if balance == 0:
                best = max(best, right - left + 1)
    return best


def check_star():
    for _ in range(250):
        initial = RNG.choices("<>*", k=RNG.randint(0, 9))
        sequence = initial.copy()
        m = RNG.randint(0, 7)
        expected = [longest_star_segment(sequence)]
        operations = []
        for _ in range(m):
            side = RNG.randint(1, 2)
            mark = RNG.choice("<>*")
            operations.append((side, mark))
            if side == 1:
                sequence.insert(0, mark)
            else:
                sequence.append(mark)
            expected.append(longest_star_segment(sequence))
        data = f"{len(initial)} {m}\n" + " ".join(initial) + "\n"
        data += "".join(f"{side} {mark}\n" for side, mark in operations)
        assert run("build-a-big-star", data) == expected, data
    return 250


def check_badges():
    for _ in range(250):
        n = RNG.randint(1, 8)
        m = RNG.randint(1, 12)
        accepted = []
        expected = []
        requests = [(RNG.randint(1, n), RNG.randint(1, n)) for _ in range(m)]
        for edge in requests:
            candidate = accepted + [edge]
            valid_masks = [
                mask for mask in range(1 << n)
                if all(((mask >> (u - 1)) ^ (mask >> (v - 1))) & 1 for u, v in candidate)
            ]
            if valid_masks:
                accepted = candidate
            else:
                valid_masks = [
                    mask for mask in range(1 << n)
                    if all(((mask >> (u - 1)) ^ (mask >> (v - 1))) & 1 for u, v in accepted)
                ]
            expected.extend((int(bool(valid_masks) and accepted == candidate), max(n - mask.bit_count() for mask in valid_masks)))
        data = f"{n} {m}\n" + "".join(f"{u} {v}\n" for u, v in requests)
        assert run("two-color-badges", data) == expected, data
    return 250


def check_platform():
    for _ in range(250):
        L = RNG.randint(1, 15)
        N = RNG.randint(1, min(6, L + 1))
        M = RNG.randint(1, 6)
        doors = [0, *sorted(RNG.sample(range(1, L + 1), N - 1))]
        passengers = sorted(RNG.randint(0, L) for _ in range(M))
        upper = 2 * (L - doors[-1])
        values = [
            sum(min(abs(2 * position - start - 2 * door) for door in doors) for position in passengers)
            for start in range(upper + 1)
        ]
        maximum = max(values)
        best_start = values.index(maximum)
        data = f"{L}\n{M}\n" + " ".join(map(str, passengers)) + f"\n{N}\n"
        if N > 1:
            data += " ".join(map(str, doors[1:])) + "\n"
        program = BIN / ("passengers-need-exercise" + (".exe" if os.name == "nt" else ""))
        output = subprocess.run([str(program)], input=data.encode("ascii"), capture_output=True, check=True).stdout.decode().split()
        expected = [f"{best_start // 2}.{5 if best_start % 2 else 0}", f"{maximum // 2}.{5 if maximum % 2 else 0}"]
        assert output == expected, (data, output, expected)
    return 250


def check_trail():
    for _ in range(250):
        n = RNG.randint(2, 12)
        parents = [0, 0]
        parents.extend(RNG.randint(1, v - 1) for v in range(2, n + 1))
        children = [[] for _ in range(n + 1)]
        for v in range(2, n + 1):
            children[parents[v]].append(v)
        leaves = [v for v in range(2, n + 1) if not children[v]]
        path_masks = []
        for leaf in leaves:
            mask = 0
            v = leaf
            while v != 1:
                mask |= 1 << (v - 2)
                v = parents[v]
            path_masks.append(mask)
        # Enumerate leaf subsets independently of the heavy-chain algorithm.
        coverage = [0] * (1 << len(leaves))
        best = [0] * (len(leaves) + 1)
        for subset in range(1, len(coverage)):
            bit = subset & -subset
            coverage[subset] = coverage[subset ^ bit] | path_masks[bit.bit_length() - 1]
            k = subset.bit_count()
            best[k] = max(best[k], coverage[subset].bit_count())

        # Check that optimal subsets can be nested into one daily schedule.
        reachable = {0}
        for subset in range(1, len(coverage)):
            if coverage[subset].bit_count() != best[subset.bit_count()]:
                continue
            if any(subset ^ (1 << i) in reachable
                   for i in range(len(leaves)) if subset & (1 << i)):
                reachable.add(subset)
        assert len(coverage) - 1 in reachable, parents
        expected = [len(leaves), *best[1:]]

        # Input labels and edge order need not follow the rooted traversal.
        labels = [1, *RNG.sample(range(2, n + 1), n - 1)]
        edges = [(labels[parents[v] - 1], labels[v - 1]) for v in range(2, n + 1)]
        RNG.shuffle(edges)
        edges = [edge if RNG.randrange(2) else edge[::-1] for edge in edges]
        data = f"{n}\n" + "".join(f"{u} {v}\n" for u, v in edges)
        assert run("forest-ranger", data) == expected, (data, expected)
    return 250


def check_encore():
    program = BIN / ("just-a-little-more" + (".exe" if os.name == "nt" else ""))
    for _ in range(250):
        initial = "".join(RNG.choices("abcd", k=RNG.randint(1, 10)))
        queries = [RNG.randint(1, 35) for _ in range(RNG.randint(1, 10))]
        versions = [initial]
        for _ in range(1, max(queries)):
            previous = versions[-1]
            versions.append(previous + previous[:(len(previous) + 4) // 5])
        data = initial + f"\n{len(queries)}\n" + "\n".join(map(str, queries)) + "\n"
        result = subprocess.run([str(program)], input=data.encode(), capture_output=True, check=True)
        assert result.stdout.decode().splitlines() == [versions[x - 1] for x in queries], data
    return 250


def check_weak_link():
    for _ in range(250):
        n = RNG.randint(1, 18)
        a = [RNG.randint(-10, 10) for _ in range(n)]
        b = [RNG.randint(-10, 10) for _ in range(n)]
        answer = None
        for l in range(n):
            minimum = a[l]
            total = 0
            for r in range(l, n):
                minimum = min(minimum, a[r])
                total += b[r]
                product = minimum * total
                answer = product if answer is None else max(answer, product)
        data = f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"
        assert run("weak-link-comeback", data) == [answer], data
    return 250


def cookie_flow(demand, supply):
    # Independent Edmonds-Karp network; no interval-summary formula is used.
    n = len(demand)
    sink = 2 * n + 1
    capacity = [[0] * (sink + 1) for _ in range(sink + 1)]
    for i in range(n):
        capacity[0][1 + i] = supply[i]
        capacity[1 + n + i][sink] = demand[i]
        for j in range(n):
            if i != j:
                capacity[1 + i][1 + n + j] = sum(supply) + 1
    flow = 0
    while True:
        parent = [-1] * (sink + 1)
        parent[0] = 0
        queue = [0]
        for u in queue:
            for v, residual in enumerate(capacity[u]):
                if residual > 0 and parent[v] == -1:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            return flow
        amount = sum(supply) + 1
        v = sink
        while v != 0:
            amount = min(amount, capacity[parent[v]][v])
            v = parent[v]
        v = sink
        while v != 0:
            u = parent[v]
            capacity[u][v] -= amount
            capacity[v][u] += amount
            v = u
        flow += amount


def check_cookies():
    for _ in range(250):
        n = RNG.randint(1, 7)
        m = RNG.randint(1, 20)
        demand = [RNG.randint(0, 5) for _ in range(n)]
        supply = [RNG.randint(0, 5) for _ in range(n)]
        data = f"{n} {m}\n" + " ".join(f"{c} {p}" for c, p in zip(demand, supply)) + "\n"
        expected = []
        for _ in range(m):
            operation = RNG.randint(1, 3)
            if operation == 3:
                l, r = sorted((RNG.randint(1, n), RNG.randint(1, n)))
                data += f"3 {l} {r}\n"
                expected.append(cookie_flow(demand[l - 1:r], supply[l - 1:r]))
            else:
                x = RNG.randint(1, n)
                value = RNG.randint(0, 5)
                data += f"{operation} {x} {value}\n"
                (demand if operation == 1 else supply)[x - 1] = value
        assert run("cookie-swap", data) == expected, data
    return 250


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"), default="R1")
    args = parser.parse_args()
    if args.batch == "R12":
        from check_r12 import main as check_batch
        check_batch()
        return
    if args.batch == "R11":
        from check_r11 import main as check_batch
        check_batch()
        return
    if args.batch == "R10":
        from check_r10 import main as check_batch
        check_batch()
        return
    if args.batch == "R9":
        from check_r9 import main as check_batch
        check_batch()
        return
    if args.batch == "R8":
        from check_r8 import main as check_batch
        check_batch()
        return
    if args.batch == "R7":
        from check_r7 import main as check_batch
        check_batch()
        return
    if args.batch == "R6":
        from check_r6 import main as check_batch
        check_batch()
        return
    if args.batch == "R5":
        from check_ra2 import check_drone, check_virus, check_chrono
        for label, check in (("drone", check_drone), ("virus", check_virus), ("chrono", check_chrono)):
            print(f"{label}: {check()} compiled-program comparisons passed", flush=True)
        return
    if args.batch == "R4":
        from check_ra1 import check_prism, check_commando, check_elite
        for label, check in (("prism", check_prism), ("commando", check_commando), ("elite", check_elite)):
            print(f"{label}: {check()} compiled-program comparisons passed", flush=True)
        return
    checks = (
        ("candy", check_candy),
        ("graph", check_graph),
        ("star", check_star),
    ) if args.batch == "R1" else ((
        ("badges", check_badges),
        ("platform", check_platform),
        ("trail", check_trail),
    ) if args.batch == "R2" else (
        ("encore", check_encore),
        ("weak-link", check_weak_link),
        ("cookies", check_cookies),
    ))
    for label, check in checks:
        print(f"{label}: {check()} compiled-program comparisons passed", flush=True)


if __name__ == "__main__":
    main()
