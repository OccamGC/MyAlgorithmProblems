# Diagonal-only grid forests: parity decomposition and cubic bounds

[中文](diagonal-only.zh.md) · [Orthogonal cubic proof](../proofs/cubic-bound.en.md) · [Tree-extension obstructions](../examples/tree-extension.en.md) · [Citation](../../../../../CITATION.md) · [Research directory](../README.md)

Date: 2026-10-12. This note gives the complete reduction for four diagonal directions only. It is a corollary of the existing orthogonal results: each parity class is isomorphic to the orthogonal integer grid, with answers and individual candidate checks preserved. No new charging proof is needed.

Search terms: diagonal-only grid forest, parity decomposition, lattice isomorphism, translation matching, cubic bound; 对角邻接、奇偶拆分、坐标变换、平移匹配。

## 1. Model and results

The board is $\{0,\ldots,n-1\}^2$, the road set is $F$, its size is $N=|F|$, and the number of actual moves is $m$. Both adjacency and movement use only

$$
D=\{(1,1),(1,-1),(-1,1),(-1,-1)\}.
$$

All such edges between roads are retained, and the induced graph must be a forest. A diagonal edge does not depend on the two orthogonally adjacent side cells; geometric crossings inside cells do not create extra vertices. There are no orthogonal edges or additional rules forbidding corner cutting.

A starting point must execute the complete movement prefix and is permanently eliminated on failure. The candidate list is filtered only at newly discovered relative displacements. Let $W$ count individual candidate checks in these scans, excluding the initial reading of roads. Then

$$
\boxed{W\le(5n-3)N},\qquad
\boxed{T=O(n^2+m+nN)\subseteq O(n^3+m)}.
$$

Space is $O(n^2)$; short walks also satisfy $T=O(n^2+m+N\min(m,n))$. When $m\ge n-1$, this candidate-list algorithm has worst-case time $\Theta(n^3+m)$. This is not a cubic lower bound for every possible algorithm.

For extending forests to a single tree by adding vertices, different parity classes give an immediate connectivity obstruction. Even within one parity class, the nonextendable families from the orthogonal model remain valid.

## 2. Each color becomes an orthogonal grid

A diagonal move changes the coordinate sum by zero or plus or minus two, preserving $x+y\pmod 2$. Define

$$
F_p=\{(x,y)\in F:x+y\equiv p\pmod 2\},\qquad p\in\{0,1\}.
$$

There are no edges between the classes. For a fixed class, define

$$
\Phi_p(x,y)=(u,v)=\left(\frac{x+y-p}{2},\frac{x-y-p}{2}\right),
\qquad
\Phi_p^{-1}(u,v)=(u+v+p,u-v).
$$

This is a bijection between the entire parity class and the integer lattice. Edges and moves transform as follows:

| Original move | Transformed move |
| --- | --- |
| $(1,1)$ | $(1,0)$ |
| $(1,-1)$ | $(0,1)$ |
| $(-1,1)$ | $(0,-1)$ |
| $(-1,-1)$ | $(-1,0)$ |

The inverse also maps every orthogonal edge to a diagonal edge, so no edges are lost or added. Induced graphs, connected components, cycles, and the forest property are all preserved.

For example, the following five road vertices all have even parity. The right diagram shifts the transformed second coordinate by one; letters preserve vertex identity, and dots denote unselected positions.

```text
A . B        . A .
. C .   ->   B C D
D . E        . E .
```

The center connects to the four corners on the left and to its four orthogonal neighbors on the right. These are two coordinate representations of the same five-vertex tree.

The transformed board need not be a solid rectangle, but each coordinate occupies at most $n$ integer values: the original sum $x+y$ and difference $x-y$ each lie in an interval of length $2(n-1)$; fixing parity gives spacing two, so division by two leaves a span of at most $n-1$. Translate the image and fill missing cells with obstacles to obtain an orthogonal instance with side length at most $n$. Ignore an empty parity class.

## 3. Exact preservation of answers and candidate checks

Let $q=(a,b)$ be a relative displacement of the original query. Diagonal moves ensure $a+b\equiv0\pmod2$. Define

$$
L(q)=\left(\frac{a+b}{2},\frac{a-b}{2}\right).
$$

For every starting point $s\in F_p$,

$$
\Phi_p(s+q)=\Phi_p(s)+L(q).
$$

Thus every movement prefix is valid on the original roads exactly when its transformed prefix is valid on the corresponding image. Leaving the board and hitting an obstacle both correspond to non-road positions. Both subproblems use the same transformed move sequence.

The linear map $L$ is injective, so first visits to relative displacements are preserved as well. Partitioning the candidates before each scan by parity gives the two subinstance candidate lists. Permanent elimination, repeated displacements, and processing after all candidates disappear correspond exactly. If $A_t$ is the answer after step $t$, then

$$
A_t=A_{t,0}+A_{t,1},\qquad W=W_0+W_1,\qquad N=N_0+N_1.
$$

Apply the [existing theorem](../proofs/cubic-bound.en.md) to the two forests, each on a board no larger than the original side length:

$$
W\le(5n-3)N_0+(5n-3)N_1=(5n-3)N.
$$

The road counts add, so the total road budget is not doubled. The same bound applies to filtering directly in the original coordinates; an implementation need not create two new boards. Initial board reading takes quadratic time, while reading moves and producing outputs takes linear time. Combining this with the trivial bound of at most one full road scan per move gives the time, space, and short-walk results in Section 1. Empty roads or zero moves give zero candidate checks.

## 4. Transferring the cubic lower bound

In the reverse direction, start with a $k\times k$ orthogonal instance and define

$$
\Psi(u,v)=(u+v,\ u-v+k-1).
$$

All image points lie in $\{0,\ldots,2k-2\}^2$ and have the same parity. This global affine map transforms the induced orthogonal graph exactly into an induced diagonal graph. Each unit move becomes one diagonal move; answers and candidate checks are preserved.

Take an orthogonal instance consisting of full even-numbered rows, with all other rows empty, and move right $k-1$ times. The roads are separated horizontal paths, with

$$
N=\left\lceil\frac{k}{2}\right\rceil k,\qquad
W=\left\lceil\frac{k}{2}\right\rceil
\sum_{j=1}^{k-1}(k-j+1)
=\left\lceil\frac{k}{2}\right\rceil\frac{(k-1)(k+2)}2
=\Theta(k^3).
$$

The transformed move is $(1,-1)$ and the board side is $2k-1$, so work remains cubic in board side length. For any sufficiently large target side, take $k=\lfloor(n+1)/2\rfloor$ and pad with obstacles. The first $k-1\le n-1$ moves already produce cubic work; then move back and forth along visited edges to extend the sequence arbitrarily. Each output still takes constant time. Therefore

$$
m\ge n-1\quad\Longrightarrow\quad T_{\mathrm{worst}}=\Theta(n^3+m).
$$

## 5. Extending a forest to a tree

If original vertices occur in both parity classes, they cannot be connected by adding vertices, even on an arbitrarily enlarged board. The two isolated vertices $(0,0)$ and $(0,1)$ already form a counterexample. Every step of every path preserves parity, and adding vertices cannot change this invariant.

If all original vertices belong to one parity class, any single diagonal tree containing them must also lie in that class. The bijection in Section 2 is defined on the entire infinite lattice, so every induced diagonal tree extension would map back to an induced orthogonal tree extension. Consequently, [the nonextendable orthogonal forests](../examples/tree-extension.en.md) remain nonextendable after the mapping in Section 4, even with arbitrary board enlargement.

This transfers both the obstruction between two large paths and the nested family of linearly many components, each of linear size, in which any selected pair cannot be extended to a tree. Vertex counts and components are preserved, and board side length changes only by a constant factor, preserving both linear orders. Original vertex positions remain fixed and all induced edges are retained; the scope of the original obstruction is unchanged.

## 6. Verification scope, dependencies, and limitations

The general result follows from the isomorphisms above and the existing orthogonal proofs. It does not cover eight-neighbor movement that retains orthogonal edges alongside diagonals, or directly cover corner-cutting restrictions based on side-cell obstacles. The original problem statement, direction encoding, and reference program retain their orthogonal definitions; this note is a separate extension.

Run from the repository root using Python 3.10 or later, standard library only:

```text
python topics/simulation/grid-forest-matching/research/verify_diagonal_only.py --output tmp/grid-forest-matching/diagonal-only-results.json
```

The [verifier](../verify_diagonal_only.py) and [published report](../diagonal-only-results.json) record:

- Both parity classes for board sides one through twelve, totaling 24 board classes: bijection, induced adjacency, and coordinate ranges.
- All 530 road subsets on boards of sides one through three: agreement of forest tests before and after splitting; 498 subsets are diagonal induced forests.
- All 256 length-four move sequences for each of those forests, totaling 127,488 combinations: stepwise answers, candidate checks, and the upper bound; an independent direct simulation that does not skip repeated displacements also checks the answers. All shorter prefixes of those sequences are included.
- Four transferred stripe lower-bound instances, with target sides 7, 15, 31, and 63 and check counts 18, 140, 1,080, and 8,432, respectively.

These finite checks do not exhaust arbitrary boards or arbitrarily long walks, and do not reverify the original cubic charging proof. The citation key is `OccamGC2026DiagonalGridForest`; see the [citation guide](../../../../../CITATION.md). The status means a written proof is supplied in this repository, not external peer review or proof-assistant verification.
