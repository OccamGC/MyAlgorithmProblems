# Redstone Computer — Solution

## Comparing solutions

The problem setter’s program converts each bit's relations into 2-SAT implications. It builds all bit graphs together, finds SCCs with recursive Tarjan, and selects consistent truth components on the condensation DAG. A variable and its negation in one SCC imply impossibility; otherwise reverse topological selection yields an assignment. There are no edges between bits, so they may be solved independently. The implication rules and proof below apply to both.

The implementation used by Codex (GPT-6) builds one bit graph at a time, reuses storage and uses explicit traversal for SCCs. For $n$ numbers, $m$ relations and $k$ bits, both take $O(k(n+m))$ time. Simultaneously stored graph space drops from $O(k(n+m))$ to $O(n+m)$ , but relation strings and output remain stored, so the total bound is still $O(k(n+m))$ . The benefits are fewer graph objects and no deep recursion, not a lower asymptotic bound for all storage.

## Solve each bit independently

Bitwise operations do not transfer information between positions. Solve the Boolean constraints separately for each bit, then combine the results. Let the two variables at one bit be $u,v$ and the required bit be $c$ .

Enumerate $(s,t)\in\{0,1\}^2$ . If $s\mathbin{\mathrm{op}}t\ne c$ , forbid this pair using the clause

$$\neg(u=s)\lor\neg(v=t)$$

It gives implications $(u=s)\Rightarrow(v=1-t)$ and $(v=t)\Rightarrow(u=1-s)$ . This handles all three operators uniformly and remains valid when $a=b$ .

## Strongly connected components and assignment

Create two nodes per variable, representing values zero and one. Find strongly connected components in the implication graph. If both nodes of a variable belong to one component, they force each other and that bit is impossible, so the whole instance is impossible.

Otherwise assign values using the component topological order. The reference uses Kosaraju's algorithm: record DFS finishing order in the original graph, then traverse the reversed graph in reverse finishing order. Its component numbers increase in topological order of the original graph. Choose the literal with the larger component number, setting $x_i=1$ exactly when its one-node has a larger number than its zero-node.

## Correctness

Each clause excludes exactly its forbidden pair and preserves the legal pairs, so the implication graph is equivalent to the Boolean constraints. Mutually reachable complementary literals cannot receive consistent values. Without such a conflict, the topological assignment satisfies every implication: an implication from a chosen literal to an unchosen one, together with its contrapositive implication, would contradict the rule of choosing the larger component number.

Combining valid assignments for all bits satisfies every bitwise relation. Conversely, an impossible bit rules out every full assignment. Thus the algorithm is correct.

## Complexity and judging

Each bit uses $O(n+m)$ graph vertices and edges and takes $O(n+m)$ time. Total time is $O(k(n+m))$ . The current graph takes $O(n+m)$ space; including relation strings and the answer, total space is $O((n+m)k)$ . Traversals use explicit stacks.

`tests/checker.cpp` takes paths for the input, reference output, and contestant output. When the reference says `No` , it checks the impossibility marker. Otherwise it evaluates all relations for the submitted assignment, accepting any valid one and rejecting wrong widths, nonbinary characters, or extra output. The empty assignment requires zero output numbers.
