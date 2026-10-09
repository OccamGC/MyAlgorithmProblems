# Recursion Practice: Merge a Prefix with Its Last Element

Problem setter's solution: recursively find a prefix maximum, then compare it with the last element. Codex (GPT-6): a clear interval interface and boundary proof, plus balanced recursion with reduced call depth.

## Preferred recursion

Use zero-based, half-open intervals $[l,r)$ . If $r-l=1$ , return the only element. Otherwise return

$$M(l,r)=\max\{M(l,r-1),a_{r-1}\}$$

Start with $M(0,n)$ . Pass the array by const reference, avoiding copies at each level.

A one-element interval is handled correctly. For a longer interval, recursion gives the maximum of its first $r-l-1$ elements; comparing this with the last element yields the interval maximum. Induction on interval length proves correctness. Returning actual elements rather than initializing to zero handles all-negative inputs.

## Cost and the recursion requirement

There are $n$ recursive calls and $n-1$ comparisons, taking $O(n)$ time. The call chain has at most $n$ levels and uses $O(n)$ stack space; total space including the input array is also $O(n)$ . The depth is suitable for $n\le100$ .

[std.cpp](std.cpp) uses the recursively returned value in its maximum calculation and satisfies the implementation requirement. Output alone cannot verify recursion, so this exercise also needs source inspection.

[Balanced interval recursion](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) reduce call depth to $O(\log(n+1))$ while retaining $O(n)$ time. The lower auxiliary stack use makes this a parallel option. Both still store an $O(n)$ input array, so the balanced implementation's total space is not logarithmic. Both pass all formal inputs.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
