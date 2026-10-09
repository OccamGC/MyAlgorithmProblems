"""Generate deterministic two-household cases and check reference answers."""
from pathlib import Path
import argparse
import io
import json
import random
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oracle import MOD, expected_answer


def parse(text):
    stream = io.StringIO(text)
    first = stream.readline().split()
    if len(first) != 1:
        raise ValueError('expected test count')
    count = int(first[0])
    if not 1 <= count <= 100000:
        raise ValueError('test count out of range')
    rows = []
    for _ in range(count):
        pair = []
        for household in range(2):
            fields = stream.readline().split()
            if len(fields) != 2:
                raise ValueError('expected population and money on each household line')
            p, m = map(int, fields)
            if not (1 if household == 0 else 0) <= p <= 1000000 or not 0 <= m <= 1000000000:
                raise ValueError('household out of range')
            if p == 0 and m != 0:
                raise ValueError('empty household must have zero money')
            pair.extend((p, m))
        rows.append(tuple(pair))
    if stream.read().strip():
        raise ValueError('extra input')
    return rows


def validate(text, group=None):
    parse(text)


def as_text(rows):
    return str(len(rows)) + '\n' + ''.join(f'{k} {m1}\n{l} {m2}\n' for k,m1,l,m2 in rows)


def rows_for(c):
    if c['mode'] == 'literal':
        return [tuple(row) for row in c['rows']]
    if c['mode'] == 'small':
        return [(k,a,l,b) for k in range(1,13) for l in range(13)
                for a in range(9) for b in (range(9) if l else [0])]
    rng = random.Random(c['seed'])
    mode, n = c['mode'], c['n']
    if mode == 'boundary':
        pool = [(k,m1,l,m2) for k in [1,2,999999,1000000]
                for l in [0,1,2,999999,1000000] for m1 in [0,1,999999999,1000000000]
                for m2 in ([0] if l == 0 else [0,1,999999999,1000000000])]
        return [pool[i % len(pool)] for i in range(n)]
    if mode == 'rich-target':
        return [(k,1000000000,rng.randint(k,1000000),rng.randrange(1000000001))
                for k in (rng.randint(1,1000000) for _ in range(n))]
    if mode in ('even','odd'):
        pool = [1,2,3,999998,999999] + [rng.randint(1,999999) for _ in range(507)]
        return [(p,rng.randrange(1001),p+(mode == 'odd'),1000000000) for p in (rng.choice(pool) for _ in range(n))]
    if mode == 'unbalanced':
        pool = [(1,1000000),(1000000,1),(2,999999),(999999,2),(3,999998),(999998,3)]
        return [(k,rng.randrange(11),l,1000000000) for k,l in (rng.choice(pool) for _ in range(n))]
    pool = [(rng.randint(1,1000000),rng.randint(1,1000000)) for _ in range(4096)]
    if mode == 'large-rich':
        return [(k,rng.randrange(101),l,1000000000) for k,l in (rng.choice(pool) for _ in range(n))]
    if mode == 'near-equal':
        pool = [rng.randint(1000,999999) for _ in range(512)]
        rows = []
        for _ in range(n):
            k = rng.choice(pool)
            l = k + rng.choice([-1,0,1])
            unit, extra = rng.randrange(501), rng.randrange(501)
            rows.append((k,k*unit+extra,l,l*unit+max(0,extra+rng.choice([-1,0,1]))))
        return rows
    if mode == 'random':
        return [(k,rng.randrange(1000000001),l,rng.randrange(1000000001))
                for k,l in (rng.choice(pool) for _ in range(n))]
    raise ValueError('unknown recipe: '+mode)


def generate(c):
    return as_text(rows_for(c))


def make_case(c):
    rows = rows_for(c)
    return as_text(rows), ''.join(str(expected_answer(row))+'\n' for row in rows)


def matches(actual, expected):
    try:
        a, b = list(map(int,actual.split())), list(map(int,expected.split()))
        return a == b and all(0 <= x < MOD for x in a)
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case',action='append')
    parser.add_argument('--std',type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    ids = {c['id'] for c in plan['cases']}
    if args.case and not set(args.case) <= ids:
        parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:
            continue
        text,expected = make_case(c)
        validate(text,c['group'])
        path = args.out_dir/(c['id']+'.in')
        path.write_text(text,encoding='utf-8',newline='\n')
        if args.std:
            output = subprocess.check_output([str(args.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n')
            if not matches(output.decode(),expected):
                raise ValueError('incorrect reference output: '+c['id'])
            path.with_suffix('.out').write_bytes(output)


if __name__ == '__main__':
    main()
