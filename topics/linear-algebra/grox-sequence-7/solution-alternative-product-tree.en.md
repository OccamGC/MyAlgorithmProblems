# Grox's Sequence VII: a product tree for the difference product

**Problem setter's solution: the Vandermonde identity and roots-of-unity transforms. Codex (GPT-6): apply product trees and multipoint evaluation to the ordered difference product.** The [program](alternative-product-tree.cpp) keeps the outer reduction from the [main editorial](solution.en.md), changing the algorithm at each evaluation point. Product trees, multipoint evaluation and polynomial inversion are standard methods.

## Preserve the direction of each difference

At a root of unity, let $v_i=A_i(\omega^t)$ . We need

$$D(v_1,\ldots,v_N)=\prod_{i<j}(v_j-v_i)$$

Split an interval into halves in original index order. Its difference product is the product of both internal difference products and all cross-half differences. If

$$F_L(y)=\prod_{i\in L}(y-v_i)$$

the cross-half part is

$$\prod_{j\in R}F_L(v_j)$$

Every left index precedes every right index, so each factor is right value minus left value. No square root or sign guess is needed. A singleton has empty product one.

## Product and remainder trees

Build the product tree for the interval. Each node stores its monic root polynomial $\prod_i(y-v_i)$ , the product of its children's polynomials.

For the cross-half part, pass $F_L$ down the right subtree, reducing modulo a node's polynomial before descending. Reduction preserves evaluation at every root of that node. Each leaf yields $F_L(v_j)$ . Multiply the leaf values for the cross-half part and combine with the recursively computed internal products.

Fast remainders use reversed polynomial division. If $A=BQ+R$ with $\deg R<\deg B$ , reverse after padding to the known degrees. The quotient's high coefficients satisfy

$$\operatorname{rev}Q=\operatorname{rev}A\cdot(\operatorname{rev}B)^{-1}\pmod{y^{\deg Q+1}}$$

The reversed monic divisor has constant term one, so Newton iteration gives its inverse. Reverse the quotient back and subtract its product with the divisor. Small divisions use direct elimination of leading terms to reduce constants.

## Correctness and repeated values

The product tree stores exact interval root polynomials, and the remainder tree preserves every leaf evaluation. Internal products and the cross product allocate each index pair exactly once, proving that recursion gives the signed Vandermonde product. The main editorial proves the outer NTT reduction and inverse transform.

Values $v_i$ need not be distinct. Repetitions make an internal product or cross evaluation zero, correctly yielding a zero determinant. Only monic polynomials or series with nonzero constant terms are inverted, never point differences, so repetitions do not cause invalid division. For $N=1$ , return empty product one.

## Complexity and tradeoffs

A cross-half multipoint evaluation of size $s$ costs $O(s(1+\log s)^2)$ time. Summing over recursive levels gives $O(N(1+\log N)^3)$ time per root of unity. Across $N$ roots, including input transforms, total time is

$$O(N^2(1+\log N)^3)$$

Input storage is $O(N^2)$ ; the current product tree and remainder recursion occupy $O(N(1+\log N))$ . Total space is their sum.

Compared with the $O(N^3)$ pairwise method, this has a lower asymptotic growth order, but many small transforms, divisions and allocations have larger constants. Here $N\le512$ , so the asymptotic bound does not imply faster execution. Pairwise multiplication remains preferred. The tree supplies another algorithm, with its practical limit determined by same-input measurements; the statement's range is not changed to conceal this tradeoff.

## Same-input measurements

Both programs agree on all 10 formal inputs. Five alternating timing runs and input, source and binary hashes are in the [full record](../../../docs/benchmark-R14-supplements.json); see the [reference environment](../../../docs/评测环境与性能.md). Largest per-input median times are 0.277414 seconds for the reference and 0.843589 seconds for this option. Peak working sets are 7.31 and 7.62 MiB respectively, including process/runtime overhead.
This implementation is below the 1.0-second indicative limit on every measured formal input. This conclusion concerns the supplied implementation, these inputs and the reference environment. Finite testing does not replace the proof or guarantee that every implementation with the same bound passes.
