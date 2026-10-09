# Gran Forest — Solution

> Time–space tradeoff: global blocks. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.

Solution contribution: Codex (GPT-6) retained heavy-light decomposition with sorted blocks, reimplementing iterative forest traversal, global blocks and separate assignment/addition states, with a composition argument and complexity analysis. Heavy-light decomposition and block decomposition are established methods.


## Split each tree path into intervals

Root each component arbitrarily and compute parents, depths, subtree sizes and the child with the largest subtree. Store the vertices of every heavy chain consecutively in a linear array.

A simple path splits into $O(\log(n+1))$ heavy-chain intervals. Repeatedly process the endpoint whose chain head is deeper, then move above that head, until both endpoints share a chain. These are vertex weights, so the final interval includes both endpoints and the LCA. The intervals do not overlap.

The implementation traverses each forest component explicitly, computes subtree sizes in reverse order and numbers chains using loops, avoiding recursion on long paths.

## Block representation and updates

Choose block width $B=\max(1,\lfloor\sqrt n\rfloor)$ . Each block stores values in their original order, a sorted copy and sorted prefix sums. It has one of two states:

- Assigned: every current value equals an assignment tag; sorted data is temporarily unused.
- Unassigned: each current value is its stored value plus a common addition tag.

A whole-block assignment sets the assignment tag and clears addition. A whole-block addition increases the assignment value if assigned, or the addition tag otherwise. Before a partial update, materialize the whole block's actual values, clear both tags, modify the affected positions and rebuild the sorted values and prefix sums. Thus assignment overrides earlier additions, while later additions still affect assigned blocks correctly.

## Threshold queries

For an assigned block, compare its single current value against the threshold and multiply by the number of covered elements.

For a complete unassigned block with addition tag $a$ and threshold $d$ , binary-search the first stored value at least $d-a$ . The remaining element count answers operation 3. Its stored suffix sum plus “count times $a$” answers operation 4.

Inspect a partial unassigned block element by element. Negative values use the same comparison, and a qualifying sum may be negative; it must not be clamped to zero.

## Correctness and complexity

The block invariant represents every current value exactly. Whole and partial updates preserve it. Subtracting the uniform addition from the threshold leaves the selected set unchanged, so each block query is exact. Summing the disjoint heavy-chain intervals therefore answers the full path query.

A path includes at most $n/B$ complete blocks and $O(\log(n+1))$ interval-boundary fragments. A complete block query costs $O(\log(B+1))$ , while rebuilding a partially modified block costs $O(B\log(B+1))$ . A bound covering all four operations is

$$O\!\left(\left(\frac nB+B\log(n+1)\right)\log(B+1)\right)$$

Initialization takes $O(n\log(B+1))$ . Total time is initialization plus $q$ times this per-operation bound, and space is $O(n)$ . This is not a logarithmic-time-per-operation structure; balanced trees with many chain crossings require separate performance measurements.

Every current vertex weight has absolute value at most $10000(q+1)$ , and every path sum has absolute value at most $10000n(q+1)$ . Weights, tags and prefix sums use 64-bit integers.

## Validation

An independent model searches each path and updates individual vertices. Tests cover separate components, isolated vertices, negatives, equality at the threshold, assignment followed by addition and partial updates across blocks. Full-scale cases include chains, stars, balanced trees and random trees.

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.

## Asymptotic bounds and measured runtime

On the 500,000-vertex balanced tree, every heavy chain has at most 19 vertices, giving per-chain widths at most five versus global width 707. Partial updates on short chains can repeatedly rebuild large global blocks, explaining the same-input gap of about 0.230 versus 1.973 seconds. Fewer block objects and lower memory remain advantages of this method.

See the [main editorial](solution.en.md#asymptotic-bounds-and-measured-runtime) for the full parameter analysis, operation counts, and measurements.
