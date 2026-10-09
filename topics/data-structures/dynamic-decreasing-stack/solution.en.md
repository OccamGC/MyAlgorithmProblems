# Solution

Contributions: Codex (GPT-6) specified the stack rules and supplied the visibility segment tree, block alternative, proofs, implementations, and verification.

## Strict maxima from the right

An element remains in the final stack exactly when no later element is at least as large. Such a later element eventually pops it; without one, no later insertion can pop it. Thus the answer is the number of strict record maxima when scanning from right to left.

Store each segment-tree node's maximum $M$ and unrestricted record count $C$ . Let $F(u,t)$ count its right-to-left records greater than threshold $t$ . If $M_u\le t$ , return zero. A leaf otherwise contributes one.

For children $L,R$ , the right interval is scanned first, leaving threshold $M_R$ for the left interval. Therefore

$$C_u=C_R+F(L,M_R).$$

To evaluate $F(u,t)$ :

- If $M_R\le t$ , every right element is blocked. Recurse only into $F(L,t)$ .
- If $M_R>t$ , the right maximum survives and fixes the left threshold at $M_R$ . The left contribution is already stored as $C_u-C_R$ . Recurse only into $F(R,t)$ and add that difference.

Only one child is visited per level, so $F$ takes $O(\log n)$ time.

## Updates and interval queries

After a point update, recompute maxima and record counts toward the root. Each merge makes one $F$ call, giving $O(\log^2 n)$ time.

Process the canonical nodes of a query **from right to left**. Start the threshold at $-1$ . For a covered node, add $F(u,t)$ and replace the threshold by $\max(t,M_u)$ . This exactly represents the restriction imposed by the already scanned suffix. There are $O(\log n)$ covered nodes, so the query costs $O(\log^2 n)$ .

The record equivalence, merge identity, and threshold invariant prove that each answer equals the specified stack size. Equality must block a left element, consistent with strict record maxima.

## Complexity and alternatives

Let $n$ be the sequence length and $m$ the operation count. A node of height $h$ needs $O(h)$ construction work, and there are $O(n/2^h)$ such nodes. Summing gives $O(n)$ construction. Each update or query takes $O(\log^2 n)$ time; space is $O(n)$ .

[std.cpp](std.cpp) is the preferred implementation. The [block alternative](solution-alternative.en.md) updates in $O(B)$ and queries in $O(B+(n/B)\log B)$ . It has a simpler structure, uses linear space, and also passes the complete data.

## Measurements

Each formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.055566 seconds and peak memory is 6.90 MiB. Twice the median, rounded up to 0.5 seconds, gives a 0.5-second limit. The alternative's slowest median is 0.063319 seconds and peak memory is 5.62 MiB. See the [environment](../../../docs/评测环境与性能.md) and [individual measurements](../../../docs/benchmark-R34.json). Recalibrate in other environments.
