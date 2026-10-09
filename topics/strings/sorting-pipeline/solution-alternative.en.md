# Sorting Pipeline: Streaming State Scan

The problem setter's teaching notes also contain a character-by-character state scan. Codex (GPT-6): direct streaming input, integer hundredths instead of floating point, and explicit state invariants.

Program: [alternative.cpp](alternative.cpp). See the [segment scan](solution.en.md) for the preferred solution and comparison. This parallel option supports the full data.

## States and transitions

Maintain the current number with its decimal point removed as an integer $v$ , a flag indicating whether the point has occurred, and the number $d$ of digits after the point. On a digit $c$ , set $v\gets10v+c$ and, if the flag is set, $d\gets d+1$ . A decimal point only sets the flag.

On a letter or end of input, flush the current number. Without a point, add $v$ to the integer sum. With a point, add $v10^{2-d}$ to the sum in hundredths. Reset the numeric state and append the converted letter to its result string. Flushing without a pending number only adds zero, so consecutive letters and the final newline cause no double counting.

## Correctness and complexity

The invariant is that the numeric state exactly represents the digits and decimal-point position read since the previous separating letter. Multiplying by ten and adding a digit preserves it. Flushing converts the number exactly into the appropriate unit. Each segment contributes once when it ends, and letters are collected in input order. Therefore the output is correct.

Let $N=|S|$ and let $L$ be the number of letters. Every character is processed once, giving $O(N)$ time. The two result strings occupy $O(L+1)$ space; all other state uses $O(1)$ space. The required output order places both sums first, so the letter strings must be retained until all input is processed. The numeric bounds are the same as in the preferred solution.
