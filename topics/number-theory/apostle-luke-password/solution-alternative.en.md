# Apostle Luke's Password — Alternative Solution

Setter method: factorial reduction and nine-base Miller–Rabin. Codex (GPT-6): safe modular multiplication, boundary and deterministic proofs, and the progression-sieve alternative.

## Sieve composites in an arithmetic progression

Let $P=kG+b$ , $U=P+k(N-1)$ , and $B=\lfloor\sqrt U\rfloor$ . Use the sieve of Eratosthenes to enumerate primes $q\le B$ , then mark terms $P+ki$ divisible by each $q$ .

- If $q\mid k$ but $q\nmid P$ , there are no such terms.
- If $q\mid k$ and $q\mid P$ , every term is divisible.
- Otherwise use extended Euclid to invert $k$ modulo $q$ . Solve $i\equiv-Pk^{-1}\pmod q$ and mark indices spaced by $q$ , starting with the least nonnegative solution.

**Do not mark a term equal to $q$**: it is the prime itself. Handle $0,1$ separately and count every other unmarked argument. Correct the initial floating-point square-root estimate in both directions using integer squares; these squares fit in 64 bits.

## Correctness and Complexity

Every marked argument greater than one has a proper prime divisor and is composite. Conversely, any composite $p\le U$ has a prime divisor $q\le\sqrt p\le B$ . The congruence cases enumerate its index, so it is marked. Prefix accumulation is unchanged.

A convenient upper bound is $O((B+N)\log U)$ time. The initial sieve costs $O(B\log\log B)$ ; each inverse costs $O(\log U)$ . Nondividing primes cause at most $N\sum_{q\le B}1/q+O(B)$ marking steps, while at most $O(\log U)$ distinct primes divide the step. The bit arrays occupy $O(B+N)$ bits, with constant additional integers.

This gives independent verification without relying on a fixed-base pseudoprime bound. Setup and inverses are often more expensive in this task, but five-run formal measurements fit the published limit. Codex (GPT-6) supplied the method and [alternative.cpp](alternative.cpp). See the [standard solution](solution.en.md) for the shared algebraic reduction.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
