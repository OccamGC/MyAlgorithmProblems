# Two Kinds of Shortest-Path Queries: Solution

Problem setter’s solution: Floyd on small graphs and heap Dijkstra for the unrestricted single-query case. Codex (GPT-6) organizes 64-bit distances, parallel edges, and diagonal initialization, and adds dense Dijkstra grouped by query source.

## Two branches cover the constraints

If $n\le500$ , compute all-pairs distances and answer queries by lookup. Otherwise, the global guarantee forces $q=1$ , so compute distances only from that query's source. These two cases cover every formal input.

## Small graphs: Floyd

Initialize a distance matrix $D$ with a zero diagonal and infinity elsewhere. Each undirected edge updates both directions, retaining the minimum among parallel edges. For $k=1,\ldots,n$ , allow one more intermediate vertex and apply

$$D_{i,j}\leftarrow\min(D_{i,j},D_{i,k}+D_{k,j})$$

After round $k$ , the matrix gives shortest paths whose intermediate vertices are restricted to $1,\ldots,k$ . Indeed, an optimal simple path either avoids $k$ or passes through it and splits into two paths with intermediates in the smaller set. The old value and the sum of those two distances represent the respective cases. Nonnegative weights allow a shortest path to be simple. Initialization covers paths with no intermediate vertices; induction then includes every path.

Time is $O(n^3+m+q)$ and space is $O(n^2)$ . Queries can be read and answered immediately without storing them all.

## Large graphs: one Dijkstra search

Store adjacency lists, initialize the query source to zero and other distances to infinity, and repeatedly extract the minimum valid heap entry. Relax its neighbors and discard stale heap entries. Nonnegative weights ensure that an unsettled vertex cannot improve through a later-settled vertex: the first edge leaving the settled set on such a path has already provided a candidate no greater than the full path length. Induction proves that a valid minimum extraction gives the true distance.

The edge count bounds the number of heap entries, giving $O((n+m)\log(n+m+1))$ time and $O(n+m)$ space. Answer the single query, using minus one for an unreachable destination.

## Boundaries and a parallel method

A finite shortest-path weight is at most $(n-1)\cdot10^9<5\times10^{14}$ , so distances require 64-bit integers. The infinity sentinel is one quarter of the maximum signed 64-bit value, making even the sum of two sentinels safe. Initialize the diagonal to zero so a self-loop cannot raise it. Recognize unreachable vertices using the sentinel rather than a smaller arbitrary threshold.

[std.cpp](std.cpp) uses these two setter algorithms. [Grouping by source](solution-alternative.en.md) runs dense Dijkstra on a small graph only for sources that actually appear in queries. It takes $O(m+rn^2+q)$ time, where $r$ is the number of distinct query sources. Fewer sources mean less work, but queries must be stored and worst-case time is still cubic. This parallel method supports the entire range.
