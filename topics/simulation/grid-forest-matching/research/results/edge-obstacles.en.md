# Vertex and edge obstacles: four- and eight-neighbor forest matching

Status: **proof supplied**. Date: 2026-10-12. Stable ID: `grid-forest-matching-edge-obstacles`.

[中文](edge-obstacles.zh.md) · [Research directory](../README.md) · [Eight-neighbor induced forests](eight-neighbor.en.md)

This result extends the existing cubic bound to independently blocked paths. The key changes are to build query trees and common intersections from actual open edges, and to revise the handling of revisited positions.

## 1. Model and conclusions

The board has side length $n$, usable cell set $F$, and $N=|F|\le n^2$. The input also specifies an open undirected edge set $E$; endpoints must be usable and directions must belong to the four- or eight-neighbor direction set. Other potential neighbor edges may be blocked individually. The actual traversable graph $G=(F,E)$ must be a forest; the complete geometric adjacency graph of the usable cells need not be a forest.

Obstacles are static, and an edge is blocked in both directions. In the eight-neighbor model, only grid points are vertices: geometric crossings of diagonal edges do not automatically create junctions. A valid start must execute the entire movement prefix, entering no blocked cell and crossing no blocked edge. Failure is permanent.

For the modified candidate-list algorithm below, both direction sets satisfy

$$
W\le(5n-3)N,\qquad
T=O(n^2+m+nN)\subseteq O(n^3+m),\qquad
S=O(n^2).
$$

$W$ counts individual candidate checks only; a bulk zero answer performs no such checks. If the first cycle-closing step scans the candidates instead of exploiting the forest to clear them in bulk, it costs at most an additional $N$ checks and still gives a cubic bound. That variant is outside the explicit constant stated above.

For $m\ge n-1$, this candidate-list algorithm still has a matching $\Theta(n^3+m)$ worst-case lower bound. This is not a lower bound for every possible algorithm.

## 2. The algorithm must change: remembered positions are insufficient

Let the current relative position be $p$, and the next destination be $q$.

1. If $q$ is new, check both the destination $a+q$ and the edge $\{a+p,a+q\}$ for every candidate start $a$, removing failures.
2. If $q$ is old and $\{p,q\}$ has already been traversed, every surviving candidate has verified this undirected edge. No further scan is needed.
3. If $q$ is old but $\{p,q\}$ has never been traversed, clear all candidates immediately.

Implement the third case by setting the candidate array's active length to zero while retaining its allocated storage, without deleting candidates individually.

The reason for the third case is that, while any candidate survives, the traversed relative vertices and edges form a tree. There is already a unique path between two old vertices; adding a new edge between them creates a cycle. Translation is injective on vertices, so this cycle cannot embed in the traversable forest.

For a four-neighbor example, name the square's corners $A$ at the top left, $B$ at the top right, $C$ at the bottom right, and $D$ at the bottom left. Open only $AB,BC,CD$ and block $DA$. Starting at $A$, east, south, and west remain valid; the fourth move north to the old position $A$ must fail. The old rule that only asks whether the destination has been visited would incorrectly skip this check.

```text
A──B
×  │
D──C
```

Solid lines are open paths, and the cross is a blocked path. All four vertices are usable.

The eight-neighbor example is shorter: open $AB,BC$ and block the diagonal $CA$. East, south, and northwest close a triangle, and the final move must again clear the candidates. The shortest simple cycle has four edges with four-neighbor moves and may have three with eight-neighbor moves; the treatment is identical.

Store the parent of each newly discovered point. While the traversed graph is a tree, its known edges are exactly its parent-child edges, so a previously traversed undirected edge can be recognized in constant time. No path search or union-find operation is needed per move. Retain the original constant-time empty-candidate and global out-of-bounds handling.

## 3. Replace the induced query tree with the actually traversed query tree

Let $Q_j=(P_j,A_j)$ consist of the vertices and edges actually traversed in a first-discovery prefix. Consider only the longest prefix with a surviving match: each successful extension adds a vertex and its discovery edge, so these prefixes are nested trees.

A successful start $a$ now means

$$
a+P_j\subseteq F,\qquad a+A_j\subseteq E.
$$

Besides containment of the vertices, every query-tree edge must be open. A successful match still embeds the query tree in an actual host tree. A nonempty intersection of two successful prefixes in the same host tree is still a connected subtree, by uniqueness of paths in a tree.

The complete geometric four- or eight-neighbor graph on the query vertices may have extra edges. Those edges need not be open or traversed. The proof can no longer treat full geometric adjacency as the query edge set.

## 4. Common intersections must check both edge copies

Continue choosing the earliest star center for each pair of host target and query row. Every non-center success produces a mark $(a,e,f)$ with horizontal label $h=f-e$, satisfying

$$
a+Q_{t(f)}\subseteq G,\qquad a+h+Q_{t(e)}\subseteq G.
$$

Containment here means graph containment. For a fixed label, define the intersection graph $H_h$ by

$$
V(H_h)=F\cap(F-h),
$$

$$
E(H_h)=\{\{x,y\}\in E:\{x+h,y+h\}\in E\}.
$$

The endpoints automatically belong to the stated vertex set. The complete early-prefix resource $a+Q_{t(e)}$ is a connected subtree of this graph, because both copies of the early prefix successfully match their respective sources.

It is insufficient to take the common vertices and join geometric neighbors, or even to retain every original host edge between them. For example, let $(0,0),(0,1),(0,2)$ all be usable, with only the edge from the first to the second open. For $h=(0,1)$, the common vertices are the first two. Their original edge is open but its translated copy is blocked, so the intersection graph must contain two isolated vertices.

## 5. Transferring the charging proof

This section depends on the [complete-history charging proof](../proofs/cubic-bound.en.md) and the [eight-direction word argument](eight-neighbor.en.md). The substitutions are as follows.

| Proof object | Corresponding object with edge obstacles |
| --- | --- |
| Induced road tree | Host tree formed by actual open edges |
| Query tree determined by geometric adjacency | Actually traversed query tree $Q_j$ |
| Induced components on the common road vertices | Components of $H_h$, retaining only edges open on both sides |
| Intersection of translated query prefixes | Graph intersection of the query trees, again retaining edges present on both sides |

In each marked intersection component $K$, both $K$ and $K+h$ are connected. The early and late successful copies of a mark meet at their target and therefore belong to the same host tree; hence the whole of $K$ and $K+h$ also lies in that tree.

Translation preserves the direction across every common open edge, so it still acts as a uniform left multiplication $g$. Four directions use a rank-two free group; eight directions use rank four. The path-word embedding of an actual tree, coordinate injectivity on that tree, unique axes, and commuting-period properties do not require every geometric neighbor edge to be open.

Connectivity for the common cut also survives. Early and late prefixes are subtrees of the same host tree. The unique path between two vertices of their intersection must occur in both prefixes, so its edges belong to their graph intersection. This uses paths in the actual tree, rather than unverified geometric neighbor edges.

Consequently, the original unit capacity within each query class, one common-cut budget, one componentwise reference-class budget, finite second-axis lemma, and two budgets for nonreference bins all apply:

$$
\widetilde M_h\le4|V(H_h)|.
$$

A strict resource remains vertex-disjoint from its label translate, so its tree-axis projection span is shorter than one label-axis length. The two points compared by the finite second-axis lemma still occur in actual finite successful copies. The lemma does not require every potential host edge to exist. No additional factor charging separately for each direction is introduced.

The query tree occupies at most $n$ rows, giving at most $nN$ star centers. Each candidate incurs at most one failed scan, for at most $N$ failures. If host row $r$ contains $k_r$ usable points, then

$$
\sum_{h=(0,d),\ d\ne0}|V(H_h)|
=\sum_r k_r(k_r-1)
\le(n-1)N.
$$

Blocking edges changes intersection components but leaves this budget of ordered pairs in the same row unchanged. Thus

$$
W\le nN+N+4\sum_h|V(H_h)|\le(5n-3)N.
$$

This conclusion concerns the edge-aware candidate algorithm on static undirected traversable forests. Neither correctness nor this complexity claim can be attributed directly to the unmodified [C++ reference program](../../std.cpp), which checks destination cells only.

## 6. A simple constant-scale reduction for four neighbors

As an independent explanation with a weaker constant, map each original vertex to $(2r,2c)$, make the midpoint of every open orthogonal edge a road vertex, and make the midpoint of every blocked edge an obstacle. The result is an induced four-neighbor forest on a board of side $2n-1$, exactly the subdivision of the original graph.

Replace each original move with two moves in the same direction and restrict candidate starts to images of original vertices. Vertex and edge traversability correspond exactly. The new road count is $N+|E|\le2N$, so the original theorem gives $O(nN)$ checks, again sufficient for the cubic bound. Restricting the start set only decreases candidate counts and cannot increase filtering work for the same move sequence.

The midpoint reduction does not transfer directly to eight neighbors: two crossing diagonals would share a midpoint and incorrectly create a junction. The intersection-graph and direction-word proof above covers eight neighbors without this geometric subdivision.

## 7. The generalized inputs still attain the cubic lower bound

Make all $n^2$ cells usable, open only horizontal edges within each row, and block all vertical edges. In the eight-neighbor model, block every diagonal as well. The traversable graph is exactly $n$ horizontal paths of $n$ vertices each, a valid forest with $N=n^2$.

Taking $n-1$ eastward steps gives

$$
W=n\sum_{j=1}^{n-1}(n-j+1)
=\frac{n(n-1)(n+2)}2=\Theta(n^3).
$$

Subsequent back-and-forth moves on the already traversed path extend the sequence to any $m\ge n-1$. Outputting an answer per step requires $\Omega(m)$. Both direction sets therefore have a matching worst-case bound for the candidate-list algorithm.

## 8. Finite verification and scope

The [verifier](../verify_edge_obstacles.py) and [report](../edge-obstacles-results.json) are published with this note; the final status is `passed`. The report retains per-case statistics and charging-assignment fingerprints, plus SHA-256 hashes of the verification sources. It does not store every raw charging assignment.

- Four neighbors: all 46 forests over all usable-vertex and open-edge subsets of a two-by-two board, with 11,776 exhaustive four-step walks; also 271 complete-history charging cases.
- Eight neighbors: 83 corresponding forests, 339,968 four-step walks, and 406 complete-history charging cases.
- In total: 351,744 short-walk combinations and 677 charging cases. The independent answer oracle moves absolute positions at every step and never skips revisited positions.
- Larger cases include seeded random open-edge forests, fully usable horizontal stripes, opposite early arms, a curved power-one fixture, and nested combs. The eight-direction cases also include refined instances using all eight move directions.
- Explicit four-step orthogonal and three-step diagonal cycles test the new-edge-to-old-vertex rule: the final step clears all candidates. A three-vertex negative control checks that translated edge openness must also be tested.
- The charging core is reused from the published verifier, with explicit substitutions for open-edge checks, query trees, host path words, and intersection components. It is not an independently implemented charging-proof checker. Both models have nonempty coverage of nonreference marks, repeated early endpoints, and the power-one case.

Experiments do not establish the asymptotic bound over unbounded inputs; the general result follows from the algorithm and proof transfer in Sections 2–5. This note also makes no new claim about extending a forest to a tree by adding vertices while blocked edges remain fixed. Permission to change edge obstacles must not be confused with permission to add only vertices.

```text
python topics/simulation/grid-forest-matching/research/verify_edge_obstacles.py --output tmp/grid-forest-matching/edge-obstacles-results.json --check-published
```

`--check-published` requires the regenerated report to equal the published JSON exactly; the website publication workflow runs this check too. Source hashes use UTF-8 with LF line endings for reproducibility across systems.

## 9. Citation

Citation key: `OccamGC2026EdgeObstacleGridForest`. See the [repository citation guide](../../../../../CITATION.md) for the fixed version and BibTeX. This result depends on the original complete-history charging proof and its eight-neighbor direction-word extension; it establishes no new tree-extension obstruction.
