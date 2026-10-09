# Factorio: Simple Rail Network — Minimum Outgoing Edges by Component

Codex (GPT-6) applies the established Borůvka algorithm after contracting nonpositive edges. Program: [alternative.cpp](alternative.cpp). Nonpositive-edge handling follows the setter's method in the [main editorial](solution.en.md).

## Merge in rounds

After selecting all nonpositive edges, repeat:

1. Scan every positive edge and record a cheapest outgoing edge for each current component.
2. Process those candidates. If their endpoints are still separate, select the edge, add its cost and unite them.
3. Stop if no union occurred; otherwise continue until one component remains.

Both endpoint components may nominate the same edge. Check the disjoint set again before charging for it. Ties retain the earlier input edge: scans have a fixed order, and a candidate is replaced only by a strictly lighter edge.

## Correctness

Every candidate is a lightest edge across the cut of a current component, so it satisfies the minimum-spanning-tree cut property. Use input index as a secondary key to give equal-cost edges a consistent strict order. Each cut then has a unique minimum under this order. Those edges belong to the same minimum spanning tree selected by that order, so they can be added together safely. Disjoint-set checks skip duplicate or already-connected candidates.

Repeated merging produces a minimum spanning tree. If several components remain after a round with no union, the scan of all edges proves that they cannot be connected. Combining this tree with all required negative edges and free zero edges is optimal.

## Complexity and tradeoffs

Within each unfinished connected region, every component nominates an outgoing edge. Each merged result therefore contains at least two previous components, halving their number per round. Isolated components remain unchanged. Every region finishes in $O(\log(n+1))$ effective phases, plus a stopping check.

The implementation initializes and visits an $n+1$ candidate table and scans all edges per round. Time is $O((n+m\alpha(n))\log(n+1))$ and space is $O(n+m)$ . It avoids sorting but rescans edges and uses an extra candidate array. It has no universal practical speed advantage over Kruskal and is retained as a backup merging strategy; see the [measurements](solution.en.md#measured-results).
