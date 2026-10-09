# A Certain Unscientific Repeated Prefix Sum: Solution

## Method and contributions

The problem setter's solution expands the polynomial in rising-binomial polynomials, so each prefix sum increments a basis index. Codex (GPT-6) reduced conversion to quadratic time and linear space through a recurrence between powers, and used batch inverses for adjacent binomial coefficients. Use [std.cpp](std.cpp). The setter's monomial-by-monomial triangular elimination has a [complete explanation](solution-alternative.en.md) and [alternative.cpp](alternative.cpp), also supporting the full range.

Work modulo the prime $p=2147483647$ . Define

$$B_0(x)=1,\qquad B_j(x)=\binom{x+j-1}{j}\quad(j\ge1)$$

## Replacing repeated summation by binomial evaluation

The adjacent-difference identity for binomial coefficients gives, for every $j\ge0$ ,

$$\sum_{x=1}^{n}B_j(x)=B_{j+1}(n)$$

For $j=0$ , this is simply the sum of $n$ ones. If the input polynomial is $P(x)=\sum_{j=0}^{k}w_jB_j(x)$ , applying $m$ prefix sums gives

$$\sum_{j=0}^{k}w_j\binom{n+m+j-1}{m+j}\pmod p$$

No recursion with $m$ levels or array of length $n$ is needed.

## Quadratic basis conversion

The basis satisfies

$$xB_j(x)=(j+1)B_{j+1}(x)-jB_j(x)$$

Keep the basis coefficients of the current monomial $x^i$ in `Current` , initially $x^0=B_0(x)$ . Add $a_i$ times those coefficients to $w$ . To obtain the next power, process $j=i+1,i,\ldots,1$ and set

$$Current_j\leftarrow j(Current_{j-1}-Current_j)\pmod p$$

Then set $Current_0=0$ . Descending order preserves the previous power's coefficients on the right, and the previously absent highest coefficient is zero. Each degree scans a linear number of entries, giving $O(k^2)$ work with two arrays of length $k+1$ .

## Binomial coefficients and batch inverses

First evaluate

$$C_0=\binom{n+m-1}{m}=\frac{n(n+1)\cdots(n+m-1)}{m!}$$

Multiply numerator and denominator separately, then invert the denominator with one binary exponentiation. This takes $O(m+\log p)$ time. Continue with

$$C_j=C_{j-1}\frac{n+m+j-1}{m+j}$$

For denominators $m+1,\ldots,m+k$ , compute prefix products $D_j$ . Invert $D_k$ once, then work backward. The current inverse product times $D_{j-1}$ is $(m+j)^{-1}$ ; multiplying it by $m+j$ obtains the preceding inverse product. All inverses therefore take $O(k+\log p)$ time.

The largest $n+m+k-1$ is $2010000299<p$ , so every positive factorial factor involved is below the modulus and invertible. Products between modular reductions fit signed 64-bit integers because $p^2<2^{63}$ .

## Correctness and complexity

The multiplication-by-$x$ identity proves inductively that `Current` represents each monomial. Weighted accumulation gives the complete input polynomial. Each prefix sum increments the basis index, so $m$ sums yield exactly the displayed binomial expression. Products, inverses, and adjacent ratios evaluate those binomial coefficients correctly, proving the output correct.

The reference takes $O(m+k^2+\log p)$ time and $O(k)$ auxiliary space. The triangular program takes $O(m+k^3+k\log p)$ time and $O(k^2)$ space, providing a direct alternative interpretation of the conversion. The reference has a clear advantage in both conversion time and space.
