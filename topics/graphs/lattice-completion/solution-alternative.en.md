# Completing Dial Relations: Alternative Solution

## Indegree peeling

Codex (GPT-6) supplied this linear algorithm and [alternative.cpp](alternative.cpp). The [main solution](solution.en.md) proves that a completion exists exactly when no cycle has length at least three.

Compute all indegrees and queue every vertex of indegree zero. Repeatedly remove a queued vertex and decrement its unique successor's indegree; queue that successor if its indegree becomes zero. Finally, every unremoved vertex must satisfy $a_{a_i}=i$ . Print `Y` exactly when all do.

A cycle vertex always retains an incoming edge from its cycle predecessor, so it is never peeled. All noncycle vertices form trees directed toward cycles and are removed from leaves inward. Thus the survivors are exactly the cycle vertices. For a survivor, $a_{a_i}=i$ holds precisely on a one- or two-cycle, proving equivalence to the criterion.

Time and space are $O(N)$ per test, with $O(T+\sum N)$ total time. The indegree array and queue give a direct peeling invariant at an extra storage constant, without an asymptotic improvement over timestamps.
