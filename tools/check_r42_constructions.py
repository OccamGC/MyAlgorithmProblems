"""Simulate legal single-resident moves for the two fixed-position constructions.

Every simulation checks exact rational wealth, conservation, identity, and the
final pure target household against the unrestricted adjacent-averaging bound.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random
import time

class Town:
    def __init__(self, rows, slots):
        self.groups = [set() for _ in range(slots)]
        self.money = [F(0) for _ in range(slots)]
        self.location = []
        self.original = []
        self.total = sum(m for _, m in rows)
        self.moves = 0
        for i, (p, m) in enumerate(rows):
            ids = list(range(len(self.location), len(self.location) + p))
            self.groups[i].update(ids)
            self.location.extend([i] * p)
            self.original.append(ids)
            self.money[i] = F(m)
        self.targets = set(self.original[0])

    def value(self, person):
        slot = self.location[person]
        return self.money[slot] / len(self.groups[slot])

    def move(self, person, dest):
        src = self.location[person]
        assert src != dest
        carried = self.value(person)
        self.groups[src].remove(person)
        self.groups[dest].add(person)
        self.money[src] -= carried
        self.money[dest] += carried
        self.location[person] = dest
        self.moves += 1
        assert sum(self.money) == self.total
        assert all(g or m == 0 for g, m in zip(self.groups, self.money))

    def target_sum(self):
        return sum(self.value(i) for i in self.targets)

    def gather(self):
        before = self.target_sum()
        mixed = [i for i, g in enumerate(self.groups) if g & self.targets and g - self.targets]
        if mixed:
            assert len(mixed) == 1 and len(self.groups[mixed[0]]) == 2
            slot = mixed[0]
            target = next(iter(self.groups[slot] & self.targets))
            other = next(iter(self.groups[slot] - self.targets))
            pure_t = [i for i,g in enumerate(self.groups) if g and g <= self.targets]
            if pure_t:
                self.move(target, pure_t[0])
            else:
                dest = next(i for i,g in enumerate(self.groups) if i != slot and not (g & self.targets))
                self.move(other, dest)
        dest = self.location[next(iter(self.targets))]
        for person in sorted(self.targets):
            if self.location[person] != dest:
                self.move(person, dest)
        assert self.groups[dest] == self.targets and self.money[dest] == before
        return before


def phi(rows):
    k, m = rows[0]
    values = [F(m, k)] * k
    for value in sorted(F(m,p) for p,m in rows[1:] for _ in range(p)):
        for i in range(k):
            if value > values[i]:
                values[i] = value = (value + values[i]) / 2
    return sum(values)


def few_outsiders(rows, n):
    q = sum(p for p, _ in rows[1:])
    assert n >= q + 2
    town = Town(rows, n)
    for ids in town.original[1:]:
        for person in ids[1:]:
            empty = next(i for i,g in enumerate(town.groups) if not g)
            town.move(person, empty)
    collection = next(i for i,g in enumerate(town.groups) if not g)
    initial = F(rows[0][1], rows[0][0])
    external = sorted((person for ids in town.original[1:] for person in ids), key=town.value)
    rich = [person for person in external if town.value(person) > initial]
    for target in town.original[0]:
        for outside in rich:
            town.move(target, town.location[outside])
        if town.location[target] != collection:
            town.move(target, collection)
    assert town.groups[collection] == town.targets
    answer = town.money[collection]
    assert answer == phi(rows), (rows, answer, phi(rows))
    return town.moves


def few_levels(rows, n):
    k, m1 = rows[0]
    initial = F(m1, k)
    rich = sorted(set(F(m,p) for p,m in rows[1:] if p and F(m,p) > initial))
    assert n >= k + len(rich) + 1
    town = Town(rows, n)
    destination = {}
    for i, (p,m) in enumerate(rows[1:], 1):
        if not p:
            continue
        value = F(m,p)
        key = value if value > initial else 'poor'
        if key not in destination:
            destination[key] = i
        else:
            for person in town.original[i]:
                town.move(person,destination[key])
    target_slots = [0]
    for person in town.original[0][1:]:
        empty = next(i for i,g in enumerate(town.groups) if not g)
        town.move(person,empty);target_slots.append(empty)
    collection = destination.get('poor')
    if collection is None:
        collection = next(i for i,g in enumerate(town.groups) if not g)
    for value in rich:
        source = destination[value]
        for person in sorted(town.groups[source]):
            for target_slot in target_slots:
                town.move(person,target_slot)
            town.move(person,collection)
    for person in town.original[0][1:]:
        town.move(person,0)
    assert town.groups[0] == town.targets
    assert town.money[0] == phi(rows), (rows, town.money[0], phi(rows))
    return town.moves


def dual_formula(rows):
    k,m1 = rows[0]
    a = F(m1,k)
    z = sorted(F(m,p)-a for p,m in rows[1:] for _ in range(p) if F(m,p)>a)
    if not z:
        return F(m1)
    coefficient = [F(1,2**k)]
    for d in range(1,len(z)):
        coefficient.append(coefficient[-1]*F(k+d-1,2*d))
    final = [sum(coefficient[i-j]*z[j] for j in range(i+1)) for i in range(len(z))]
    return m1 + sum(z) - sum(final)


def main():
    rng = random.Random(421003)
    start = time.perf_counter()
    counts = {'single_outsiders': 0, 'three_richer_levels': 0}
    moves = dict.fromkeys(counts, 0)
    initially_full = 0
    for _ in range(2000):
        k = rng.randint(1, 12)
        rows = [(k, rng.randrange(101))]
        rows += [(1, rng.randrange(101)) for _ in range(rng.randrange(13))]
        rows += [(0, 0)]
        moves['single_outsiders'] += few_outsiders(rows, len(rows))
        assert dual_formula(rows) == phi(rows)
        counts['single_outsiders'] += 1
    for _ in range(2000):
        k = rng.randint(1, 7)
        rows = [(k, rng.randrange(31))]
        levels = rng.sample([F(0), F(1,3), F(2,3), F(3,2), F(7,3), F(9)], 3)
        for _ in range(rng.randint(1, 16)):
            value = rng.choice(levels)
            scale = rng.randint(1, 3)
            rows.append((value.denominator*scale, value.numerator*scale))
        initial = F(rows[0][1], k)
        g = len({F(m,p) for p,m in rows[1:] if F(m,p) > initial})
        n = max(len(rows), k+g+1)
        initially_full += n == len(rows)
        rows += [(0,0)] * (n-len(rows))
        moves['three_richer_levels'] += few_levels(rows, n)
        counts['three_richer_levels'] += 1
    result = {'seed':421003, 'exact_constructive_cases':counts, 'legal_moves':moves,
              'level_cases_with_no_initial_empty':initially_full,
              'seconds':time.perf_counter()-start,
              'checks':['fixed slots','wealth conservation','empty-slot zero wealth',
                        'target identity','pure final target household',
                        'equality to unrestricted upper bound']}
    out = Path(__file__).resolve().parents[1]/'build/R42'
    out.mkdir(parents=True, exist_ok=True)
    (out/'constructive-checks.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
