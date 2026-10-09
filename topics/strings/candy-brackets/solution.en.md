# Candy Brackets: Solution

Problem setter's solution: local deque reductions for nonnegative weights. Codex (GPT-6) extends this structure to signed weights using the prefix and suffix summaries from maximum-subarray maintenance, and supplies the proof and C++17 implementation.

## Reductions and the nonnegative subtask

Compress each complete matching string into a matching block. Keep only unmatched brackets and matching blocks in a deque. Apply three rules: concatenate adjacent matching blocks; turn an empty bracket pair into a block; turn a bracket pair enclosing a block into a new block.

Append the initial elements from the right. After each insertion, repeatedly reduce at the updated end until no rule applies. The previous interior was irreducible, so any new rule must touch the updated end. The result remains at that end, and the interior does not need rescanning.

Ignoring blocks, the remaining brackets must be some closing brackets followed by some opening brackets. Otherwise consecutive opening and closing brackets in that subsequence have at most one block between them and can be reduced. No matching substring can cross an unmatched bracket, so every matching substring lies inside a block.

The problem setter's solution stores only each block's total weight. If all weights are nonnegative, the whole block is at least as good as any of its substrings, so keep the largest block total ever seen. Each reduction removes at least one element, giving $O(N+M+1)$ total time and space. This solves the nonnegative subtask.

With negative weights, the total alone loses information. Two adjacent candies worth $-10,100$ have total $90$ , but their best matching substring is the second candy, worth $100$ . More information about selectable parts of a block is required.

## Four values per matching block

For a matching block $A$ , maintain:

| Symbol | Meaning |
| --- | --- |
| $S_A$ | Total weight of the entire block |
| $P_A$ | Maximum weight of a matching prefix |
| $Q_A$ | Maximum weight of a matching suffix |
| $B_A$ | Maximum weight of a matching substring |

Prefixes, suffixes and substrings may be empty, so the last three values are at least zero. The total $S_A$ must retain its actual value; do not clamp negative totals to zero.

For a candy of weight $w$ , initialize $S=w$ and $P=Q=B=\max(0,w)$ . All four values of the empty block are zero. Store an unmatched bracket's actual weight separately; it is not yet a matching block eligible for the answer.

## Concatenating matching blocks

Let $C=AB$ :

$$
\begin{aligned}
S_C&=S_A+S_B\\
P_C&=\max(P_A,S_A+P_B)\\
Q_C&=\max(Q_B,S_B+Q_A)\\
B_C&=\max(B_A,B_B,Q_A+P_B)
\end{aligned}
$$

A prefix either ends inside $A$ , or takes all of $A$ followed by a matching prefix of $B$ . Suffixes are symmetric.

A matching substring crossing the boundary must use a matching suffix of $A$ and a matching prefix of $B$ . To see why, consider bracket height. Each complete matching block starts at zero, stays nonnegative and returns to zero. If a crossing substring started at positive height inside $A$ , reaching the block boundary would drop below its starting height, violating validity. It must therefore start at height zero in $A$ and end at height zero in $B$ . The best crossing value is $Q_A+P_B$ .

These prefixes and suffixes must match. Ordinary maximum-subarray summaries that ignore brackets are insufficient.

## Wrapping a matching block in brackets

Let $C=(A)$ , with opening and closing bracket weights $u,v$ :

$$
\begin{aligned}
S_C&=u+S_A+v\\
P_C=Q_C&=\max(0,S_C)\\
B_C&=\max(B_A,S_C)
\end{aligned}
$$

After the outer opening bracket and before the outer closing bracket, the height stays strictly positive. Thus the only nonempty matching prefix or suffix is the entire $C$ . Similarly, any matching substring containing either outer bracket must be all of $C$ ; every other candidate lies inside $A$ .

Even if $B_A$ is large, it cannot replace $S_A$ in the wrapped total: a contiguous substring cannot skip undesirable elements in its interior. An empty bracket pair is the case where $A$ is empty.

![Signed reductions showing the total and the best matching substring](assets/reductions.svg)

A dot denotes a matching block; numbers below dots or brackets are weights. The right side shows the resulting total $S$ and best matching substring value $B$ . The first and third rows show that they can differ. Maintain the remaining prefix and suffix values using the formulas above.

## Online maintenance and correctness

The reduction rules depend only on element types; negative weights do not affect their applicability. Each reduction updates the four values using the formulas above. Induction from individual candies and the empty block proves that every block's summary stays exact. Since every matching substring lies inside a reduced block, the current answer is the maximum block value $B$ , or zero.

Inserting at an end preserves every existing substring, so the answer never decreases. The reduction formulas also retain the best substrings of their input blocks. Maintain a global answer initially equal to zero. After each insertion and its reductions, update it with the endpoint block's $B$ , if that endpoint is a matching block. There is no need to scan the entire deque.

When processing the right end, swap the opening/closing roles when checking bracket patterns. However, concatenation formulas must still use physical left-to-right order. Reversing that order exchanges prefix and suffix information and can corrupt later updates at either end.

## Complexity, implementation and choice

Let $L=N+M$ . Each insertion adds one element and each reduction removes at least one, so there are $O(L)$ reductions, each using constant work. Total time and space are $O(L+1)$ , with constant amortized time per insertion.

The absolute weight of any contiguous segment is at most $2\times10^6\cdot4\times10^9=8\times10^{15}$ . Signed 64-bit integers suffice for all four values and intermediate sums. The implementation is iterative, so deep nesting does not overflow the call stack. Initial types use one byte each to control memory use.

[std.cpp](std.cpp) uses the four-value reductions and handles all data. For nonnegative weights, the problem setter's total-only method is also linear and stores fewer values, but it cannot directly handle negative weights. Rescanning after each update is a small-case oracle and may take quadratic total time. Offline activation of adjacent atoms within bracket levels provides an independent check, but needs all operations, the matching hierarchy and disjoint-set state, taking $O(L\alpha(L))$ time. It has no advantage over the online linear method and is used internally for validation.
