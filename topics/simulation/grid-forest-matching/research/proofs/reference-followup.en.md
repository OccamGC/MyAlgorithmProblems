# Ten follow-up rounds on reference-class deletion

**Current overall result:** the [general cubic proof](cubic-bound.en.md) is complete. The finite investigations, unsuccessful approaches, and local lemmas below retain their historical scope and statistics.

Date: 2026-10-12. This completes the ten research rounds following the [initial investigation](../examples/reference-components.en.md).

**Later update:** opposite early arms now refute direction A's general disjointness conjecture; a capacity-two replacement draft appears in the [new record](reference-capacity.en.md). Statements of open status and experimental totals below describe the end of these ten rounds. The three proved results remain valid.

**At the end of these ten rounds, the general cubic bound and direction A were unresolved.** Three rigorous conclusions emerged: failure edges cannot be charged a constant number of sources; column bands prove disjointness for nested combs in their original order; and general resource disjointness is equivalent to an axis-projection span bound. Experiments found no counterexample satisfying every hypothesis of A, but also exposed geometric configurations the search has not reached.

## 1. One failure edge can serve linearly many remaining sources

This supplements [Section 40 of the label proof](complexity-labels.en.md), which establishes a failure exit edge for every nonreference source without bounding its multiplicity.

**Proposition.** A family of valid induced trees has linearly many sources using the same failure exit edge even after paying four long-axis classes, choosing a new reference class, and assigning source blocks. Their unpaid excess on that edge also grows without bound.

### Construction and first failure

Use the [nested-comb family](../examples/nested-combs.zh.md) with one source-column group:

$$
k\ge6,\quad t=1,\quad w\ge3,\qquad
D=6w,\quad R=D+3,\quad s=2w+5,\quad d=3s,\quad h=(0,d).
$$

Its upper sources are

$$
a_i=(-iR,0),\qquad 1\le i<k.
$$

The query visits short right combs layer by layer. The construction includes the designated complete early prefix at every shifted source. In particular,

$$
a_i+h=(-iR,d)
$$

survives through the short comb on layer $i$. Its last new point is $(iR+D,2+w)$; returning to the layer root visits only old points. The next discovery down the query trunk is

$$
q_{j_i}=(iR+1,0).
$$

At the shifted source it lands at $(1,d)$. Expanding the host construction gives exactly

$$
F\cap(\{1\}\times\mathbb Z)
=\{1\}\times\{0,2,s,d+2,d+s\}.
$$

This row meets only the main trunk, short right-comb trunks, and the two special-comb trunks. Teeth start at depth three; other layers are farther apart than the comb depth. Hence $(1,d)$ is absent, whereas every earlier discovered point belongs to the designated early prefix. This is the first failure.

At the unshifted source, the parent edge is always

$$
a_i+(iR,0)=(0,0),\qquad
a_i+(iR+1,0)=(1,0).
$$

Its first vertex is in the label domain and its second is a road vertex outside that domain. All these sources therefore share the **same directed exit edge**

$$
(0,0)\longrightarrow(1,0).
$$

### Unbounded reuse survives the existing payments

The number of nonroot vertices in one comb is

$$
B=2w^2+6w.
$$

Using an allowed choice in the existing proof, pay the bottom class and the three latest upper long-axis classes, then use class $k-4$ as the reference in the remainder. The surviving sources are

$$
a_1,\ldots,a_{k-5}.
$$

Each still has $B+1$ long-resource markers, while its point-block capacity is $d+1$. Thus the actual unpaid excess associated with the single edge is

$$
(k-5)(B-d)=(k-5)(2w^2-15).
$$

In particular, for fixed $w=3$,

$$
n=42k-2,\qquad
\#\{\text{remaining sources}\}=k-5=\Theta(n),\qquad
\text{remaining excess}=3(k-5).
$$

This refutes both constant remaining-source multiplicity and constant unpaid charge per failure edge. It **does not refute every version of direction B**: sources sharing an edge might still draw on other road resources. The family already admits unit allocation within complete resources and does not refute the algorithm's cubic target.

Round ten rebuilt long-axis spans, four-class payments, the reference choice, and per-source excess from actual markers rather than using the formula as experimental output. The largest checked member has side 1258, exceeding the official limit; it checks the mathematical parameter family and was not run as an official input through the standard program.

## 2. Column bands prove disjointness for the original nested-comb order

**Proposition.** For the public nested-comb family, its original discovery order, and its designated label, choose any genuine strict marker subfamily and the reference class with latest early endpoint. After deleting that class, the entire remaining early-resource union is disjoint from its label translate. Every component therefore satisfies A.

The construction parameters are arbitrary within their valid range. The statement does not change the query root or order and does not assert the same property for other labels.

All bottom-class early endpoints follow all upper-class early endpoints. If a subfamily contains bottom-class markers, that is its reference class; otherwise all remaining classes are already upper classes. Their early prefixes have not visited the special bottom combs or long arms, so all query columns belong to

$$
[0,w+2].
$$

Their source columns are $5sj$. Consequently the remaining resource union satisfies

$$
\mathcal U\subseteq
\bigcup_{j=0}^{t-1}\{(r,c):5sj\le c\le5sj+w+2\}.
$$

Shifting these bands by $d=3s$ cannot meet any original band, because

$$
w+2<3s,\qquad 3s+w+2<5s.
$$

Thus

$$
\mathcal U\cap(\mathcal U+h)=\varnothing.
$$

No component decomposition is needed. This explains repeated experimental success as the original family grows and shows why merely increasing its parameters cannot effectively test the general conjecture.

The argument directly covers the designated resources in the original order. Bent subdivisions, order perturbations, and rerooting may introduce new genuine markers; those require fresh analysis rather than an appeal to visual similarity.

## 3. General disjointness is equivalent to an axis-span bound

**Lemma.** Let a host label component carrying genuine markers have nontrivial tree translation $g$, axis $L$, and translation length $\ell>0$ measured in edges. For every finite nonempty connected subset $U$ of that label component,

$$
\boxed{
U\cap(U+h)=\varnothing
\quad\Longleftrightarrow\quad
\operatorname{diam}\pi_L(U)<\ell.
}
$$

Axis coordinates count edges, and $\pi_L$ is nearest-point projection in the tree. It is not simply the range of horizontal coordinates, especially for curved axes.

**Proof.** If $x,gx$ both belong to $U$, their unique tree path lies in $U$. It reaches the axis, traverses one full translation length, and then leaves the axis for its endpoint. Its projected span is therefore at least $\ell$.

Conversely, if two projections are separated by at least one translation length, the unique path between the original vertices contains that axis segment. Since $U$ is connected, the segment is in $U$. Choose two axis vertices exactly $\ell$ edges apart on it: they differ by $g$, hence by the physical displacement $h$, giving a translated overlap. This proves the equivalence.

Only unique paths in the host tree and its translation axis are used; no infinite repetition of the entire label domain is assumed.

### The remaining proof target

For every resource component remaining in A, the necessary and sufficient bound is

$$
\operatorname{diam}\pi_L(U)\le\ell-1.
$$

Individual early resources already satisfy it. The difficulty is that their projection intervals may form a longer interval through actual resource adjacency. Short individual intervals, or bounds involving only two consecutive intervals, do not automatically control a whole chain.

Round nine checked the equivalence on ordinary components and positive controls retaining reference markers: 94 components included three actual translated overlaps, all agreeing with the span criterion. This checks the implementation; the lemma itself follows from the unique-path proof above.

## 4. Ten-round record

The [experiment script](../explore_reference_rounds.py) reuses coordinate and word helpers from the public verifier and rebuilds candidate histories. The table separates valid conjecture tests, positive controls, and rejected constructions.

| Round | Target | Outcome and evidence |
| --- | --- | --- |
| 1 | Retain reference markers as positive controls, then delete them correctly | Controls recover repeated early endpoints and translated overlap; both correctly filtered inputs pass. [Record](../reference-round-01.json) |
| 2 | Source multiplicity at one failure edge | Six parameter members agree with linear growth; the proof is in Section 1. [Record](../reference-round-02.json) |
| 3 | Why original-order nested combs keep passing | Eighteen members and 288 resource components pass; Section 2 proves the column-band explanation. [Record](../reference-round-03.json) |
| 4 | Shift source columns in either direction | Of 270 attempts, 207 create induced cycles and 63 are valid; valid cases have no counterexample. [Record](../reference-round-04.json) |
| 5 | Vary layer gaps, short arms, and source phases together | Of 600 attempts, 283 have invalid queries and 317 invalid hosts; no valid conjecture test. [Record](../reference-round-05.json) |
| 6 | Reroot queries with depth-first, breadth-first, and random discovery | 144 combinations yield only four nonempty reference scenarios and seven components; no counterexample. [Record](../reference-round-06.json) |
| 7 | Add and remove host leaves while preserving one full query copy | 160 combinations yield 44 nonempty scenarios and 51 components; no counterexample. [Record](../reference-round-07.json) |
| 8 | All horizontal labels and all early-time cuts on small cases | 31 combinations yield 18 nonempty scenarios; no counterexample and no mixed-axis component. [Record](../reference-round-08.json) |
| 9 | Equivalence between axis span and actual overlap | Section 3 proves the general lemma; ordinary and positive-control checks agree. [Record](../reference-round-09.json) |
| 10 | Enumerate earliest stars directly from full prefixes and recompute the final remainder | All markers agree on two small inputs; five parameter members' first failures, actual remaining sources, and excess agree with Section 1. [Record](../reference-round-10.json) |

For each label in round eight, every observed early time defines a cut using all genuine markers up to that early time, followed by strict filtering. This covers common cuts of those marker subfamilies, not all grids or queries.

Correct reference-deletion tests total 418 runs with 414 distinct road/discovery-order pairs. Summed over reference scenarios, they examine 1406 components, including 292 with mixed axes. No translated overlap or repeated early endpoint appears. Cases and components can be reused across scenarios; these are not independent random samples.

**A stronger limitation is that no component in those valid checks has column span reaching the label distance.** The search therefore has not crossed a simple necessary geometric threshold for translated overlap. Many constructions acquire induced cycles before reaching it; rerooting and randomization often eliminate the high-power mixed-axis remainder. Absence of counterexamples here is not strong evidence for the general conjecture.

## 5. Consequences for further work

Direction B must bound total cost after sources share a failure edge; constant multiplicity of the edge is no longer a viable target. Direction A can focus on chains of projected intervals, using the common reference late prefix, earliest-star conditions, and failure order to bound the accumulated span. A counterexample search should first reach a full label-length axis span in a valid nonreference resource component, then verify the complete history. Adding more axis classes inside short column bands does not help.

To reproduce one round from the repository root, for example round two:

```text
python topics/simulation/grid-forest-matching/research/explore_reference_rounds.py --round 2 --output topics/simulation/grid-forest-matching/research/reference-round-02.json
python topics/simulation/grid-forest-matching/research/check_documents.py
```

Round numbers run from one through ten. Rounds one and nine deliberately retain reference classes in positive controls; their overlaps do not refute A. The formal algorithm is unchanged.
