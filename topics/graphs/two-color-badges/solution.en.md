# Two-Color Badges: Solution

## Comparing solutions

The problem setter’s solution uses a parity DSU. XOR values to roots encode relative colors, merges maintain the two color-class sizes, and a relation within one component checks consistency. Each component may be flipped independently, so the optimum is the sum of its larger class sizes. The invariant and proof below retain this method in full.

Path compression and union by rank give $O((n+m)\alpha(n))$ time and $O(n)$ space. Codex (GPT-6) contributed the program implementation and boundary explanations.

## Approach

Use a disjoint-set union structure with parity. For each vertex, store the XOR of its color with the color of its component root. For each root, maintain two counts: $c_0$ counts vertices with the same color as the root, and $c_1$ counts vertices with the opposite color. These subscripts describe colors relative to the root, rather than the final assigned color labels.

When both endpoints of a request already belong to the same component, accept the edge exactly when their relative parity is $1$ . Otherwise merge the components, forcing the endpoints to have different colors. Their parities to the roots determine whether the two class counts of one component need to be swapped.

The answer is always the sum of $\max(c_0,c_1)$ over all components. On a merge, subtract the contributions of the old components and add that of the new one. Rejection leaves the answer unchanged. Each isolated vertex initially contributes $1$ .

## Correctness

The DSU invariant is that each stored parity gives the required color difference from the component root. In one component, an edge between vertices with equal parity contradicts its different-color requirement; an edge between vertices with opposite parity is compatible. Two separate components can always be flipped independently to satisfy a new edge, and the merge updates their color-class counts accordingly. Thus acceptance and the class counts stay correct.

Within a component, a proper coloring can only exchange the two entire classes. Its maximum contribution to color $0$ is therefore $\max(c_0,c_1)$ . Components can choose their orientations independently, so the maintained sum is exactly the required maximum after each request.

## Complexity

Union by size and path compression give $O(\alpha(n))$ amortized time per request, $O((n+m)\alpha(n))$ total time, and $O(n)$ space.
