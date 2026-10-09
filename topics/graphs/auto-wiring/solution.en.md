# Automatic Connectors Editorial

Solution contribution: Codex (GPT-6) supplied the constructive proof from maximum matching to minimum vertex cover, rewrote Hopcroft–Karp with explicit stacks, and added a checker for nonunique outputs. The underlying bipartite matching and vertex-cover methods are established algorithms.

## Comparing solutions

The reference uses Hopcroft–Karp. It stores one adjacency target per relation plus matching arrays. Explicit unit flow also stores forward/reverse residual edges and capacities for relations and source/sink edges. The asymptotic bounds agree; specialized matching uses smaller edge records.

The problem setter’s method partitions selectable endpoints into left and right sides, builds unit-capacity edges from source to left, left to right and right to sink, and uses Dinic for maximum matching. It then constructs a minimum vertex cover by alternating reachability. Unit flows correspond exactly to disjoint matching edges. Starting from unmatched left vertices and following unmatched edges rightward and matched edges leftward gives the cover $(L\setminus Z_L)\cup Z_R$ , whose size equals the maximum matching, as proved below.

Cover construction must start at unmatched left vertices, following unmatched edges rightward and matched edges leftward. Starting on the right requires reversing both the rule and the traversable adjacency directions. The implementation by Codex (GPT-6) uses Hopcroft–Karp’s layered augmentation and explicit stacks. For $V$ vertices and $E$ relations, both Dinic on the unit matching network and Hopcroft–Karp take $O((V+E)\sqrt V)$ time and $O(V+E)$ space.

## Bipartite vertex cover

Workbench ports form the left side $U$ and computer ports form the right side $W$ . Every cable is an edge between them. The desired set is a minimum vertex cover: at least one endpoint of every edge must be selected.

Let $M$ be a maximum matching. Its edges have pairwise disjoint endpoints, so every vertex cover contains at least $\lvert M\rvert$ vertices. Constructing a cover of exactly this size proves optimality.

## Find a maximum matching

Use the [Hopcroft–Karp algorithm](https://epubs.siam.org/doi/10.1137/0202019). Each phase starts a BFS from all unmatched left vertices to layer alternating paths, then finds a collection of disjoint shortest augmenting paths in these layers. Edges on such a path alternate between unmatched and matched; flipping them increases the matching size by one.

The reference stores levels for left vertices only. Crossing a right vertex's matched edge reaches the next left level. An explicit stack replaces recursive DFS. Once a free right endpoint is found, matching edges are flipped from the top of the stack backward. Current-edge indices and failed-vertex marks prevent repeated scans of failed branches in a phase. Searches must respect the shortest augmenting-path length found by BFS.

## Construct the cover by alternating reachability

After finding a maximum matching, search from all unmatched left vertices, using these directions:

- Left to right: follow only unmatched edges.
- Right to left: follow only matched edges.

Let the reachable sets on the two sides be $Z_U,Z_W$ . Output

$$S=(U\setminus Z_U)\cup Z_W$$

**Coverage.** If an edge's left endpoint is outside $Z_U$ , that endpoint is selected. Otherwise its right endpoint belongs to $Z_W$ : an unmatched edge reaches it directly, while for a matched edge the right endpoint is the predecessor that reached this matched left vertex. Thus every edge is covered.

**Size.** No unmatched right vertex is reachable, since that would give an augmenting path and contradict maximality of the matching size. Every unmatched left vertex is in $Z_U$ , so unmatched vertices on either side are unselected. Both endpoints of a matched edge are either reachable or unreachable, and exactly one is selected. Hence $\lvert S\rvert=\lvert M\rvert$ , attaining the lower bound.

The search must start from unmatched **left** vertices with the directions above. Selecting all matched vertices on one side alone need not cover the graph, as a star with one workbench and several computers demonstrates.

## Complexity and judging

Time is $O((n+m)\sqrt n)$ and space is $O(n+m)$ . Isolated vertices do not affect the answer. Parallel cables do not change the optimum and are handled by the implementation.

`tests/checker.py` takes input, reference-answer, and contestant-output paths. It checks integer syntax, ID range, duplicates, declared size, optimal size, and coverage of every edge. Only the optimal size is taken from the reference answer; the selected ports may differ.

Small-instance validation enumerates every nonempty $3\times3$ bipartite graph and every vertex subset to find the optimum directly, with additional random multigraphs. For performance measurements, see [environment and measurements](../../../docs/评测环境与性能.md).
