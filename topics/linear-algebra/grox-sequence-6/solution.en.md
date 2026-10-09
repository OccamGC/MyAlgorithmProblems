# Editorial for Grox's Sequence VI

**Problem setter’s solution: precompute the coefficient matrix of polynomial particular solutions and represent the recurrence using a polynomial and an exponential term.** Codex (GPT-6) makes the $\beta=1$ finite-summation branch explicit, retains handling of negative values and zeroth powers, and composes coefficients at parameter replacement so that queries evaluate one polynomial rather than all basis functions.

## Polynomial particular solutions

All arithmetic is modulo $P=1000000007$ . Write

$$T(n)=\sum_{i=0}^k a_i n^i$$

For $\beta\ne1$ , seek a polynomial $g(n)$ of degree at most $k$ such that

$$g(n)-\beta g(n-1)=T(n)$$

If $g(n)=\sum_{j=0}^k c_j n^j$ , comparison of coefficients of $n^d$ gives

$$(1-\beta)c_d-\beta\sum_{j=d+1}^k\binom jd(-1)^{j-d}c_j=a_d$$

This is a triangular system solved from high degrees downward, with invertible diagonal $1-\beta$ . Precompute a coefficient vector for each basis function $T(n)=n^i$ and denote its polynomial by $g_i(n)$ .

For any parameters, the linear combination $g(n)=\sum_i a_i g_i(n)$ is a particular solution. Hence

$$f(n)=g(n)+(\alpha-g(0))\beta^n$$

The last term satisfies the homogeneous recurrence, and the zeroth term equals $\alpha$ , so the formula satisfies the complete initial value problem. Modular powers here use $\beta^0=1$ , including $\beta=0$ , to recover the initial value at index zero. For $n>0,\beta=0$ , the exponential term vanishes.

## When beta equals one

The diagonal $1-\beta$ is not invertible. Instead, seek a discrete antiderivative of degree at most $k+1$ , with $g(0)=0$ :

$$g(n)-g(n-1)=T(n)$$

Its coefficient system is

$$\sum_{j=d+1}^{k+1}(-1)^{j-d+1}\binom jd c_j=a_d\qquad(0\le d\le k)$$

Solve from $d=k$ downward. The coefficient of $c_{d+1}$ in each row is $d+1$ , which is smaller than $P$ and invertible. Fixing $c_0=0$ determines the polynomial uniquely. Precompute monomial basis functions in the same way. The answer is then $f(n)=\alpha+g(n)$ , consistent with the unified formula above.

## Query and replacement tradeoff

After precomputing basis functions, the setter’s method evaluates them separately at every query and weights them by the current $a_i$ . Coefficient comparison and elimination correctly determine those basis functions. Each query uses $O((k+1)^2)$ polynomial work, plus exponentiation. Replacement only stores the input parameters, costing $O(k+1)$ .

The reference program retains that precomputation and combines the coefficients of $g$ and the value $\alpha-g(0)$ at initial input or replacement. Replacement takes $O((k+1)^2)$ ; Horner evaluation makes each query $O(k+1+\log(n+1))$ . Several queries under one parameter set avoid repeated weighting. Frequent replacements incur quadratic composition work instead of linear parameter storage, so this is not a claim of faster execution for every operation mix.

## Correctness and complexity

The triangular systems in the two branches give basis functions satisfying their respective particular-solution equations. Linear combinations preserve those equations. Adding the homogeneous exponential term satisfies the initial value, so uniqueness of the recurrence gives the required sequence. A replacement recomposes current coefficients rather than retaining terms of the previous sequence.

Let $Q_0$ be the number of queries, $Q_1$ the number of replacements, and $N_{\max}$ the largest queried index. Including exponentiation for inverses, precomputation takes $O((k+1)^3+(k+1)^2\log P)$ time. Subsequent work takes $O((Q_1+1)(k+1)^2+Q_0(k+1+\log(N_{\max}+1)))$ time, with $O((k+1)^2)$ space. Normalize all negative input values into $[0,P-1]$ .

## Supplementary solution

Finite differences and a Newton binomial basis reduce the particular-solution equation to adjacent coefficients, with $O(k+1)$ space and $O(k+1+\log P)$ preprocessing. Update and query bounds match the reference, with different conversion and evaluation constants; it is retained as a lower-space parallel option.

[Complete editorial and measurements](solution-alternative-newton.en.md) · [Program](alternative-newton.cpp)
