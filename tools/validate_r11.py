"""Input, score-group and output contracts for R11."""
from pathlib import Path
import importlib.util
import re

PROBLEMS = (('trees', 'festival-plan'), ('trees', 'grinder'),
            ('graphs', 'tour-planning'),
            ('strings', 'magic-bread'), ('graphs', 'auto-wiring'),
            ('optimization', 'metro-delivery'))
GROUP_SHARES = {slug: (100,) for _, slug in PROBLEMS}
GROUP_SHARES['metro-delivery'] = (10, 20, 10, 20, 40)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('wiring_checker', ROOT/'topics/graphs/auto-wiring/tests/checker.py')
CHECKER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CHECKER)


def tree(path, downward):
    data = list(map(int, path.read_bytes().split()))
    n, low, high = data[:3]
    assert 1 <= n <= (500000 if downward else 300000)
    assert (1 if downward else 0) <= low <= high <= (n if downward else n-1)
    assert len(data) == 3+n+2*(n-1)
    values = data[3:3+n]
    assert all(-1000 <= v <= 1000 for v in values)
    parent = list(range(n))
    def find(u):
        while u != parent[u]:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    edges = data[3+n:]
    for u, v in zip(edges[::2], edges[1::2]):
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u-1), find(v-1)
        assert a != b
        parent[a] = b
    expected = None
    if path.stem == 'maximum-positive': expected = n*1000
    if path.stem == 'maximum-negative-single': expected = -1000
    return dict(n=n, L=low, R=high, expected_constant=expected)


def metro(path):
    data = list(map(int, path.read_bytes().split()))
    n, k = data[:2]
    assert 1 <= n <= 100000 and 0 <= k <= 500000000
    assert len(data) == 2+3*(n-1)
    nums, times, travel = data[2::3], data[3::3], data[4::3]
    assert all(0 <= x <= 100000 for x in nums+travel)
    assert all(0 <= x <= 1000000000 for x in times)
    expected = None
    if path.stem == 'no-reductions':
        assert k == 0
        arrival = quantity = production = total = 0
        for num, ready, distance in zip(nums, times, travel):
            if num: arrival = max(arrival, ready)
            arrival += distance
            quantity += num
            production += num*ready
            total += quantity*arrival-production
        expected = total % 1000000009
    if path.stem == 'one-sparse-goods':
        assert k == 1 and nums == [1]+[0]*(n-2) and times[0] == 0
        assert travel == [1]*(n-1)
        expected = ((n-1)*n//2-(n-1)) % 1000000009
    if path.stem == 'medium-zero-travel':
        assert not any(travel) and all(num == 0 or ready == 0 for num, ready in zip(nums, times))
        expected = 0
    if path.stem == 'maximum-overflow':
        assert nums == travel == [100000]*(n-1) and times == [1000000000]*(n-1)
        m = n-1
        b = min(k//100000, m)
        residual = min(k-b*100000, 100000)
        sum1 = lambda t: t*(t+1)//2
        sum2 = lambda t: t*(t+1)*(2*t+1)//6
        expected = (100000**2*(sum2(m)-sum2(b)-b*(sum1(m)-sum1(b)))
                    -100000*residual*(sum1(m)-sum1(b))) % 1000000009
    return dict(n=n, K=k, max_num=max(nums, default=0), max_time=max(times, default=0),
                max_travel=max(travel, default=0), zero_goods=not any(nums), expected_answer=expected)


def bread(path):
    tokens = path.read_bytes().split()
    assert len(tokens) == 3
    n, k = map(int, tokens[:2])
    text = tokens[2]
    assert 1 <= n <= 1000000 and 1 <= k <= 20
    assert len(text) == n and set(text) <= {48, 49}
    return dict(n=n, K=k)


def tour(path):
    data = list(map(int, path.read_bytes().split()))
    n, m = data[:2]
    assert 1 <= n <= 1000 and 1 <= m <= 5000 and len(data) == 2+3*m+5*n
    for i in range(m):
        u, v, w = data[2+3*i:5+3*i]
        assert 1 <= u <= n and 1 <= v <= n and u != v and abs(w) <= 1000000000
    travelers = 0
    for i in range(n):
        k, quantity, visits, capacity, price = data[2+3*m+5*i:7+3*m+5*i]
        assert 0 <= k <= 10 and 0 <= quantity <= 1000000000 and 0 <= capacity <= 1000000000
        assert 0 <= visits <= 30 and 0 <= price <= 30
        travelers += quantity
    return dict(n=n, m=m, travelers=travelers)


def wiring(path):
    data = list(map(int, path.read_bytes().split()))
    n, m = data[:2]
    assert 1 <= n <= 100000 and 1 <= m <= 200000 and len(data) == 2+n+2*m
    side = data[2:2+n]
    assert set(side) <= {0, 1}
    edges = data[2+n:]
    for u, v in zip(edges[::2], edges[1::2]):
        assert 1 <= u <= n and 1 <= v <= n and side[u-1] != side[v-1]
    return dict(n=n, m=m)


VALIDATORS = {'festival-plan': lambda p: tree(p, True), 'grinder': lambda p: tree(p, False),
              'metro-delivery': metro, 'tour-planning': tour, 'magic-bread': bread, 'auto-wiring': wiring}


def validate_group(slug, case, dimensions):
    group = case['group']
    if slug != 'metro-delivery':
        assert group == 1
        return
    if group == 1: assert dimensions['K'] == 0
    if group == 2: assert dimensions['K'] <= 1
    if group == 3:
        assert dimensions['n'] <= 50 and dimensions['K'] <= 50
        assert dimensions['max_num'] <= 50 and dimensions['max_time'] <= 500 and dimensions['max_travel'] <= 100
    if group == 4: assert dimensions['n'] <= 2000 and dimensions['K'] <= 2000


def check_wiring_tokens(input_path, actual, expected):
    data = list(map(int, input_path.read_bytes().split()))
    n, m = data[:2]
    assert actual and all(re.fullmatch(rb'\d+', token) for token in actual)
    count = int(actual[0])
    chosen = set(map(int, actual[1:]))
    assert count == len(actual)-1 == len(chosen) == int(expected[0])
    assert all(1 <= v <= n for v in chosen)
    edges = data[2+n:]
    assert all(u in chosen or v in chosen for u, v in zip(edges[::2], edges[1::2]))


def check_output(slug, path, dimensions):
    tokens = path.read_bytes().split()
    if slug == 'tour-planning' and b' '.join(tokens) == b'Negative loop found.':
        return
    assert all(re.fullmatch(rb'-?\d+', token) for token in tokens), path
    result = list(map(int, tokens))
    n = dimensions['n']
    if slug in ('festival-plan', 'grinder'):
        assert len(result) == n
        assert all(x == -1061109568 or abs(x) <= n*1000 for x in result)
        expected = dimensions['expected_constant']
        if expected is not None: assert all(x == expected for x in result)
    elif slug == 'magic-bread':
        assert len(result) == n and all(0 <= x < 1 << (n*dimensions['K']).bit_length() for x in result)
    elif slug == 'metro-delivery':
        assert len(result) == 1 and 0 <= result[0] < 1000000009
        if dimensions['zero_goods']: assert result[0] == 0
        if dimensions['expected_answer'] is not None: assert result[0] == dimensions['expected_answer']
    elif slug == 'tour-planning':
        assert len(result) == 1 and 0 <= result[0] <= dimensions['travelers']*900
    else:
        check_wiring_tokens(path.with_suffix('.in'), tokens, tokens)
