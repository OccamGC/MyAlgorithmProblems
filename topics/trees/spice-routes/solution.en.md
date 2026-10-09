# Spice Routes: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: path classification for at most two high-price vertices.** Path classification exploits the limit of at most two high-price vertices and is used in the reference. Three-state tree DP also handles more high-price vertices, making it a peer method with wider scope. Both use $O(n+U)$ time and space, where $U$ is the largest input denominator.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the three-state tree DP method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [peer method editorial](solution-alternative.en.md).

## Complement event

A trade route exists exactly when a high-price vertex connects to a low-price vertex. Compute the probability that every high-price vertex fails to connect to any low-price vertex, then subtract it from one.

With no high-price vertex, return zero. With one, the main path below is its singleton path. With two, let their unique connecting path be $x_0,\ldots,x_t$ .

## Compressing attached branches

For a branch vertex $u$ , let $f_u$ be the probability that it cannot reach a low-price vertex through its branch. If $u$ is low-price, set $f_u=0$ ; otherwise

$$f_u=\prod_{v\text{ a branch child}}\bigl(q_{uv}+(1-q_{uv})f_v\bigr),$$

where $q_{uv}$ is the edge-failure probability. The edge is either closed, or open with the child still failing. These cases are disjoint, and different branches are independent.

Compute the same product at each main-path vertex, excluding main-path children. Its resulting $f_i$ describes failure through itself and its attached branches. The edge sets underlying different $f_i$ are disjoint.

## First and last closed edges

Let $q_i$ be the failure probability of $(x_i,x_{i+1})$ . Define

$$A_i=\prod_{k=0}^{i}f_k\prod_{k=0}^{i-1}(1-q_k),\qquad
B_i=\prod_{k=i}^{t}f_k\prod_{k=i}^{t-1}(1-q_k).$$

If the whole path is open, failure has probability $B_0$ . Otherwise let $i$ be the first closed edge from the left:

- If it is the only closed edge, the contribution is $A_iq_iB_{i+1}$ .
- If the last closed edge is $j>i$ , the contribution is $A_iq_iq_jB_{j+1}$ . Everything between these cuts is unrestricted and sums to probability one: that portion contains no high-price endpoint.

The total failure probability is therefore

$$B_0+\sum_{i=0}^{t-1}A_iq_i\left(B_{i+1}+\sum_{j=i+1}^{t-1}q_jB_{j+1}\right).$$

The unique first and last cuts make these cases disjoint and exhaustive. Precompute $B_i$ and the suffix sums, then update $A_i$ incrementally. A low-price vertex on the main path has $f_i=0$ , automatically eliminating invalid events. Overlapping high- and low-price vertices work the same way.

## Modular arithmetic and complexity

For $P=10^9+7$ , all input denominators are smaller than $P$ . Precompute inverses through $U$ and multiply each numerator by its denominator's inverse. Never divide by $f_i$ or an open-edge probability, so zero probabilities and certain failures/openings are valid.

Explicit traversals build the path and processing order. Branch products and prefix/suffix calculations are linear, giving $O(n+U)$ time and space.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
