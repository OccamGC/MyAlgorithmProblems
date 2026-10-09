"""Deterministic recipes, exact small cases, and independent matrix-power checks."""
from pathlib import Path
from fractions import Fraction
import argparse
import io
import json
import random
import subprocess

MOD = 1000000007


def parse(text):
    lines = text.splitlines()
    if not lines or len(lines[0].split()) != 1:
        raise ValueError('expected n')
    n = int(lines[0])
    rows = [tuple(map(int, line.split())) for line in lines[1:] if line.strip()]
    if len(rows) != n or any(len(row) != 2 for row in rows):
        raise ValueError('expected exactly n pairs')
    return n, rows


def validate(text, group=None):
    stream = io.StringIO(text)
    first = stream.readline().split()
    if len(first) != 1:
        raise ValueError('expected n')
    n = int(first[0])
    if not 1 <= n <= 1000000:
        raise ValueError('n out of range')
    for i in range(n):
        row = stream.readline().split()
        if len(row) != 2:
            raise ValueError('expected p and m')
        p, m = map(int, row)
        if not 1 <= p <= (20 if i == 0 else 1000000) or not 1 <= m <= 1000000:
            raise ValueError('household out of range')
    if stream.read().strip():
        raise ValueError('extra input')


def residue(x):
    return x.numerator % MOD * pow(x.denominator, -1, MOD) % MOD


def literal(rows):
    k, money = rows[0]
    target = [Fraction(money, k)] * k
    others = sorted(Fraction(m, p) for p, m in rows[1:] for _ in range(p))
    for value in others:
        for i in range(k):
            if value > target[i]:
                target[i] = value = (value + target[i]) / 2
    return residue(sum(target))


def matrix_multiply(a, b):
    k = len(a)
    return [[sum(a[i][s] * b[s][j] for s in range(j, i+1)) % MOD if j <= i else 0
             for j in range(k)] for i in range(k)]


def grouped_matrix(rows):
    # Build the one-person averaging matrix from its literal coordinate update,
    # then apply generic matrix squaring. No binomial-tail formula is used.
    k, money = rows[0]
    initial = Fraction(money, k)
    counts = {}
    for p, m in rows[1:]:
        value = Fraction(m, p)
        if value > initial:
            counts[value] = counts.get(value, 0) + p
    if not counts:
        return money
    if len(counts) > 128:
        raise ValueError('matrix oracle is reserved for grouped recipes')
    half = (MOD+1)//2
    base = [[0]*k for _ in range(k)]
    for column in range(k):
        carry = 0
        for i in range(k):
            carry = (carry + int(i == column)) * half % MOD
            base[i][column] = carry
    powers = [base]
    for _ in range(max(counts.values()).bit_length()-1):
        powers.append(matrix_multiply(powers[-1], powers[-1]))
    target = [residue(initial)]*k
    for value, count in sorted(counts.items()):
        v = residue(value)
        delta = [(x-v) % MOD for x in target]
        bit = 0
        while count:
            if count & 1:
                delta = [sum(powers[bit][i][j]*delta[j] for j in range(i+1)) % MOD for i in range(k)]
            count >>= 1
            bit += 1
        target = [(x+v) % MOD for x in delta]
    return sum(target) % MOD


def rows_for(c):
    if c['mode'] == 'literal':
        return parse(c['input'])[1]
    rng = random.Random(c['seed'])
    n = c['n']
    rows = [(c['k'], c['money'])]
    mode = c['mode']
    if mode == 'poor':
        rows += [(rng.randint(20, 1000000), rng.randint(1, 1000000)) for _ in range(n-1)]
    elif mode == 'same':
        rows += [(p, p) for p in (rng.randint(1, 1000000) for _ in range(n-1))]
    elif mode == 'groups':
        for _ in range(n-1):
            g = rng.randrange(128 if c.get('around_one') else 64)
            numerator, denominator = (g+1, 64) if c.get('around_one') else (1001+g, 1+g)
            scale = rng.randint(1, 1000000//max(numerator, denominator))
            rows.append((denominator*scale, numerator*scale))
    elif mode == 'distinct':
        rows += [(p, 1000000) for p in range(2, n+1)]
    elif mode == 'random':
        rows += [(rng.randint(1, 1000000), rng.randint(500001, 1000000)) for _ in range(n-1)]
    elif mode == 'modulus':
        others = []
        for value, total in [(1, MOD-1), (2, MOD), (3, MOD+1)]:
            while total:
                people = min(total, 1000000//value)
                others.append((people, people*value))
                total -= people
        others += [(1000000, 1)]*(n-1-len(others))
        rng.shuffle(others)
        rows += others
    else:
        raise ValueError(mode)
    return rows


def as_text(rows):
    return str(len(rows))+'\n'+''.join(f'{p} {m}\n' for p, m in rows)


def generate(c):
    return as_text(rows_for(c))


def make_case(c):
    rows = rows_for(c)
    text = as_text(rows)
    if c['mode'] == 'literal':
        answer = literal(rows)
    elif c['mode'] == 'poor':
        answer = rows[0][1]
    elif c['mode'] in ['distinct', 'random']:
        # These deterministic full-size answers were cross-checked by both
        # published algorithms. They are not an independent exhaustive oracle.
        answer = c['expected']
    else:
        answer = grouped_matrix(rows)
    return text, str(answer)+'\n'


def matches(actual, expected):
    try:
        values = list(map(int, actual.split()))
        return len(values) == 1 and 0 <= values[0] < MOD and values == list(map(int, expected.split()))
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append')
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    ids = {c['id'] for c in plan['cases']}
    if args.case and not set(args.case) <= ids:
        parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:
            continue
        text, expected = make_case(c)
        validate(text, c['group'])
        path = args.out_dir/(c['id']+'.in')
        path.write_text(text, encoding='utf-8', newline='\n')
        if args.std:
            output = subprocess.check_output([str(args.std.resolve())], input=text.encode()).replace(b'\r\n', b'\n')
            if not matches(output.decode(), expected):
                raise ValueError(f'wrong reference output for {c["id"]}')
            path.with_suffix('.out').write_bytes(output)


if __name__ == '__main__':
    main()
