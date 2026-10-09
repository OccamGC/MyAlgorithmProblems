"""Input contracts and score groups for the two new melon problems."""
import re

PROBLEMS = (('graphs', 'melon-planting-2'), ('dynamic-programming', 'melon-planting-3'))
GROUP_SHARES = {slug: (20, 30, 50) for _, slug in PROBLEMS}


def graph(path):
    lines = path.read_text(encoding='ascii').splitlines()
    p, q = map(int, lines[0].split())
    assert 0 <= p <= 24 and 1 <= q <= 96 and len(lines) == p + 1
    edges = 0
    for line in lines[1:]:
        values = list(map(int, line.split()))
        degree, row = values[0], values[1:]
        assert 0 <= degree <= 4 and len(row) == degree == len(set(row))
        assert all(1 <= v <= q for v in row)
        edges += degree
    expected = None
    if edges == 0:
        expected = 0
    elif path.stem == 'maximum-private':
        expected = p
    elif path.stem in ('eighteen-cycle', 'maximum-cycle'):
        expected = (2 * p + 2) // 3
    return dict(p=p, q=q, edges=edges, expected=expected)


def grid(path):
    lines = path.read_text(encoding='ascii').splitlines()
    n, m = map(int, lines[0].split())
    assert 1 <= n and 1 <= m and n * m <= 5000 and min(n, m) <= 8
    rows = lines[1:]
    assert len(rows) == n and all(len(row) == m and set(row) <= set('lox') for row in rows)
    p = sum(row.count('l') for row in rows)
    expected = None
    if p == 0 or not any('o' in row for row in rows):
        expected = 0
    elif path.stem == 'long-row':
        expected = (n * m + 1) // 3
    elif path.stem in ('long-column-pairs', 'maximum-pairs'):
        expected = n * m // 4
    elif path.stem == 'striped-board':
        expected = m * ((n + 1) // 3)
    return dict(n=n, m=m, p=p, expected=expected)


VALIDATORS = {'melon-planting-2': graph, 'melon-planting-3': grid}


def validate_group(slug, spec, dimensions):
    group = spec['group']
    if slug == 'melon-planting-2':
        assert dimensions['p'] <= (10, 18, 24)[group - 1]
    else:
        assert min(dimensions['n'], dimensions['m']) <= (1, 4, 8)[group - 1]


def check_output(slug, path, dimensions):
    tokens = path.read_bytes().split()
    assert len(tokens) == 1 and re.fullmatch(rb'\d+', tokens[0]), path
    answer = int(tokens[0])
    assert 0 <= answer <= dimensions['p'], path
    if dimensions['expected'] is not None:
        assert answer == dimensions['expected'], (path, answer, dimensions['expected'])
