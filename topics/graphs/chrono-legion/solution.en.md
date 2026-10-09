# Chrono Legion: Solution

## Comparing solutions

The problem setter’s graph construction builds a two-dimensional segment tree over the full grid, answering point counts and maximum ages in squares. For each requirement, it binary-searches the smallest Chebyshev radius whose count suffices, then connects to the oldest point in that closed square. The matrix-tree theorem, Laplacian determinant and factorial for deletion orders are inherited and proved below. The binary search must include radius zero and find the first feasible radius; this ensures that the selected square is the smallest feasible one.

Let the grid be $N\times M$ , with $K$ occupied points and $S$ requirements. Grid-based storage is $O(NM+K^2+S)$ ; graph queries take at most $O(S\log(\max(N,M)+1)\log(N+1)\log(M+1))$ , besides grid construction and insertions. The implementation used by Codex (GPT-6) sorts distances from each occupied point and processes equal-distance groups together. Graph construction takes $O(K^2\log(K+1)+S)$ time and $O(K^2+S)$ space. Both retain the same determinant stage. The alternative fits sparse points on a large grid; it explicitly enumerates point pairs and is not universally faster on dense instances.

## Constructing the communication graph

There are only $K\le200$ buildings, so no two-dimensional data structure over the whole grid is needed.

For each building $i$ , compute its Chebyshev distance to every building: the maximum of the absolute coordinate differences. Include its own zero distance and sort the list. The minimum radius for threshold $D$ is the distance of the $D$-th entry.

Process equal-distance entries as a group. First update the greatest construction time using the whole group, then store the current newest building at every position in that group. A query at position $D$ now includes every building on the radius boundary. The zero-distance group also handles overlapping coordinates correctly.

If the selected building differs from the center, add an undirected edge. Deduplicate edges with a Boolean adjacency matrix. Graph construction takes $O(K^2\log K+\sum_iP_i)$ time.

## Optimal deletions correspond to spanning trees

Let the graph contain $E$ edges. A connected graph must retain at least $K-1$ edges. Keeping any spanning tree allows all other edges to be removed, so the maximum number of deletions is

$$q=E-K+1$$

Every optimal deletion sequence leaves exactly one spanning tree. Conversely, after fixing a spanning tree, the other $q$ edges can be deleted in any order: the tree remains intact throughout, so connectivity is preserved. Different remaining trees give different deleted edge sets, preventing double counting.

If the graph has $\tau$ spanning trees, the answer is

$$\tau\cdot q!\pmod{\mathrm{mod}}$$

## The matrix-tree theorem

Construct the Laplacian matrix $L$ . A diagonal entry is the vertex degree; an off-diagonal entry is $-1$ for an edge and $0$ otherwise. Delete the row and column belonging to the same vertex to obtain a $(K-1)$ by $(K-1)$ matrix $A$ . The matrix-tree theorem gives $\tau=\det A$ .

For $K=1$ , the cofactor is an empty matrix, whose determinant is $1$ . This also counts the unique empty spanning tree.

## Determinants with composite moduli

A nonzero pivot need not have a modular inverse. Use Euclidean elimination instead, storing every entry as its representative in $[0,\mathrm{mod}-1]$ .

When processing column $i$ , for each later row $j$ , repeat while $A_{ji}\ne0$ :

1. Compute the ordinary integer quotient $h=\lfloor A_{ii}/A_{ji}\rfloor$ .
2. Subtract $h$ times row $j$ from row $i$ , reducing all entries modulo $\mathrm{mod}$ .
3. Swap rows $i$ and $j$ , and negate the determinant sign.

Adding a multiple of another row preserves the determinant, while a row swap negates it. These identities hold modulo any integer. The two representatives in the current column follow the Euclidean algorithm, so the loop terminates. If the resulting pivot is zero, the determinant is zero. Otherwise continue; at the end multiply the diagonal entries and the accumulated sign.

Every row swap must contribute its negative sign. Elimination using Fermat inverses is not valid for arbitrary moduli. Finally multiply by $q!$ .

## Correctness

Distance sorting with complete equal-distance groups finds the minimum radius and newest included building for every threshold, so it constructs the required graph. Optimal deletion sequences correspond bijectively to a spanning tree together with a permutation of all remaining edges. The matrix-tree theorem counts the trees, and Euclidean row operations preserve the correct determinant and sign for every modulus. The resulting product is therefore the required sequence count.

## Complexity

Graph construction costs $O(K^2\log K+\sum_iP_i)$ . A conservative determinant bound is $O(K^3\log\mathrm{mod})$ , and the factorial costs $O(E)$ . Auxiliary space is $O(K^2+\sum_iP_i)$ , which is $O(K^2)$ under these constraints.

Use 64-bit integers for construction times and modular products. Coordinates are used only to measure distances between buildings, with no storage proportional to $NM$ .
