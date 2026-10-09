# Counting Sublattices: Alternative Solution

## Subset dynamic programming

Codex (GPT-6) supplied this method and [alternative.cpp](alternative.cpp). The setter's more space-efficient search is in the [main solution](solution.en.md).

Represent a set by a bitmask $M$ . Let $Need[M]$ be the union of the set itself and all join and meet results of its element pairs, also stored as a bitmask. Let $p$ be its least set-bit element and $R=M\setminus\{p\}$ . Then

$$Need[M]=Need[R]\cup\{p\}\cup\bigcup_{j\in R}\{p\lor j,p\land j\}$$

Start with $Need[0]=0$ and process masks in increasing order. Removing a set bit strictly decreases the mask, so the dependency is ready. Count a nonempty mask exactly when every set bit of `Need[Mask]` also occurs in `Mask` .

Pairs either lie wholly in $R$ or include $p$ . The first group is covered by $Need[R]$ , the loop covers the second, and operating on $p$ with itself returns $p$ . The recurrence therefore includes exactly all required results. Closure holds exactly when they all belong to the set, proving the test and count correct.

This stores results of one binary operation, not a repeatedly expanded closure. Compute $Need[R]$ even when $R$ is not closed: adding $p$ may supply its missing elements.

Each mask scans at most $n$ elements, for $O(n2^n)$ time. The 32-bit `Need` array and 8-bit single-bit-index lookup array use about $5\cdot2^n$ bytes. Including the operation table, space is $O(2^n+n^2)$ ; the two arrays use about $20$ MiB at maximum size. The largest measured median was about $0.085$ seconds, versus $0.444$ for the reference search. This is a measured constant-factor gain at an extra space cost; the original search retains its space advantage.
