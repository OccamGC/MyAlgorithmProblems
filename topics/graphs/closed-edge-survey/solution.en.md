# Minimum-Cost Pairing of Odd-Degree Vertices

Problem setter's solution: the doubled-tree special case, shortest paths between odd vertices, and subset minimum perfect pairing. Codex (GPT-6): portable implementation, complete proof, boundary handling, and independent covered-edge-state verification. The primary program is [std.cpp](std.cpp).

## Start Vertex and Special Cases

A closed walk covering every edge visits every vertex because the graph is connected. Rotate the walk to start at any visited vertex without changing its cost. Every start therefore has the same optimum, so the first output line is always 1.

In a tree every edge is a bridge. A closed walk that crosses it must cross back, so each edge is required twice. Traversing every tree edge out and back attains this bound, giving twice the sum of edge weights. Handle trees first: they may have far more than 20 odd vertices.

If all degrees are even, the connected graph has an Euler circuit. Traversing every edge once costs exactly the sum of weights.

## Extra Traversals Become Odd-Vertex Pairings

Include every edge once, for cost $S$ . View additional traversals as added parallel copies. Every final degree must be even, so the odd vertices of the added multigraph are exactly the original odd set $O$ . Its size $k$ is even, and for non-trees $k\le20$ .

Any such added multigraph decomposes into paths pairing the odd vertices, plus closed walks. Nonnegative weights make the closed walks nonnegative in cost, and every pairing path costs at least the shortest distance between its endpoints. Thus the extra cost is at least the minimum perfect-pairing cost on the odd vertices.

Conversely, take a minimum pairing and add the edges of a shortest path for each pair. Internal path vertices gain even degree; each odd endpoint is toggled once. Every degree becomes even, and connectivity is preserved, so an Euler circuit exists. This attains $S$ plus the pairing lower bound. Shared edges between added paths are harmless because their copies form a multigraph.

## Distances and Pairing DP

Run Dijkstra from each odd vertex to obtain pairwise distances $d_{ij}$ . Zero-weight edges are valid; discard stale priority-queue entries.

Let $F(M)$ be the minimum pairing cost for the vertex bitset $M$ , with $F(0)=0$ . Take its smallest-indexed vertex $i$ and enumerate its partner:

$$F(M)=\min_{j\in M\setminus\{i\}}\left(d_{ij}+F(M\setminus\{i,j\})\right).$$

Every perfect pairing gives $i$ exactly one partner, so the recurrence covers all possibilities. Process masks in increasing order because removing bits decreases the mask. Odd-cardinality states stay infinite; the final mask has even cardinality. An empty odd set naturally gives zero.

## Complexity and Verification

Time is $O(k(n+m)\log(n+1)+k2^k)$ and space is $O(n+m+k^2+2^k)$ . The tree branch takes $O(n+m)$ time. Distances and costs use 64 bits. Although the optimum is at most twice the total weight, hence at most $4\cdot10^8$ , wider types simplify infinity arithmetic.

Small tests independently run shortest paths over states consisting of the current vertex and covered-edge bitset. Formal data covers trees with unrestricted odd counts, parallel Euler edges, 20 odd vertices, zero weights, bridges, and cycles with chords. Chord cases also use degree-two chain contraction and Floyd distances, checked against full-graph Dijkstra.

## Validation and Performance

Every formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.584849 seconds and its peak memory is 21.16 MiB. Twice the median, rounded up to 0.5 seconds, gives a 1.5-second reference limit.

See the [test guide](tests/README.md), [environment](../../../docs/评测环境与性能.md), and [individual timings and hashes](../../../docs/benchmark-R35.json). Recalibrate on other environments.
