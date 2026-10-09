# Grox's Sequence I: A Polynomial Coefficient Recurrence

## Counting Identity

First work over the rationals with exponential generating functions. Arbitrary counts, even counts, and zero or positive odd counts correspond to $e^x$ , $\cosh x$ , and $1+\sinh x$ . Multiplication accounts for the binomial choices of labelled positions for different symbols. The answer is therefore

$$N![x^N]\ e^{ax}(\cosh x)^b(1+\sinh x)^c.$$

Let $d=2(b+c)$ and define

$$F(z)=(1+z^2)^b(z^2+2z-1)^c=\sum_{i=0}^{d}f_i z^i.$$

Writing the hyperbolic functions as exponentials gives the answer identity

$$2^{-(b+c)}\sum_{i=0}^{d}f_i(a-b-c+i)^N.$$

This is first an identity over the rationals. Clearing the power-of-two denominator gives an integer identity, so it can be reduced modulo $p$ for arbitrarily large $N$ . We never divide by $N!$ in the modular field; only the inverse of two is needed. The zero-occurrence option of the third group creates the coefficient $2z$ , which must be included.

## Large Exponents and Implementation Boundaries

Read $a\bmod p$ and $N\bmod(p-1)$ digit by digit, while separately tracking whether $N$ is actually zero. Fermat's theorem reduces exponents only for nonzero bases. A zero base raised to a positive exponent gives zero; an actual zero exponent gives one. In particular, a positive multiple of $p-1$ is not an empty sequence length.

Normalize residues into $[0,p-1]$ . Use 64-bit products and reduce immediately; $p^2<2^{63}$ ensures safety. Every small integer inverted below is at most $d<p$ .

## A Four-Term Recurrence

Polynomial convolution can be avoided. Differentiate $F$ and clear denominators to get $QF'=RF$ , where

$$Q=z^4+2z^3+2z-1,$$

$$R=(2b+2c)z^3+(4b+2c)z^2+(-2b+2c)z+2c.$$

Compare coefficients of $z^k$ , treating negative-index coefficients as zero:

$$\begin{aligned}(k+1)f_{k+1}={}&(2k-2c)f_k+(2b-2c)f_{k-1}\\&+(2k-4-4b-2c)f_{k-2}+(k-3-2b-2c)f_{k-3}.\end{aligned}$$

Start with $f_0=(-1)^c$ , precompute inverses from one through $d$ , and generate the coefficients in order while accumulating the answer. Only the last four coefficients need to be retained.

## Correctness

The generating-function identity proves that the weighted coefficient sum counts valid sequences. The constant term of $Q$ is negative one, and every $k+1$ is invertible, so the differential equation and the initial coefficient uniquely determine each subsequent coefficient. Exact coefficient comparison gives the stated recurrence; hence it produces the coefficients of $F$ . Handling zero bases and actual zero exponents separately then evaluates the identity for every input.

## Complexity and Algorithm Choice

Let $D$ be the total number of decimal input characters in $a,N$ . Time is $O(D+(d+1)\log p)$ and auxiliary space is $O(D+d)$ , including the linear inverse table. Modular exponentiation accounts for most of the computation.

The problem setter's solution uses the same exponential-generating-function identity, expands two polynomials and convolves them by a number-theoretic transform. Its complete derivation, proof and implementation are in the [NTT solution](solution-alternative.en.md) and [alternative.cpp](alternative.cpp). Its time is $O(D+b+c^2+L\log L+(d+1)\log p)$ and space is $O(D+L+b)$ , where $L$ is the smallest power of two strictly greater than $d$ . Both programs support the full constraints.

The preferred [std.cpp](std.cpp) removes the quadratic expansion and convolution through the four-term recurrence and uses less storage. This changes coefficient computation; the generating-function model remains the problem setter's contribution. Explicit expansion and NTT also extend naturally to different polynomial products and are retained as a complete alternative. See the [measurements](../../../docs/benchmark-R24.json).

## Attribution and Validation

Problem setter's solution: the exponential generating function, exponential-sum identity and NTT convolution. GPT-6: the differential-identity recurrence, proof, both standard C++17 implementations and boundary repairs. Small cases use a combinatorial DP that chooses positions for each symbol. Formal cases use explicit trinomial expansion and an independent NTT implementation, including zero type counts, empty sequences, modulus-related exponents and power-of-two polynomial degrees.
