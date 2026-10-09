# Grox's Sequence V A: one decimal modular power

**Problem setter's solution: Stirling numbers and falling factorials. Codex (GPT-6): one decimal modular power followed by repeated doubling, and truncation of unnecessary Stirling columns.** The [program](alternative-decimal.cpp) uses the counting identity from the [main editorial](solution.en.md), while changing exponent handling. It needs no modulus factorization, Euler totient or modular inverse.

## Compute powers from the smallest exponent upward

For $k=0$ , the specified zero-power convention gives $2^n-1$ . Compute this power directly from decimal digits; for $n=0$ , the answer is zero.

For $k>0$ , put $m=\min(n,k)$ . The main editorial proves

$$S=\sum_{j=1}^{m}S(k,j)(n)_j2^{n-j}\pmod p$$

Use the rolling recurrence to obtain $S(k,1),\ldots,S(k,m)$ . Only the first $m$ columns are needed in every row, since each update depends on its own column and the preceding one. Compute falling factorials successively from $n\bmod p$ and store

$$W_j=S(k,j)(n)_j\bmod p$$

Saturated counting while reading decimal digits determines $m$ . Subtract this small integer from the decimal string to obtain the nonnegative integer $n-m$ . Borrowing may pass through many zero digits; an exponent residue cannot replace this actual subtraction.

Compute $B=2^{n-m}\bmod p$ . If the processed prefix represents $t$ and the next digit is $d$ , then

$$2^{10t+d}=(2^t)^{10}2^d$$

Scanning the digits with this identity handles arbitrarily long exponents without requiring a coprime base and modulus.

Finally scan from $j=m$ down to $1$ , add $W_jB$ and double $B$ . The exponents are $n-m,n-m+1,\ldots,n-1$ , all nonnegative.

## Correctness and boundaries

The finite Stirling sum holds over the integers; the rolling recurrence and falling-factorial products yield its correct weights. The decimal power maintains the residue for the actual exponent through the digit identity, and doubling generates the other powers exactly. Each term therefore matches the finite sum for any positive modulus. Return zero separately for $p=1$ and $n=0$ . Normalize negative falling-factorial factors before multiplication; even after a zero factor, no division is used.

## Complexity and tradeoffs

Let $D$ be the decimal digit count. The nonzero branch takes $O(km+D)$ time and $O(m+D)$ space. When $k=0$ or $n=0$ , time is only $O(D)$ . In the worst case $m=k$ , time is $O(k^2+D)$ .

The Euler-exponent method uses $O(\sqrt p)$ trial division and a modular power per term. This option removes both and the noncoprime exponent boundary cases while preserving the counting algorithm. It is a simpler full-range implementation, presented alongside the reference; same-input measurements establish actual time and memory differences.

## Same-input measurements

Both programs agree on all 10 formal inputs. Five alternating timing runs and input, source and binary hashes are in the [full record](../../../docs/benchmark-R14-supplements.json); see the [reference environment](../../../docs/评测环境与性能.md). Largest per-input median times are 0.036134 seconds for the reference and 0.035908 seconds for this option. Peak working sets are 5.30 and 5.32 MiB respectively, including process/runtime overhead.
This implementation is below the 0.5-second indicative limit on every measured formal input. This conclusion concerns the supplied implementation, these inputs and the reference environment. Finite testing does not replace the proof or guarantee that every implementation with the same bound passes.
