# A Certain Unscientific Polynomial-Weighted Geometric Sum with Updates — Alternative Solution

Codex (GPT-6) derived and implemented the moment recurrences and constant-time coefficient updates for this problem. See [alternative.cpp](alternative.cpp).

## Store all moments

For fixed current $n$ , define $S_j(n)=\sum_{i=1}^n a^i i^j$ . The answer is $\sum_jb_jS_j(n)$ . A single coefficient update adds $\Delta b_jS_j(n)$ in $O(1)$ time. Recompute moments only when the upper bound changes.

For $a\ne1$ , subtract shifted sums and expand $(i-1)^j$ to obtain

$$(1-a)S_j=a[ j=0]+\sum_{t=0}^{j-1}(-1)^{j-t+1}\binom jt S_t-a^{n+1}n^j.$$

In particular, $S_0=(a-a^{n+1})/(1-a)$ . Compute moments in increasing degree; do not omit the boundary term $a[j=0]$ . The same formula works for $a=0$ .

For $a=1$ , telescope $(i+1)^{j+1}-i^{j+1}$ to get

$$S_j=\frac{(n+1)^{j+1}-1-\sum_{t=0}^{j-1}\binom{j+1}{t}S_t}{j+1}.$$

Use precomputed modular inverses for division and multiplication to advance consecutive powers $n^j$ and $(n+1)^{j+1}$ .

## Correctness, Complexity, and Status

Both recurrences follow by finite-sum identities and depend only on lower moments. Induction proves every $S_j$ correct, and hence the inner product and incremental coefficient update are correct.

Let $q$ be the number of upper-bound updates. Binomial preprocessing takes $O(k^2)$ ; each recomputation takes $O(k^2+\log n+\log P)$ ; coefficient updates cost $O(1)$ ; space is $O(k^2)$ . Coefficient-heavy workloads avoid repeatedly maintaining a whole polynomial, but exclusively changing bounds gives $O(mk^2)$ work. The slowest five-run formal median was about 0.702 seconds, above the 0.5-second limit. This is a backup; use the [triangular-transform method](solution.en.md) for the complete range.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
