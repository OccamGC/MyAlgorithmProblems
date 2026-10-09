# Building a Tree in Order: Prüfer Codes and Edge Permutations

## Determine the Final Structure

For $n\ge2$ , having exactly one simple path between each pair of vertices is equivalent to being a tree. Each tree has $n-1$ edges, which can be added in any of $(n-1)!$ orders. Every prefix remains a forest, so it causes no obstacle to later additions.

## Count Trees with Prüfer Codes

Given a labelled tree, repeatedly remove the smallest-labelled leaf and record its neighbor until two vertices remain. This produces a sequence of length $n-2$ , with each entry a vertex label.

Conversely, given such a sequence, set each vertex's degree to one plus its number of occurrences. For each next label $v$ , choose the smallest current degree-one vertex $u$ , add edge $(u,v)$ , delete $u$ , and reduce the degree of $v$ . Finally join the last two vertices. At each step, some degree-one vertex is absent from the unread sequence, so the process is defined. This decoding and the leaf-removal encoding undo each other.

Labelled trees therefore correspond bijectively to Prüfer sequences of length $n-2$ , giving $n^{n-2}$ trees. The answer is

$$n^{n-2}(n-1)!\pmod{998244353}\qquad(n\ge2).$$

For $n=0$ or $n=1$ , the empty operation sequence is the only answer. The answer for $n=2$ is also one. No negative exponent is needed.

![Two orders of the same tree](assets/orders.svg)

## Correctness

Every valid edge-addition sequence uniquely determines a labelled tree and a permutation of its edges. Conversely, every such tree and edge permutation forms a valid sequence. The Prüfer bijection counts the trees, and the factorial counts the orders for each tree. Their product counts all answers exactly once.

## Implementation, Complexity and Attribution

Compute the factorial by successive products and $n^{n-2}$ by binary exponentiation, reducing after each product. Two residues multiply to less than $998244353^2<2^{63}$ , so standard 64-bit arithmetic suffices. Time is $O(n+\log(n+1))$ and auxiliary space is $O(1)$ , retaining only the running factorial.

The problem setter's solution uses Cayley's formula and edge permutations; the Prüfer bijection is a classical proof of that formula. GPT-6 supplied the complete bilingual proof, empty-graph explanation and constant-space implementation. [std.cpp](std.cpp) is preferred. The matrix-tree theorem would add computation and implementation cost without an independent advantage for this scope, so no separate program is included. Small cases enumerate edge sets and verify trees with disjoint sets, then count edge permutations. Large cases use an independent product tree. See the [measurements](../../../docs/benchmark-R24.json).
