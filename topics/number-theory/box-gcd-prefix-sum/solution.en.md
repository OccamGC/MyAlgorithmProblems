# Solution: A Certain Unscientific Prefix Sum of GCDs in Boxes

Codex (GPT-6): application of totient expansion, quotient grouping, summatory recurrences, and Lagrange interpolation, with derivation, proof, and implementation. These standard methods are not claimed as model inventions.

## Eliminate tuple enumeration

The totient identity is $g=\sum_{d\mid g}\varphi(d)$ . In a box of side $t$ , exactly $\lfloor t/d\rfloor^m$ tuples have every coordinate divisible by $d$ . Exchange the summations:

$$A=\sum_{d=1}^{n}\varphi(d)\sum_{t=d}^{n}\lfloor t/d\rfloor^m$$

Let $q=\lfloor n/d\rfloor$ and $S_m(x)=\sum_{j=1}^{x}j^m$ , with $S_m(0)=0$ . Each quotient from one through $q-1$ occurs $d$ times; the final quotient occurs $n-dq+1$ times. Hence

$$A=\sum_{d=1}^{n}\varphi(d)\left[dS_m(q-1)+(n-dq+1)q^m\right]$$

For a common quotient on $d\in[l,r]$ , the contribution is

$$
\left(\sum_{d=l}^{r}d\varphi(d)\right)\left[S_m(q-1)-q^{m+1}\right]
+(n+1)q^m\sum_{d=l}^{r}\varphi(d)
$$

The right endpoint is $r=\lfloor n/q\rfloor$ . There are $O(\sqrt n)$ groups. These steps only reorder and group finite sums, preserving the answer.

## Two totient prefixes

Define $\Phi(x)=\sum_{d\le x}\varphi(d)$ and $\Psi(x)=\sum_{d\le x}d\varphi(d)$ . Starting from

$$\sum_{d\mid u}\varphi(d)=u,\qquad \sum_{d\mid u}d\varphi(d)\frac ud=u^2$$

sum over $u\le x$ , then separate the term whose quotient parameter is one:

$$\Phi(x)=\frac{x(x+1)}2-\sum_{k=2}^{x}\Phi(\lfloor x/k\rfloor)$$

$$\Psi(x)=\frac{x(x+1)(2x+1)}6-\sum_{k=2}^{x}k\Psi(\lfloor x/k\rfloor)$$

Group equal quotients on the right. The coefficient for a group in the second recurrence is the sum of its integers. A linear sieve handles arguments through a threshold $B$ ; recursively evaluate and memoize larger arguments. Every recursive argument decreases, so induction from the precomputed prefixes proves both recurrences correct.

All large arguments have the form $\lfloor n/i\rfloor$ , a property preserved by nested integer division. Index their cache by $\lfloor n/x\rfloor$ , using $O(n/B)$ entries. Both a group endpoint and its preceding endpoint have this form. This indexing must not be used for arbitrary integer queries.

## Interpolate power sums

Precompute $1^m,\ldots,B^m$ and their prefixes. This handles power-sum queries through $B$ . The function $S_m(x)$ is a polynomial of degree at most $m+1$ : its finite difference is $S_m(x)-S_m(x-1)=x^m$ , reducing degree by one, and $S_m(0)=0$ fixes the constant.

Set $D=m+1$ and use consecutive interpolation points $0,1,\ldots,D$ . For larger $x$ ,

$$
S_m(x)=\sum_{i=0}^{D}S_m(i)
\frac{\prod_{0\le j\le D,\ j\ne i}(x-j)}{i!(-1)^{D-i}(D-i)!}
$$

Prefix and suffix products give each numerator, and inverse factorials give the denominator inverses, in $O(m)$ time per evaluation. Since $D<P$ , every denominator is nonzero. Also $n<P$ , so the queried integers lie in the same residue range. The implementation chooses $B=\min(n,2000000)$ . Whenever interpolation is needed, $B\ge D$ , and all interpolation values have been precomputed.

## Correctness and complexity

Totient expansion counts the gcd contribution of every tuple. Quotient groups accumulate exactly the requested upper bounds. The two recurrences and interpolation return the exact required residues. Summing the group contributions therefore gives the answer.

For threshold $B$ , the power table costs $O(B\log(m+1))$ . A large prefix argument $x$ takes $O(\sqrt x)$ groups; together they cost

$$O\left(\sum_{i\le n/B}\sqrt{n/i}\right)=O(n/\sqrt B)$$

At most $n/B$ distinct quotients exceed $B$ , so interpolation costs $O(nm/B)$ . Total time is $O(B\log(m+1)+n/\sqrt B+nm/B)$ and space is $O(B+n/B+m)$ , with $O(\log n)$ recursion depth. Use 64-bit intermediate products, reduce after multiplication, and normalize subtraction.

The [standard program](std.cpp) and [prefix component](totient-sums.hpp) compile locally within this directory. Sieving every totient and iterating over all divisors is useful for small checks, but unsuitable at $n=10^9$ . See the [test recipes](tests/README.md) and [measurements](../../../docs/benchmark-R36.json).
