# Lower-Weight Imperfect Non-Matching: Traversing a Minimum Spanning Tree Twice

Problem setter's solution: Kruskal's minimum spanning tree and an out-and-back traversal. Codex (GPT-6): iterative traversal, boundary handling, complete scoring checker, and independent verification. The primary program is [std.cpp](std.cpp).

## Construction

Sort edges by weight and use a disjoint-set structure to select a minimum spanning tree. Keep each selected edge's input ID. Root the tree at 1. Before entering a child, output its connecting edge; after finishing that child, output the same edge again. An explicit stack stores the vertex, parent, next tree edge to process, and return edge.

A self-loop cannot connect different components. Parallel edges remain separate candidates. Break equal-weight ties by input ID to make the reference output reproducible.

## Correctness

Kruskal repeatedly takes a minimum-weight edge joining different components. The cut property makes every such choice safe, so the final tree has minimum weight $W$ .

Induct on subtrees. Each child is entered through its tree edge, its subtree is completely visited, and the same edge returns to the parent. Thus processing a subtree visits all its vertices and ends at its root. The complete walk starts and ends at 1.

Every tree edge is used exactly twice. The output length is $2(n-1)\le5n$ , and its cost is $Y=2W=B\le2B$ , earning full credit. For $n=1$ , outputting zero also satisfies the rules. No claim that this is the globally shortest closed walk is needed.

## Complexity and Checker

Time is $O(m\log(m+1)+(n+m)\alpha(n))$ and space is $O(n+m)$ . Accumulate costs in 64-bit integers. An explicit stack supports long chains without recursive stack growth.

[checker.py](checker.py) independently computes the baseline using Prim. It checks edge IDs, length, continuity, return to 1, coverage, and extra output. Integer arithmetic implements partial-credit rounding exactly. A zero baseline is handled by the first branch without division. A legal partial-credit answer also returns exit status zero; read its score from standard output.

Replacing Kruskal with Prim gives the same MST construction, so a second implementation differing only in containers is unnecessary. Traversing an arbitrary spanning tree is legal but can cost much more than the baseline and does not guarantee full credit.

## Validation and Performance

Every formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.100009 seconds and its peak memory is 15.23 MiB. Twice the median, rounded up to 0.5 seconds, gives a 0.5-second reference limit.

See the [test guide](tests/README.md), [environment](../../../docs/评测环境与性能.md), and [individual timings and hashes](../../../docs/benchmark-R35.json). Recalibrate on other environments.
