# Solution: A Certain Unscientific Sum of Falling Factorials and Binomial Coefficients

Codex (GPT-6): application of a falling-factorial identity, fixed-modulus factorial checkpoints, and a constant-space Wilson-complement alternative. The identity, Fermat's little theorem, and Wilson's theorem are established mathematical methods.

## A counting identity

Choose a subset of $n$ objects, then choose $k$ designated objects from that subset in order. For a subset of size $i$ , there are $\binom ni i^{\underline{k}}$ choices.

Alternatively, first choose the ordered $k$ designated objects in $n^{\underline{k}}$ ways. Each of the other $n-k$ objects independently joins the subset or stays out. The two procedures describe the same objects, so for $k\le n$ ,

$$\sum_{i=1}^{n}\binom ni i^{\underline{k}}=n^{\underline{k}}2^{n-k}$$

For $k>n$ , every term is zero. Since $k\ge1$ , no additional $i=0$ term is needed.

## Fixed-modulus factorial checkpoints (primary)

Since $n<P$ , all required factorials are nonzero and

$$n^{\underline{k}}=\frac{n!}{(n-k)!}\pmod P$$

Choose block length $B=10^6$ and store $F_j=(jB)!\bmod P$ , including zero factorial. To compute $x!$ , start at $F_{\lfloor x/B\rfloor}$ and multiply the remaining factors in its block, requiring at most $B-1$ products. Fermat's little theorem gives $a^{-1}=a^{P-2}$ .

The [checkpoint table](factorial-table.hpp) is a computational resource for a fixed modulus, not a table of arbitrary input answers. The [generator](tests/generate-table.cpp) multiplies all factors sequentially, prints a constant at every block boundary, and checks $(P-1)!\equiv-1\pmod P$ . It completely regenerates the header.

Generating the checkpoints costs $O(P)$ offline time and $O(P/B)$ output space. An online input costs $O(B+\log P)$ time and $O(P/B)$ table space. The offline cost is real: this method relies on the fixed modulus and stated upper bound, and does not offer the same preprocessing-free speed for arbitrary new moduli.

## Correctness and implementation

The factorial recurrence gives each checkpoint. Multiplying the remaining block factors gives the exact factorial. The denominator is invertible, so Fermat inversion yields the falling factorial. Multiplication by $2^{n-k}$ then gives the answer by the counting identity. Use 64-bit modular products; intermediate values are below $P^2$ .

The [standard program](std.cpp) chooses checkpoints to reduce online work at the largest sizes. The [constant-space solution](solution-alternative.en.md) and [program](alternative.cpp) store no checkpoints. They use less space and are convenient for short products, but intermediate-length products are slower and exceed the full time limit. The programs agree on every formal input; see the [measurements](../../../docs/benchmark-R36.json) for timing scope.

Checks include literal evaluation of the original sum on small inputs, random short products, a [table verifier](tests/verify-table.cpp) that reverses multiplication within every million-factor interval, and a Wilson tail check. See the [generation and verification notes](tests/README.md).
