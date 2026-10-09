# Signal Network: A Circular Origin with XOR Interval Tags

Problem setter's solution: combine a circular origin with a segment tree. Codex (GPT-6): standard C++17 recursive interval traversal, explicit wrap splitting and bit-order handling. [alternative.cpp](alternative.cpp) supplements the [integer method](solution.en.md) and passes all formal inputs.

## Circular representation

Physical positions stay fixed. Store an origin $s$ representing the physical position of the current least significant bit. Logical bit $i$ maps to physical bit $(s+i)\bmod B$ , with $B=128$ . A right rotation by $k$ only changes $s\leftarrow(s+k)\bmod B$ .

Map a logical flip interval onto this physical ring using its start and length. If it crosses the end, split it into a suffix and prefix. Flip each piece through the segment tree.

## How tags represent bits

Each node stores one XOR flag recording the parity of whole-interval flips. Toggle it when an update covers the entire node interval; otherwise recurse into intersecting children. Tags need no downward propagation.

A physical bit equals the XOR of all flags on its root-to-leaf path. During a query, carry the XOR of ancestor tags, visit the requested leaves and place each bit at its output offset. A range update decomposes its interval into disjoint node ranges. Every covered leaf therefore gains exactly one toggled ancestor, while uncovered leaves remain unchanged.

To read the lowest $W=16$ logical bits, split at the circular boundary into at most two pieces. Shift the second result by the length of the first and combine them with bitwise OR. The origin mapping restores every bit to its correct logical offset. Consecutive queries with no intervening modification may reuse a cached result.

## Complexity and tradeoffs

Let $R,F,Q$ be the numbers of rotations, flips and queries. Initializing tags takes $O(B)$ ; rotation takes $O(1)$ ; a flip takes $O(\log B)$ . An uncached query visits two boundary paths and at most $W$ leaves, taking $O(\log B+W)$ . Total time is bounded by

$$O\bigl(B+R+F\log B+Q(\log B+W)\bigr)$$

Space is $O(B)$ and recursion depth is $O(\log B)$ . Cache hits take constant time. Since $B,W$ are fixed here, total time is also linear in the operation count, but interval traversal has a larger constant than two machine words. Its value is separating rotation from physical storage and demonstrating general circular interval maintenance. Direct word operations remain preferred for this problem.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
