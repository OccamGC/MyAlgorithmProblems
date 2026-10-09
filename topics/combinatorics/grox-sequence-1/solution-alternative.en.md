# Grox's Sequence I: Problem Setter's Solution with EGF and NTT

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

## Computing the Polynomial

Use binomial coefficients for $A(z)=(1+z^2)^b$ : its odd coefficients vanish and $[z^{2i}]A=\binom bi$ . Successive coefficients are obtained using $(b-i)/(i+1)$ in linear time.

Start with one and multiply by $z^2+2z-1$ exactly $c$ times to construct $B(z)$ . Update coefficients from high degree to low degree to preserve the values still needed. The total cost is $O(c^2)$ .

Let $L$ be the smallest power of two strictly greater than $d=2(b+c)$ . Pad both arrays to $L$ , transform them, multiply pointwise, then apply the inverse transform and divide by $L$ to obtain $F=AB$ . Use $L=1$ for $d=0$ . A degree-$d$ polynomial has $d+1$ coefficients; choosing $L=d$ would wrap the leading term into the constant coefficient.

The modulus is $479\times2^{21}+1$ , with primitive root three. The maximum transform length here is $2^{18}$ , so all needed roots exist. NTT changes convolution into pointwise multiplication, and inverse NTT recovers the coefficients in the field. Since the product degree is below $L$ , cyclic convolution equals ordinary polynomial multiplication.

## Correctness and Complexity

The binomial recurrence constructs $A$ exactly, repeated quadratic multiplication constructs $B$ exactly, and NTT obtains their complete product. Substitution into the proved exponential-sum identity gives the answer.

Let $D$ be the number of decimal input characters in $a,N$ . Time is $O(D+b+c^2+L\log L+(d+1)\log p)$ and space is $O(D+L+b)$ . [alternative.cpp](alternative.cpp) supports the full constraints. The preferred [four-term recurrence](solution.en.md) removes the quadratic expansion and convolution.

The problem setter's solution contributed the generating-function and NTT approach. GPT-6 supplied the complete derivation and standard C++17 implementation, including the zero-occurrence coefficient, transform length and zero-exponent boundaries. Both programs were checked by a combinatorial DP, independent trinomial expansion and formal stress cases. See the [measurements](../../../docs/benchmark-R24.json).
