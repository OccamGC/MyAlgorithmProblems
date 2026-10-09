# Transport with Capacities on a Line: Block Decomposition

## Source and role

Keep the problem setter's residual-transport model and nearest-vacancy choice from the [preferred solution](solution.en.md). Codex (GPT-6) implements sorted blocks. The marginal-cost formulas and optimality proof are shared; this explanation supplies the complete replacement range structure. The [program](alternative-blocks.cpp) supports the full formal range.

## Block representation

Divide the $n$ edges into consecutive blocks of at most $B$ edges. Store raw flows $a_i$ and one block offset $t$ , so actual flow is $a_i+t$ . Sort the pairs $(a_i,d_i)$ by raw flow and build prefix sums of distances. Equal-flow ties may be ordered by distance; a threshold query includes the entire equal-flow group.

A full block's rightward marginal cost is its total distance minus twice the distance sum of edges with negative actual flow. Binary search finds $a_i<-t$ . Leftward cost is twice the distance sum of nonpositive actual flows minus the total, using $a_i\le-t$ . Scan partial blocks directly.

For a range increment or decrement, change only the offset of a full block. Modify individual raw values in at most two partial blocks, then sort and rebuild their prefix sums. Their offset need not be pushed: changing a raw value changes its actual value by the same amount.

## Correctness and complete algorithm

Sorting changes only query order and preserves each flow-distance association. The prefix queries select exactly negative or nonpositive actual flows, reproducing the edgewise absolute-value differences. Both lazy full-block shifts and explicit partial-block changes perform the required range increment exactly. These operations can therefore replace the segment-tree operations in the preferred model.

Use an ordered set to find the nearest vacancy on each side, choose the minimum marginal route, update its flows, consume a slot and add the marginal cost to the answer. The shared minimum-cost augmentation proof establishes optimality for every prefix.

## Complexity and comparison

Initialization takes $O(n\log B)$ . A query uses binary search in $O(n/B)$ full blocks and scans $O(B)$ boundary edges. An update re-sorts at most two partial blocks. Total time is
$$
O\left(n\log B+m\left(\log n+\frac nB\log B+B\log B\right)\right),
$$
with $O(n)$ space. The program uses $B=320$ , close to the square root of the maximum input size; the formula explicitly retains the block length. Choosing $B=\lceil\sqrt n\rceil$ as a function of the input gives the usual square-root bound.

The per-operation bound does not depend on flow sign crossings, and measured memory is smaller. The cost is scanning multiple blocks and sorting. Both programs should pass the full range. The limit covers the slower program in the [measurements](../../../docs/benchmark-R28.json); this does not claim blocks are faster on every input.
