# Gran Forest: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: separate blocks for each heavy chain.** Per-chain blocks are used in the reference. Global blocks need fewer small blocks and containers and have lower measured peak memory, but a short-chain update can rebuild vertices belonging to other chains in the same block. Under the 1.0-second reference limit, the supplied global-block program times out on the balanced-tree case. It illustrates a time–space tradeoff and does not pass the complete test set.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the global blocks method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [time–space tradeoff editorial](solution-alternative.en.md).

## Split each tree path into intervals

Root each component arbitrarily and compute parents, depths, subtree sizes and the child with the largest subtree. Store the vertices of every heavy chain consecutively in a linear array.

A simple path splits into $O(\log(n+1))$ heavy-chain intervals. Repeatedly process the endpoint whose chain head is deeper, then move above that head, until both endpoints share a chain. These are vertex weights, so the final interval includes both endpoints and the LCA. The intervals do not overlap.

The implementation traverses each forest component explicitly, computes subtree sizes in reverse order and numbers chains using loops, avoiding recursion on long paths.

## Block representation and updates

For each heavy chain of length $L$ , choose its own width $B=\lceil\sqrt L\rceil$ . Blocks never cross chain boundaries. Each block stores values in their original order, a sorted copy and sorted prefix sums. It has one of two states:

- Assigned: every current value equals an assignment tag; sorted data is temporarily unused.
- Unassigned: each current value is its stored value plus a common addition tag.

A whole-block assignment sets the assignment tag and clears addition. A whole-block addition increases the assignment value if assigned, or the addition tag otherwise. Before a partial update, materialize the whole block's actual values, clear both tags, modify the affected positions and rebuild the sorted values and prefix sums. Thus assignment overrides earlier additions, while later additions still affect assigned blocks correctly.

## Threshold queries

For an assigned block, compare its single current value against the threshold and multiply by the number of covered elements.

For a complete unassigned block with addition tag $a$ and threshold $d$ , binary-search the first stored value at least $d-a$ . The remaining element count answers operation 3. Its stored suffix sum plus “count times $a$” answers operation 4.

Inspect a partial unassigned block element by element. Negative values use the same comparison, and a qualifying sum may be negative; it must not be clamped to zero.

## Correctness and complexity

The block invariant represents every current value exactly. Whole and partial updates preserve it. Subtracting the uniform addition from the threshold leaves the selected set unchanged, so each block query is exact. Summing the disjoint heavy-chain intervals therefore answers the full path query.

Suppose a path crosses $h$ heavy chains, with chain lengths $L_j$ and block sizes $B_j=\lceil\sqrt{L_j}\rceil$ . A conservative bound covering all four operations is

$$O\!\left(\sum_{j=1}^{h}\left(\frac{L_j}{B_j}+B_j\right)\log(B_j+1)\right)$$

Here $h=O(\log(n+1))$ , and the chains are disjoint, so $\sum_j L_j\le n$ . Cauchy–Schwarz also bounds this by $O(\sqrt{n\log(n+1)}\log(n+1))$ . Initialization is bounded by $O(n\log(n+1))$ , and space is $O(n)$ . Add the corresponding operation bounds for all $q$ operations to obtain the total time.

Every current vertex weight has absolute value at most $10000(q+1)$ , and every path sum has absolute value at most $10000n(q+1)$ . Weights, tags and prefix sums use 64-bit integers.

## Asymptotic bounds and measured runtime

This problem provides a case where separation is measurable: on the same 500,000-vertex balanced-tree input, per-chain blocks took about 0.230 seconds and global blocks about 1.973 seconds. The extra work repeatedly rebuilds whole arrays, unlike adding a few integer-query steps over a shallow depth range.

The generated tree has height 18 edges, so any heavy chain has at most 19 vertices. Its per-chain block width is at most $\lceil\sqrt{19}\rceil=5$ , while the global version uses $\lfloor\sqrt{500000}\rfloor=707$ . Updating a path across several short chains can modify only a few positions at each boundary yet require materializing, sorting, and rebuilding prefix sums for a global block containing other chains. Assignment and addition tags avoid this work only for fully covered blocks.

This shape repeatedly triggers the extra work, and the time gap is measured on the same input. Global blocks still use fewer block objects and containers and have a lower peak working set, but that does not ensure meeting the current 1.0-second limit. The comparison shows why actual operations triggered by an input matter; the other three problems do not establish that an extra logarithm is generally unimportant. Block widths follow directly from the implementation and generator. Individual phases were not timed, so the entire gap is not attributed to sorting alone.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
