# Jumping through Lexicographic Permutations — Alternative Solution

Codex (GPT-6) applies established Lehmer codes, mixed-radix addition, and Fenwick order statistics to this problem.

## Permutation ranks without large integers

Let $d_i$ count values smaller than $a_i$ to its right. The zero-based lexicographic rank is

$$rank=\sum_{i=1}^{n}d_i(n-i)!,\qquad 0\le d_i<n-i+1.$$

Scan right to left with a Fenwick tree counting previously seen values. At the same time, add the step count. Initialize carry $c=k$ ; the radix at this position is $r=n-i+1$ . Set

$$d_i'=(d_i+c)\bmod r,\qquad c=\lfloor(d_i+c)/r\rfloor.$$

Discard carry beyond the highest digit, implementing reduction modulo $n!$ . The rightmost radix is one: its digit is zero and the carry passes entirely leftward.

Decode left to right by selecting the $(d_i'+1)$-st smallest remaining value and deleting it. Binary descent inside the Fenwick tree selects a rank in $O(\log n)$ ; an external binary search would introduce another logarithm.

## Correctness and Tradeoffs

Each digit counts complete suffix blocks preceding its prefix, proving the rank formula. Mixed-radix carrying adds exactly $k$ modulo $n!$ . Order-statistic decoding inverts the same formula, yielding the correct cyclic successor.

Each case takes $O(n\log n)$ time and $O(n)$ space. No enormous rank or factorial is stored, and the structure is uniform. It is slower than the [suffix-block method](solution.en.md): the slowest median across five formal runs was about 0.741 seconds, exceeding the 0.5-second limit. Thus [alternative.cpp](alternative.cpp) is a backup; this measurement alone does not rule out every implementation with the same asymptotic complexity.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
