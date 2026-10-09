# Melon Planting — Solution

## Comparing solutions

The problem setter’s maximum-yield solution uses a unit-capacity flow network for maximum matching. For minimum yield, it recursively chooses for each vine either no fruit or one unoccupied neighbor. If a vine remains unmatched, every neighbor must eventually be occupied by another vine, or the process has not finished. The search tracks these required positions and how many remaining vines can reach them, enabling pruning. Its terminal states are precisely maximal matchings, so minimizing their sizes is valid. With at most four neighbors per vine, the unpruned search bound is $O(5^p)$ time and $O(V+p)$ auxiliary space, for $p$ vines and $V$ cells.

The implementation used by Codex (GPT-6) enumerates the set $S$ of fruit-producing vines. All neighbors of vines outside $S$ become mandatory occupied positions; matching tests whether both $S$ and these positions can be covered. The equivalence is proved below. This phase takes $O(2^p(V+p^2))$ time and $O(V+p)$ space. It reduces branching and makes terminal feasibility explicit, but runs matching for each subset. The problem setter’s pruning may be faster in practice; no timing comparison was made. Maximum yield remains a maximum-matching problem.

## Model growth as a matching

Put vines on the left and initially empty cells on the right, with an edge for orthogonal adjacency. Producing a melon chooses one edge. Each vine and each empty cell can be used at most once, so the final harvest is a matching.

Growth stops exactly when no edge has two unmatched endpoints: the matching is **maximal**. This means no edge can be added directly; it does not mean the matching has **maximum** size. Conversely, every maximal matching can be realized by letting its vines grow along the chosen edges in any order. These choices do not conflict, and no further growth is possible afterward.

## Maximum harvest

A maximum matching is maximal, so ordinary bipartite maximum matching solves this part. Start augmenting paths from the left vertices, rearranging existing matches when necessary. Each successful augmentation increases the size by one. The absence of augmenting paths characterizes a maximum matching.

## Minimum harvest

Let $p$ be the number of vines. Enumerate the set $S$ of vines that eventually produce melons. Every neighbor of an unproductive vine must be occupied when growth stops. Let the required empty cells be

$$R=N(\overline S)$$

We need a matching that:

- uses only vines in $S$ ;
- covers every vine in $S$ ;
- covers every empty cell in $R$ .

Reject immediately if $|R|>|S|$ . Otherwise, first start augmenting paths from $R$ , using only vines in $S$ , to cover all of $R$ . Then start augmenting paths from unmatched vines of $S$ , allowing all empty cells, to cover all of $S$ .

The second phase preserves the first phase's coverage. Internal vertices of an augmenting path change partners but remain matched. If a matching satisfying both requirements exists, any matching from the first phase can be augmented to size $|S|$ while keeping every vertex of $R$ matched. Thus the two-phase test is necessary and sufficient.

A successful matching has $|S|$ edges, and every neighbor of every unproductive vine is occupied. It is therefore maximal. Minimize $|S|$ over successful sets. The maximum matching size provides an initial upper bound, so sets that cannot improve it may be skipped.

## Complexity and implementation

Let $V=nm$ . There are at most four edges per vine, so $E\le4p$ . The maximum case takes $O(V+pE)=O(V+p^2)$ time. The minimum case enumerates $2^p$ sets and spends $O(V+p^2)$ per set, for $O(2^p(V+p^2))$ total time. Both use $O(V+p)$ space.

Minimum-case inputs guarantee $p\le18$ . With no vines or no empty cells, the answer is zero. The reference uses bit masks only for the minimum case; the maximum case has no bit-width restriction on its vine count.

## Verification

The independent checker enumerates every three-state $2\times3$ grid, directly enumerates its matchings, and checks which are terminal. It verifies both extrema and also tests random small grids. This model does not use the two-phase feasibility test.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
