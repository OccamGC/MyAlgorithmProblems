"""Exact small-state search and an independent optimal-schedule evaluator."""
from fractions import Fraction as F
from functools import lru_cache
from heapq import heappop, heappush

MOD = 1000000007


@lru_cache(None)
def search_factor(k, l):
    """All four move types, including repeated moves by either class."""
    if not (1 <= k <= 30 and 1 <= l <= 30):
        raise ValueError('exact state search supports populations 1..30')
    best = {(0, 0): F(1)}
    queue = [(F(-1), 0, 0)]
    while queue:
        neg, x, y = heappop(queue)
        value = -neg
        if value != best[x, y]:
            continue
        if (x, y) == (k, l):
            return value
        a = k - x + y
        b = k + l - a
        for nx, ny, count in [(x+1,y,b),(x-1,y,a),(x,y+1,a),(x,y-1,b)]:
            if not (0 <= nx <= k and 0 <= ny <= l):
                continue
            if k - nx + ny in (0, k+l):
                continue
            nv = value * F(count, count+1)
            if nv > best.get((nx, ny), F(0)):
                best[nx, ny] = nv
                heappush(queue, (-nv, nx, ny))
    return F(0)


def exact_answer(row):
    k, m1, l, m2 = row
    if l == 0 or m1*l >= m2*k:
        return F(m1)
    return F(k*(m1+m2), k+l) + F(k*l, k+l)*(F(m2,l)-F(m1,k))*search_factor(k,l)


def residue(value):
    return value.numerator % MOD * pow(value.denominator, -1, MOD) % MOD


def schedule_answer(row):
    """Apply bulk moves and generic 2x2 matrix squaring to actual household money."""
    k, m1, l, m2 = row
    if l == 0 or m1*l >= m2*k:
        return m1 % MOD
    n, h = k+l, (k+l)//2
    money = [m1 % MOD, m2 % MOD]

    def transfer(start, end):
        if start > end:
            remaining = money[0] * end * pow(start, -1, MOD) % MOD
            money[1] = (money[1] + money[0] - remaining) % MOD
            money[0] = remaining
        elif start < end:
            remaining = money[1] * (n-end) * pow(n-start, -1, MOD) % MOD
            money[0] = (money[0] + money[1] - remaining) % MOD
            money[1] = remaining

    def multiply(a, b):
        return [[sum(a[i][s]*b[s][j] for s in range(2)) % MOD for j in range(2)] for i in range(2)]

    transfer(k, h)
    incoming, leaving = pow(n-h, -1, MOD), pow(h+1, -1, MOD)
    up = [[1, incoming], [0, (1-incoming) % MOD]]
    down = [[(1-leaving) % MOD, 0], [leaving, 1]]
    matrix = multiply(down, up)
    power = min(k, l)
    while power:
        if power & 1:
            money = [sum(matrix[i][j]*money[j] for j in range(2)) % MOD for i in range(2)]
        matrix = multiply(matrix, matrix)
        power >>= 1
    transfer(h, l)
    return money[1]


@lru_cache(maxsize=8192)
def schedule_coefficients(k, l):
    other = schedule_answer((k, 0, l, 1))
    # Equal initial per-capita wealth is invariant under every moving schedule.
    target = (k - l * other) * pow(k, -1, MOD) % MOD
    return target, other


def expected_answer(row):
    k, m1, l, m2 = row
    if l == 0 or m1*l >= m2*k:
        return m1 % MOD
    if k <= 30 and l <= 30:
        return residue(exact_answer(row))
    c1, c2 = schedule_coefficients(k, l)
    return (c1*m1 + c2*m2) % MOD
