# Jumping through Lexicographic Permutations — Solution

Setter method: descending suffixes and factorial-sized lexicographic blocks. Codex (GPT-6) clarified cyclic semantics, supplied dynamic storage, proofs and validation, and added the Lehmer-digit alternative.

## Jump from the end of a permutation block

After fixing a prefix, $s$ remaining distinct elements have $s!$ arrangements. Choices for the next element form consecutive equal-sized blocks in increasing value order.

Scan position $i$ right to left, maintaining a descending suffix of length $s=n-i$ . The current permutation is the last one in its prefix block. Suppose $g$ suffix elements exceed $a_i$ ; they occupy the first $g$ positions of the descending suffix. The last permutation of the entire suffix $[i,n]$ is exactly $g\cdot s!$ steps ahead.

If enough steps remain, subtract that distance and move $a_i$ past those larger elements. The enlarged suffix is descending, so continue leftward. If $g=0$ , the invariant already holds without any change.

## Land inside a block

If fewer than $g\cdot s!$ steps remain, spend one step reaching the first arrangement of the next first-element block. The remaining distance skips

$$q=\left\lfloor\frac{k-1}{s!}\right\rfloor$$

additional blocks. Choose the $(q+1)$-st smallest suffix value greater than $a_i$ . Reverse the suffix into ascending order, swap in the chosen value, and insert the displaced smaller element leftward into its sorted position. The remaining distance becomes $(k-1)\bmod s!$ .

Now unrank within an ascending suffix: choose its $(\lfloor k/s!\rfloor+1)$-st smallest value for the next position, then use the remainder for subsequent positions. Swaps and insertion keep the unused suffix sorted. Only sufficiently small factorials can have nonzero digits.

Here $12!\le2^{31}-1<13!$ , so store factorials only through $12!$ . A suffix longer than 12 has blocks larger than any remaining distance, hence quotient zero. After the descending permutation, one step wraps to the ascending permutation. Reduce $k$ modulo $n!$ when $n\le12$ ; otherwise $k<n!$ and at most one wrap occurs.

## Correctness

The descending-suffix invariant locates the current permutation at a block end, making $g\cdot s!$ the exact distance to the enlarged suffix's end. Full jumps cannot skip the requested destination. When a full jump is impossible, crossing the boundary and dividing into blocks selects the correct next value; the remainder is exactly the desired suffix rank. Sorted-suffix unranking realizes that rank position by position. The final wrap also follows the specified cycle, proving the result.

## Complexity and Tradeoffs

Let $K$ be the allowed maximum step count and $D$ the smallest positive integer with $D!>K$ ; here $D=13$ . Scanning and at most one long suffix reversal and insertion cost $O(n)$ ; short-tail work costs $O(D^2)$ . Each case takes $O(n+D^2)$ time and $O(n+D)$ space. At most two calls preserve these bounds. Total input/output volume follows the aggregate length constraint.

Use [std.cpp](std.cpp) by default. The [Fenwick alternative](solution-alternative.en.md) expresses ranks more directly but takes $O(n\log n)$ and exceeds the measured 0.5-second limit on full stress cases. It remains a correct backup and cross-check.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
