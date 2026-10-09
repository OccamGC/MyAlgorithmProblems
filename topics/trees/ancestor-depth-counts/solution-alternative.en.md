# Depth Counts across Ancestor Subtrees: Path Addition and Path Sums

[alternative.cpp](alternative.cpp) uses heavy-light decomposition and two Fenwick trees, supporting all constraints in $O(n)$ space. It is a parallel option to [centroid decomposition](solution.en.md) when lower memory use is desired.

## The effect of activating a node

For an activated set, let $V_u$ be the number of activated nodes in the subtree of $u$ . Activating $y$ adds one to every node on the root-to-$y$ path.

The sum along the root-to-$x$ path is

$$Q(x)=\sum_{u\in A(x)}V_u=\sum_{y\text{ activated}}|A(x)\cap A(y)|.$$

This is exactly the repeated count of activated nodes in the ancestor subtrees of $x$ . Process complete depth groups: query $L_x$ before activating the group and $U_x$ after activating the entire group. With subtree size $s_x$ , compute $T_x=T_{\operatorname{parent}(x)}+s_x$ and $T_0=0$ . Output $L_x,U_x-L_x,T_x-U_x$ .

## Heavy-light decomposition

At each nonleaf, designate a child of maximum subtree size as heavy; other child edges are light. Crossing a light edge at least halves the remaining subtree size, so any root path meets $O(\log n)$ heavy chains.

Assign consecutive positions from top to bottom within each heavy chain. A root path becomes a sequence of intervals: operate on the current chain head through $x$ , then move to the parent of the chain head and repeat. Only consecutive numbering within each chain is required; subtree intervals are unnecessary.

## Two Fenwick trees

For range addition and range sums, let $b_i=V_i-V_{i-1}$ . Store $b_i$ and $(i-1)b_i$ in two Fenwick trees. The prefix sum is

$$\sum_{i=1}^rV_i=r\sum_{i=1}^rb_i-\sum_{i=1}^r(i-1)b_i.$$

Adding one to $[l,r]$ adds one at $b_l$ and subtracts one at $b_{r+1}$ . The weighted tree receives $l-1$ and $-r$ at those positions. Subtract two prefixes for an interval sum. All weighted values and sums use 64-bit integers.

## Correctness and complexity

A root-path increment updates precisely the subtrees containing the newly activated node. Heavy-chain intervals partition that path, and the Fenwick formulas implement exact range additions and sums. Hence each query equals $Q(x)$ . Depth-group activation then yields the shallower and no-deeper weight sums; subtraction produces all three answers.

Tree traversal, subtree sizes and chain numbering use explicit arrays, supporting arbitrary parent labels and deep chains. A path has $O(\log n)$ segments, each requiring $O(\log n)$ Fenwick work. Total time is $O(n\log^2n)$ and space is $O(n)$ . The maximum measured working set is about $157.6$ MiB; see the [performance record](../../../docs/benchmark-R25.json). GPT-6 applies classical heavy-light decomposition and Fenwick trees, supplying the activation model, proof, bilingual explanation and implementation. The underlying data structures are established techniques.
