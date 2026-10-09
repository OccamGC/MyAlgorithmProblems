# Two Kinds of Shortest-Path Queries: Alternative Solution

Contribution: Codex (GPT-6) adds dense Dijkstra grouped by query source. The large-graph single-query branch retains the setter's heap Dijkstra. See the [preferred explanation](solution.en.md) for comparison with Floyd.

## Compute only the sources that are needed

For $n\le500$ , store the minimum direct edge weight for each pair in an adjacency matrix, with zero diagonal and infinity for missing edges. Read all queries and group their destinations and original indices by source. Run Dijkstra once for each nonempty group.

The small-graph search needs no heap: scan all unsettled vertices for the smallest distance, then scan its whole matrix row to relax neighbors. Stop when no finite unsettled vertex remains. Fill answers for that group's destinations at their original query indices. After all groups, print answers in input order.

## Correctness and complexity

All queries with one source depend on the same single-source distance array. Keeping only the lightest parallel edge preserves shortest paths: a heavier direct edge can always be replaced by the lightest edge with those endpoints. Dense scanning and a min-heap merely implement the same minimum-candidate selection, so nonnegative-weight Dijkstra has the same settling order and proof. Each group therefore receives correct distances, and restoring original indices yields the correct answer sequence.

Let $r$ be the number of distinct query sources. Reading edges, grouping, searching, and output take $O(m+rn^2+q)$ time and $O(n^2+q)$ space. Small $r$ avoids computing distances for unused sources. In the worst case $r=n$ , time remains cubic and query and answer storage adds space. For large graphs, $q=1$ still holds; heap Dijkstra takes $O((n+m)\log(n+m+1))$ time and $O(n+m)$ space.

This is a full-range parallel method chosen according to the actual query distribution. It retains 64-bit distances and a safe sentinel and supports equal-endpoint queries, zero weights, parallel edges, and disconnected graphs. Program: [alternative.cpp](alternative.cpp).
