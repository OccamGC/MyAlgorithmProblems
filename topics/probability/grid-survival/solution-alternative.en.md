# Survival on a Grid: Alternative Solution

Contribution: Codex (GPT-6) compresses roads into a sparse graph so each DP round depends on the road count. Full path-counting and normalization arguments are in the [grid-DP explanation](solution.en.md).

## Number only road cells

Read the grid row by row and create a vertex only for a one. Keep road IDs for the previous row and the ID immediately to the left in the current row. A road connects to existing roads above and to its left, recording both directions. A pit resets its column and left-neighbor state to empty. Each undirected adjacency is thus created once when first encountered, without storing the whole grid or a full-size ID matrix.

Let $V$ be the road count. Each vertex has at most four neighbors and starts with count one. In every round, sum each road's previous neighbor counts using two rolling arrays. Sum the final counts and divide by $nm\cdot4^k$ . The denominator still uses every grid cell, not just roads, because a starting cell may be a pit.

## Correctness

The ID mapping preserves exactly the roads and all legal one-step moves between them. Every safe grid path corresponds uniquely to a graph walk of equal length. Initial count one at each road and the last-step recurrence preserve this correspondence, so the final sum is the safe-process count. No vertex represents a pit or an out-of-grid position, so failed processes are excluded. With no roads the arrays and total are empty and zero. An isolated road contributes one process for zero steps and none for a positive number of steps.

## Costs and suitable shapes

Again let $B=\lceil\log_2 P\rceil$ . Construction takes $O(nm)$ time and each round $O(V)$ , for $O(nm+kV+B^2)$ total time. Space is $O(V+m)$ , including previous-row IDs and the current input row. Each exact count is at most $2^{50}$ . Modular arithmetic uses the same overflow-safe method as the preferred implementation.

Sparse roads avoid scanning many pits in every round. Dense roads require additional adjacency storage and do not guarantee an advantage over grid scanning. Both are parallel full-range methods; the reference program keeps the setter's grid DP, which needs no graph construction. Program: [alternative.cpp](alternative.cpp).
