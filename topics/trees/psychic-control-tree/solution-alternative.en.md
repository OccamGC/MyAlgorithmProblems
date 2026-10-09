# Psychic Control Tree — Solution

> Peer method: small-to-large sets with cyclic DFS-distance sums. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.


## The minimum connecting subtree

Let $S$ be the controlled vertices. The union of all routes to a meeting point is connected and contains $S$ , so it must contain the minimal subtree $H$ connecting $S$ . Meeting anywhere inside $H$ uses only $H$ . Since vertex weights are positive, the optimum is the vertex-weight sum of $H$ minus that of $S$ .

## Maintain the subtree weight in DFS order

Place each non-root vertex weight $v_x$ on the edge from its parent to $x$ . Let $d(a,b)$ be distance under these edge weights and let $g$ be the lowest common ancestor of all vertices in $S$ . The vertex-weight sum of $H$ is its edge-weight sum plus $v_g$ .

Sort $S$ by DFS entry order as $s_1,\ldots,s_t$ and set $s_{t+1}=s_1$ . Then

$$W(H)=\frac12\sum_{i=1}^{t}d(s_i,s_{i+1})+v_g$$

Each edge of $H$ separates selected vertices on both sides. Selected vertices on its descendant side form a contiguous block in DFS order, so the cyclic sequence crosses this edge exactly twice. Edges outside $H$ are never crossed. This proves the identity, including singleton sets.

Store DFS indices in an ordered set. If a new vertex $x$ has cyclic predecessor $a$ and successor $b$ , insertion adds

$$d(a,x)+d(x,b)-d(a,b)$$

to the cyclic distance sum. Also maintain the sum of selected vertex weights. The LCA of the first and last selected vertices in DFS order is $g$ : every subtree occupies a contiguous interval, so the smallest ancestor subtree containing both extremes contains all selected vertices between them.

## Merging and correctness

Process control vertices from leaves to root. Keep the largest child's set, insert the vertices from all other child sets, and insert $e_u$ . These disjoint sets form exactly $S_u$ , because $e$ is a permutation. The insertion identity maintains the exact cyclic distance sum. Applying the subtree formula and subtracting the controlled weights therefore yields the optimum for every vertex.

## Complexity and implementation

Whenever a vertex moves from a smaller set into a larger one, its set size at least doubles. It moves $O(\log n)$ times, and each insertion with binary-lifting LCA queries costs $O(\log n)$ . Total time is $O(n\log^2(n+1))$ and space is $O(n\log(n+1))$ . An explicit stack and reversed DFS order avoid recursion proportional to tree height. Distance sums use 64-bit integers.
