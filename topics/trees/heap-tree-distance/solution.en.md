# Infinite Binary Tree Distances: Move the Larger Label Up

Problem setter's solutions: move the larger label to its parent, or align depths as described in the teaching notes. Codex (GPT-6): integer implementations, correctness proofs and large-label validation.

## Algorithm

The parent of a non-root vertex $v$ is $\lfloor v/2\rfloor$ . While $a\ne b$ , replace the larger endpoint label by its parent and increase the answer by one. Stop when the endpoints coincide.

## Why the meeting point is never crossed

The graph is a tree rooted at $1$ : every other vertex has exactly one smaller parent, and repeated parent steps reach the root. The unique simple path between two vertices passes through their lowest common ancestor.

If currently $a>b$ , then $a$ cannot be an ancestor of $b$ , because a proper ancestor has a strictly smaller label. Thus $a$ has not reached the endpoints' lowest common ancestor. Moving it to its parent takes exactly one step along their shortest path without crossing that ancestor. Each operation reduces the remaining distance by one. They eventually meet at their lowest common ancestor, so the accumulated count is the distance.

## Complexity and numeric bounds

Let $U$ be the largest queried label and $H=\lfloor\log_2U\rfloor$ the maximum depth. A query takes at most $2H$ parent steps. Total time is $O(m(H+1))$ and extra space is $O(1)$ .

Here $U\le10^{18}$ , so depth is at most $59$ and distance at most $118$ . Use an unsigned integer type of at least 64 bits for labels; an ordinary integer suffices for distances. No explicit infinite tree or floating-point logarithm is needed. Equal endpoints return zero immediately.

[std.cpp](std.cpp) implements the preferred larger-label ascent. The setter's [depth-alignment method](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) compute depths explicitly, illustrating the general lowest-common-ancestor procedure with the same asymptotic complexity. Both methods pass all formal inputs.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
