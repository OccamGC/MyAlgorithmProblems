# A cubic time bound for translation matching in four-neighbor grid forests

[中文](cubic-bound.zh.md) · [Full proof](../proofs/cubic-bound.en.md) · [Citation](../../../../../CITATION.md) · [Research directory](../README.md)

On a square board whose road cells induce a forest, a sequence of orthogonal moves is revealed one step at a time. The task is to count all starting cells that can execute the complete current movement prefix. The candidate-list algorithm that scans only at newly discovered relative displacements has a cubic bound on total candidate checks. The proof covers arbitrary forests, without restricting them to a single tree, paths, or combs.

Search terms: grid forest matching, translation matching, walk prefix matching, candidate filtering, amortized analysis, cubic time bound, removing a logarithmic factor; 网格森林匹配、平移匹配、摊还分析。

## Model and precise result

Let $n$ be the board side length, $N\le n^2$ the number of road vertices, and $m$ the number of actual moves. All four-neighbor edges between roads are retained, and their induced graph must be a forest; the road set may be empty. Matching permits translation, without rotation, reflection, or re-embedding.

A candidate start is permanently eliminated once its movement prefix leaves the roads. Previously checked relative displacements require no new scan; only a newly discovered displacement filters the current candidates. Let $W$ count the individual candidate checks in these scans. Then

$$
W\le(5n-3)N,\qquad T=O(n^2+m+nN)\subseteq O(n^3+m).
$$

Space is $O(n^2)$. When $m\ge n-1$, there is a matching worst-case total-time lower bound of $\Omega(n^3+m)$ for this candidate-list algorithm. This is not a cubic lower bound for every possible algorithm. Shorter move sequences also admit the bound $O(n^2+m+N\min(m,n))$.

Extension: [with diagonal directions only](diagonal-only.en.md), coordinate isomorphisms on the two parity classes preserve these check and complexity bounds. That corollary has its own model specification and complete reduction proof.

## Proof idea

The proof counts successful checks over the entire history at once. Group successes by the host road vertex reached and the query row, retain the earliest success in each group, and pair later successes with it. Each pair receives a horizontal translation label and a complete early-prefix resource.

For a fixed label, resources are divided into the common-cut class, a reference class in each road-intersection component, and the remaining classes. A finite second-axis lemma separates remaining copies with the same early endpoint. Bin the left endpoints of resource projections by the label-axis length: road vertices can be assigned injectively within each bin, and a vertex participates in at most two bins.

The common-cut, reference, and remaining charges have capacities one, one, and two. Each label therefore uses at most four road-intersection budgets. Summing over horizontal labels counts ordered pairs of road vertices in the same row, bounded by board side times road count. See the [full proof](../proofs/cubic-bound.en.md) for definitions, the finite second-axis lemma, a worked charge, and the lower bound; see the [editorial](../../solution.en.md) and [reference implementation](../../std.cpp) for the algorithm.

## Result status and research history

The status here is “general proof provided in the repository.” Finite program checks are supporting evidence, not a replacement for the proof for arbitrary sizes; this page makes no claim of external peer review.

The earlier $O(n^3\log(n+1)+m)$ upper bound remains valid but is weaker. Direction A's conjecture that every connected resource union is disjoint from its label translate after removing a reference class was refuted by opposite early arms. The current proof bounds per-vertex capacity and does not require that disjointness. See the [result index](../../../../../research-index.json) for document statuses.

## Reproduction and citation

Run from the repository root using Python 3.10 or later:

```text
python -c "from pathlib import Path; Path('tmp/grid-forest-matching').mkdir(parents=True, exist_ok=True)"
python topics/simulation/grid-forest-matching/research/verify_cubic_bound.py --output tmp/grid-forest-matching/cubic-bound-results.json
```

The [published report](../cubic-bound-results.json) records 1,886 cases, including all induced forests on a three-by-three board under specified traversals, constructed cases, and fixed-seed random cases. It does not exhaust arbitrary board sizes or all move sequences. See the [verification instructions](../README.md) for C++ comparisons and document checks.

Proof version: [commit 640ae4a](https://github.com/OccamGC/MyAlgorithmProblems/commit/640ae4ac52a1ce5a3082022162611839f97591fe), published on 2026-10-12. The citation key `OccamGC2026GridForestCubic` and an immutable proof link are in the [citation guide](../../../../../CITATION.md).
