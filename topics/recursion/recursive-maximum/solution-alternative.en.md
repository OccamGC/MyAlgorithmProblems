# Recursion Practice: Balanced Interval Splitting

Codex (GPT-6): apply balanced divide and conquer to reduce recursive call depth. [alternative.cpp](alternative.cpp) is a parallel option to [prefix recursion](solution.en.md), satisfies the recursion requirement and passes all formal inputs.

For a nonempty interval $[l,r)$ , return its element if its length is one. Otherwise set $m=l+\lfloor(r-l)/2\rfloor$ , recursively evaluate $[l,m)$ and $[m,r)$ in sequence, and return the larger result.

The subintervals are disjoint and together cover the original interval. Assuming each recursive result is its subinterval's maximum, their maximum is the maximum of the whole interval. Each call reduces the interval while keeping it nonempty, eventually reaching a single element. Induction proves correctness.

The recursion tree has $n$ single-element leaves. Every internal node has two children, so there are $n-1$ internal nodes and $O(n)$ total work. An interval roughly halves along any call chain, giving $O(\log(n+1))$ depth and auxiliary stack space. The two calls execute sequentially; the whole recursion tree is never stored. The input array still uses $O(n)$ space, and total space is $O(n)$ .

This structure extends naturally to longer sequences, at the cost of an extra interval split compared with prefix recursion. Both implementations handle the current constraints.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
