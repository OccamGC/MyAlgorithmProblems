# Suffix Arrays, Adjacent LCPs, and Expectation

Problem setter's solution: count distinct and unique substrings using a suffix array and LCPs. Codex (GPT-6): integer doubling sort, expectation derivation, 64-bit queries, noninvertible-denominator handling, and verification. The primary program is [std.cpp](std.cpp); a complete [suffix automaton solution](solution-alternative.en.md) is available as [alternative.cpp](alternative.cpp).

## From Counts to Expectation

Let $D$ be the number of distinct nonempty substrings and $U$ the number occurring exactly once. The whole string occurs once, so $U\ge1$ . Each trial succeeds with probability $p=U/D$ .

The number of trials until the next success is geometric with expectation $1/p$ . The wait for $N$ successes is the sum of $N$ such waits. Linearity of expectation gives $ND/U$ . The final successful trial is included; do not subtract one. For $N=0$ , the answer is zero.

## Two Suffix-Array Formulas

Sort all suffixes lexicographically. Let $L_i$ be the length of suffix $i$ in this order, and let $h_i$ be its longest common prefix with its predecessor. Set $h_0=h_n=0$ .

$$D=\sum_{i=0}^{n-1}(L_i-h_i),\qquad U=\sum_{i=0}^{n-1}\bigl(L_i-\max(h_i,h_{i+1})\bigr).$$

Suffixes sharing a prefix form a contiguous interval. Thus the prefixes of suffix $i$ already represented by earlier suffixes are exactly those of length at most $h_i$ , proving the formula for $D$ .

To test occurrence at any other position, only the two neighboring suffixes matter. If a farther suffix shares a prefix, the intervening adjacent suffix also shares it. Hence the longest repeated prefix has length $\max(h_i,h_{i+1})$ . Longer prefixes occur once and cannot be counted at another suffix, proving the formula for $U$ . Overlapping occurrences still have different suffix starts and are handled normally.

Build the suffix array by integer rank doubling and two stable counting sorts per round. A linear LCP scan computes neighboring common prefixes. Integer ranks provide exact comparisons without floating-point ranking.

## Modular Fractions

If $P\nmid U$ , compute $(N\bmod P)(D\bmod P)U^{-1}\bmod P$ .

If $P\mid U$ , the bound $1\le U\le n(n+1)/2<P^2$ means the denominator contains exactly one factor $P$ . If $P\mid N$ , divide both $N$ and $U$ by $P$ . Otherwise, if $P\mid D$ , divide both $D$ and $U$ by $P$ . Otherwise the reduced denominator still contains $P$ , so print $-1$ . After cancellation the denominator is invertible. Canceling factors other than $P$ does not change the residue, so the potentially overflowing product $ND$ is never formed.

This case is reachable: $S=a^{11879}b^2c^{84166}$ has $U=1000000007$ and $D=1000096051$ . For $N=1$ , output $-1$ ; for $N=P$ , output 96044; for $N=0$ , output zero.

## Complexity and Comparison

Time is $O(n\log n+Q+\log P)$ and space is $O(n)$ . Counts and queries use 64-bit integers; reduce both factors below $P$ before modular multiplication.

The suffix automaton provides a separate model based on end-position equivalence classes. Construction is linear for the fixed 94-character alphabet, but dense transitions use $O(94n)$ space. Both implementations pass the complete data. The suffix array follows the setter's counting method and uses less measured memory here, so it remains primary. Shared modular-fraction code is in [expectation.hpp](expectation.hpp).

## Validation and Performance

Every formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.033904 seconds and its peak memory is 7.22 MiB. Twice the median, rounded up to 0.5 seconds, gives a 0.5-second reference limit. The automaton's slowest median is 0.069435 seconds, with 80.46 MiB peak memory; both pass.

See the [test guide](tests/README.md), [environment](../../../docs/评测环境与性能.md), and [individual timings and hashes](../../../docs/benchmark-R35.json). Recalibrate on other environments.
