# Forest Ranger: Solution

> Alternative: comparison sorting. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.


## Daily routes

A leaf here means a non-root vertex with no children. Entering two different child subtrees of a vertex in one day would visit that vertex before the first subtree, between the two subtrees, and after the second subtree. The root also cannot be visited between the endpoints of a walk. Thus each day's walk follows one simple downward path from the root and returns along the same edges. If it stops short of a leaf, extending it to a leaf cannot reduce the tasks completed or violate the visit limit.

At most one leaf can be visited per day, and every leaf has a task. At least one day per leaf is therefore necessary. Taking one path to each leaf attains that bound.

## Marginal gains of optimal prefixes

Let $F_v(0)=0$ , and let $F_v(k)$ be the maximum number of vertices covered in the subtree of $v$ using at most $k$ paths from $v$ to leaves. Consider only its positive marginal gains $F_v(k)-F_v(k-1)$ , up to the point where all leaves are selected.

A leaf has the single gain $1$ . Assume each child's gain sequence is nonincreasing. Allocating the $t$-th path to a child requires taking that child's first $t-1$ gains as well. Merge all child sequences in decreasing order, preserving the order within each child on ties. Any prefix of the merged sequence satisfies this requirement and has the largest possible sum.

Selecting at least one path also covers $v$ itself. Adding $1$ to the first element of the merged sequence therefore gives the gain sequence for $v$ . It remains nonincreasing, and its first gain is the number of vertices on a longest path from $v$ to a leaf. This completes the induction.

Let $h_v$ be the number of vertices on a longest downward path from vertex $v$ to a leaf, including both endpoints; a leaf therefore has $h_v=1$ . Choose a child with the largest $h_v$ as the heavy child of each vertex. The first heavy chain from the root to a deepest leaf contributes $h_1-1$ tasks. Every non-heavy child $v$ starts another chain whose marginal gain is $h_v$ . Sort these gains in decreasing order and print their prefix sums. The number of gains equals the number of leaves.

Each step of the merge appends one path from a child without undoing earlier choices. It therefore produces an ordering of leaves whose first $k$ paths are optimal for every $k$ . Selecting all leaves uses exactly the minimum number of days $D$ . The root has no task, so subtract $1$ from its first gain and leave the others unchanged. This explains the special treatment of the first heavy chain in the implementation.

## Implementation and complexity

Use an iterative traversal to find parents and an order of vertices, then process that order in reverse to compute $h_v$ and heavy children. The implementation stores $h_v$ in `PathVertices[v]` , emphasizing that it counts vertices. Iteration avoids recursion depth problems on a million-vertex chain. Collect and sort chain gains, then print prefix sums.

Time complexity is $O(n\log n)$ and space complexity is $O(n)$ .

## Asymptotic bounds and measured runtime

Sorting handles only $D$ leaf gains, whose sum is $n-1$ : a chain has one item and a star has only ones. Shared input, traversal, and output work, plus the bucket version's full scan, narrow the total runtime gap. Repetition does not guarantee linear comparison sorting: the million-vertex star still executes about 17.23 million comparisons.

See the [main editorial](solution.en.md#asymptotic-bounds-and-measured-runtime) for the full parameter analysis, operation counts, and measurements.
