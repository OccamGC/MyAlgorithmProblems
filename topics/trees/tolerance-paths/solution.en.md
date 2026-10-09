# Solution

Contributions: Codex (GPT-6) completed the specification and supplied feasible-last-weight propagation, its proof, implementation, and verification.

## Each route follows the unique simple path

In a tree, a nonempty walk repeating a vertex must repeat an underlying edge. A legal route is therefore a simple path. For a fixed start and destination, only the choices of special edges along that unique path remain.

Sort and deduplicate the special weights on each tree edge. Root the tree at a chosen start. For every reachable vertex $u$ , store $S_u$ , the set of possible last-edge weights of legal routes from the root to $u$ .

The first edge is unrestricted, so every weight on an edge adjacent to the start is possible. For any later step from $u$ to child $v$ , retain candidate weight $w$ exactly when

$$S_u\cap[w-R_u,w-L_u]\ne\varnothing.$$

Binary-search the first element of sorted $S_u$ that is at least $w-R_u$ , then test whether it is at most $w-L_u$ . Scanning child weights in order also produces a sorted $S_v$ . An empty set means the entire descendant branch can be skipped.

## Correctness

Induct on depth. All first-edge choices are legal, so the first-layer sets are exact. Assuming $S_u$ is exact, a weight $w$ extends a legal path precisely when some $p\in S_u$ satisfies $L_u\le w-p\le R_u$ . This is exactly the interval-intersection condition. Thus $S_v$ contains every feasible weight and no infeasible weight. Vertices with nonempty sets are precisely the reachable vertices; include the start itself. Repeating this process for each start gives all answers.

Keeping only minimum and maximum weights is incorrect. If $S_u=\{0,2\}$ and the tolerance is $[0,0]$ , weight 1 cannot follow. Reachability also need not be symmetric: reversing a positive weight change may violate a positive tolerance.

## Complexity and implementation

Let $n$ be the vertex count and $m$ the special-edge count. Sorting costs $O(m\log(m+1))$ . For one start, each tree edge is visited at most once and each special weight is checked at most once, with a binary search costing $O(\log(m+1))$ . Total time is

$$O(m\log(m+1)+n(n+m\log(m+1))).$$

Each nonroot vertex's feasible set comes from its unique parent edge, so all such sets together have at most $m$ elements per traversal. Space is $O(n+m)$ . An explicit queue avoids recursion on long chains; use 64-bit arithmetic for weight differences and interval endpoints.

[std.cpp](std.cpp) implements the algorithm. Enumerating all edge choices is useful for small checks but can branch exponentially. Keeping interval endpoints is incorrect. Neither is a complete-data alternative.

## Measurements

Each formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.330252 seconds and peak memory is 6.05 MiB. Twice the median, rounded up to 0.5 seconds, gives a 1-second limit. See the [environment](../../../docs/评测环境与性能.md) and [individual measurements](../../../docs/benchmark-R34.json). Recalibrate in other environments.
