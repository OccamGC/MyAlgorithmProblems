# First investigation after merging the logarithm-removal directions

**Current overall result:** the [general cubic proof](../proofs/cubic-bound.en.md) is complete. The finite investigations, unsuccessful approaches, and local lemmas below retain their historical scope and statistics.

Date: 2026-10-12. This tests [direction A in the overview](../../complexity-research.en.md).

**Current status:** a later opposite-arm construction satisfies every hypothesis and refutes general disjointness. See the [obstruction and replacement capacity draft](../proofs/reference-capacity.en.md). The original investigation's conclusions and scope are retained below.

**Status: finite checks passed; the general conjecture remains unproved.** Candidate histories, earliest stars, and resources were recomputed. No counterexample was found, but these reproducible observations do not close the complexity gap.

The subsequent ten research rounds are complete. They add a parameter counterexample to constant failure-edge multiplicity, a column-band proof for original-order nested combs, and an axis-projection equivalence for general disjointness. See the [follow-up record](../proofs/reference-followup.en.md). The original scope and results of the initial experiment remain below.

## 1. Why start with this conjecture?

The overall aim remains a budget shared across prefix scales. Direction A offers a concrete local target: fix a genuine label and common cut, select one high-power conjugacy family, and remove the reference axis class containing the latest early endpoint. Must every remaining connected resource component satisfy

$$
U\cap(U+h)=\varnothing?
$$

Connectivity includes all unit grid edges between resources, not just shared vertices. If the conjecture holds, the established axis-spacing lemma rules out repeated query early endpoints within a component, and the complete-prefix Hall argument gives unit capacity. See [Sections 30–40 of the label proof](../proofs/complexity-labels.en.md) for the precise hypotheses and implication.

Individual early resources are already proved disjoint from their own translates. Extending this to their connected union is exactly the missing step; the forest condition alone does not provide it.

## 2. What actual objects are checked?

The [verifier](../verify_reference_components.py) uses only the standard library and the public input verifier, with no private historical dependencies.

1. Check that all induced host-grid edges form a forest. Start with every road candidate and filter at every newly discovered displacement, retaining the complete-prefix condition.
2. For each target road cell and query row, use the first successful nonzero query point as the star center. Later markers use this center rather than arbitrary pairs of successes.
3. For each tested label, define the actual common cut using the latest early time among all its genuine markers. Write this time as $t_*$ and set

$$
P=P_{t_*},\qquad
\tau=\min\{t(x):x\in P,\ x+h\in P\}.
$$

If the set is empty, take $\tau=t_*+1$. Retain only strict markers with $t(e)<\tau$ and $t(f)>t_*$.

4. Use direction words from the query root to compute

$$
g_e=w(f)w(e)^{-1}.
$$

Cyclically reduce each reduced word and extract its shortest period. Group by label, the cyclic-rotation class of the primitive cyclic word, and exponent; test only families with $q\ge4$. Full reduced words distinguish query axis classes within each group.

5. For each possible reference axis class, take its latest early time, retain markers no later than that time, and remove the entire class. Check each induced component of the remaining complete-resource union for self-translation overlap and repeated early endpoints.
6. Also check that every nonreference source matches the reference late prefix, its shifted source first fails in the correct early-time interval, and the failure parent edge exits the label domain.
7. Realize generated discovery orders as actual tree walks, counting return moves. Compare set-based scan counts against an independent bitset implementation for every case; save total cost, costs in doubling ranges, and input fingerprints.

Step 5 uses the existing monotonicity argument to cover **all marker subfamilies for that fixed cut**. Any subfamily using a given reference class is contained in its maximal eligible family. Deleting resources cannot create connectivity, translated overlap, or repeated early endpoints. This does not cover all problems obtained by choosing different cuts.

Early prefixes at one source are nested, so their union can be computed from the largest resource. All markers are nevertheless retained when counting markers and repeated early endpoints.

## 3. Inputs and variations

| Group | Runs | Scope |
| --- | ---: | --- |
| Public representative inputs | 8 | Read inputs, verify fingerprints, and check every horizontal label that actually occurs |
| Regenerated nested combs | 72 | Eighteen parameter choices and four discovery orders each; only the designated construction label |
| Periodically bent constructions | 20 | Five base parameter choices and four orders each; only the transformed designated label |

The nested combs use $k\in\{6,7,9\}$, $t\in\{1,2,3\}$, and $w\in\{3,4\}$, rebuilding roads and queries directly from the [public construction](nested-combs.zh.md). Each fixed board uses its original order and three randomized orders with priority windows 8, 64, and the query size. Priorities perturb original discovery ranks while requiring parents before children, so every prefix remains connected. The seed rule is saved in the script.

The bent group uses base parameters $(4,2,1),(5,2,1),(5,2,2),(7,2,1),(9,2,1)$. Small-width members reuse the generation rule and are individually checked; results from the original parameter proof requiring $k\ge6,w\ge3$ are not assumed.

The transformation scales original vertices by six, replaces each vertical edge by six vertical steps, and replaces each rightward edge by

$$
E^2S^2E^2N^2E^2.
$$

This path moves six columns right with a downward detour and return; the label is scaled by six as well. Its shortest period has length ten, so the investigation is not restricted to straight axes. Every induced edge of the transformed host is checked afresh, without assuming that the transformation preserves validity. Every tested instance is within the official side-length limit.

## 4. Results and interpretation

The [result JSON](../reference-components-results.json) contains individual records. Reference scenarios can overlap, so their resource and marker counts are not counts of globally distinct objects.

| Measurement | Result |
| --- | ---: |
| Distinct road/discovery-order pairs | 100 |
| Components checked after reference deletion, summed over scenarios | 904 |
| Components containing multiple nonreference axis classes | 678 |
| Components containing at least three nonreference axis classes | 537 |
| Maximum nonreference axis classes in one component | 8 |
| Components overlapping their label translate | 0 |
| Components containing repeated query early endpoints | 0 |

Thus the checks do reach connected unions of several nonreference axis classes, rather than only single-class or empty remainders. Some changed discovery orders eliminate nonempty reference scenarios; these runs remain in the record but are not counted as evidence that a difficult configuration was reached.

**The observations do not prove the conjecture.** Most geometry comes from one nested-comb mechanism. The bent family adds only one shortest period, not arbitrary periods or forests. The search uses actual common cuts without enumerating all inputs and cuts, and establishes no general capacity bound for the hardest remainder.

## 5. What still needs a proof?

Consider a minimal connected resource subfamily whose union overlaps its translate. Each resource is individually disjoint, so a conflict can arise only after resources are connected. One could combine the shared reference late-prefix matches with the ordering of shifted-source failures before the reference early endpoint, and try to force two distinct connecting paths in the host.


This is a concrete proof target, not a completed derivation that every conflict creates a cycle. If translate-disjointness is too strong, the weaker sufficient statement is still worth studying: query early endpoints are distinct within each component after reference deletion. It was checked separately here and also had no counterexample.

Reproduce from the repository root:

```text
python topics/simulation/grid-forest-matching/research/verify_reference_components.py --output topics/simulation/grid-forest-matching/research/reference-components-results.json
python topics/simulation/grid-forest-matching/research/check_documents.py
```

The formal algorithm is unchanged; the general cubic upper bound remains open.
