# Factorio: Technology Tree — Three-State Dynamic Programming

Codex (GPT-6) applies established three-state depth-first traversal and memoization to evaluate finish times along dependencies. Program: [alternative-depth-first.cpp](alternative-depth-first.cpp). The [main editorial](solution.en.md) provides the shared model and proof of optimal finish times.

## Evaluating dependencies

Ignore dependencies with any completed endpoint. Here, store $u\to v$ to mean that $u$ depends on $v$ , reversing the queue algorithm's graph direction. Each node is unseen, active or finished.

Start at an unseen node. An explicit frame stores the current node and next dependency edge. For an unseen dependency, push its frame first; the parent reads its result after it finishes. For a finished dependency, update the maximum prerequisite finish time. After all dependencies are processed, add the node's duration and mark it finished.

## Cycle detection and correctness

Active nodes are exactly the current depth-first path. An edge to an active node closes a cycle with that path, so print `bad idea` . Conversely, an acyclic directed graph cannot have such a back edge.

A node is finalized only after all its dependencies. Induction over finalization order therefore proves that its result equals the earliest-finish recurrence. Several dependents may reuse a finished result without expanding it again. Explicit frames preserve recursive entry and return order.

## Complexity and tradeoffs

Each node enters and leaves once. Each edge is inspected at most before descending to a child and after returning. Time is $O(n+m)$ . Adjacency, states, results and the explicit stack use $O(n+m)$ space.

This avoids indegree counts but maintains traversal states and frames instead. Both algorithms are linear; the distinction is their traversal organization. Add a node's duration only when its frame finishes, and use 64-bit results. See the [main measurements](solution.en.md#verification-and-use).
