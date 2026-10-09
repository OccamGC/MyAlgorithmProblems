# Grox's Sequence IV: residue-valued tensor transforms

**Codex (GPT-6): combine the setter's aligned-square decomposition with residue-valued tensor transforms to compute the three totals directly.** Tensor products and polynomial quotient rings are standard methods; this editorial explains their application here. The [program](alternative-residue.cpp) is a parallel option to the [phased FWT](solution.en.md) and [per-square FWT](solution-alternative.en.md); all three are retained.

## Keep only the three required coefficients

Use $L,B$ and the aligned-square decomposition from the main editorial. Define

$$\mathcal R=\mathbb F_P[z]/(z^3-1)$$

An element needs only three modular residues for its constant, linear and quadratic coefficients. Multiplication by $z^w$ cyclically shifts these positions by $w\bmod3$ ; no cube root of unity is needed.

For a bitwise operation $\circ$ , the required answers are the coefficients of

$$\sum_{i+j\le n}a_i b_j z^{i\circ j}$$

in this ring. There is no need to recover every convolution index before grouping it.

## A matrix for one bit

For a bit of weight $w=2^h$ , put $q=z^w$ . With the left index bit selecting the row and the right index bit selecting the column, the weight matrices are

$$K_h^{\mathrm{XOR}}=\begin{pmatrix}1&q\\q&1\end{pmatrix},\qquad K_h^{\mathrm{OR}}=\begin{pmatrix}1&q\\q&q\end{pmatrix},\qquad K_h^{\mathrm{AND}}=\begin{pmatrix}1&1\\1&q\end{pmatrix}$$

For example, OR contributes $1$ only when both bits are zero; the other three pairs contribute $q$ . Different bits are independent, so the complete matrix is the tensor product of these matrices.

In an accepted square of side $s=2^d$ starting at $(a,b)$ , define

$$H_d(u)=\sum_{v=0}^{s-1}b_{b+v}z^{u\circ v}$$

Start with $H_0(0)=b_b$ and apply the corresponding two-by-two matrix when adding a bit. Advancing every aligned interval in the global array together produces $H_d$ for all intervals of length $2^d$ at level $d$ . Components use only modular additions and cyclic shifts.

The square contributes

$$z^{a\circ b}\sum_{u=0}^{s-1}a_{a+u}H_d(u)$$

Add this immediately to the three answers. No cross-level result buffers or inverse transforms are required. Process the three operations consecutively using one working array.

## Correctness

Each one-bit matrix entry is exactly the exponent weight of that pair. The tensor product multiplies bit weights into $z^{u\circ v}$ , so advancement computes $H_d$ correctly. Aligned starting indices have zero low bits, separating high and low parts; multiplication by $z^{a\circ b}$ adds the high part. The accepted squares are disjoint and cover all legal pairs, so their sum is precisely the target ring element. The relation $z^3=1$ groups exponents by the required residues. Zero indices and singleton squares are handled at the initial level.

## Complexity and tradeoffs

Global advancement takes $O(L)$ time per level. The total length of accepted-square dot products at a level is also $O(L)$ . Total time is $O(L(1+B))$ ; inputs, the three-component working array and square lists occupy $O(L)$ space, with an $O(1+B)$ recursion stack.

This keeps the phased FWT's time bound while reducing its $O(L(1+B))$ space to $O(L)$ . Compared with per-square FWT, it removes one logarithmic time factor. Each working value has three components, with different modular-multiplication and grouping constants. Phased FWT remains the reference program, and the three options expose different time/space tradeoffs; actual performance is determined by same-input measurements.

## Same-input measurements

Both programs agree on all 10 formal inputs. Five alternating timing runs and input, source and binary hashes are in the [full record](../../../docs/benchmark-R14-supplements.json); see the [reference environment](../../../docs/评测环境与性能.md). Largest per-input median times are 0.499386 seconds for the reference and 0.584175 seconds for this option. Peak working sets are 125.83 and 41.74 MiB respectively, including process/runtime overhead.
This implementation is below the 1.0-second indicative limit on every measured formal input. This conclusion concerns the supplied implementation, these inputs and the reference environment. Finite testing does not replace the proof or guarantee that every implementation with the same bound passes.
