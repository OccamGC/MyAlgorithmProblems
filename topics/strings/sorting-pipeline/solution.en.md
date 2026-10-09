# Sorting Pipeline: Scanning Maximal Segments

Problem setter's solution: identify numeric segments and collect letters by type. Codex (GPT-6): exact accumulation in integer hundredths, amortized constant-time character appending, boundary proofs and validation.

## Preferred solution

Scan from left to right. Convert each letter and append it to the appropriate result string. On a digit or decimal point, consume the entire maximal numeric segment. A segment containing a decimal point belongs to type B; otherwise it belongs to type A.

For a decimal with whole part $w$ and fractional part $f$ padded to two digits, store $100w+f$ hundredths. For example, ` .1` becomes $10$ and `7.` becomes $700$ . Use two 64-bit integers for the integer sum and the sum in hundredths. To print the latter, divide by $100$ and print the remainder with two digits.

Let $N=|S|$ . There are at most $N$ numeric segments, each less than $10^6$ . The integer sum is below $N\cdot10^6$ , and the sum in hundredths is below $N\cdot10^8\le10^{13}$ . Signed 64-bit integers suffice; no binary floating-point approximation or rounding is needed. Long runs of leading zeros do not increase intermediate values.

## Correctness

Letters separate every pair of numbers, so each maximal numeric segment corresponds to exactly one number. The scan never merges or splits numbers. Every number is added exactly once to the type determined by its decimal point; padding the fractional part preserves its value. Every letter is appended exactly once, and scanning order preserves the relative order within each result. Thus all four output lines are correct.

## Complexity and implementation

The scan takes $O(N)$ time and $O(N+1)$ space including the input and result strings. Use `push_back` to avoid repeatedly copying entire strings. Empty input and missing types still require four output lines. A missing whole or fractional part contributes zero.

See [std.cpp](std.cpp). The [streaming state scan](solution-alternative.en.md) is a parallel option based on the character-by-character method in the teaching notes. It reads directly from the input stream and avoids storing the input string. It takes $O(N)$ time and $O(L+1)$ space, where $L$ is the number of letters. The preferred implementation keeps segment boundaries explicit. Both programs support the full data.

The [test plan](tests/plan.json) covers empty input and output lines, long leading zeros, one-sided decimals, sums above the per-number bound, and maximum length. See the [measurements](../../../docs/评测环境与性能.md).
