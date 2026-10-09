# Removing the Logarithm: Results, Failed Approaches, and Open Questions

This article collects proved results, refuted approaches, and open questions. Start with the [detailed general upper-bound proof](complexity.en.md), then use the [research directory](research/README.md) to find detailed proofs and constructions.

## 1. The exact current status

For an induced four-neighbour road forest with $N\le n^2$ road cells, the candidate-list algorithm has the proved bound

$$
T=O(n^2+m+nN\log(n+1)).
$$

When $m\ge n-1$, a legal family gives

$$
T=\Omega(n^3+m).
$$

**A general $O(n^3+m)$ upper bound remains unproved, and no asymptotic counterexample satisfying all requirements is known from this work.**

The stronger estimate $W=O(nN)$ would suffice, where $W$ counts actual candidate checks. A “capacity” assigns markers to permitted road vertices while bounding assignments per vertex. “Paying” markers means bounding them by a quantity with an established total budget. These are proof devices, not additional program steps.

Results below have three statuses:

- **Proved:** a general argument with explicit hypotheses.
- **Refuted:** a concrete counterexample or parameter family satisfying the relevant hypotheses.
- **Open:** a sufficient target, conjecture, or direction to test.

Finding no counterexample in finite searches is not a proof. Refuting an auxiliary estimate does not refute the algorithm's complexity.

## 2. Subclasses where the logarithm has been removed

Each row gives an independent sufficient condition; they need not hold together. The query tree is always the last complete displacement tree with a surviving candidate. The final failing new vertex is excluded.

| Condition | Proved scan bound or conclusion | Idea and proof |
| --- | --- | --- |
| The query tree or every road component has a uniformly bounded number of leaves | $W\le N+3(n-1)\sum_C|C|\min(L_T,\ell_C)$ | Each root-to-leaf chain contributes only linearly many successes to a fixed target. Interchanging query and host gives the smaller leaf count. [Chain proof](research/proofs/complexity-chains.en.md) |
| All road components are paths, or the effective query is a path growing from alternating ends | $W\le(6n-5)N$ | A direct consequence of the preceding row. The older direction-string argument remains in the [path proof](research/proofs/complexity-paths.en.md). |
| Every road component is within tree distance at most a fixed constant $r$ of some spine | $W\le(2r^2+2r+1)(6n-5)N$ | Project branch hits onto the spine and bound the short connections. [Second half of the chain proof](research/proofs/complexity-chains.en.md) |
| Every road component has $O(n)$ branching vertices, with arbitrary branch lengths | $W\le(6n-5)N+\sum_C|C|B_C$ | After the query first branches, a successful branching location must map to a host branch. [Branch proof](research/proofs/complexity-branches.en.md) |
| Complete a query diameter and its connection to the root first; then grow the remaining path attachments | $W\le(10n-7)N$ | The completed template constrains both sides of each attachment. The discovery-order hypothesis cannot yet be removed. [Branch proof](research/proofs/complexity-branches.en.md) |
| Every nonempty horizontal translation intersection of the query is connected | $W\le2nN$ | For a fixed label, markers of one query-potential type inject into the road intersection. Includes straight-spine, straight-tooth combs with any root and discovery order. [Label proof, Section 7](research/proofs/complexity-labels.en.md) |
| In each pair of adjacent rows, every nonzero difference between vertical-edge columns has multiplicity at most a fixed constant $b$ | $W\le[(b+2)n-b]N$ | Local vertical edges limit repeated early endpoints, followed by assignment to complete early prefixes. Allows dense roads and more than linearly many branches. [Label proof, Section 15](research/proofs/complexity-labels.en.md) |
| Relevant label-translation words have uniformly bounded power exponents | $W=O(nN)$ | Group by shortest axis period and resource projections. With no nontrivial powers, $W\le(4n-2)N$ is available. [Label proof, Sections 20 and 27](research/proofs/complexity-labels.en.md) |

Here $L_T$ is the rooted query leaf count, $\ell_C$ the unrooted leaf count of a road component, and $B_C$ its branching-vertex count; a singleton has one leaf. Both trees may have many leaves, so the first row does not settle the general case.

Another instructive restricted family mixes comb layers of different heights in one board. Their total cost is bounded using the total tooth height. The key is to charge how long a candidate can survive, instead of granting the entire road budget anew at every prefix. Mixing many heights therefore need not create a logarithmic lower bound. See the [mixed-height proof](research/examples/comb-scales.en.md).

## 3. Complete-prefix labels: the clearest remaining target

### 3.1 From successful checks to early and late query points

Each candidate fails at most once, so failed checks total at most the road count. For successful checks, fix a target road cell and a query row. Let $e$ be the earliest successful point in that group and $f$ a later one. The initial zero displacement is excluded when selecting the star.

Define

$$
h=f-e=(0,d)\ne0,\qquad a=v-f.
$$

The two successes imply

$$
a+P_{t(f)}\subseteq F,\qquad
a+h+P_{t(e)}\subseteq F.
$$

Define the label intersection

$$
G_h=F\cap(F-h).
$$

Since the early prefix is contained in the late prefix, the entire early resource lies in the intersection:

$$
S_{a,e}=a+P_{t(e)}\subseteq G_h.
$$

This is stronger than having the root-to-early-endpoint path. Several failed charging schemes discarded the other branches of this complete prefix.

Let $M_h$ count markers grouped only by row. Then

$$
W\le(n+1)N+\sum_hM_h,\qquad
\sum_{d\ne0}|G_{(0,d)}|
=\sum_r k_r(k_r-1)\le(n-1)N.
$$

Here $k_r$ is the road count in row $r$. A uniform per-label estimate $M_h\le C|G_h|$ would therefore remove the logarithm. This sufficient target remains open.

### 3.2 Why complete early resources help

**Proved: a marker family with distinct early endpoints has unit capacity.** In any subfamily, choose the marker with the latest early endpoint. Its complete prefix already contains every distinct query early endpoint in that subfamily. That one resource has at least as many vertices as there are selected markers, establishing Hall's condition.

Only query early endpoints must be distinct; sources may differ. One early endpoint may instead occur at many sources, so this argument cannot be used without checking that condition.

Other proved local capacities include unit capacity for collinear sources, capacity four when complete resources lie in a simple path, and constant capacities for short axis projections or few early-endpoint types. See the exact hypotheses in the [label proof, Sections 13, 17, 21, 24, and 27](research/proofs/complexity-labels.en.md).

### 3.3 A common cut and axis-based reductions

Markers from different query-intersection components have reversed time order: an earlier early endpoint has a later late endpoint. A common cut based on the latest early endpoint pays completed markers and those with intersecting prefix copies in one budget. The remaining relevant query subtrees are disjoint, and every late source still matches one common complete prefix.

Translation on a label domain also determines an axis in the direction-word tree. Write its translation word as a power of a shortest word, with shortest period length $p$ and exponent $q$. The label's axis length is

$$
\ell=qp.
$$

This is a tree-path edge count, not always the horizontal coordinate difference. Different “query axis classes” record different query-side axes. An “actual reference-axis image” additionally specifies where an axis lies in the host tree.

Existing capacity rules pay low powers, path domains, single-point axis intersections, few early endpoints, and short axis spans. Four long-early-axis classes can also be paid in each remaining component. Unpaid markers must therefore lie in high-power branching domains with many long-axis classes, and every remaining resource contains at least two periods of axis span.

### 3.4 Reference classes and per-source blocks: the final proved reduction

Within a selected conjugacy class of periods, use the class of the latest early endpoint as reference. All reference-class markers can be paid, including off-axis early endpoints.

Every nonreference source matches the reference late prefix and the complete prefix of the earliest nonreference late endpoint. Matching two different query axes forces distinct sources sharing one reference-axis image to be separated along it by more than a label length. Each source can therefore receive $\ell+1$ nonconflicting axis vertices.

**Within one reference-axis image, complete common-early-tree copies are also disjoint.** Resources from different images may overlap, so their sizes cannot simply be added.

For shortest period one, the road intersections of different reference images are disjoint, allowing the block cost to be combined across labels. To avoid historical round labels, denote the final unpaid quantity by

$$
E=E_{\rm curved}
+\sum_h\sum_{a\ {\rm nonref}}\bigl(r_{h,a}-(|h|+1)\bigr)_+.
$$

Here $E_{\rm curved}$ counts markers of shortest period greater than one after the reductions above. The quantity $r_{h,a}$ counts nonreference markers of shortest period one within that same reduced family. The reference class must be chosen anew inside that remainder. The proved estimate is

$$
\boxed{W\le(12n-10)N+E.}
$$

**The estimate $E=O(nN)$ is still unproved.** This is the explicit remaining gap. Counting axes or domains, or merely having a block for each source, does not bound it. See the [label proof, Sections 29–38](research/proofs/complexity-labels.en.md).

### 3.5 Another constraint: failure of the label-shifted source

Every nonreference source matches the reference late prefix, but its label-shifted source has failed by the reference early endpoint. Otherwise the reference early prefix would lie wholly in the original label domain, whose uniform translation would force the source into the reference class.

The parent edge of the first failed query vertex maps to an edge leaving that domain. The unshifted late source still matches both endpoints. This retains the full historical conditions, but multiple sources may reuse one exit edge. No constant-multiplicity payment through these edges is proved. See the [label proof, Section 40](research/proofs/complexity-labels.en.md).

## 4. Refuted approaches and what actually fails

Each row refutes an auxiliary claim. None of these constructions directly provides a supercubic algorithmic counterexample.

| Refuted strengthening | What the counterexample shows | What remains valid and where to read it |
| --- | --- | --- |
| Once the pattern is larger than linear, only linearly many candidates remain | Legal combs have both pattern and candidate counts much larger than the side length, while their product reaches the general bound's order | The single-prefix product bound remains valid. [Multiscale comb constructions](research/examples/comb-scales.en.md) |
| Apply the static parallelogram restriction to all historical successful displacements | Different successful events use different complete prefixes; their union can contain a nondegenerate parallelogram | The main proof must fix one complete pattern. [Local counterexamples](research/examples/local-obstructions.en.md) |
| Every success enlarges the bounding box or the union of copies | Both may remain unchanged through successive legal successes | New occupied space cannot pay every success individually. [Overlap proof](research/proofs/complexity-overlaps.en.md) |
| General query frontiers total only a constant times the roads | Same-root induced grid trees can have $\,\Theta(nN)\,$ frontiers | Those events have conflicting complete prefixes; actual direct matching has no corresponding counterexample. [Frontier construction](research/proofs/complexity-overlaps.en.md) |
| Historical third-longest-arm capacity pays all repeated charges | The capacity can stay nine while charges grow without bound; transferring candidates does not enlarge it | Failure cutoffs and short-early-arm windows remain valid. [Final section of the branch proof](research/proofs/complexity-branches.en.md) |
| Each marker can use only its own root-to-early path with constant capacity | Quadratically many genuine markers can crowd into a linear-size path union | Other branches of the complete early prefix must be available. [Label proof, Section 9](research/proofs/complexity-labels.en.md) |
| Association graphs are acyclic, or connected resource unions separate types from repeated early endpoints | Association graphs can have cycles; connected actual resource groups can have both several types and repeated early endpoints | Acyclic roads do not imply acyclic auxiliary graphs. [Label proof, Sections 5, 8, and 18](research/proofs/complexity-labels.en.md) |
| Add resource-union sizes across potential classes or axis images | Reuse causes unbounded overcount; taking the smaller horizontal/vertical budget also fails in general | Single-class injection and within-image disjointness remain valid. [Label proof, Sections 10, 22, and 39](research/proofs/complexity-labels.en.md) |
| Periodically translating the whole label domain preserves a forest | Different off-axis branches can align in distant copies and form a cycle | One strict-cut resource satisfies stronger hypotheses and still has a periodic forest extension. [Label proof, Sections 34–35](research/proofs/complexity-labels.en.md) |
| Per-source blocks pay everything, so the excess can be discarded | Deep hooks and two-dimensional combs retain genuine excess | That excess still has explicit unit assignments: the rule is insufficient, not the algorithm. [Label proof, Sections 38–39](research/proofs/complexity-labels.en.md) |

For example, the latest nested-comb family simultaneously satisfies

$$
N=\Theta(n^2),\qquad
\sum |S^{\max}|=\Theta(n^{5/2}),\qquad
W=\Theta(n^{5/2}),\qquad m=\Theta(n^{3/2}).
$$

It refutes a road-linear budget for coarse resource sizes, while actual scans stay below the target cubic bound. The [parameter proof](research/examples/nested-combs.zh.md) checks induced acyclicity, genuine earliest stars, unit assignment, and the real move count.

## 5. Possible directions to continue

These are open ideas, not established conclusions.

### A. Are connected resource components free of their label translates after removing the reference class?

Fix an actual common cut, one high-power conjugacy class, and a selected marker family. Remove the reference axis class containing the latest early endpoint. Let $U$ be a connected component of the union of remaining complete early resources, including unit grid edges between different resources. The conjecture is

$$
U\cap(U+h)=\varnothing.
$$

**Why it could help:** if one query early endpoint repeats in that component, the corresponding sources are separated along their own host axis by more than a label length, because they also match a different reference late axis. Their connecting tree path lies in the resource component and would contain two points differing by the label, contradicting the conjecture. Early endpoints would then be distinct, enabling unit capacity.

**What is missing:** each individual resource is disjoint from its own translate; this has not been proved for the connected union. Arbitrary connected unions do not have the property. Reference selection, the common late prefix, and actual earliest stars must all be used. Saved finite inputs have no counterexample, which is not a proof.

### B. Pay source excess through failure edges

Each nonreference source has a real exit edge from its label domain. One could try to show that many sources producing large excess through one edge force extra road space through their complete late prefixes, or create a forbidden second connection.

Only the existence of the edge is proved. Its multiplicity is not bounded. Summing all early-resource sizes per source has already been refuted by nested combs.

### C. Combine budgets across curved periods

Long axes with one common shortest period have a linear length budget. For shortest period one, distinct actual axis intersections are disjoint. There is no sufficient combined budget for different growing periods sharing road space.

The number of relevant domains and the total number of periodic repetitions have established bounds. The target, however, is actual marker count. A repetition budget is not a budget for the sum of all axis lengths or resource sizes.

### D. Prove that multiple scales cannot saturate together

The general logarithm comes from charging prefix scales separately. Historical nonparallel high-overlap translations obey geometric restrictions, and maximum repetition multipliers of same-direction runs have a linear total budget. Deleted candidates can therefore retain useful constraints.

The missing step is charging all actual successes to that budget. A budget using only one fixed reference direction already has a counterexample. See the [overlap proof](research/proofs/complexity-overlaps.en.md).

### E. Refine the remaining height-record charges

Some branching costs under arbitrary discovery orders have been paid. What remains can be reduced to genuine successes while a diameter or root height grows. Repeated records satisfy root-projection order, failure cutoffs, and short-arm windows.

The accumulated multiplicity of candidate transfers is uncontrolled. Records can themselves reach cubic cost and require arbitrarily many root-to-leaf chains. The refuted general linear-frontier bound and historical third-arm capacity cannot replace this missing argument.

## 6. How to evaluate the next proof or counterexample

This is a resumption checklist, not a new conjecture:

1. **Identify the count.** Is it actual candidate checking, or an auxiliary quantity that can substantially overcount?
2. **Keep the complete prefix.** A successful candidate must match every previously visited position.
3. **Check the earliest-star condition.** An arbitrary successful pair need not be a marker under the definition.
4. **Check the induced forest.** Adjacent coordinates automatically create edges, including edges not intended by the construction.
5. **Count real moves.** Returning along tree edges adds no filtering rounds but still contributes to running time.
6. **Separate proof from experiments.** Finite searches, mathematical families beyond the official side limit, and standard-program checks establish different facts.
7. **Check the quantifiers.** Within-image disjointness does not imply across-image disjointness; a fixed-period budget cannot be granted independently to all periods without a bound on reuse.

The [research directory](research/README.md) contains standalone construction proofs, representative inputs, their fingerprints, and a verification script.
