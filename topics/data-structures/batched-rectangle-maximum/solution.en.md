# Batch Updates, Then Build a Static Query Structure

Codex (GPT-6): combining two-dimensional differences with a compact static two-dimensional segment tree under the limit of 20 update runs, including proof, implementation, and verification. The primary program is [std.cpp](std.cpp). The setter's two-dimensional tree idea is used as a static query component; its incomplete cross-dimensional lazy propagation is not a valid dynamic solution.

## Processing Runs

There is no query inside an update run. Its additions commute, so accumulate them in a two-dimensional difference array. For a half-open rectangle $[x_1,x_2)\times[y_1,y_2)$ , add $v,-v,-v,v$ at its four corners. Corners beyond the bottom or right boundary can be omitted.

At the first following query, take two-dimensional prefix sums, add the resulting increments to the current cells, and clear the difference array. Rebuild the static rectangle-maximum structure once. Consecutive queries reuse it until the next update run. Queries at the beginning require one initial build; a final run without queries needs no materialization.

## Compact Two-Dimensional Segment Tree

A one-dimensional iterative tree stores $k$ leaves in $[k,2k)$ without rounding to a power of two. Use a $2n\times2m$ array. Leaf $(i+n,j+m)$ stores one cell. Build column trees within leaf rows, then merge rows. Each node stores the maximum over the Cartesian product of its represented row and column sets.

A query selects $O(\log(n+1))$ row nodes and queries a column interval in each, taking $O(\log(m+1))$ per node. Leaf order inside a numbered node may wrap, but the iterative interval procedure still selects disjoint leaf sets covering exactly the requested interval. Maximum is associative.

## Correctness

The prefix sum of one four-corner update contributes $v$ inside its rectangle and zero outside. By linearity, materialization produces exactly the effect of executing all updates in that run.

Leaves contain the true current values, and each merge takes the maximum of its two parts, so every stored maximum is correct. The row and column decompositions partition the queried rectangle; the maximum over their blocks is the answer. Rebuilding whenever pending updates exist ensures that every query sees the current matrix.

## Why the Cross-Dimensional Tags Are Insufficient

Two-dimensional lazy propagation must maintain both dimensions consistently. Temporarily passing a column node's tag to row children is insufficient. For example, start with a zero $2\times2$ matrix, add 1 twice to the entire first column, then query both columns of the first row. The answer is 2. The setter's dynamic attempt returns 0 because the first-column tag is not included correctly in this wider column query. This propagation defect does not invalidate the static merge invariant; only the static tree is used here.

## Complexity and Numeric Bounds

Let $U\le20$ be the number of update runs. Each update changes four corners. Total time is $O((U+1)nm+Q\log(n+1)\log(m+1))$ , with $O(nm)$ space.

Every cell has absolute value at most $20000+10^5\cdot20000=2000020000<2^{31}$ , so the tree stores signed 32-bit values. Differences and prefix intermediates use 64 bits. The main arrays occupy about $16nm+8nm=24nm$ bytes. Initialize query maxima to the minimum integer, not zero. Literal cell updates degenerate on large rectangles, while a four-dimensional sparse table uses too much space for ten million cells.

## Validation and Performance

Every formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 1.796455 seconds and its peak memory is 234.07 MiB. Twice the median, rounded up to 0.5 seconds, gives a 4-second reference limit.

See the [test guide](tests/README.md), [environment](../../../docs/评测环境与性能.md), and [individual timings and hashes](../../../docs/benchmark-R35.json). Recalibrate on other environments.
