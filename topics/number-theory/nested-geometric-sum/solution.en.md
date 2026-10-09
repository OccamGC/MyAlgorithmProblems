# A Certain Unscientific Repeated Geometric Sum: Iterate over the Smaller Dimension

## Idea

Let $p=2147483647$ and let $S$ denote prefix summation. We choose the smaller of the position count $n$ and the number of summations $m$ .

### Fewer positions: a binomial convolution kernel

After $m$ prefix sums, the coefficient of the initial value at position $x$ in the value at position $n$ is

$$\binom{n-x+m-1}{m-1}.$$

Starting with coefficient one for one summation, Pascal's identity proves this by induction. Equivalently, distribute $n-x$ increments among $m$ stages. Thus

$$F_m(n)=\sum_{t=0}^{n-1}\binom{m+t-1}{t}F_0(n-t).$$

Start with $w_0=1$ and update $w_{t+1}=w_t(m+t)/(t+1)$ . For $a\ne1$ ,

$$F_0(x)=\frac{a^{2x+1}-a^x}{a-1}.$$

Iterate downwards from $x=n$ , updating the powers with $a^{-1}$ and $a^{-2}$ . For $a=1$ , use $F_0(x)=x+1$ . This branch visits $n$ terms.

### Fewer summations: a recurrence in the number of rounds

Define $H_t(n,q)=S^t(q^x)(n)$ . A geometric sum gives

$$S(q^x)(n)=\frac{q}{q-1}(q^n-1).$$

Apply $S^{t-1}$ and use $S^{t-1}(1)(n)=\binom{n+t-2}{t-1}$ to obtain

$$H_0(n,q)=q^n,\qquad H_t(n,q)=\frac{q}{q-1}\left(H_{t-1}(n,q)-\binom{n+t-2}{t-1}\right).$$

Maintain this recurrence for both $q=a$ and $q=a^2$ , then combine them:

$$F_m(n)=\frac{aH_m(n,a^2)-H_m(n,a)}{a-1}.$$

Within the input range, $a\ne1$ implies $a^2\not\equiv1\pmod p$ : the only two roots are one and $p-1$ , and the latter exceeds the input bound. All denominators are invertible. For $a=1$ , use

$$F_m(n)=\binom{n+m}{m+1}+\binom{n+m-1}{m}.$$

This is the sum of the repeated prefix sums of $x$ and of the constant one. Compute its binomial coefficients by successive multiplication.

## Correctness

The kernel branch counts the exact multiplicity of every initial entry. The round recurrence follows from linearity of prefix summation and the geometric-sum identity at every step. The unit-base formula covers the remaining case. Choosing the kernel for $n\le m$ and the round recurrence otherwise therefore returns the required value for every input.

## Implementation and Complexity

Work in the modular field. Precompute the needed small inverses using $\operatorname{inv}(i)=-(p\mathbin{//}i)\operatorname{inv}(p\bmod i)\bmod p$ . Here $n+m<p$ , and the table extends only to $\min(n,m)+1$ , so no denominator is zero modulo $p$ . Use signed 64-bit products and reduce after each multiplication: every product of two residues is below $p^2<2^{63}$ .

Time is $O(\min(n,m)+\log p)$ and auxiliary space is $O(\min(n,m))$ . Both summation directions are implemented in [std.cpp](std.cpp); short positions with many rounds use the kernel branch.

## Attribution and Validation

Geometric sums, binomial convolution kernels and finite-difference identities are classical methods. GPT-6 supplied their combined application, derivation, implementation and independent checks; the available material contains no working problem setter's solution. Small cases use direct repeated prefix sums. Formal cases use a partial-fraction expansion or independently computed weights, including unit bases and the branch boundary. See the [measurements](../../../docs/benchmark-R24.json).
