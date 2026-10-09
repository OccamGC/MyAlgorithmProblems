# Distributing into Unlabeled Containers: Alternative Solution

## Pentagonal recurrence and removing large parts

Codex (GPT-6) applies the classical Euler pentagonal identity and truncated generating functions in [alternative.cpp](alternative.cpp). The [main solution](solution.en.md) explains conjugation and knapsack. Keep only coefficients of degree at most $n$ throughout.

Unrestricted integer partitions have generating function

$$P(x)=\prod_{j\ge1}\frac1{1-x^j}$$

Euler's pentagonal identity gives its inverse; see [NIST DLMF 27.14](https://dlmf.nist.gov/27.14#E4):

$$\prod_{j\ge1}(1-x^j)=1+\sum_{k\ge1}(-1)^k\left(x^{k(3k-1)/2}+x^{k(3k+1)/2}\right)$$

Their product is one. Comparing each positive-degree coefficient $s$ gives

$$p_s=\sum_{k\ge1}(-1)^{k-1}\left(p_{s-k(3k-1)/2}+p_{s-k(3k+1)/2}\right)$$

Here $p_0=1$ and negative-index entries are zero. There are only $O(\sqrt s)$ relevant pentagonal numbers for each $s$ , so all unrestricted counts take $O(n\sqrt n)$ time.

## Removing parts beyond the container bound

By conjugation, the target generating function is

$$P_m(x)=\prod_{j=1}^{m}\frac1{1-x^j}=P(x)\prod_{j=m+1}^{n}(1-x^j)\pmod{x^{n+1}}$$

Factors of degree above $n$ cannot affect the answers. To multiply by $1-x^j$ , process $s=n,n-1,\ldots,j$ and set $p_s\leftarrow p_s-p_{s-j}$ . Descending order is essential to use the coefficients from before this multiplication. Each pass cancels exactly the geometric-series factor allowing part size $j$ .

The pentagonal recurrence follows from an exact generating-function identity. Cancelling those factors leaves precisely the partitions with parts at most $m$ . Conjugation gives all answers to the container problem. Normalize every addition and subtraction modulo the specified modulus.

Time is $O(n\sqrt n+\max(n-m,0)^2)$ and space is $O(n)$ . For $m\ge n$ , no factors need cancellation and time is $O(n\sqrt n)$ . For small $m$ , cancellation is nearly quadratic and knapsack is more suitable. This is a complementary method with a different useful parameter range, tested over the complete bounds.
