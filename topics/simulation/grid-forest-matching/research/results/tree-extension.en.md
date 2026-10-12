# Induced four-neighbor grid forests need not extend to trees by adding vertices

[中文](tree-extension.zh.md) · [Full constructions and proof](../examples/tree-extension.en.md) · [Citation](../../../../../CITATION.md) · [Research directory](../README.md)

Every abstract forest can be extended to a tree by adding connections, but an induced forest at fixed integer-grid positions has additional constraints. If all original vertices and all four-neighbor edges must be retained and only grid vertices may be added, some forests cannot be contained in any induced grid tree. Arbitrarily enlarging the board does not remove the obstruction.

Search terms: induced grid forest, induced tree extension, vertex addition, vertex-deleted grid tree, nonextendable forest, forbidden separator; 诱导网格森林、森林扩充成树、树删除顶点、禁止桥接格点。

## Model and precise result

For a finite integer-grid vertex set $F\subset\mathbb Z^2$, let $G(F)$ contain every edge between vertices at Manhattan distance one. If $G(F)$ is a forest, must there be a finite set $S\supseteq F$ such that $G(S)$ is a tree?

No. Equivalently, a forest need not be obtainable by deleting vertices from an induced grid tree in the same embedding. Original vertices may not be moved, rescaled, or deleted, and newly created four-neighbor edges cannot be selectively omitted.

| Scale | Counterexample provided |
| --- | --- |
| Small | A 13-vertex path and an isolated vertex on a 5×5 board cannot be joined into an induced tree by adding vertices |
| Two large components | Two paths of linear size, separated by a ring that any connecting path must enter but whose cells cannot be added |
| Many large components | A square board of side $n$ contains $\Theta(n)$ trees, each with $\Theta(n)$ vertices; any selected pair remains impossible to join into an induced tree even if all other components are removed |

Linear scale refers to board side length, not total road count. The nested construction has $\Theta(n^2)$ road vertices in total.

## Why the obstruction works

If an empty cell is adjacent to two distinct vertices of a retained tree, adding it creates a cycle with the existing unique path in that tree. No final induced tree containing the retained tree can contain this cell.

The constructions make these forbidden cells form a separating ring around another component. Any connecting path must enter the ring, so a connection is impossible regardless of exterior space. Nesting staircase paths with gaps produces linearly many pairwise obstructions.

![Three nested paths on a board of side 25 have 93, 69, and 45 vertices; the crossed rings are forbidden separators.](../../assets/nested-tree-obstructions.svg)

The full proof specifies the coordinates, forbidden rings, and counts. For example, for an integer $s\ge1$, choosing $n=12s+1$ gives $s+1$ trees, each having between $2n-5$ and $4n-7$ vertices. See the [small example, two-path family, and nested family](../examples/tree-extension.en.md).

## Scope

This refutes the direct reduction that adds vertices to turn every fixed-position induced forest into one tree. Other reductions that permit movement, scaling, changes to the edge model, or separate treatment of components require their own analysis.

This static construction is not a supercubic matching-complexity counterexample. The candidate-list algorithm on general forests still satisfies the [cubic bound](cubic-bound.en.md). This result has the status “counterexample families and proofs for arbitrary parameters provided in the repository”; finite instance checks are supporting evidence, without a claim of external peer review.

## Reproduction and citation

Run from the repository root using Python 3.10 or later:

```text
python topics/simulation/grid-forest-matching/research/verify_tree_extension.py
```

The [verifier](../verify_tree_extension.py) regenerates every four-neighbor edge from coordinates and checks component sizes, the forest property, forbidden cells, and separating radii. Nonextendability for arbitrary parameters follows from the written proof, not finite enumeration.

Proof version: [commit 640ae4a](https://github.com/OccamGC/MyAlgorithmProblems/commit/640ae4ac52a1ce5a3082022162611839f97591fe), published on 2026-10-12. The citation key `OccamGC2026GridForestTreeExtension` and an immutable version link appear in the [citation guide](../../../../../CITATION.md). Machine-readable assumptions and conclusions appear in the [result index](../../../../../research-index.json).
