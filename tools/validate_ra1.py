"""Input bounds, score groups and selected independent answers for batch R4."""
import importlib.util
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from check_ra1 import commando_brute, elite_brute


def validate_prism(path):
    lines = path.read_text(encoding='ascii').splitlines()
    n_text, block_limit_text, e_text, rounding_offset_text = lines[0].split()
    n, block_limit, e = int(n_text), int(block_limit_text), int(e_text)
    rounding_offset = Fraction(rounding_offset_text)
    assert 1 <= n <= 2000 and 0 <= e < n and 0 <= block_limit <= e
    assert 0 <= rounding_offset <= 1 and (rounding_offset * 100).denominator == 1
    assert len(lines) == e + 3
    parent = list(range(n))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    edges = []
    for line in lines[1:1+e]:
        u, v = map(int, line.split())
        assert 1 <= u <= n and 1 <= v <= n
        u -= 1
        v -= 1
        a, b = find(u), find(v)
        assert a != b
        parent[a] = b
        edges.append((u, v))
    damage = [Fraction(x) for x in lines[-2].split()]
    probabilities = [Fraction(x) for x in lines[-1].split()]
    assert len(damage) == len(probabilities) == n
    assert all(0 <= d <= 5000 and (100*d).denominator == 1 for d in damage)
    assert all(0 <= p <= 1 and (1000*p).denominator == 1 for p in probabilities)
    generator = Path(__file__).resolve().parents[1] / 'topics/trees/prism-tank/tests/generate.py'
    spec = importlib.util.spec_from_file_location('prism_generator', generator)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    value = module.expected_value(n, edges, list(map(float, damage)), list(map(float, probabilities)), block_limit > 0)
    z = value + float(rounding_offset)
    answer = math.floor(z + 0.5)
    assert abs(z - answer) <= 0.30000001
    return dict(n=n, block_limit=block_limit, e=e, shifted_expectation=z, expected_output=[str(answer)])


def validate_commando(path):
    lines = path.read_text(encoding='ascii').splitlines()
    m, xmin, ymin, xmax, ymax = map(int, lines[0].split())
    assert 1 <= m <= 30000 and len(lines) == m + 1
    assert all(abs(v) <= 10**8 for v in [xmin,ymin,xmax,ymax])
    assert 0 <= xmax-xmin <= 1000 and 0 <= ymax-ymin <= 1000
    operations = []
    queries = 0
    seen_query = False
    offline = True
    for line in lines[1:]:
        operation = list(map(int, line.split()))
        op = operation[0]
        assert op in (0,1,2) and len(operation) == (6 if op == 2 else 5)
        if op == 1:
            _, x, y, r, p = operation
            assert abs(x) <= 10**8 and abs(y) <= 10**8
            assert 1 <= r <= 10**8 and 0 <= p <= 10000
        else:
            _, x1,y1,x2,y2,*p = operation
            assert all(abs(v) <= 10**8 for v in [x1,y1,x2,y2])
            assert x1 <= x2 and y1 <= y2
            if p:
                assert 0 <= p[0] <= 10000
        if op == 0:
            seen_query = True
            queries += 1
        elif seen_query:
            offline = False
        operations.append(operation)
    result = dict(m=m, width=xmax-xmin+1, height=ymax-ymin+1,
                  min_span=min(xmax-xmin,ymax-ymin), offline=offline, query_count=queries)
    if result['width'] * result['height'] <= 400:
        result['expected_output'] = commando_brute((xmin,ymin,xmax,ymax),operations)
    return result


def elite_safe_order(types, counts, hp, attack, addition):
    """Independent scheduling oracle when every positive-type order is safe."""
    units = [(h,a,c,(h+attack-1)//attack) for (h,a),c in zip(types,counts) if c]
    harmful = [u for u in units if u[1] > 0]
    healers = [u for u in units if u[1] <= 0]
    positive_sum = sum(a*c for h,a,c,q in harmful)
    healing = sum(-a*c for h,a,c,q in healers)
    rounds = sum(c*q for h,a,c,q in harmful)
    assert positive_sum <= healing or hp > positive_sum * rounds
    best = 0
    for removed in [-1, *range(len(harmful))]:
        health = hp + (addition if removed == -1 else 0)
        remaining = [u for i,u in enumerate(harmful) if i != removed]
        incoming = sum(a*c for h,a,c,q in remaining) - healing
        # Smith's exchange rule, independently of subset DP and its peak formula.
        for h,a,c,q in sorted(remaining, key=lambda u: Fraction(u[3],u[1])):
            for _ in range(c):
                health -= (q-1) * incoming
                assert health > 0
                incoming -= a
                health -= incoming
                assert health > 0
        rate = healing
        health += sum(c*(q-1) for h,a,c,q in healers) * rate
        for h,a,c,q in sorted(healers, key=lambda u: -u[1]):
            for _ in range(c):
                rate += a
                health += rate
        best = max(best, health)
    return str(best)


def validate_elite(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    k,n,hp,attack,addition = map(int,lines[0].split())
    assert 1 <= k <= 5000 and 1 <= n <= 50000 and len(lines) == 1+k+n
    assert 1 <= hp <= 10**9 and 1 <= attack <= 10**5 and 0 <= addition <= 10**9
    names = {}
    types = []
    for line in lines[1:k+1]:
        name,h,a = line.split()
        h,a = int(h),int(a)
        assert 1 <= len(name.encode('utf-8')) <= 100 and not any(c.isspace() for c in name)
        assert name not in names and 1 <= h <= 10**5 and abs(a) <= 10**5
        names[name] = len(types)
        types.append((h,a))
    assert sum(a>0 for h,a in types) <= 20
    assert all(name in names for name in lines[k+1:])
    units = [names[name] for name in lines[k+1:]]
    count_map = Counter(units)
    counts = [count_map[i] for i in range(k)]
    if n <= 5 and sum((types[i][0]+attack-1)//attack for i in units) <= 30:
        answer = elite_brute(types, units, hp, attack, addition)
    elif path.stem == 'fatal':
        # Even after removal, at least one 100000-attack enemy survives a turn.
        assert hp == 1 and attack == 1 and addition == 0
        answer = 'leave!'
    else:
        answer = elite_safe_order(types, counts, hp, attack, addition)
    return dict(k=k,n=n,positive_types=sum(a>0 for h,a in types),expected_output=[answer])


VALIDATORS = {'prism-tank': validate_prism, 'psychic-commando': validate_commando,
              'elite-combatant': validate_elite}
GROUP_SHARES = {'prism-tank': (100,), 'psychic-commando': (20,20,20,20,20),
                'elite-combatant': (100,)}


def validate_group(slug, spec, dimensions):
    if slug == 'psychic-commando':
        group = spec['group']
        if group <= 4:
            assert dimensions['m'] <= 10000
        if group <= 2:
            assert dimensions['min_span'] <= (0 if group == 1 else 50)
        if group == 3:
            assert dimensions['offline']


def check_output(slug, output_path, dimensions):
    actual = output_path.read_text(encoding='ascii').split()
    if 'expected_output' in dimensions:
        assert actual == dimensions['expected_output'], (slug, output_path, actual, dimensions['expected_output'])
    else:
        assert slug == 'psychic-commando'
        assert len(actual) == dimensions['query_count']
        bound = dimensions['m'] * 10000 * dimensions['width'] * dimensions['height']
        assert all(abs(int(value)) <= bound for value in actual)
