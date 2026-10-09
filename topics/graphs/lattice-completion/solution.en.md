# Completing Dial Relations: Solution

## Method and contributions

View the initial relation as a functional graph with exactly one outgoing edge $i\to a_i$ per vertex. A valid completion exists exactly when every directed cycle has length at most two.

The reference program preserves the setter's timestamp traversal, cycle-vertex counting, and subtraction of one- and two-cycle vertices. Codex (GPT-6) organized the C++17 implementation and supplied a sufficiency proof using a total-order extension. See [std.cpp](std.cpp) and the [indegree-peeling alternative](solution-alternative.en.md).

## Proof of the criterion

**Necessity.** A directed cycle of length at least three forces the reverse of each cycle edge by transitivity. Each vertex has only one initial outgoing edge, so that reverse is initially absent. Adding it violates the restriction. Allowing symbol aliases does not avoid this: symbols representing one element must still have relations in both directions.

**Sufficiency.** Suppose cycles have only length one or two. Merge the two symbols of each two-cycle into one element and make every remaining symbol a separate element. After contraction and removal of self-loops, the graph is acyclic. Choose a topological ordering and order all elements in a chain accordingly. Define the completed symbol relation by the resulting non-strict total order.

A nonempty finite chain is a lattice: the larger element of each pair is its join and the smaller its meet. Every initial edge between different elements points forward in the topological order, so its reverse remains absent. Inside one element, both directions of a two-cycle, or the singleton self-loop, were already present. Thus no forbidden reverse is newly added. Every element has a representing symbol, as required, and the construction is valid.

## Timestamp algorithm

Assign increasing numbers to vertices on their first visit. When starting from an unvisited vertex, save this traversal's first number $Begin$ and follow outgoing edges until reaching a visited vertex $v$ .

- If $Number_v<Begin$ , the walk entered an earlier traversal and found no new cycle.
- Otherwise $v$ is on the current walk. With current counter $Timer$ , the new cycle has length $Timer-Number_v+1$ .

Every cycle is counted on its first encounter only. Sum the numbers of cycle vertices, then subtract one for each vertex satisfying $a_{a_i}=i$ . That equality holds exactly for vertices on one- or two-cycles. The remaining count is zero exactly when no longer cycle exists. Each test uses fresh arrays, including when test sizes grow and shrink.

## Complexity

Each vertex is visited once and scanned once more: $O(N)$ time and $O(N)$ space per test. Total time is $O(T+\sum N)$ . There is no need to materialize a dense completed relation.
