# Guess the Common Divisor: Divisor Frequencies

Problem setter's solution: enumerate divisors from selected input positions and test whether each candidate divides enough entries. Codex (GPT-6): deterministic divisor-frequency implementation, complete-coverage stopping rule, sampling limitations and validation. Trial division, sorting and counting are established basic methods.

## Preferred solution: enumerate and count

If $m=0$ , output $k$ . Assume $m>0$ below.

For each $a_i$ , enumerate $1\le d\le\min(\lfloor\sqrt{a_i}\rfloor,k)$ . When $d\mid a_i$ , append $d$ , and also append its paired divisor $a_i/d$ if $a_i/d\le k$ and $a_i/d\ne d$ . Count a square-root divisor only once. Sort the divisor array. The length of each equal-value run equals the number of input entries divisible by that value. Choose the largest value whose run has length at least $m$ .

Process each index separately; do not deduplicate repeated input values. Use `d <= a / d` as the loop condition to avoid overflow in a squared comparison.

## Correctness

Every valid candidate $x$ divides at least one input value. Paired divisor enumeration appends it exactly once for each index it divides. Its frequency is therefore $\#\{i:x\mid a_i\}$ . This is at least $m$ exactly when the required $m$ indices can be selected. Taking the largest such divisor yields the answer. For $m>0$ , divisor $1$ is always feasible. For $m=0$ , the empty selection imposes no restriction, so the answer is $k$ .

## Complexity

Let $U=\max_i a_i$ , and let $D$ be the total number of divisors at most $k$ , counted separately for each input index. For nonempty input, trial division takes $O(n\min(\sqrt U,k))$ time. Sorting and counting take $O(D\log(D+1))$ time and $O(D+1)$ space. Pairing divisors gives $D\le2n\lfloor\sqrt U\rfloor$ ; the actual $D$ depends on the divisor counts of the values. When $m=0$ , the program reads the input and outputs the answer in $O(n+1)$ time and $O(1)$ extra space.

For $U\le10^9$ , an individual value has at most $1344$ divisors, attained by $735134400$ , so $D\le1344000$ . The [exponent-pattern enumeration](../../../tools/check_r17_divisor_bound.py) verifies this bound. For a fixed collection of prime exponents, assigning larger exponents to smaller primes minimizes the value without changing its divisor count. It is therefore sufficient to enumerate nonincreasing exponents on consecutive primes from the smallest prime, with product at most the limit. The program exhausts these patterns and maximizes $\prod_j(e_j+1)$ . The formal stress data includes this witness.

## The setter's approach and deterministic coverage

The setter's approach enumerates divisors of selected positions and scans all input values for each candidate. Inspecting any $h=n-m+1$ distinct positions must intersect every set of $m$ positions, so it always includes a source for the optimal divisor. See the [candidate-testing solution](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) for the proof and implementation.

These are parallel options. Candidate testing uses $O(n)$ extra space and does not store many divisors. The preferred frequency method avoids scanning all inputs repeatedly for each candidate, removing the extra factor $n$ from candidate verification. It uses more space; the other method's space advantage remains relevant even when it runs more slowly on an input. Both deterministic programs pass the current full data.

## Limits of finite sampling

Inspecting a fixed number of randomly selected positions does not guarantee the answer. If the optimal divisor divides $q$ entries, a uniform sample of $t$ positions without replacement misses all of them with probability

$$\frac{\binom{n-q}{t}}{\binom nt}$$

This is zero when $t>n-q$ , but may be positive otherwise. For example, let $n=1000,m=200,k=2$ , with $800$ entries equal to $1$ and $200$ equal to $2$ . If all $50$ sampled entries are $1$ , the algorithm returns $1$ instead of $2$ . A fixed $50$-sample version therefore cannot be a reference program with guaranteed correctness.

The one-draw success probability is not always at least $1/5$ : the constraint is $m\ge\lfloor n/5\rfloor$ , and $n=9,m=1$ allows a ratio of only $1/9$ . Sampling with and without replacement also have different probability formulas. Deterministic coverage avoids these approximations.

See the [test plan](tests/plan.json) and [measurements](../../../docs/评测环境与性能.md). Validation covers empty selections, repeated values, perfect squares, a restrictive upper bound, and optimal-divisor witnesses concentrated near the end of the input.
