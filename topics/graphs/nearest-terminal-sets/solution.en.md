# Starts and Destinations: Solution

Problem setter’s solution: add a virtual source and sink and run Dijkstra. Codex (GPT-6) supplies the C++17 implementation, empty-set and distance-bound explanations, and direct multi-source initialization.

## Turn endpoint selection into one shortest path

Add a virtual source $s_0$ and sink $t_0$ . Add a directed zero-weight edge from $s_0$ to every vertex in $S$ , and from every vertex in $T$ to $t_0$ . Store each original undirected edge in both directions.

Every eligible original path extends with two zero-weight edges to an equal-weight path from $s_0$ to $t_0$ . Conversely, the virtual source only has outgoing edges and the virtual sink only incoming edges, so the middle of any such path connects a valid source and destination. Their minimum weights are equal. If either set is empty, the virtual endpoints cannot be connected.

## Shortest paths with nonnegative weights

Set the source distance to zero and all others to infinity. Use a min-heap to extract the smallest tentative distance and relax outgoing edges, pushing an entry only on a strict improvement. Old entries may remain in the heap; discard an extracted entry if its distance differs from the current array value.

Dijkstra is correct because weights are nonnegative. An unsettled vertex with minimum tentative distance cannot later improve via another unsettled vertex: the first edge leaving the settled set on such a path has already been relaxed, and later edges cannot decrease its length. Induction proves that each first valid minimum extraction has its true shortest distance. Read the final sink distance and output minus one for infinity. Zero weights, parallel edges, and self-loops preserve this reasoning.

## Complexity, numeric bounds, and alternatives

The augmented graph has $n+2$ vertices and $O(n+m)$ directed edges. A binary heap allowing stale entries gives $O((n+m)\log(n+m+1))$ time and $O(n+m)$ space. Parallel edges are allowed, so the heap bound accounts for the number of edges rather than unconditionally expressing the logarithm only in terms of vertices.

A finite shortest path can be simple because weights are nonnegative. Its original-graph weight is at most $(n-1)\cdot10^9<5\times10^{14}$ . Use signed 64-bit distances and a sufficiently large, addition-safe infinity sentinel. Relax only from finite distances.

[std.cpp](std.cpp) retains the virtual-node model. [Direct multi-source Dijkstra](solution-alternative.en.md) initializes all valid sources to zero and avoids virtual edges, giving a more direct model. Both have the same asymptotic bounds and support all inputs; this simplification is not an asymptotic speed improvement. Repeating a search from every source adds a factor of $\lvert S\rvert$ without a compensating benefit.
