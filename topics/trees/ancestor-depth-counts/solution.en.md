# Depth Counts across Ancestor Subtrees: Distance Sums and Centroid Decomposition

## Express repeated counting as a pair weight

Let $d_x$ be depth and $s_x$ subtree size. A node $y$ belongs to exactly those ancestor subtrees of $x$ whose roots are common ancestors of $x,y$ . These are their lowest common ancestor $\operatorname{lca}(x,y)$ and all its ancestors. Thus the weight of $y$ is

$$w(x,y)=d_{\operatorname{lca}(x,y)}+1.$$

The sum of all three answers is easy: set $T_0=0$ and $T_x=T_{\operatorname{parent}(x)}+s_x$ . It remains to find weight sums over nodes with depth strictly below and at most $d_x$ .

## Convert weights to distances

For an activated set $B$ , maintain its size $C$ , depth sum $H$ , and the sum $D(x)$ of distances from $x$ to its nodes. The identity

$$\operatorname{dist}(x,y)=d_x+d_y-2d_{\operatorname{lca}(x,y)}$$

implies

$$\sum_{y\in B}w(x,y)=\frac{(d_x+2)C+H-D(x)}2.$$

The numerator is even. This is ordinary integer division, with no modulus.

Process original-tree depths in increasing order, one entire depth group at a time. Query before activation to obtain $L_x$ . Activate every node in the group, then query again to obtain $U_x$ . Output $L_x,U_x-L_x,T_x-U_x$ . Complete all first queries before any activation in the group, so equal-depth nodes never enter the shallower count.

## Dynamic distance sums with centroid decomposition

Choose a centroid of each component: removing it leaves components of at most half its size. Recurse on those components to obtain a centroid tree of depth $O(\log n)$ . Record each node's original-tree distance to every centroid ancestor.

At a centroid $c$ , maintain:

- $A_c$ , the number of activated nodes in its centroid subtree;
- $B_c$ , their total distance to $c$ ;
- for centroid child $b$ , separate values $A'_b,B'_b$ for that child component, with distances in $B'_b$ measured from its **parent centroid**.

Insert $y$ by walking its centroid-ancestor chain, updating the total and corresponding child-component statistics. To query $x$ , walk its chain and add $B_c+A_c\operatorname{dist}(x,c)$ at each center. If $x$ lies in child component $b$ , subtract $B'_b+A'_b\operatorname{dist}(x,c)$ .

For each activated $y$ , consider the first common centroid where $x,y$ occupy different child components, or one is the centroid itself. Their original-tree path passes through that center, so this layer contributes their true distance. At higher layers, both are in one child component and the subtraction cancels the addition. Lower layers do not contain both. Hence each distance is counted exactly once.

## Correctness and implementation

Centroid statistics give the exact $D(x)$ , and the distance identity gives the weight sum for any activated set. Depth grouping makes the two queries cover strictly shallower nodes and all nodes no deeper than $x$ , respectively. Taking differences with each other and the total gives the required three counts.

Breadth-first traversal provides depth order; its reverse accumulates subtree sizes. Parent labels may be larger, so label order cannot replace traversal order. Component traversals use explicit arrays. Only the centroid decomposition itself is recursive, with logarithmic depth even when the original tree is a long chain.

Distances at each centroid level use 32-bit integers. All aggregate values and answers use 64-bit integers; a single answer is at most $n^2$ . Construction, all insertions and both queries per node take $O(n\log n)$ time and space. The measured maximum working set is about $350.4$ MiB, within the $512$ MB limit; see the [full measurements](../../../docs/benchmark-R25.json).

## Two methods for the full constraints

The reference [std.cpp](std.cpp) uses centroid decomposition for an $O(n\log n)$ time bound. The [heavy-light method](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) provide a parallel option with $O(n)$ space and $O(n\log^2n)$ time. On the reference environment, their largest medians are about $6.83$ and $5.51$ seconds, respectively. Heavy-light decomposition is also faster on these measured cases; asymptotic expressions alone do not determine constants. Both pass all data under the same time limit. Other platforms require new measurements.

The supplied materials contain no usable solver or algorithm explanation. GPT-6 combines classical LCA distance identities, centroid decomposition and heavy-light decomposition into these two algorithms, with proofs and C++17 implementations. Small trees use pairwise ancestor-set intersections. Formal outputs are compared in full between both programs; chain and star outputs also use complete closed-form checks. Other large trees use direct traversals for selected vertices and total-count checks for every vertex.
