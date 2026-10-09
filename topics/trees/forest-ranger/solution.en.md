# Forest Ranger: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: longest-chain gains with counting buckets.** Counting buckets exploit integer gains whose sum is at most $n-1$ , giving the preferred $O(n)$ method. Comparison sorting has an $O(n\log(n+1))$ upper bound; their measured runtimes are discussed below. Explicit traversal supports million-vertex chains.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the comparison sorting method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [alternative editorial](solution-alternative.en.md).

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

Traverse explicitly to find parents and an order; process it backward to compute longest downward vertex counts $h_v$ and longest children. The root chain gives $h_1-1$ , and each non-longest child $v$ starts a chain of gain $h_v$ . Count every positive gain $g$ in $\operatorname{cnt}[g]$ .

All gains are integers between $1$ and $n-1$ . Scan buckets downward, taking each gain its recorded number of times and printing cumulative sums. This implements the decreasing order required above. Counting and scanning take $O(n)$ ; including traversal and output, total time and space are $O(n)$ .

## Asymptotic bounds and measured runtime

In the measurements, the million-vertex random tree took about 0.247 seconds with buckets and 0.254 seconds with comparison sorting. The four-million-vertex random tree also showed little separation. This does not contradict the linear method's worst-case advantage: examine how many items are sorted and what the rest of each program does.

### The sorting parameter is the leaf count

Let $D$ be the number of leaves and $g_1,\ldots,g_D$ the positive gains. Sorting costs $O(D\log(D+1))$ ; the whole algorithm is usually counted as $O(n+D\log(D+1))$ basic operations, with decimal output additionally processing its actual characters. Using $D\le n-1$ gives the simpler $O(n\log(n+1))$ bound. It does not mean every vertex participates in a sort of $n$ items.

The gain chains partition all non-root vertices, so

$$\sum_{i=1}^{D}g_i=n-1,\qquad g_i\ge1.$$

At most $(n-1)/t$ gains can be at least $t$ . Few leaves mean few items; many leaves imply small average gains. A chain has one item, while a star has only unit gains. Instrumenting the existing million-vertex cases gives:

| Shape | Gain count | Distinct gains | Sorting comparisons |
| --- | ---: | ---: | ---: |
| Chain | 1 | 1 | 0 |
| Star | 999,999 | 1 | 17,232,314 |
| Random tree | 499,853 | 28 | 8,749,136 |

The random tree has 281,711 unit gains and maximum gain 28. Sorting operates on contiguous integers; a comparison does not itself traverse a tree path. **Repeated values do not guarantee linear time for this comparison sort**: the star still performs about 17.23 million comparisons, so sorting is not free.

### Buckets also have a fixed linear cost

Reading edges, building adjacency, finding parents and longest chains, and constructing the output string use the same code in both programs. Buckets additionally zero an array of length $n$ and scan all $n-1$ possible gains, whereas sorting processes only the $D$ collected gains. On a chain, that full bucket scan does more work than sorting a single item.

Shared work and differing constants narrow the whole-program time ratio. The measurements record wall-clock time including input and output, without timing individual phases. It cannot establish an I/O percentage or attribute the entire gap to I/O. The gain and comparison counts above come from a separate [operation-count run](../../../docs/performance-work-P1.json), and do not measure phase durations.

### Why multiplying the size is insufficient

If the leaf fraction stays similar, multiplying the size by four adds only two to $\log_2 D$ . Near a million items, that is a modest relative change in the extra logarithmic factor. Unless sorting already dominates shared work and constants, a fewfold size increase need not produce a fewfold speed gap. Buckets retain their better worst-case bound; these observations explain the measured inputs, not every possible input or platform.

### A construction targeting pivot selection

A special ordering does widen the gap. Attach disjoint paths to the root: their lengths realize the gains. Place the longest path first and label the others in the desired order to control the sequence entering the sort, while keeping the gain sum equal to $n-1$.

The measured GCC 16.2.0 libstdc++ implementation selects a median of three. Put a few large gains at successive sampled positions and make all other gains one. This produces repeatedly unbalanced partitions until introsort reaches its depth guard. The four-million-vertex input has only 86 distinct gains, including 3,996,256 unit gains, yet performs 257,562,524 sorting comparisons. Many duplicates alone do not rule out expensive comparison sorting.

| Vertices | Bucket median (s) | Sorting median (s) | Sorting / buckets |
| --- | ---: | ---: | ---: |
| 1,000,000 | 0.152050 | 0.196939 | 1.30 |
| 2,000,000 | 0.290520 | 0.389631 | 1.34 |
| 4,000,000 | 0.578046 | 0.854063 | 1.48 |

Each median uses seven runs; the last two sizes exceed the published limit and are scaling experiments only. The gap is stable and measurable, but sorting still takes less than twice the bucket time on the same input. A limit allowing twice the reference time and rounding up to 0.5 seconds cannot reliably exclude this sorting implementation. The construction depends on this pivot policy, so it does not establish the behavior of every sorting library. Construction and stress inputs: Codex (GPT-6). See [tree constructions and performance](../../../docs/树形构造与性能.md) for reproduction.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
