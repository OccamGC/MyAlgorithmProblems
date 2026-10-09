# Melon Planting 2: Solution

**Solution improvement: Codex (GPT-6).** This solution simplifies the subset feasibility test and combines established Gray-code and augmenting-path methods to design and implement the incremental matching solution for this problem, improving the time bound to $O(p2^p)$ .

## Terminal states are maximal matchings

Build a bipartite graph with vines on one side, plots on the other, and designated connections as edges. Every growth step selects a matching edge. Growth stops exactly when no edge has two unmatched endpoints, so we need a **maximal matching of minimum size**. Any maximal matching can be realized by executing its selected growth steps in any order.

## Enumerate the vines allowed to grow

Let $L$ contain all vines. Enumerate $S\subseteq L$ : only these vines are allowed to grow, but they need not all grow. Vines outside $S$ remain unmatched, so all their neighboring plots must be occupied. Define

$$R=N(L\setminus S)$$

It is sufficient to test whether $G[S,R]$ has a matching covering all of $R$ . If its maximum matching size is $\nu(S,R)$ , the test is

$$\nu(S,R)=|R|$$

Why does the smallest passing value of $|S|$ give the answer?

1. For a passing set, execute a matching covering $R$ . Then let unmatched vines in $S$ continue growing into other empty plots until no step remains. Plots in $R$ stay occupied throughout, so vines outside $S$ never get an opportunity. The result is a maximal matching with at most $|S|$ edges.
2. Take an optimal terminal state and let $S$ be its matched vines. No vine outside $S$ can grow, so every plot in $R$ is occupied. The optimal matching's edges incident to $R$ form a matching covering $R$ . Thus this set passes, with $|S|$ equal to the optimum.

Together these imply

$$\mathrm{OPT}=\min_{\nu(S,R)=|R|}|S|$$

Only the optimal count is required. To construct a terminal state from an arbitrary passing set, also perform the additional growth steps in the first argument.

## Enumerate sets in Gray-code order

Ordinary binary counting may flip several bits at once. Instead use the reflected Gray code

$$g(t)=t\mathbin{\oplus}\lfloor t/2\rfloor$$

for $t=0,1,\ldots,2^p-1$ , where $\oplus$ is bitwise XOR. Consecutive codes differ in exactly one bit, so each step changes the membership of one vine. For example, the three-bit order is `000,001,011,010,110,111,101,100` .

For each relevant plot, maintain $c_v$ , the number of adjacent vines in $L\setminus S$ . Then $v\in R$ exactly when $c_v>0$ . Changing one vine affects at most its four designated plots. Insert or delete a right-side vertex only when its counter crosses zero.

One Gray-code step therefore inserts or deletes at most one left-side vertex and four right-side vertices of $G[S,R]$ .

## Repair the maximum matching after one vertex changes

Maintain a maximum matching of the current graph. A single vertex insertion or deletion changes the maximum size by at most one:

| Operation | Action |
| --- | --- |
| Insert a vertex | Search for one augmenting path starting at the new vertex; increase the size if successful. |
| Delete an unmatched vertex | Delete it; the existing matching remains maximum. |
| Delete a matched vertex | Remove its matching edge, then search for one augmenting path starting at its former partner; restore one edge if successful. |

The search may start on either side. Alternate between unselected and selected edges, and flip the path when an unmatched vertex on the opposite side is reached.

After insertion, any new augmenting path must start or end at the new vertex; otherwise the old graph already had one. After deletion of a matched vertex, a path restoring the old matching size must start or end at its newly unmatched partner, for the same reason. Thus one search is sufficient after every update.

Split each set change into individual vertex updates and restore a maximum matching after each one. Only after the vine and all affected plots have been updated do we test $\nu(S,R)=|R|$ and update the answer. Intermediate graphs have valid maximum matchings but are not evaluated as candidate sets.

An insertion needs no search if every vertex on the opposite side is already matched. After removing a matching edge, no search is needed if the remaining matching already saturates the smaller side. These optimizations use an upper bound on matching size and preserve the test.

## Complexity and boundaries

Let $E$ be the edge count. Discard plots with no adjacent vine, leaving at most $E\le4p$ relevant plots. One augmenting search takes $O(p+E)=O(p)$ time. Each Gray-code step makes a constant number of vertex updates, giving $O(p2^p)$ time and $O(p)$ space. The simple loop locating the changed bit is also within this time bound.

If there are no connections, return zero immediately. Otherwise initialize $S=\varnothing$ , an empty matching, and all relevant plots in $R$ . Use an unsigned mask; this problem has $p\le24$ . The maximum number of search-stamp updates also fits in a signed 32-bit integer. The exponential complexity parameter remains the number of vines $p$ .

## Verification and reproduction

The small-instance oracle enumerates all matchings and requires every unselected edge to have at least one matched endpoint. Checks cover all graphs with three vertices on each side, unequal degrees, isolated vertices, and random connections. Small grid instances are also compared with the frontier DP for Melon Planting 3 and the original two-stage matching algorithm.

See [std.cpp](std.cpp) and the [generation plan](tests/plan.json). The [matching-rebuild baseline](tests/slow.cpp) retains both matching phases for timing comparisons. Performance measurements are in [environment and measurements](../../../docs/评测环境与性能.md).
