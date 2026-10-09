# Grinder Editorial

> Peer method: centroid decomposition with a segment tree. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.

Solution contribution: Codex (GPT-6) adapted centroid decomposition and segment trees to exclude endpoint classes by depth and propagate candidate values to path interiors, with a proof and iterative implementation. Centroid decomposition and segment trees are established methods.


## Count length in edges

The statement already counts edges, so set $A=L$ and $B=R$ . If $A=0$ , single-vertex paths must be considered.

Let $[A,B]$ be the permitted edge-count interval. Choose a centroid $c$ of the current component: removing it leaves components of size at most half the original size. A valid path either passes through $c$ or lies entirely in one remaining component. Process the former paths, then process the remaining components separately.

## Valid endpoint pairs through the centroid

For each eligible endpoint $x$ , record its distance $d_x$ from $c$ in edges and the vertex-weight sum $s_x$ on that path, including both endpoints. Combining endpoints $x,y$ gives value

$$s_x+s_y-v_c$$

The length constraint becomes

$$A-d_x\le d_y\le B-d_x$$

Assign a distinct class to each branch left after deleting $c$ . The simple path between two non-centroid endpoints passes through $c$ exactly when they belong to different branches. A query therefore excludes the current endpoint's branch.

Combining endpoints in the same branch would count a shared segment twice and create a route with repeated vertices. Their actual simple path is handled later inside that branch's component.

The centroid has its own class $-1$ , depth $0$ , and sum $v_c$ . A non-centroid endpoint may pair with the centroid. When querying for the centroid, exclude no class; if zero edges are permitted, it may pair with itself, giving value $v_c$ .

Endpoints deeper than $B$ cannot participate in a valid path through the centroid, so collection may stop in that direction. Such vertices remain available in later decomposition components.

## Keep two distinct classes at each depth

At each depth, consider the largest path sum from every class. Keep only the two largest values from **distinct classes**, and apply the same rule when merging segment-tree nodes.

Two classes suffice because a query excludes only one class. If the largest candidate is allowed, use it; otherwise use the best candidate of another class. Each child interval need supply only its best two distinct classes: a discarded candidate cannot become one of the needed candidates after merging. Values may tie, but the retained classes must differ.

For endpoint $x$ , query the depth interval

$$[\max(0,A-d_x),\min(D,B-d_x)]$$

where $D$ is the maximum collected depth. An empty interval or absence of an eligible class gives no candidate. Otherwise obtain $g_x$ , the best value of a path with endpoint $x$ passing through $c$ .

## Update every vertex on the path

Updating only endpoints misses internal vertices. Store parent indices in the traversal rooted at $c$ . Initialize each vertex's tag to $g_x$ , then traverse in reverse order and maximize each parent's tag with each child's tag.

Every candidate $g_x$ comes from a path containing the entire segment from $x$ to $c$ , so propagating it to these ancestors is valid. Conversely, any valid path through $c$ and a vertex $u$ has at least one endpoint in the local subtree of $u$ . That endpoint has a candidate at least as good as this path, which propagates to $u$ . Thus this step computes each vertex's best value among paths through $c$ .

Take the maximum across all decomposition rounds. Every path is handled when it first encounters a removed centroid; until then, it stays within one remaining component. No valid path is omitted.

## Implementation and complexity

Let $s$ be the current component size. Iterative traversals compute parents, subtree sizes, the centroid, and endpoint records. Building the segment tree and propagating tags take $O(s)$ time; all range queries take $O(s\log(s+1))$ time.

There are $O(\log(n+1))$ decomposition levels, so total time is $O(n\log^2(n+1))$ and space is $O(n)$ . Components are held in an explicit work stack, with no recursive traversal of the original tree. Temporary arrays are released after processing each component.

Every path value has absolute value at most $1000n$ . The implementation uses an internal marker smaller than all valid values, never adds it to a path sum, and finally prints `-1061109568` for vertices without an answer. Negative valid values must not be replaced by zero.

## Validation

Small-instance checks enumerate valid paths directly and update every vertex on each path. They cover random trees, chains, stars, single vertices, negative weights, and impossible length requirements. Maximum-size tests also check traversal and memory use; see [environment and measurements](../../../docs/评测环境与性能.md).

## Asymptotic bounds and measured runtime

The edge-decomposition method expands the tree to $2n-1$ vertices and handles dummy vertices, depth buckets, and edge-to-vertex answer conversion. This method works directly on the edge-decomposition method tree. A star becomes singletons after removing its center, giving $O(n)$ work here, while the edge-decomposition method's dummy chain still needs several edge-decomposition levels. On the measured random tree, the edge-decomposition method's component-size sum is about 3.66 times larger. A higher general worst-case bound is therefore consistent with lower measured runtime.

See the [main editorial](solution.en.md#asymptotic-bounds-and-measured-runtime) for the full parameter analysis, operation counts, and measurements.
