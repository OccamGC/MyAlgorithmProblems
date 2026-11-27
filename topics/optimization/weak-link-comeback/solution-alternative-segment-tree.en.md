# The Weak Link Strikes Back — Monotone stack and segment tree

[The C++17 implementation](alternative-segment-tree.cpp) by Codex (GPT-6) queries extrema of prefix sums on both sides of each assigned minimum. Their differences give the largest and smallest sums for intervals containing that position.

At a stack pop, the span begins after the preceding value at most as small and ends before the first strictly smaller value on the right. This assigns ties consistently. Take the maximum sum for nonnegative $a_i$ and minimum sum for negative $a_i$. Time is $O(n\log(n+1))$ and space is $O(n)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
