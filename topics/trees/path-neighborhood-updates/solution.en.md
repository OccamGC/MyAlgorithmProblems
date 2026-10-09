# Mental Omega Device: Caterpillar Heavy-Chain Numbering and Interval Sets

Problem setter's solution: number a heavy chain first, then its light-child roots, then the remaining vertices of those light subtrees, representing paths, neighborhoods, and subtrees with few intervals. Codex (GPT-6): interval unions and differences, iterative preprocessing, 64-bit lazy tags, empty-set rules, and verification. The primary program is [std.cpp](std.cpp).

## Numbering Order

Compute parents, depths, and subtree sizes, choosing a child of maximum subtree size as the heavy child. For each heavy chain:

1. Its head has already been numbered by the parent chain; number root 1 separately. Number the remaining chain vertices consecutively.
2. In top-to-bottom chain order, number every vertex's light-child roots, recording `Hair[u]` .
3. In the same order, recursively process the chains headed by these light children. Record the remaining vertices of all those light subtrees in `Descendants[u]` .

The non-head part of a chain is contiguous. Its light-child roots are contiguous, and the remaining light-subtree blocks follow the order of their attachment vertices. Represent an empty interval with its left endpoint greater than its right endpoint; vertex ID zero must never enter an operation.

Parent and size preprocessing is iterative. Numbering recurses only across light edges, where subtree size at least halves, giving $O(\log n)$ recursion depth even on a chain of one hundred thousand vertices.

## The Three Sets

Heavy-chain decomposition splits a path into $O(\log n)$ same-chain segments $[u,v]$ . Each segment needs at most its head singleton and one interval for the rest, giving $O(\log n)$ intervals overall.

The subtree of $u$ contains the chain suffix from $u$ to the chain tail, the light-child roots attached to this suffix, and the remaining vertices of those light subtrees. The last two parts are one interval each; the first takes at most two. Thus a subtree needs at most four intervals.

For the external neighborhood, collect the light-child roots of each path segment, the heavy child of each segment's bottom, and the parent of the path's lowest common ancestor. Merge these intervals and subtract the union of all path intervals.

## Why These Sets Are Exact

The numbering procedure completely processes every light subtree in attachment order. The three subtree parts therefore include every descendant without omission.

Every child of a path vertex is light or heavy. All light children enter the candidate set. Heavy children internal to a chain segment lie on the path; only the bottom's heavy child can lie outside it. A path vertex's parent lies outside the path only when it is the parent of the lowest common ancestor. Thus every external neighbor is a candidate, and every non-path candidate is adjacent to the path. Subtracting the path gives exactly $H(a,b)$ .

Merge before subtracting so that each vertex is updated or added to a sum once. There are $O(\log n)$ intervals; union and difference preserve this asymptotic count.

## Unified Range Operations

Map values to a one-dimensional lazy segment tree in numbering order. Store sum, maximum, pending addition, pending assignment, and a Boolean indicating whether an assignment exists. Assigning $v$ sets the sum to length times $v$ , the maximum to $v$ , and clears the pending addition. Adding $v$ increases the sum by length times $v$ , and increases both maximum and pending addition by $v$ . Push assignment before addition to preserve operation order. Do not use a legal value as the sentinel for no assignment.

The exact interval sets and segment-tree invariants prove all 12 operations correct by induction. An empty interval list has sum zero and maximum output `EMPTY` . Maxima may be negative, so query aggregation must not start at zero.

## Complexity and Implementation Bounds

Preprocessing takes $O(n)$ time. Path and neighborhood operations take $O(\log^2 n)$ , subtree operations take $O(\log n)$ , and space is $O(n)$ . Sorting intervals costs $O(\log n\log\log n)$ and is included in the overall bound.

Individual values have absolute value at most $m10^8\le10^{13}$ ; sums have absolute value at most $nm10^8\le10^{18}$ . Tags, propagation parameters, and sums must all use 64 bits. Widening only stored fields is insufficient. Explicit set difference avoids fragile fixed-size exclusion lists and counters shared across operations. Ordinary heavy-chain decomposition compresses paths and subtrees, but a neighborhood can contain linearly many scattered vertices in a star; processing them individually does not meet these bounds.

## Validation and Performance

Every formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.403565 seconds and its peak memory is 29.02 MiB. Twice the median, rounded up to 0.5 seconds, gives a 1-second reference limit.

See the [test guide](tests/README.md), [environment](../../../docs/评测环境与性能.md), and [individual timings and hashes](../../../docs/benchmark-R35.json). Recalibrate on other environments.
