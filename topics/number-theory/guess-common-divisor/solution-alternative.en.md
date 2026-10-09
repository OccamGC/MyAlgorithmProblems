# Guess the Common Divisor: Candidate Testing with Complete Coverage

Problem setter's solution: enumerate candidate divisors from input entries, then count divisible entries. Codex (GPT-6): a stopping rule covering $n-m+1$ positions and its deterministic proof; correctness does not rely on finite sampling.

Program: [alternative.cpp](alternative.cpp). This parallel option supports the full data and has an $O(n)$ space advantage over [divisor frequencies](solution.en.md).

## Algorithm

If $m=0$ , output $k$ . Otherwise inspect the first $h=n-m+1$ positions. Enumerate every divisor at most $k$ of each value by trial division. Test only candidates $d$ strictly larger than the current answer. Scan the input and count entries divisible by $d$ . Update the answer when the count reaches $m$ ; stop a failed test when the count plus the number of remaining entries is below $m$ . Stop the entire search if the answer reaches $k$ .

Different positions may generate the same candidate, and testing it again does not affect correctness. The program does not keep a candidate set, avoiding storage proportional to the divisor count.

## Correctness

Let $x$ be the optimal answer and choose any $m$ positions divisible by it. If these positions were disjoint from the inspected $h$ positions, there would be $m+h=n+1$ distinct positions, a contradiction. At least one inspected value is divisible by $x$ , so its divisor enumeration produces $x$ .

Candidate verification exactly matches the required count, so the maintained answer is always valid. The optimum is generated. If it is skipped, the current valid answer is already at least the optimum and therefore equals it. The counting bounds justify both early success and early failure. Once $k$ is reached, no larger valid value exists.

## Complexity

Let $U$ be the largest input value, and let $H$ be the sum of the numbers of divisors at most $k$ among the first $h$ entries, counted by position. Trial division takes $O(h\min(\sqrt U,k))$ time. Verification takes at most $O(nH)$ time, and storing the input uses $O(n)$ space. Repeated candidates and early termination affect observed runtime, but the worst-case $nH$ term must remain in the bound.

When $m$ is close to $n$ , $h$ is small; for $m=n$ , only one input value supplies candidates. This method avoids sampling error but may perform more divisibility checks. See the [measurements](../../../docs/评测环境与性能.md) for both methods.
