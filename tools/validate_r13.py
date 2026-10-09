"""Input constraints and output checks for R13."""
from collections import Counter
from pathlib import Path
from check_r13 import PROBLEMS
from validate_r12 import Forest, read_line

GROUP_SHARES = {slug:(100,) for _,slug in PROBLEMS}


def validate(slug, path):
    with Path(path).open(encoding='ascii') as stream:
        if slug == 'catalyst-sequence':
            n, = read_line(stream,1)
            assert 1 <= n <= 100000
            a = read_line(stream,n)
            assert all(1 <= v <= 250000 for v in a)
            result = dict(n=n,upper=max(a),outputs=max(a))
        elif slug == 'equipment-amplification':
            q, = read_line(stream,1)
            assert 1 <= q <= 100
            values = []
            for _ in range(q):
                row = stream.readline().strip()
                assert row.isascii() and row.isdigit()
                value = int(row)
                assert 0 <= value < 10**30
                values.append(value)
            result = dict(q=q,maximum=max(values),outputs=q)
        elif slug == 'grox-sequence-2':
            n, = read_line(stream,1)
            assert 0 <= n <= 100000
            result = dict(n=n,outputs=3)
        elif slug == 'grox-sequence-3':
            n,q = read_line(stream,2)
            assert 0 <= n <= 5000 and 1 <= q <= 200000
            for _ in range(q):
                a,b = read_line(stream,2)
                assert 0 <= a <= 5000 and 0 <= b <= 5000
            result = dict(n=n,q=q,outputs=q)
        elif slug == 'spode-seminary':
            n,m,q = read_line(stream,3)
            assert 1 <= n <= 1000 and 1 <= m <= 1000 and 1 <= q <= 10
            assert all(0 <= v <= m for v in read_line(stream,n))
            assert all(0 <= v <= 1000 for v in read_line(stream,m))
            for _ in range(n):
                row = read_line(stream,m)
                assert all(v == -1 or 1 <= v <= m for v in row)
                assert all(count <= 3 for tier,count in Counter(row).items() if tier != -1)
            for _ in range(q):
                assert sorted(read_line(stream,n)) == list(range(1,n+1))
            result = dict(n=n,m=m,q=q,outputs=2*n*q)
        elif slug == 'hagen-farm':
            n, = read_line(stream,1)
            assert 1 <= n <= 2000
            tree = Forest(n)
            for _ in range(n-1):
                a,b,w = read_line(stream,3)
                assert 1 <= a <= n and 1 <= b <= n and 0 <= w <= 10000
                tree.join(a,b)
            result = dict(n=n,outputs=1)
        else:
            raise ValueError(slug)
        assert not stream.read().strip(), 'trailing input'
        return result


def validate_group(slug, spec, dimensions):
    assert spec['group'] == 1 and spec['score_percent'] > 0
    for key in ('n','m','q','upper'):
        if key in spec:
            assert spec[key] == dimensions[key], (slug,key,spec,dimensions)


def check_output(slug, path, dimensions):
    values = list(map(int,Path(path).read_text(encoding='ascii').split()))
    assert len(values) == dimensions['outputs']
    if slug == 'catalyst-sequence':
        assert all(v == 0 or 2 <= v <= dimensions['n'] for v in values)
    elif slug == 'equipment-amplification':
        assert all(1 <= v <= 715704 for v in values)
    elif slug == 'spode-seminary':
        n,m = dimensions['n'],dimensions['m']
        for k in range(dimensions['q']):
            assert all(v == -1 or 1 <= v <= m for v in values[2*k*n:(2*k+1)*n])
            assert all(-1 <= v < n for v in values[(2*k+1)*n:(2*k+2)*n])
    else:
        modulus = {'grox-sequence-2':1004535809,'grox-sequence-3':921260340,'hagen-farm':1000000007}[slug]
        assert all(0 <= v < modulus for v in values)
        if slug == 'grox-sequence-2':
            assert values[1] == values[2]


VALIDATORS = {slug:(lambda path,slug=slug:validate(slug,path)) for _,slug in PROBLEMS}
