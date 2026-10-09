# A Certain Unscientific Arithmetic-Geometric Sum: Solution

## Method and contributions

The problem setter's solution differentiates a finite geometric series to obtain the index-weighted sum. Codex (GPT-6) completed the modular-ratio-one case and organized the standard C++17 implementation. Use [std.cpp](std.cpp); the [block-concatenation method](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) give a division-free approach of comparable complexity.

Let $p=10^9+7$ and $q=c^b\bmod p$ . The target is

$$c^d\sum_{i=l}^{r}(a+bi)q^i\pmod p$$

## Geometric and weighted sums

Define $S(n)=\sum_{i=1}^{n}q^i$ and $T(n)=\sum_{i=1}^{n}iq^i$ , both zero for an empty prefix. For $q\ne1$ , the finite geometric identity and its formal derivative give

$$S(n)=\frac{q^{n+1}-q}{q-1}$$

$$T(n)=\frac{nq^{n+2}-(n+1)q^{n+1}+q}{(q-1)^2}$$

Division here means multiplication by a modular inverse. Since $p$ is prime and $q-1\not\equiv0\pmod p$ , binary exponentiation computes the inverse as $(q-1)^{p-2}\bmod p$ . Square that inverse for the second formula.

Set $H(n)=aS(n)+bT(n)$ . The range answer is $c^d(H(r)-H(l-1))\bmod p$ . Normalize subtraction into $[0,p-1]$ .

For $q=1$ , every geometric factor is one, so compute

$$c^d\left(a(r-l+1)+b\frac{(l+r)(r-l+1)}{2}\right)\pmod p$$

The condition concerns $c^b\bmod p$ . For example, $c=4,b=500000003$ also gives ratio one. In this branch, two is invertible and its inverse is $(p+1)/2$ .

## Correctness

Differentiate the geometric identity term by term and multiply by $q$ . Its left side becomes $T(n)$ , and simplifying the right side yields the weighted formula. Thus $H(n)$ is exactly the required prefix sum for a nonunit ratio, and subtracting prefixes leaves precisely indices $l$ through $r$ . For ratio one, the formula follows directly from the number and sum of those indices. Multiplication by the common factor $c^d$ gives the requested answer in both cases.

## Complexity and implementation

Each query uses a constant number of binary exponentiations, taking $O(\log(b+1)+\log(d+1)+\log(r+1)+\log p)$ time and $O(1)$ auxiliary space. Queries are processed independently.

Use signed 64-bit integers. Raw products such as $bl$ are at most $10^{18}$ , and a sum step combines at most two products of about that size. The implementation reduces intermediate values in the stated order. Block concatenation removes inverses but maintains more quantities per level. Both methods support the complete input range.
