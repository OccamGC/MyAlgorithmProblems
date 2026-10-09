# Grox's Sequence VI: a Newton binomial basis

**Codex (GPT-6): convert the forcing polynomial with finite differences so the particular-solution equation becomes a recurrence between adjacent coefficients.** Finite differences and Newton expansion are standard methods; their application is implemented in the [program](alternative-newton.cpp). The [power-basis coefficient-matrix method](solution.en.md) remains the reference, with both presented as parallel options.

## A shifted basis

Put $T(n)=\sum_{i=0}^k a_i n^i$ . Evaluate it at $1,2,\ldots,k+1$ , then take successive adjacent differences to obtain

$$t_j=\Delta^jT(1),\qquad T(n)=\sum_{j=0}^k t_j\binom{n-1}{j}$$

Here $\Delta T(x)=T(x+1)-T(x)$ . Binomial polynomials satisfy $\Delta\binom{x}{j}=\binom{x}{j-1}$ , so successive differences extract exactly the Newton coefficients. These $k+1$ values uniquely determine a polynomial of degree at most $k$ .

Use a different shift for the particular solution:

$$g(n)=\sum_j c_j\binom nj$$

Pascal's identity gives

$$g(n)-\beta g(n-1)=\sum_j\big((1-\beta)c_j+c_{j+1}\big)\binom{n-1}{j}$$

The full triangular system becomes a relation between adjacent coefficients.

## The two beta cases

For $\beta\ne1$ , set $c_{k+1}=0$ and solve downward:

$$c_j=\frac{t_j-c_{j+1}}{1-\beta}\qquad(j=k,k-1,\ldots,0)$$

For $\beta=1$ , simply set $c_0=0$ and $c_{j+1}=t_j$ , giving a discrete antiderivative of degree at most $k+1$ . No separate basis function is stored for each monomial.

Both branches use

$$f(n)=g(n)+(\alpha-c_0)\beta^n$$

Starting with $\binom n0=1$ , evaluate a query in linear time using

$$\binom n{j+1}=\binom nj\frac{n-j}{j+1}$$

Denominators are at most $k+2<P$ , so their inverses exist. Once a coefficient becomes zero for $n<j$ , no division by that zero is performed. Use $\beta^0=1$ to preserve the initial value when $\beta=0,n=0$ .

## Correctness and complexity

Finite differences give the exact expansion of $T$ , and the adjacent-coefficient relation ensures the particular-solution equation. The exponential term solves the homogeneous recurrence and makes the value at zero equal to $\alpha$ . Uniqueness of the initial-value recurrence proves all terms. An update recomputes the complete set of Newton coefficients.

Use $Q_0,Q_1,N_{\max}$ from the main editorial. Preparing integer inverses and one modular inverse takes $O(k+1+\log P)$ time. Initial input or each replacement takes $O((k+1)^2)$ time, and a query takes $O(k+1+\log(n+1))$ time. Total time is

$$O(k+1+\log P+(Q_1+1)(k+1)^2+Q_0(k+1+\log(N_{\max}+1)))$$

Space is $O(k+1)$ . Compared with the power basis, this removes cubic basis preprocessing and the quadratic coefficient matrix. Updates and queries retain their asymptotic bounds, but binomial evaluation uses more modular multiplications per term. Actual performance depends on the operation mix; less preprocessing does not imply faster execution on every input.

## Same-input measurements

Both programs agree on all 10 formal inputs. Five alternating timing runs and input, source and binary hashes are in the [full record](../../../docs/benchmark-R14-supplements.json); see the [reference environment](../../../docs/评测环境与性能.md). Largest per-input median times are 0.045359 seconds for the reference and 0.081370 seconds for this option. Peak working sets are 5.84 and 5.33 MiB respectively, including process/runtime overhead.
This implementation is below the 0.5-second indicative limit on every measured formal input. This conclusion concerns the supplied implementation, these inputs and the reference environment. Finite testing does not replace the proof or guarantee that every implementation with the same bound passes.
