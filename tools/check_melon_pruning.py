"""Verify melon pruning, block enumeration, and deterministic coverage bounds."""
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rank(adj, q):
    match = [-1] * q

    def augment(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if match[v] < 0 or augment(match[v], seen):
                match[v] = u
                return True
        return False

    return sum(augment(u, set()) for u in range(len(adj)))


def candidate_masks(adj, q):
    p = len(adj)
    upper = rank(adj, q)
    relevant = {v for row in adj for v in row}
    candidates = []
    for mask in range(1 << p):
        covered = {v for u, row in enumerate(adj) if mask >> u & 1 for v in row}
        required = {v for u, row in enumerate(adj) if not (mask >> u & 1) for v in row}
        if covered == relevant and len(required) <= mask.bit_count() < upper:
            candidates.append(mask)
    values = set(candidates)
    assert all(((1 << p) - 1) ^ mask not in values for mask in values)
    assert len(candidates) <= (1 << (p - 1))
    return upper, candidates


def terminal_masks(adj):
    masks = []

    def visit(u, occupied, selected):
        if u == len(adj):
            if all(selected >> x & 1 or all(v in occupied for v in row)
                   for x, row in enumerate(adj)):
                masks.append(selected)
            return
        visit(u + 1, occupied, selected)
        for v in adj[u]:
            if v not in occupied:
                visit(u + 1, occupied | {v}, selected | (1 << u))

    visit(0, set(), 0)
    return masks


def neighborhoods(adj, q):
    return [mask for v in range(q)
            if (mask := sum(1 << u for u, row in enumerate(adj) if v in row))]


def covering_masks(p, clauses):
    """Generate only complete assignments covering every clause, without a 2**p loop."""
    ending = [[] for _ in range(p)]
    for clause in clauses:
        ending[clause.bit_length() - 1].append(clause)

    def visit(u, mask):
        if u == p:
            yield mask
            return
        for selected in (False, True):
            value = mask | ((1 << u) if selected else 0)
            if all(value & clause for clause in ending[u]):
                yield from visit(u + 1, value)

    yield from visit(0, 0)


def block_pairs(p, a, b):
    """One representative per complementary pair, omitting the two bad block patterns."""
    assert a and b and not (a & b)
    anchor = a & -a  # Keep this bit zero in every representative.
    local = [1 << u for u in range(p) if ((1 << u) & (a | b)) and (1 << u) != anchor]
    free = [1 << u for u in range(p) if not ((1 << u) & (a | b))]
    for bits in range(1 << len(local)):
        chosen = sum(bit for i, bit in enumerate(local) if bits >> i & 1)
        if not (chosen & a) and (chosen & b) == b:
            continue  # Never enumerate the free suffix of this entire block.
        for tail in range(1 << len(free)):
            yield chosen | sum(bit for i, bit in enumerate(free) if tail >> i & 1)


def small_disjoint_pair(clauses):
    a = min(clauses, key=int.bit_count)
    choices = [b for b in clauses if not a & b]
    return (a, min(choices, key=int.bit_count)) if choices else None


def check_coverage(adj, q, candidates=None):
    p = len(adj)
    clauses = neighborhoods(adj, q)
    expected = {mask for mask in range(1 << p) if all(mask & c for c in clauses)}
    generated = list(covering_masks(p, clauses))
    assert len(generated) == len(set(generated)) and set(generated) == expected
    # Shearer with singleton padding, checked using exact integers.
    edges = sum(c.bit_count() for c in clauses)
    product = math.prod((1 << c.bit_count()) - 1 for c in clauses)
    assert len(expected)**4 <= (1 << (4*p - edges)) * product
    pair = small_disjoint_pair(clauses) if clauses else None
    if pair:
        a, b = pair
        reps = list(block_pairs(p, a, b))
        count = (1 << (p-1)) - (1 << (p-a.bit_count()-b.bit_count()))
        assert len(reps) == len(set(reps)) == count
        full = (1 << p) - 1
        represented = set(reps) | {full ^ mask for mask in reps}
        if candidates is not None:
            assert set(candidates) <= represented


def checkerboard(n, m):
    left = [(x, y) for x in range(n) for y in range(m) if (x+y) % 2 == 0]
    right = {(x, y): i for i, (x, y) in enumerate(
        (cell for cell in ((x, y) for x in range(n) for y in range(m)) if sum(cell) % 2))}
    adj = [[right[cell] for cell in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
            if cell in right] for x, y in left]
    return adj, len(right)


def check_large_structure():
    rng = random.Random(2026092904)
    tested = 0
    for p in (16, 17, 18, 24, 48, 96):
        for _ in range(100):
            # Four permutations ensure all p plots are relevant; degrees remain <= 4.
            permutations = [rng.sample(range(p), p) for _ in range(4)]
            adj = [sorted({perm[u] for perm in permutations}) for u in range(p)]
            clauses = neighborhoods(adj, p)
            a, b = small_disjoint_pair(clauses)
            assert a.bit_count() + b.bit_count() <= 8
            tested += 1
        for q in (p, 2*p, 4*p):
            for _ in range(100):
                adj = [rng.sample(range(q), rng.randrange(1, 5)) for _ in range(p)]
                clauses = neighborhoods(adj, q)
                if len(clauses) >= p:
                    a, b = small_disjoint_pair(clauses)
                    assert a.bit_count() + b.bit_count() <= 8
                tested += 1
    for n in range(1, 17):
        for m in range(1, 17):
            adj, q = checkerboard(n, m)
            p = len(adj)
            clauses = neighborhoods(adj, q)
            if p >= 10 and len(clauses) >= p:
                a, b = small_disjoint_pair(clauses)
                assert a.bit_count() + b.bit_count() <= 8
            tested += 1
    return tested


def dense_counts(n, m):
    adj, q = checkerboard(n, m)
    p = len(adj)
    upper = rank(adj, q)
    clauses = neighborhoods(adj, q)
    covered = 0
    candidates = 0
    for mask in covering_masks(p, clauses):
        covered += 1
        size = mask.bit_count()
        if size < upper and sum(bool(c & ~mask) for c in clauses) <= size:
            candidates += 1
    pair = small_disjoint_pair(clauses)
    r = sum(c.bit_count() for c in pair) if pair else None
    return dict(n=n, m=m, vines=p, plots=q, all_subsets=1 << p,
                covering_subsets=covered, necessary_condition_candidates=candidates,
                two_block_pairs=(1 << (p-1)) - (1 << (p-r)) if pair else None)


def main():
    largest = 0
    for edges in range(1 << 16):
        adj = [[v for v in range(4) if edges >> (4*u+v) & 1] for u in range(4)]
        _, candidates = candidate_masks(adj, 4)
        largest = max(largest, len(candidates))
        check_coverage(adj, 4, candidates)
    for edges in range(1 << 9):
        adj = [[v for v in range(3) if edges >> (3*u+v) & 1] for u in range(3)]
        upper, candidates = candidate_masks(adj, 3)
        terminals = terminal_masks(adj)
        optimum = min(mask.bit_count() for mask in terminals)
        reduced = min([upper] + [mask.bit_count() for mask in terminals if mask in candidates])
        assert optimum == reduced, adj
        for u in range(3):
            neighborhood = set(adj[u])
            remaining = [[v for v in row if v in neighborhood]
                         for x, row in enumerate(adj) if x != u]
            forced = rank(remaining, 3) < len(neighborhood)
            assert forced == all(mask >> u & 1 for mask in terminals), (adj, u)
    structure_checks = check_large_structure()
    report = {'complement_pair_graphs': 65536, 'optimality_and_forced_vertex_graphs': 512,
              'coverage_and_block_enumeration_graphs': 65536,
              'large_structure_graphs': structure_checks,
              'dense_boards': [dense_counts(n, m) for n, m in ((4, 4), (4, 6), (6, 6), (6, 8))],
              'largest_candidate_count_p4': largest, 'status': 'passed'}
    path = ROOT/'build/melon-pruning-audit.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
