# Festival Plan: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: centroid decomposition with monotone windows.** Monotone windows give the preferred $O(n\log(n+1))$ method. Segment-tree range queries provide an alternative endpoint-pairing implementation with an $O(n\log^2(n+1))$ upper bound. Both implementations use explicit traversal to avoid deep recursion on chains.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For centroid decomposition with a segment tree, as used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [alternative editorial](solution-alternative.en.md).

## Lengths and admissible paths

Set $A=L-1$ and $B=R-1$ to convert vertex counts into edge counts. Keep the original tree rooted at vertex $1$ throughout.

Choose a centroid $c$ of the current component. A downward path through $c$ pairs an endpoint on the original ancestor chain with an original descendant. The upward collection cannot enter siblings of an ancestor. Stop at removed vertices or depths exceeding $B$ . Include $c$ in both lists with depth zero and sum $v_c$ .

For an endpoint $x$ , let $d_x$ be its depth from $c$ and $s_x$ the inclusive vertex sum. A partner from the other list must satisfy

$$A-d_x\le d_y\le B-d_x,$$

and contributes $s_x+s_y-v_c$ . The two halves share only $c$ , so these pairs are exactly the admissible downward paths through $c$ .

## Monotone depth windows

For the partner list, store the largest sum $M[d]$ at each depth. Process the current list in nondecreasing depth: the ancestor chain already has this order, and breadth-first traversal gives it for descendants. Query

$$[\max(0,A-d_x),\ \min(D,B-d_x)],$$

where $D$ is the largest partner depth. Both boundaries move toward smaller depths. Insert newly eligible depths from large to small into a monotone deque, discard dominated values at the back, and remove indices above the current upper boundary at the front. Each depth enters and leaves at most once. An empty window gives no candidate.

Run this procedure in both directions to obtain each endpoint's best full-path score $g_x$ . Including the centroid twice in the lists is harmless: the formula counts its weight once. When $A=0$ , it also includes the singleton path.

## Propagating to internal vertices

Store each visited record's parent toward the centroid. Initialize its mark to $g_x$ and propagate maxima in reverse traversal order.

Every candidate contains the whole segment from its endpoint to $c$ , so propagation is sound. Conversely, a path through $c$ containing $u$ has an endpoint in the local subtree of $u$ . That endpoint's best candidate is at least this path's score and propagates to $u$ . This proves that the round finds every vertex's optimum among paths through $c$ .

Delete $c$ and process the remaining components. Each path is handled when the decomposition first removes a centroid on that path.

## Implementation and complexity

Finding the centroid, collecting endpoints, processing windows, and propagating marks take $O(s)$ for a component of size $s$ . Remaining components have at most half its size. Total time is $O(n\log(n+1))$ and space is $O(n)$ . Traversals and decomposition scheduling are explicit. Components of at most eight vertices are handled by direct ancestor-path enumeration, a constant-size base case.

Use 64-bit sums and never add a missing-value sentinel. Negative valid scores remain negative; only vertices with no admissible path output `-1061109568` .

## Asymptotic bounds and measured runtime

On the measured 500,000-vertex random tree, monotone windows took about 0.741 seconds and the segment tree about 0.816 seconds. At two million vertices the respective times were about 4.015 and 4.391 seconds. Both logarithms in the worst-case bound need not reach their upper bounds on every input or query.

### Queries are indexed by depth

For a decomposition component, let $m_c$ be the collected endpoint count and $D_c$ the maximum collected depth. The segment-tree method builds a segment tree over depths, rounding the range $0$ through $D_c$ up to a power of two. Its segment-tree work has the more specific bound

$$O\bigl(D_c+1+m_c\log(D_c+2)\bigr).$$

A query does not automatically traverse $\log n$ levels. Stars have tiny depth ranges; balanced trees and this measured random tree are also shallow, and the upper length bound truncates collection. A deep chain can make depth proportional to component size, bringing this logarithm close to $\log n$ ; shallow trees may give much smaller values. Combining this possibility with centroid-decomposition levels gives the general $O(n\log^2(n+1))$ bound.

Intersecting the admissible depths with $[0,D_c]$ may also produce an empty query, which skips the query loop. A singleton interval handles one leaf. Many small components cannot reach the lower length bound $L$ , producing further empty queries. For nonempty intervals, each iteration shifts both indices by one bit, and interval alignment affects how many canonical ranges are merged.

### What executed counts show

These counts include all decomposition rounds in the segment-tree implementation. A loop iteration means one execution of `while (Left < Right)` , not one machine instruction.

| 500,000-vertex case | Maximum collected depth | Queries | Empty queries | Total query-loop iterations |
| --- | ---: | ---: | ---: | ---: |
| Random tree, full length range | 29 | 4,306,142 | 0 | 16,692,524 |
| Chain, vertex lengths 100000–250000 | 249,999 | 8,975,731 | 7,775,730 | 18,840,416 |
| Positive chain, full length range | 250,000 | 8,975,732 | 0 | 86,738,817 |

The random tree averages only about 3.88 iterations per query. The restricted chain is deep, but about 86.6% of its queries are empty. The last row shows that a deep chain with a wide window really does increase the extra work; similar overall timings do not erase the complexity difference.

Here, the random tree specifically comes from attaching each new vertex to an existing parent and then relabeling, as in the supplied generator. Its depth statistics do not apply to every random-tree generation method.

### An extra logarithm does not multiply the entire runtime

Both versions repeatedly traverse components, find centroids, collect endpoints, and propagate answers. The monotone-window method also builds per-depth maxima and processes the ancestor and descendant directions separately. Linear work per component still includes multiple scans, initializations, and allocations. The segment-tree method queries contiguous arrays iteratively. Endpoint records occupy 32 and 24 bytes respectively in this compiler environment, adding a storage-constant difference. Smaller records may reduce memory traffic, but cache hit rates were not measured, so this is not an established percentage of the time gap.

Record sizes, shared work, and actual component depths explain why the bound does not directly predict a large timing ratio. The [operation counts](../../../docs/performance-work-P1.json) verify executed loops; Whole-program timings do not isolate each cause's contribution. Multiplying the size by four also adds only two to $\log_2 n$ , rather than multiplying the extra logarithmic factor by four. The monotone-window method's better worst-case guarantee and the segment-tree method passing at the current scale are consistent.

### Constructions targeting depth and query windows

A chain with a wide window increases both decomposition depth and the number of nonempty queries. Combs, subdivided binary trees and double brooms vary the number of endpoints at each depth. Upper length bounds near one third or one half of the size, and near powers of two, probe interval decomposition and alignment. Weight patterns include random, positive, zero and alternating signs.

On a 500,000-vertex comb with teeth of length seven, seven-run medians are 0.369029 seconds for monotone windows and 0.430357 seconds for the segment tree, a 17% difference. At one and two million vertices, five-run ratios are 1.24 and 1.18. Double brooms also give only about a 10% gap, insufficient to separate pass from timeout while allowing twice the reference time.

Labels also affect these implementations. On one randomly relabeled 500,000-vertex chain with vertex-length range $[1,249997]$, the medians are 1.742455 and 1.356307 seconds: monotone windows are slower. Relabeling preserves the mathematical tree but changes accesses to arrays indexed by labels. This is consistent with locality effects; without cache profiling, it does not attribute the entire difference to caches.

These targeted inputs and experiments at twice and four times the formal size have not found a reliable exclusion gap. They do not prove that every legal construction fails to do so. Stress inputs: Codex (GPT-6). Parameters, repeated timings and limit calibration are in [tree constructions and performance](../../../docs/树形构造与性能.md).

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
