# Prism Tank Solution

## Comparing solutions

The problem setter’s solution enumerates the final firing root and performs tree DP. It sorts child contributions in descending order, tries the number $k$ of retained children, multiplies the top-$k$ sum by the corresponding attenuation factor, and adds the current vertex's damage. For fixed $k$ , choosing the largest contributions is optimal; induction from leaves gives the recurrence below. If blocking is unavailable, all children are retained.

The implementation by Codex (GPT-6) generates an explicit traversal order and processes it in reverse, avoiding recursion on deep trees. Worst-case time is $O(n^2\log(n+1))$ and space is $O(n)$ . Coefficients, rounding and boundary handling are explained below.

## Two blocking regimes

If $b=0$ , no edge may be blocked. If $b\ge1$ , any subset of edges may be blocked: root every component arbitrarily and let the child endpoint select each unwanted parent edge. Each vertex has at most one parent edge, so it selects at most one edge. Even when many edges around one vertex must be blocked, its children can select their respective edges.

## Enumerate the initial target

Fix the initial target as the root and visit its component. Because paths in a tree are unique, when a non-root vertex $u$ is hit, its parent has already been hit and none of its children have. Propagation can therefore continue only through unblocked edges to its children.

Let $f_u$ be the maximum expected damage in the subtree of $u$ , conditional on hitting $u$ and with the blocking plan chosen in advance. This includes the damage of $u$ itself. If edges to $k\ge1$ children $v_1,\ldots,v_k$ are retained, their expected contribution is

$$\left(p_u+\frac{1-p_u}{k}\right)\sum_{j=1}^k f_{v_j}$$

Each child is hit with probability $p_u+(1-p_u)/k$ : it is always hit when the beam branches to every child, and is selected with probability $1/k$ otherwise. Child subtrees are disjoint, so an optimal blocking plan can be fixed independently for each. The events of hitting different children may be correlated, but linearity of expectation still lets us add their contributions.

For $b=0$ , retain every child edge and use the number of children and the sum of their $f$ values in the formula. If there are no children, their contribution is zero.

For $b\ge1$ , sort child values in descending order and enumerate the retained count $k$ . Prefix sums evaluate each candidate. For fixed $k$ , the common coefficient is nonnegative, so the largest $k$ values are optimal. Retaining no child is also an option and contributes zero. Add $d_u$ to the best contribution.

Evaluate bottom-up for every possible root and take the maximum. The implementation uses iterative traversal to handle long chains.

## Correctness

A leaf contributes its own damage. Assume all optimal child values have been computed correctly. For a fixed retained set, the contribution formula has a nonnegative coefficient, so each child should use its optimal subtree plan. These plans act on disjoint subtrees, and when $b\ge1$ their combined set of blocked edges is feasible.

If blocking is forbidden, the algorithm evaluates the only allowed child set. Otherwise, it considers every retained count and the best set for that count. Thus it neither misses an optimal choice nor uses an infeasible plan. Adding the vertex's own damage gives $f_u$ . Induction proves the optimum for a fixed root; enumerating every vertex as root covers all initial targets in the forest.

## Complexity and precision

Time is $O(n^2\log n)$ and space is $O(n)$ . Isolated vertices are valid targets. Compute expectations in floating point and explicitly apply $\lfloor V+\delta+0.5\rfloor$ instead of relying on formatted-output rounding. The input guarantee leaves a gap of at least $0.2$ from a half-integer boundary.

In the code, `BlockLimit` represents the blocking allowance $b$ and `RoundingOffset` represents the rounding offset $\delta$ .
