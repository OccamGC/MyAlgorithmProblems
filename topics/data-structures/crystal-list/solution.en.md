# Crystal List: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: a uniform-type segment tree.** The uniform-type segment tree is the preferred method. An ordered interval map directly represents equal-type runs and provides an alternative with the same asymptotic amortized bounds. Segment-tree construction must handle an empty sequence separately instead of recursing on an empty interval.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the ordered interval map method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [alternative editorial](solution-alternative.en.md).

## Segment tree with uniform-type tags

Build a segment tree over positions. Each node either records one type for its entire segment or is marked mixed. Type energies live in a separate array, so an energy update changes only one array entry. When a replacement fully covers a uniform node, its score is the segment length times the absolute energy difference between the old and new types; the node then receives the new type. Mixed or partially covered nodes recurse into their children, pushing uniform tags when needed. On return, children with equal types are merged into a uniform parent.

Every position in a uniform node contributes the same amount, and its children partition the segment, so this computes exactly the score of individual replacements. Tags represent types, and replacement still changes a type when the two energies are equal.

An individual replacement can visit more than logarithmically many nodes, but the method has a deterministic amortized bound. Count only active mixed nodes, excluding descendants hidden by a uniform ancestor tag. Initially there are $O(n)$ such nodes. One operation can create new mixed nodes only at the $O(\log(n+2))$ nodes near its two boundaries. Every fully covered mixed node that is expanded becomes uniform afterward, so that traversal is charged to a disappearing mixed node. Total time is therefore $O(n+k+m\log(n+2))$ and space is $O(n+k)$ , where $n$ is the number of positions, $k$ the number of types and $m$ the number of operations.


## Implementation boundaries

Types start at one; zero denotes a mixed node. Pushing a uniform tag overwrites both children, and a parent becomes uniform only when its children have the same type. Energy changes update the lookup array without traversing the tree.

Skip construction when $n=0$ ; valid input then contains no interval replacements. When $k=0$ , no energy update occurs either. A score is at most $49999n$ , so products and totals use 64-bit integers. Equal-energy but distinct types must still be replaced because future energy updates can distinguish them.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
