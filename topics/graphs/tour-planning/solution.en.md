# Tour Planning Editorial

Credits: Johnson reweighting and the min-cost maximum-flow model come from the problem setter’s solution. Codex (GPT-6) uses successive shortest augmenting paths and contributed global negative-cycle detection, boundary handling and proof exposition.

## Comparing solutions

The problem setter’s method computes global potentials, reweights roads for Dijkstra from each origin, selects destinations by distance and index difference, and builds a min-cost maximum-flow network for origin populations, interest edges and reception capacities. Potential terms telescope along paths, and integral flow represents traveler assignments; both proofs are shared below. It stores all-pairs distances and uses queue relaxation for road potentials. Its flow routine pushes along zero reduced-cost edges, then adjusts labels across the reachable cut to expose another zero-cost edge and continue.

For $q$ interest edges and $e=O(n+q)$ flow edges, storing all-pairs distances uses $O(n^2+m+q)$ space. Given valid road potentials, all-source Dijkstra takes $O(n(m+n)\log(n+1))$ . With $a_0$ flow searches and $r$ relabeling steps, the label-adjustment flow work is bounded by $O((a_0+r)(n+e))$ ; these counts must remain in the bound. The implementation must handle zero targets, negative cycles anywhere in the graph and the full capacity range.

The Codex implementation uses Bellman–Ford's $n$th-round criterion for global negative cycles and discards distances after each origin. Flow uses Dijkstra with potentials and successive shortest augmentations, pushing the bottleneck capacity each time. Total space falls to $O(n+m+q)$ ; full road and augmentation bounds follow below. Benefits are an explicit cycle criterion, no distance matrix, and sufficiently wide numeric types. Flow implementations were not timed against each other, and the actual augmentation count remains a parameter.

## Detect negative cycles globally and compute distances

A negative cycle must be reported even in an isolated region with no travelers. Conceptually add a super-source with zero-length edges to all vertices. Initialize every potential $h_i$ to zero and run Bellman–Ford relaxations over all roads. A strict improvement in round $n$ detects a negative cycle.

Otherwise every edge satisfies $h_v\le h_u+w(u,v)$ . Define

$$w'(u,v)=w(u,v)+h_u-h_v\ge0$$

Potential terms telescope along any path. Run Dijkstra with nonnegative reweighted lengths, then restore

$$d(i,j)=d'(i,j)-h_i+h_j$$

This is [Johnson's reweighting method for sparse shortest paths](https://doi.org/10.1145/321992.321993). Compute distances separately for each origin with residents and $k_i>0$ , discarding them afterward; no full distance matrix is required.

## Select destinations precisely

Exclude the origin itself and unreachable vertices. Sort the rest by $(d(i,j),\lvert i-j\rvert)$ . Take the first $k_i$ and every destination tied on both quantities at the cutoff.

For fixed $i$ and an ID difference, there is at most one ID on each side. Thus a sorting key represents at most two villages, and no more than $k_i+1$ destinations are selected. If $k_i=0$ , select none without accessing rank $k_i-1$ . An origin with no residents needs no distance calculation or preference edges, but still participates in global negative-cycle detection.

## Build a cost-flow network

Create an origin vertex $U_i$ and a reception vertex $W_i$ for each village, plus source $s$ and sink $t$ :

- $s\to U_i$ : capacity $V_i$ , cost $0$ .
- $U_i\to W_j$ : present only if $j$ interests residents of $i$ , capacity $V_i$ , cost $C_iP_j$ .
- $W_j\to t$ : capacity $H_j$ , cost $0$ .

One unit of flow represents one traveler. Integral capacities admit integral flow, and the capacity constraints exactly enforce resident counts and reception limits. Each source-to-sink path costs exactly that traveler's spending. The required answer is therefore a minimum-cost maximum flow.

Residents staying home need no special edges. Maximum flow sends as many residents as possible; everyone else remains at home.

## Successive shortest augmentations

Initially all forward costs are nonnegative and flow is zero, so initialize flow potentials to zero. On each iteration, run Dijkstra on reweighted residual costs, send the full bottleneck capacity along a shortest augmenting path, and update potentials. Reverse edges have negated costs, allowing earlier assignments to be canceled and replaced.

Each augmentation preserves minimum cost for the current flow value: it has the smallest additional cost, and no negative residual cycle can improve the current flow. Stop only when no source-to-sink path remains. The resulting flow is maximum, with minimum cost at that value. A positive-cost augmenting path must still be used because traveler count takes priority.

## Complexity and numeric bounds

Let $q$ be the number of preference relations, let $e=O(n+q)$ be the flow-network edge count, and let $a$ be the number of augmentations performed. The road stage takes $O(nm+n(m+n)\log(n+1)+n^2\log(n+1))$ time, with the last term bounding per-origin sorting. The flow stage takes $O(ae\log(n+1))$ . Total space is $O(n+m+q)$ .

The augmentation parameter is explicit; large capacities are not treated as unit capacities. Each augmentation sends its whole bottleneck amount. Integer capacities give the general bound $a\le F\le\sum_i V_i$ , where $F$ is the maximum flow. This is a pseudopolynomial bound for successive shortest augmentations, not a strongly polynomial guarantee. The reference time limit is measured on the supplied maximum-size cases.

Use signed 64-bit integers for distances, capacities, potentials, and accumulated costs. The final cost is at most $900\sum_i V_i$ , or $9\times10^{14}$ . Road lengths affect preference rankings and must not be confused with purchase prices.

## Validation

The independent small-instance oracle uses Floyd for distances, then enumerates the destination or stay-home choice of each individual traveler, merging states by used reception capacities. It maximizes traveler count before minimizing cost. Checks include zero preferences, tied destinations, negative edges and cycles, free purchases, and parallel roads. For performance measurements, see [environment and measurements](../../../docs/评测环境与性能.md).
