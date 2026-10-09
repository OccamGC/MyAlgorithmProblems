# Minimum-Weighted Subarray Sums: Grouping by Right Endpoint

Contribution: Codex (GPT-6) applied classical monotone-stack DP to groups of left endpoints, with invariants, proof and implementation. This is a parallel solution with the same linear complexity as the [setter's owner-interval method](solution.en.md).

## Fix a right endpoint

Let $P_r$ be the sum of the first $r$ values. Group all subarrays ending at $r$ by their minimum. A group stores its minimum $m$ , number of left endpoints $c$ , and the sum of prefixes immediately before those endpoints:

$$S=\sum_{l\text{ in group}}P_{l-1}.$$

Its contribution is $m(cP_r-S)$ . Maintain

$$U=\sum_{\text{groups}}mc,\qquad V=\sum_{\text{groups}}mS.$$

Then all subarrays ending here contribute $P_rU-V$ .

## Update the monotone stack

In increasing order of left endpoints, subarray minima are nondecreasing. Merge consecutive equal minima into one group. Group minima are strictly increasing and can be stored in a stack.

Before reading $x=A_r$ , the groups describe right endpoint $r-1$ . Create a new group with $c=1,S=P_{r-1}$ for the singleton. Pop all final groups with minimum $m\ge x$ :

1. Remove their $mc,mS$ from $U,V$ .
2. Add their $c,S$ to the new group.

Every popped group now has minimum $x$ , while its left endpoints and prefixes $P_{l-1}$ remain unchanged. Groups not popped keep their minima. Push the merged group, update $U,V$ , set $P_r=P_{r-1}+x$ , and add $P_rU-V$ to the answer.

## Correctness

Assume the stack exactly partitions the subarrays ending at $r-1$ . Extending them to $r$ changes each minimum to $\min(m,x)$ . Monotonicity makes the groups that change to $x$ exactly one stack suffix, which is precisely what the algorithm merges. The singleton joins the new group of minimum $x$ . Thus the new stack exactly partitions all subarrays ending at $r$ and preserves their correct $c,S$ . The formula $m(cP_r-S)$ gives the exact group contribution, so each round computes all contributions for its right endpoint. Every subarray has exactly one right endpoint; summing rounds is correct.

## Arithmetic, complexity and use

Each group is pushed and popped once, giving $O(N)$ time and $O(N)$ stack space. An entry stores two thirty-two-bit integers and one sixteen-byte wide integer, totalling twenty-four bytes. Both $P_r$ and $U$ have magnitude at most $10^{16}$ and fit in sixty-four bits. Use the main solution's portable 128-bit type for $S,V$ , the product $P_rU$ and the answer. The product has magnitude at most $10^{32}$ , well below its range; the final answer obeys the main solution's sum-of-absolute-contributions bound.

Input can be streamed. The stack can still have $N$ entries, so this does not promise sublinear worst-case space. On the measured formal inputs it runs faster, with a peak working set close to the owner-interval method. These observations still require recalibration on another platform. Both programs pass the full range, independent subarray enumeration, maximum-size subtree aggregation and separate wide-arithmetic checks.

Program: [alternative.cpp](alternative.cpp). See the [complete measurements](../../../docs/benchmark-R26.json).
