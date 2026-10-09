# Clue Generator: Binary Search on Occurrences

Contribution: this keeps the setter's prefix-sum block decomposition. Codex (GPT-6) supplied complete block-interval answers, occurrence-list binary searches that remove the block-by-value count matrix, proofs and implementation. Binary search is classical. This is a parallel option to the [main solution](solution.en.md), supporting the same full range.

## Retained statistics and the omitted matrix

Convert zero-sum subarrays to equal-prefix position pairs, use block width $B=\lceil\sqrt{N+1}\rceil$ , and precompute every complete block-interval distance sum $H[s][t]$ . For each starting block, scan rightward and add the preceding occurrence count times the current index minus the preceding position sum. This takes $O(NK)$ time, where $K$ is the number of blocks.

For each value $v$ , retain only its sorted occurrence positions $J_v$ and local prefix sums $Z_v$ . Omit the matrix $C[b][v]$ . For complete middle interval $[F,G)$ , find

$$x=\operatorname{lower\_bound}(J_v,F),\qquad y=\operatorname{lower\_bound}(J_v,G).$$

Here $x,y$ are zero-based insertion indices. The count is $y-x$ and the position sum is $Z_v[y]-Z_v[x]$ . Store all lists contiguously in flat arrays, including a zero prefix per value, to avoid many small containers.

## Queries and correctness

Partition prefix-index interval $[L,R]$ into a complete middle and two fringes exactly as in the main solution. Use $H$ for middle pairs. A left-fringe position $i$ contributes $z-ci$ against the middle, and a right-fringe position contributes $ci-z$ . Scan both fringes in increasing order with temporary counts and position sums to add all fringe pairs. If the middle is empty, directly scan at most two blocks. Cache middle statistics once per visited value in a query, and clear only visited temporary entries afterward.

In a sorted occurrence list, positions at least $F$ and below $G$ occupy precisely insertion indices $x$ through $y-1$ . Thus binary search returns the same counts and sums as the matrix. The middle, cross and fringe pair classes remain disjoint and exhaustive. Together with the bijection between zero-sum subarrays and equal-prefix pairs, this proves the answer. Induction using each exact preceding answer also proves the decoding sequence correct.

## Complexity and tradeoff

Preprocessing takes $O(N\log N+NK)$ time. Each query takes $O(B\log(N+1))$ worst-case time, with $O(N+K^2)$ space. Square-root width makes space $O(N)$ , a clear reduction from the primary method's $O(N\sqrt N)$ matrix. Each binary search actually spans only one value's occurrences, and repeated fringe values reuse the cached result.

Use sixty-four-bit arithmetic for position sums, pair contributions, complete answers and XOR, with the bounds proved in the main solution. The program passes the full formal range. It is useful with tighter memory or poor cache behavior in a large block-by-value matrix; the main solution has a better worst-case query bound. See the [five-run measurements](../../../docs/benchmark-R26.json) for observed time and memory. A single distribution does not establish which method is faster for every input.

Program: [alternative.cpp](alternative.cpp). Every formal answer agrees with the primary method and independent Mo verification; small cases additionally use subarray enumeration.
