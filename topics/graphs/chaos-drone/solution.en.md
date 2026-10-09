# Chaos Drone — Solution

## Comparing solutions

The problem setter’s solution connects units that may be handled together, finds a maximum matching in the general graph, and subtracts its size from the number of units. Matching edges give disjoint pairs, and every grouping's pairs form a matching, proving the equivalence. The problem setter’s program uses blossom contraction for odd cycles. The reduction, contraction and augmentation explanation below retains this method.

With an adjacency matrix, time is $O(n^3)$ and space is $O(n^2)$ . Codex (GPT-6) contributed the array and queue implementation and the algorithm exposition.

## Model

Represent units by vertices and allowed pairs by undirected edges. An action covers the endpoints of an edge or one individual vertex. If a maximum matching has size $\nu$ , the answer is

$$n-\nu$$

Use one action for each matching edge and one for each of the $n-2\nu$ unmatched vertices. This uses $n-\nu$ actions.

For the lower bound, delete redundant actions from any cover until no action can be deleted. A singleton action cannot share its vertex with another action. Every nontrivial component of the chosen edges must be a star: an edge whose endpoints both have another incident edge could be deleted. Choose one edge from each star to obtain a matching. A star with $v$ vertices uses $v-1$ actions, while an isolated vertex uses one. Thus a minimal cover with $k$ actions yields a matching of size $n-k$ . Since $n-k\le\nu$ , no cover uses fewer than $n-\nu$ actions.

## Maximum matching in a general graph

The graph can contain odd cycles, so bipartite matching is insufficient. The reference program uses Edmonds' blossom algorithm:

1. Start at an unmatched vertex and grow an alternating tree, alternating unmatched and matched edges.
2. Reaching another unmatched vertex gives an augmenting path. Flip the edges along that path to increase the matching size by one.
3. An edge between two even-level vertices in the same alternating tree forms an odd cycle. Find their common base, temporarily contract the cycle, and maintain parent pointers so an augmenting path can later be expanded.
4. If the search fails, try the next unmatched root. Continue until every root has been processed.

All vertices of a blossom except its base are paired inside the cycle. An alternating path through the contracted vertex can be expanded along the side of the odd cycle with the required parity. Conversely, an augmenting path in the original graph can be represented in the contracted graph. Contraction therefore preserves the existence of an augmenting path. A matching with no augmenting path is maximum; the cover formula then gives the answer.

## Implementation and complexity

Map names to vertex IDs, leaving unnamed units as isolated vertices. `Match` stores partners, `Parent` stores alternating-tree predecessors, and `Base` stores contracted bases. Reset the temporary search arrays for each root while retaining the matching.

Time complexity is $O(n^3)$ and graph storage is $O(n+m)$ . Name storage is linear in the total number of input name bytes.
