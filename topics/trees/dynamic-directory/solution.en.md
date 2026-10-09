# Dynamic Directory Tree — Solution

Credits: the problem setter’s solution uses a Link-Cut Tree with edge nodes and edge reuse. Codex (GPT-6) contributed multi-node LCA handling, auxiliary-ancestor propagation, endpoint mapping and proof exposition.

## Comparing solutions

### Problem setter’s solution: a Link-Cut Tree with edge nodes

The problem setter’s program represents each edge by a weighted auxiliary node and maintains path sums with a Link-Cut Tree. Rerooting reverses a path; moving a subtree cuts its parent edge and reuses that edge node to connect the new parent. Weight updates use a lowest common ancestor and path predecessors to check adjacency. The following sections explain the operations and their correctness.

For a query containing several nodes, the problem setter’s method computes the lowest common ancestor of every consecutive pair in the input order and selects the one with **minimum structural depth**. A singleton query uses that node directly. Let $c$ be the lowest common ancestor of all queried nodes. Every consecutive-pair ancestor lies in $c$'s subtree. If a queried node equals $c$ , an adjacent pair yields $c$ . Otherwise the queried nodes occupy at least two child subtrees of $c$ , and some consecutive pair must cross those groups. Thus the shallowest pair ancestor is exactly $c$ . The problem setter’s program compares the number of original nodes on a root path, rather than weighted distance, so the argument also holds for negative weights.

Let $K$ be the total number of query nodes. Standard Link-Cut Tree operations give $O((n+m+K)\log(n+1))$ total amortized time and $O(n)$ space. Before a splay, push tags only along auxiliary ancestors; following path-parent pointers beyond auxiliary roots adds work not covered by this analysis.

### Implementation details

The Codex implementation folds lowest common ancestors one at a time, removing the original-node count and repeated depth comparisons. It explicitly stores the current root and pushes tags only along the auxiliary ancestor chain before each splay, matching the standard operations used in the analysis. Path sums use 64-bit integers.

An ordered map from endpoint pairs to edge nodes makes edge-existence checks and bookkeeping after moves more direct. It adds linear-space overhead and map lookups and insertions. Both implementations use the same dynamic-tree algorithm. No direct timing comparison between these implementations is available.

## The common path ends at the LCA

Under the current root $r$ , the intersection of paths to the queried vertices is exactly the path to their lowest common ancestor. Fold the vertices by setting $c=a_1$ and repeatedly computing $c=\operatorname{LCA}(c,a_i)$ .

This is a structural statement about paths, independent of the signs of edge weights. Minimum weighted distance cannot replace the LCA when weights may be negative.

## Represent each edge by a node

Replace an edge $u,v$ by $u\!\to e\!\to v$ . The auxiliary node $e$ stores its weight; original vertices have weight zero. Thus sums of node weights on expanded paths equal sums of edge weights in the original tree. There are $2n-1$ expanded nodes.

A Link-Cut Tree represents access paths by splay trees storing children, parent pointers, reversal tags, values and subtree sums. These auxiliary child pointers are not the parent-child relations in the problem.

- `Access(x)` exposes the path from the represented root to $x$ and splays $x$ to its auxiliary root.
- `MakeRoot(x)` reverses this exposed path, making $x$ the represented root.
- `Link` joins known-disconnected nodes, and `Cut` removes an edge between known-adjacent nodes.

With a fixed represented root, call `Access(a)` and then `Access(b)` . The final auxiliary path junction processed by the second access is their LCA; the implementation returns it. The LCA of original vertices is still an original vertex.

## Implement the operations

Before a query, make $r$ the represented root and fold its requested vertices into their LCA $c$ . After accessing $c$ , the exposed sum is the answer.

For rerooting, only record the new current root. The next operation needing root-dependent information calls `MakeRoot` .

For edge updates, an ordered map associates each unordered endpoint pair with its edge node. Ignore a missing pair; otherwise access that edge node and change its value.

Before a subtree move, compute $\operatorname{LCA}(a,b)$ under the current root. It equals $a$ exactly when $b$ lies in $a$'s subtree, so ignore those moves, including $a=b$ and moving the current root.

Otherwise access $a$ . Its predecessor on the exposed root path is its parent-edge node $e$ . Find it by following right children in the left auxiliary subtree, then immediately splay it. Its recorded endpoints identify the old parent. Cut both connections of $e$ , reuse this same node with the new weight, link $a\!\to e\!\to b$ , and update the endpoint map. The number of allocated nodes stays fixed.

Since $b$ is outside the detached subtree, the new edge connects two different components, preserving a tree. Internal subtree edges remain unchanged. Moving to the existing parent is legal and simply replaces that parent edge's weight.

## Correctness and complexity

Edge nodes preserve path sums between original vertices. Moves and rerooting maintain exactly the required tree and root, and the map contains exactly the current edges. Exposed path sums and the LCA intersection property therefore answer every query correctly. Reversal tags are propagated down auxiliary ancestors before rotations, so structural decisions use current child directions.

Let $K$ be the total number of queried vertices. Total time is $O((n+m+K)\log(n+1))$ amortized, with $O(n)$ space. Propagation and predecessor search use explicit stacks or loops, avoiding recursion proportional to the original tree's height.

For the underlying structures, see Sleator and Tarjan's [A Data Structure for Dynamic Trees](https://www.cs.cmu.edu/~sleator/papers/dynamic-trees.pdf) and [Self-Adjusting Binary Search Trees](https://www.cs.cmu.edu/~sleator/papers/Self-Adjusting.htm).

## Validation

An independent adjacency-list model constructs root paths directly, intersects their prefixes and performs subtree moves. Tests include negative weights, moves after rerooting, self-subtree moves, nonexistent edges, single- and multiple-vertex queries and no operations. Formal cases additionally exercise long chains and repeated edge-node reuse.

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.
