# You Wrote This Problem Yourself: Solution

Contributions: Codex (GPT-6) completed the encoding specification and supplied the block-pair matrix, 2D Fenwick tree, per-value AVL position trees, proof, implementation, and verification.

## Full blocks and fringes

Let block length be $B$ and the number of blocks be $K=\lceil n/B\rceil$ . Let $c_b(v)$ count value $v$ in block $b$ . Maintain

$$F_{b,d}=\sum_v c_b(v)c_d(v).$$

This counts ordered equal-value pairs between blocks $b,d$ . Diagonal entries also count ordered pairs, including a position paired with itself. A 2D Fenwick tree supports point changes and rectangle sums on $F$ .

For each value, also keep its positions in an AVL tree augmented with subtree sizes. This supports counting its occurrences in a position interval. A node's key is its position; an update removes the node from the old value's tree and inserts it into the new value's tree. Ordered maps store per-block frequencies and the root for each value.

## Decomposing a query

Split the first interval into full blocks $I_0$ and fringe positions $I_1$ , and the second into $J_0,J_1$ . Each fringe has at most $2B$ positions. Partition the answer into three disjoint sets:

1. $I_0\times J_0$ : one matrix rectangle sum.
2. $I_1\times(J_0\cup J_1)$ : enumerate the first fringe and count matching values throughout the second interval using position trees.
3. $I_0\times J_1$ : enumerate the second fringe and count matching values only in the continuous position range covered by the first interval's full blocks.

This works even when the intervals overlap. Querying the entire first interval in the third step would double-count fringe pairs. When there are no full blocks, treat the whole interval as one fringe and process it once.

## Updating the matrix

Change one position in block $b$ from $x$ to $y$ . If $x=y$ , nothing changes. For $d\ne b$ , only row and column $b$ change, with increments

$$F_{b,d},F_{d,b}:\quad c_d(y)-c_d(x).$$

Update the diagonal only once, by

$$\bigl((c_b(x)-1)^2-c_b(x)^2\bigr)+\bigl((c_b(y)+1)^2-c_b(y)^2\bigr)=2(c_b(y)-c_b(x)+1).$$

Use frequencies from before the update. Change the matrix first, then the frequencies and position trees.

The matrix definition holds initially, and these formulas describe every update exactly. AVL insertion, deletion, and subtree sizes preserve the position counts. The three query terms partition all ordered pairs, proving the answer correct. Using that answer to decode the next operation completes an induction over the encrypted stream.

## Initialization, complexity, and implementation

Group occupied blocks and their frequencies by value. A value appearing in $d_v$ blocks contributes $d_v^2$ block pairs. Since $d_v\le K$ and $\sum_v d_v\le n$ , initialization needs at most $O(nK)$ such contributions, without enumerating position pairs.

Preprocessing takes $O(n\log n+nK+K^2\log^2(K+1))$ . An update costs $O(K(\log(B+1)+\log^2(K+1))+\log n)$ ; a query costs $O(B\log n+\log^2(K+1))$ . Space is $O(n+K^2)$ . The implementation uses $B=400$ , a time tradeoff that does not affect correctness.

[std.cpp](std.cpp) uses standard C++17 without an extension-based order-statistics tree. AVL rotations recompute both heights and subtree sizes. Matrix counts, answers, and encoded fields use 64-bit types. Negative values are decoded explicitly using the specified two's-complement rule, avoiding out-of-range unsigned-to-signed conversion.

Scanning each queried interval and counting frequencies is an independent checking model but costs $O(nm)$ in the worst case. A block matrix without position ranks leaves expensive fringe counting; offline Mo's algorithm cannot know queries that have not yet been decoded. These candidates are not complete-range alternatives.

## Measurements

Each formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.707113 seconds and peak memory is 30.11 MiB. Twice the median, rounded up to 0.5 seconds, gives a 1.5-second limit. See the [environment](../../../docs/评测环境与性能.md) and [individual measurements](../../../docs/benchmark-R34.json). Recalibrate in other environments.
