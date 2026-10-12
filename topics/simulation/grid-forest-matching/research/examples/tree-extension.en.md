# Induced grid forests cannot always be extended to trees

Discussion note: 2026-10-12. If road positions and all four-neighbor edges are preserved, adding grid vertices need not turn a forest into a tree. The obstruction extends beyond small examples: a square board can contain linearly many trees, each with linearly many vertices, such that no pair can be joined into an induced tree by adding vertices. This note records the questions, constructions, proofs, and examples. See the [Chinese version](tree-extension.zh.md).

## 1. The precise question

Let $n$ be the board side length and $R=|F|$ the road count. The uppercase N used for scale in the discussion means the side length n here; other research documents usually use uppercase N for the road count. “Linearly many” below means a $\Theta(n)$ construction, not merely a big O upper bound.

For a set S of integer grid vertices, let G(S) include every edge between vertices of S at Manhattan distance one. The question is whether every road set F inducing a forest admits a finite set S such that

$$
F\subseteq S,\qquad G(S)\text{ is a tree}?
$$

Equivalently, can the original forest be obtained by deleting vertices from an induced grid tree in the same embedding? Original roads cannot be moved, deleted, or rescaled; edges created by adding roads cannot be selectively ignored. The counterexamples even allow arbitrary enlargement of the board.

For abstract graphs the answer is yes: add a new vertex and connect it to one vertex in each component. If grid positions are retained but edges may be freely omitted, the original forest can also be extended to a spanning tree of a larger connected rectangular grid. Neither operation is the induced model of this problem, which permits only the addition of road vertices.

| Question | Conclusion |
| --- | --- |
| Is every induced four-neighbor grid forest a vertex-deleted induced grid tree? | No; a two-component example on a 5×5 board suffices. |
| Can both obstructed trees have linear size? | Yes; both can even be simple paths, with linearly many forbidden bridge cells directly adjacent to both sides. |
| Can there also be linearly many such trees? | Yes; linearly many components can each have linear size, and no selected pair can be joined into an induced tree by adding vertices. |
| Can a larger board or a long detour fix these examples? | No; cells that every connecting path must visit are themselves forbidden, regardless of exterior space. |

## 2. A basic obstruction to adding a vertex

Let A be a tree that must be retained, and let an empty cell x be adjacent to distinct vertices u and v of A. The existing unique path from u to v, together with the two edges through x, creates a cycle when x is added.

Thus **no induced tree containing A can contain x**. This is not a failure of one insertion order: every final supergraph would contain that cycle, and adding more vertices cannot remove it.

If forbidden cells of this kind separate another component from A, the components cannot be joined. All constructions below use this fact.

## 3. A 5×5 counterexample

Each character below denotes a grid vertex. A is a path on 13 vertices, B is a singleton, and both × and · are empty cells. The crosses mark the four neighbors of B.

```text
· A A A ·
· A × A A
· × B × A
· A × A A
· A A A ·
```

A and B are not adjacent, so the initial induced graph is a forest with two components. Every cross has at least two neighbors in A and is therefore forbidden. The first step from B must enter one of these cells, making any connection to A impossible.

Embedding this example inside a larger board does not change the argument. It is a small counterexample; no minimality in board side length or road count is claimed.

## 4. Two trees of linear size can also be isolated

### 4.1 A staircase path with a gap

Center coordinates at the origin and define

$$
\rho(x,y)=|x|+|y|.
$$

For an integer $t\ge2$, first construct the staircase cycle

$$
C_t=\{(x,y):\rho(x,y)=t\}
\cup\{(x,y):\rho(x,y)=t+1,\ xy\ne0\},
$$

then delete three consecutive vertices on one side:

$$
P_t=C_t\setminus\{(-1,-t),(0,-t),(1,-t)\}.
$$

If the first coordinate is the row and the second is the column, the gap is on the left. Vertices on the two radii alternate around the four quadrants, making C_t an induced simple cycle: every vertex has degree two and the cycle is connected. Each radial layer has $4t$ vertices. Deleting three consecutive vertices leaves an induced simple path with

$$
|P_t|=8t-3,\qquad P_t\subseteq[-t,t]^2.
$$

### 4.2 A parameter family of two paths

For an integer $k\ge5$, set

$$
n=2k+1,\qquad A=P_k,\qquad B=P_{k-3}.
$$

Both paths fit in a board of side n, and

$$
|A|=8k-3=4n-7,\qquad |B|=8k-27=4n-31.
$$

A has radius at least k and B has radius at most k minus two, so there are no four-neighbor edges between them. Both trees have $\Theta(n)$ vertices.

![An eleven by eleven example has an outer path A on 37 vertices, an inner path B on 13 vertices, and a separating ring of 16 forbidden cross-marked cells.](../../assets/two-growing-tree-obstruction.svg)

Both road paths have gaps. The complete ring of forbidden empty cells prevents a connection; neither road component is a cycle.

### 4.3 Why the gap is not a passage

Consider the empty ring

$$
X_k=\{(x,y):\rho(x,y)=k-1\}.
$$

A non-axis cell in this ring has two outward neighbors, both in the radius-k layer of A. An axis cell originally has three such neighbors; even the cell facing the gap loses only one and retains two. The other two deleted gap vertices have radius k plus one and cannot be adjacent to this ring.

Every cell of X_k is therefore forbidden by Section 2. Each four-neighbor step changes the radius by exactly one, so every path from B to A must visit X_k. Enlarging the board does not change this necessary crossing.

The two paths of linear size consequently cannot be joined into an induced tree. The forbidden ring contains

$$
|X_k|=4k-4=2n-6.
$$

Except for its four axis cells and two cells next to the gap, all forbidden cells also directly neighbor B. The number of cells adjacent to both trees, but creating a cycle as soon as they are added, is exactly

$$
4k-10=2n-12=\Theta(n).
$$

For example, the illustrated board has side 11, paths of 37 and 13 vertices, and 16 forbidden cells, 10 of which directly neighbor both paths. This enlarges a small local obstruction into one of linear size.

## 5. Linearly many trees can coexist

For a positive integer s, set

$$
n=12s+1,\qquad t_i=6s-3i\quad(0\le i\le s),\qquad T_i=P_{t_i}.
$$

Start at radius 6s, decrease the radius by three per layer, and stop at radius 3s. All paths fit in the same board of side n. The radial separation excludes four-neighbor edges between different layers, so these paths are exactly the forest components.

The number of trees is

$$
s+1=\frac{n+11}{12}=\Theta(n).
$$

Each tree has

$$
|T_i|=48s-24i-3,\qquad 2n-5\le |T_i|\le4n-7.
$$

Thus every component has $\Theta(n)$ vertices. The count is not obtained from singleton components, and nesting stops before inner paths become constant-sized. The total road count is

$$
R=\sum_{i=0}^{s}|T_i|=(s+1)(36s-3)=36s^2+33s-3=\Theta(n^2).
$$

![Three staircase paths on a board of side 25 have 93, 69, and 45 vertices. Two rings of crosses separate each outer path from all paths further inside.](../../assets/nested-tree-obstructions.svg)

For every path except the innermost one, define

$$
X_i=\{(x,y):\rho(x,y)=t_i-1\}\qquad(0\le i<s).
$$

Each cell of X_i neighbors at least two vertices of T_i and is forbidden; all further inner paths lie inside this ring. For any two distinct paths, take the ring associated with the outer path to prove that they cannot be connected. **The conclusion remains true when only the selected two paths are retained; it does not rely on other components blocking the way.**

These disjoint separating rings contain

$$
\sum_{i=0}^{s-1}|X_i|=18s^2+2s=\Theta(n^2)
$$

forbidden cells in total.

| s | Board side | Trees | Smallest tree | Largest tree | Total roads |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 13 | 2 | 21 | 45 | 66 |
| 2 | 25 | 3 | 45 | 93 | 207 |
| 3 | 37 | 4 | 69 | 141 | 420 |
| 5 | 61 | 6 | 117 | 237 | 1062 |
| 10 | 121 | 11 | 237 | 477 | 3927 |
| 20 | 241 | 21 | 477 | 957 | 15057 |
| 33 | 397 | 34 | 789 | 1581 | 40290 |

Unbounded parameters give an asymptotic family; the table lists individual instances. For other sufficiently large board sizes, choose the largest preceding side from this family and pad with empty cells. The side lengths differ by only a constant, preserving linear component sizes, a linear component count, and the obstruction.

If every tree is required to contain at least linearly many vertices, the number of components is at most

$$
\frac{n^2}{\Omega(n)}=O(n).
$$

The construction therefore attains the asymptotic order allowed by area. This optimality statement requires every tree to have linear size; it is not a bound on the component count of an arbitrary grid forest.

## 6. Consequences for the complexity question

This refutes a direct reduction: an arbitrary road forest cannot always be extended to one tree while preserving its positions and induced edges, so a single-tree result cannot be transferred to all forests solely by that operation. Other reductions involving relocation, rescaling, changes to the edge model, or separate accounting for components need their effects on matching and cost proved separately.

These counterexamples **do not establish supercubic candidate-checking work**. In fact, every component is a path, placing the constructions in a subclass for which the logarithm has already been removed in the [root-to-leaf-chain proof](../proofs/complexity-chains.en.md). The number of tree components is also different from the number of translation candidates.

The earlier questions about a single comb tree, quadratic candidate counts after linear scanning rounds, and the cubic cost of that construction are recorded in the [comb-tree questions](comb-candidates.en.md). The [complete-history charge](../proofs/cubic-bound.en.md) now proves $O(n^3+m)$ for general forests; see the [research overview](../../complexity-research.en.md) for the history.

## 7. Reproducible finite checks

The [construction verifier](../verify_tree_extension.py) generates all four-neighbor edges directly from coordinates. It checks the small counterexample, the two-path family, and every nested instance in the table: exactly the intended path components, correct vertex and edge counts, no unintended edges between layers, at least two outer-path neighbors for every forbidden cell, and the radial separator relations.

Run from the repository root:

```text
python topics/simulation/grid-forest-matching/research/verify_tree_extension.py
python topics/simulation/grid-forest-matching/research/check_documents.py
```

The script checks finite instances and exact counts. Nonextendability for arbitrary parameters follows from Sections 2, 4, and 5 rather than finite search. These static forests are not presented as supercubic query inputs.
