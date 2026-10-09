# Giant Christmas Tree — Alternative Solution

Setter method: centroid decomposition for diameter maintenance under deletion. Codex (GPT-6): the reverse-time method, plus local Euler intervals, path operations, and iterative construction for the online method.

## Centroid decomposition and local reachability

This method retains the setter's centroid-based diameter idea and supplies the path-deletion interface. For every centroid $c$ , root its decomposition component at $c$ and compute a local Euler order. Record each vertex's distance, first branch, and local subtree interval. Track only vertices still reachable from $c$ by lit edges within this component.

Each branch has an ordered set of active `(distance, vertex)` pairs. Another set stores the maximum distance of each nonempty branch. Include a zero-distance candidate for the centroid itself. The sum of the two largest distances from different branches is the longest lit path through $c$ . A global ordered set stores all centroid candidates.

## Delete an edge

Consider only centroid ancestors common to its two endpoints. Relative to each such centroid, the deeper endpoint's local subtree is exactly the part disconnected by this edge. Use `lower_bound` in the ordered set of active Euler indices to find and remove points in that interval. Update branch maxima, the centroid candidate, and the global candidate. If an earlier deletion already disconnected the subtree, the interval contains no active point.

Each vertex is removed at most once at each centroid level. Initialize by deleting initially dark edges through the same interface. For each path operation, use parents, LCA, and ancestor skipping to submit only still-lit edges. Explicit stacks construct the decomposition and Euler intervals without recursion proportional to the original tree depth.

## Correctness

In each relevant local tree, removing the deeper endpoint's subtree deletes exactly the newly disconnected vertices, preserving the reachability invariant. Two active vertices from different branches have an entirely lit path through the centroid, so every candidate is valid.

Conversely, take any lit path and the first decomposition centroid that separates its endpoints into different branches, allowing an endpoint equal to the centroid. That centroid lies on the path, and both endpoints are active in its component. Its candidate is at least this path's length. The global maximum is therefore exactly the forest diameter.

## Complexity and Tradeoffs

There are $O(N\log N)$ vertex-centroid records. Each insertion or deletion costs $O(\log N)$ ; locating first deletions along paths adds $O(M\log N)$ . Total time is $O(N\log^2N+M\log N)$ , with $O(N\log N)$ space. Reading the global maximum takes constant time.

Answers are available online, at a higher time and memory cost from ordered sets. The 1024 MiB limit is preserved, and measured timing allows this approach. The simpler, faster [offline method](solution.en.md) remains the default. Codex (GPT-6) supplied local interval deletion, iterative construction, input adaptation, and validation; see [alternative.cpp](alternative.cpp).

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
