# Eight-neighbor induced forests retain the cubic bound

Status: **proof provided**. Date: 2026-10-12. Stable ID: `grid-forest-matching-eight-neighbor`.

[中文](eight-neighbor.zh.md) · [Research directory](../README.md) · [The different diagonal-only reduction](diagonal-only.en.md)

This result extends the original cubic proof to eight-neighbor induced forests. Direction words use four inverse pairs; complete-history charging and the finite second-axis lemma remain valid.

## Result and model

On a square board of side $n$, let $F$ be the road set, with $N\le n^2$ road vertices. Allowed moves are

$$
D_8=\{(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)\}.
$$

**Every eight-neighbor edge between road cells is retained, and this entire induced graph must be a forest.** A diagonal move requires its destination to be a road, without additional requirements on the two side cells. The query is an actual walk of $m$ moves; each prefix asks for the number of still-valid starts.

Extend the candidate-list algorithm's direction table to eight directions, still filtering only at the first visit to a relative displacement. For the total number $W$ of individual candidate checks,

$$
\boxed{W\le(5n-3)N},\qquad
\boxed{T=O(n^2+m+nN)\subseteq O(n^3+m)}.
$$

Space remains $O(n^2)$. When $m\ge n-1$, the same algorithm has worst-case time $\Theta(n^3+m)$. This is not a lower bound for every possible algorithm.

The upper bound follows by auditing the dependencies of the [published complete-history charging proof](../proofs/cubic-bound.en.md). Experiments supplement, rather than establish, this general proof. The original statement and four-direction reference program remain unchanged.

## 1. Why the diagonal-only coordinate reduction does not apply

Diagonal-only moves preserve the parity of $r+c$, splitting the problem into two disconnected parts. Orthogonal moves in the eight-neighbor model switch parity, so that decomposition no longer applies.

Nor is every orthogonal forest a valid eight-neighbor input. For example, the three cells $(0,0),(0,1),(1,1)$ form an orthogonal path, but the extra diagonal edge creates a triangle.

The extension instead uses **direction words of trees and the charging structure**. It does not require transforming the eight-neighbor board into an orthogonal board.

## 2. From two inverse direction pairs to four

Assign four inverse letter pairs to north/south, east/west, southeast/northwest, and northeast/southwest. Only adjacent inverse letters cancel. All reduced words form the rank-four free group $\mathbb F_4$, whose Cayley graph is still a tree.

Equal displacement must be distinguished from equal direction words. If $s,e,d$ denote south, east, and southeast, respectively, then

$$
\rho(d)=\rho(s)+\rho(e),\qquad d\ne se\quad(\mathbb F_4).
$$

Here $\rho:\mathbb F_4\to\mathbb Z^2$ is the coordinate homomorphism. A diagonal letter cannot be replaced by two orthogonal steps, and that additional relation must not be imposed on words.

Root an actual eight-neighbor road tree and associate each vertex with the direction word of its unique root path. A tree path has no immediate reversal, so its word is reduced. Each direction determines the next cell uniquely, so different tree paths cannot produce the same word. The actual road tree therefore embeds in the abstract direction-word tree.

The coordinate homomorphism is not injective on the entire abstract tree, but is injective on the vertex set of one actual road tree. The original proof uses coordinate injectivity only within this finite, actually present set.

## 3. Auditing the original proof's dependencies

### 3.1 Query prefixes, stars, and intersections

Let $P_j=\{q_0,\ldots,q_j\}$ be a prefix in first-discovery order, with $q_0=0$. Retain the longest prefix having a surviving candidate. The actual walk makes every prefix connected; a successful translation embeds it in the induced host forest, so its eight-neighbor induced graph is a tree. The longest successful prefix occupies at most $n$ query rows.

Group nonroot successful checks by host target and query row. Keep the earliest event of each group as its star, giving at most $nN$ stars. Every other event forms a marker $(a,e,f)$ with its star, satisfying

$$
h=f-e=(0,d),\quad d\ne0,\qquad
a+P_{t(f)}\subseteq F,\quad a+h+P_{t(e)}\subseteq F.
$$

The label $h$ is a difference of query points, **not necessarily an allowed single step**. Grouping by query row still gives horizontal labels even if the walk uses many diagonal steps.

Each marker carries a connected resource

$$
S_{a,e}=a+P_{t(e)}\subseteq G_h:=F\cap(F-h).
$$

All connectivity, intersections, and components use eight-neighbor adjacency. The two successful prefixes intersect at the marked target and hence lie in the same host tree. A nonempty intersection of connected subtrees is connected, regardless of whether edges are diagonal.

### 3.2 Uniform translation, axes, and unit capacity

A marked intersection component $K$ and its translate $K+h$ lie in the same host tree. Corresponding edges have equal directions, so translation is a uniform nonidentity left multiplication $g$, with $\rho(g)=h$.

If the source word is $\alpha$ and query vertex words are $w_x$, then

$$
k_e=w_f w_e^{-1}=\alpha^{-1}g\alpha.
$$

A nonidentity free-group left multiplication has a unique translation axis. Split its cyclically reduced word into primitive periods, with period length $p$, power $q$, and translation length $\ell=qp$. The coordinate displacement per period is

$$
\delta=h/q\ne0.
$$

A nonidentity left multiplication commuting with $g$ moves along the same axis by $sp$ edges, with coordinate displacement $s\delta$, for an integer $s\ne0$. Axis uniqueness, primitive periods, and this commuting relation do not require rank two; they hold unchanged in rank four.

Thus different sources of the same query class still occupy the same row. If two such markers have the same early resource image, their late targets also agree and their early query points are on the same row. The unique earliest star for that target and row forces the markers to coincide. The early images therefore still give an injective unit-capacity charge for each query class.

### 3.3 Common cut and reference class

For a fixed label, cut at the maximum early index. A marker attaining that index places the common prefix and its translate simultaneously in one host tree. Connected subtree intersections force the initially paid part into a single query class, costing at most $|G_h|$.

The remaining strict resources satisfy $S\cap(S+h)=\varnothing$. In each intersection component, choose a strict marker with the largest early index as reference. Its query class costs at most one further component budget. Every nonreference marker still satisfies

$$
t(e)<t(e_*)<t(f_*)<t(f).
$$

Consequently, every nonreference source matches the complete reference late prefix, including an actual reference-axis segment $A$ of length $\ell$. These steps use only tree connectivity, discovery order, and direction-preserving translation.

### 3.4 The finite second-axis lemma is unchanged

Consider two nonreference copies with the same early endpoint and source words $\alpha,\beta$. Their relative left multiplication $T=\beta\alpha^{-1}$ commutes with the host translation. Their axis separation is therefore $|s|p$, and their physical source difference is $b-a=s\delta$.

If $|s|p\le\ell$, the reference segment $A$ contains two points $v,u_*^s v$, where $u_*$ is the primitive root of the reference translation. Both sources match this actual segment, so the following host vertices both exist and have equal coordinates:

$$
a+\rho(u_*^s v)=a+s\delta+\rho(v)=b+\rho(v).
$$

Coordinate injectivity within the same actual road tree gives

$$
\alpha u_*^s v=\beta v,
\qquad T=\alpha u_*^s\alpha^{-1}.
$$

The unique axis of $T$ must then be both the host axis and the image of the reference query axis, forcing the nonreference and reference query axes to coincide, a contradiction. Distinct query classes do have distinct axes: their translation lengths agree and their coordinate displacement is the same nonzero $h$. On one axis they could only be the same translation or inverses; an inverse would have displacement $-h$.

Thus

$$
|\Delta_{\mathrm{axis}}(a,b)|>\ell.
$$

The proof compares only points in actual finite segments. Extra direction words with identical coordinate displacements do not cause injectivity to be used incorrectly on a virtual axis.

### 3.5 Bin capacity and the four budgets

A strict resource is disjoint from its label translate, so tree convexity bounds its axis-projection span by $\ell-1$. Group resources by the length-$\ell$ interval containing their leftmost projection. Early endpoints are distinct within a bin; increasing early-index order permits assigning an unused vertex from each complete-prefix resource. A fixed resource vertex participates in at most two bins.

The per-label budgets are therefore unchanged:

| Part | Budget |
| --- | --- |
| Markers paid at the common cut | $\lvert G_h\rvert$ |
| Component-local reference classes | $\lvert G_h\rvert$ |
| Nonreference strict markers | $2\lvert G_h\rvert$ |

Hence

$$
\widetilde M_h\le4|G_h|.
$$

The coefficient four is $1+1+2$, not the number of orthogonal directions. Increasing the direction count to eight does not increase this budget to eight.

## 4. Total work remains cubic

Each start fails at most once, so there are at most $N$ failed checks. If row $r$ contains $k_r$ roads, then

$$
\sum_{h=(0,d),\ d\ne0}|G_h|
=\sum_r k_r(k_r-1)
\le(n-1)N.
$$

This identity counts ordered pairs of road cells on the same row, without requiring them to be adjacent.

Therefore

$$
W\le nN+N+4\sum_h|G_h|
\le(n+1)N+4(n-1)N
=(5n-3)N.
$$

Adding board input, move processing, and output gives $O(n^2+m+nN)$. The original treatment of empty roads, immediate candidate exhaustion, and repeated displacements continues to apply.

## 5. The matching lower bound remains valid

Fill every cell of rows $0,2,4,\ldots$ with roads, leaving odd rows empty. Each road row is a horizontal path. Distinct road rows differ by at least two, so even eight-neighbor adjacency adds no edges between them. This is a valid induced forest.

Move right for $n-1$ steps. Immediately before filtering at step $j$, there are $\lceil n/2\rceil(n-j+1)$ candidates. Thus

$$
W=\left\lceil\frac n2\right\rceil
\sum_{j=1}^{n-1}(n-j+1)
=\left\lceil\frac n2\right\rceil\frac{(n-1)(n+2)}2
=\Theta(n^3).
$$

Subsequent moves may traverse visited edges back and forth, extending the walk to any $m\ge n-1$. Outputs require another $\Omega(m)$ time, so the candidate-list algorithm has worst-case time $\Theta(n^3+m)$.

## 6. Finite verification, coverage, and reproduction

Script: [verify_eight_neighbor.py](../verify_eight_neighbor.py). Report: [eight-neighbor-results.json](../eight-neighbor-results.json), with final status `passed`.

The audit covers:

- Every road subset on boards of sides $1,2,3$: respectively $2,11,194$ eight-neighbor induced forests, totaling $207$.
- All $8^4$ four-step walks for each forest, totaling $847,872$ cases. Bitset filtering agrees with an independent simulation that moves surviving absolute positions at every step; all check counts satisfy the bound.
- $881$ complete-history charging certificates, including every-root traversals of those small boards, fixed-seed random forests and walks, horizontal stripes, and mixed-eight-direction versions of opposite early arms, curved power-one axes, and nested combs.
- Across these certificates, $304,032$ candidate checks, $423$ nonreference markers, and $163$ adjacent pairs of same-early-endpoint copies, including nonempty curved power-one and repeated-early-endpoint cases.
- Mixed-direction fixtures with up to $5,305$ roads. Each original orthogonal edge is replaced at scale six by a bent eight-neighbor path, with branches leaving coarse vertices in distinct diagonal directions. Every resulting induced edge is then checked; unchecked orthogonal fixtures are not assumed valid under eight-neighbor adjacency.
- A three-cell right-angle path as a negative control: the orthogonal forest check accepts it, while the eight-neighbor check rejects its triangle.

The complete-charge checks reuse the published certificate core in an isolated module, replacing the direction, forest, query-tree, and answer dependencies. This is not a completely independent implementation of the charging certificate algorithm. Independent answer comparison and per-marker charging checks provide different layers of verification.

The largest observed nonreference vertex usage was one; the largest total per-label usage was two. These satisfy the proved capacity-two and capacity-four bounds, but **do not establish smaller general constants**.

During experiment preparation, an old fixture with shortened layer spacing was rejected by the original orthogonal forest check and replaced with parameters from the original verifier. A coverage assertion requiring nonreference usage to reach two was also not met; it was replaced by a check that the observed maximum lies between one and two, with the actual statistics retained above. Neither issue was an upper-bound counterexample.

Run from the repository root:

```text
python topics/simulation/grid-forest-matching/research/verify_eight_neighbor.py --output tmp/grid-forest-matching/eight-neighbor-results.json
```

The mathematical result depends on the proof transfer in Sections 2–4. Finite checks only help detect inconsistencies in eight-direction adjacency, candidate answers, and the charging implementation.

This note extends matching complexity only; it does not transfer orthogonal or diagonal-only tree-extension obstructions to the eight-neighbor model. Verification needs Python 3.10 or later, standard library only. The citation key is `OccamGC2026EightNeighborGridForest`; see the [citation guide](../../../../../CITATION.md). Proof status indicates a written proof in this repository, not external peer review or proof-assistant verification.

Further extension: [vertex and edge obstacles](edge-obstacles.en.md) allow selective edge blocking, require the actual traversable graph to be a forest, and explain the necessary algorithm and intersection changes.
