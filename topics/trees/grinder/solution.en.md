# Grinder: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: degree-three expansion, edge decomposition and monotone windows.** Edge decomposition gives the reference its $O(n\log(n+1))$ bound. Centroid decomposition with a segment tree has an $O(n\log^2(n+1))$ general bound, but runs faster and uses less memory on the measured inputs. These are peer methods: edge decomposition has the stronger general worst-case guarantee, while centroid decomposition does less work on these inputs, as discussed below.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For centroid decomposition with a segment tree, as used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [peer method editorial](solution-alternative.en.md).

## Converting vertex weights

Give an original edge $(u,v)$ weight $v_u+v_v$ and length one. Its path sum plus the two endpoint weights equals twice the original vertex sum: internal vertices are counted by two incident edges, and the extra terms supply the second endpoint copies. Maintain doubled scores and divide by two at the end.

## Degree-three expansion

Root the original tree arbitrarily. For children $v_1,\ldots,v_k$ of $u$ , create a dummy chain $u,z_1,\ldots,z_k$ with zero weights and lengths. Attach $v_i$ to $z_i$ by an edge of length one and weight $v_u+v_{v_i}$ . Paths between original vertices keep their lengths and scores. Only original vertices may be endpoints.

There are $2n-1$ vertices, all of degree at most three. Every length-one edge retains its original-edge identity; dummy edges only provide connectivity.

## Balanced cuts and depth windows

Choose an edge minimizing the larger remaining component. In a degree-three tree, a vertex centroid has an adjacent component of size between $(s-1)/3$ and $s/2$ . Cutting that edge leaves both sides of size at most about $2s/3$ . Thus the decomposition has $O(\log(n+1))$ levels.

For cut edge $e$ of length $\ell_e\in\{0,1\}$ and weight $w_e$ , collect depth $d_x$ and edge sum $s_x$ from each side's cut endpoint. Original endpoints $x,y$ must satisfy

$$L-d_x-\ell_e\le d_y\le R-d_x-\ell_e,$$

and their doubled score is

$$s_x+v_x+w_e+s_y+v_y.$$

Store the largest $s_y+v_y$ at every partner depth, excluding dummy endpoints. Zero-length edges mean traversal order need not be depth order, so use depth buckets to order queries in linear time. Their window boundaries decrease monotonically; a monotone deque answers all queries in linear time. Process both directions.

## Updating every original edge

Propagate each endpoint's best full-path score toward its side's cut endpoint in reverse traversal order, updating original edges encountered. Also update the cut edge if it is original. Propagated candidates necessarily contain those edges. Conversely, every edge of a crossing path receives a candidate from an endpoint on its corresponding side.

Continue in the two remaining components. Each path with an edge is processed when a cut first separates its endpoints. For an original vertex, take the largest score of its incident original edges and divide by two. Every nonsingleton path containing that vertex uses such an edge. If $L=0$ , also consider the vertex's own weight.

## Complexity and boundaries

Each component performs linear work, and component sizes sum to $O(n)$ per level. Total time is $O(n\log(n+1))$ and space is $O(n)$ . Components of at most eight vertices directly enumerate original endpoint pairs. Traversal and scheduling are explicit; sums use 64-bit integers.

Handle singleton trees, zero-edge paths, all-negative weights, and missing admissible lengths. Output `-1061109568` only for missing answers; do not include sentinels in arithmetic.

## Asymptotic bounds and measured runtime

In the measurements, edge decomposition took about 0.959 seconds on a 300,000-vertex random tree, while centroid decomposition with a segment tree took about 0.407 seconds. At one million vertices the times were about 4.106 and 1.978 seconds. The program with the higher general worst-case bound is actually faster here. The trees and operations it processes explain much of this difference.

### The edge-decomposition method expands the tree being decomposed

The edge-decomposition method turns $n$ vertices into $2n-1$ vertices and $n-1$ edges into $2n-2$ edges. Cut selection and collection must visit dummy vertices and zero-length edges too. Only original vertices can be endpoints, but dummy vertices still participate in connectivity and propagation.

It also builds depth buckets on both sides, performs two monotone-window passes, propagates answers to original edges, and converts edge answers back to vertex answers. Its visit records occupy 32 bytes versus 24 in the centroid-decomposition method. Peak working sets in the baseline measurements were about 63.75 and 38.27 MiB respectively. This establishes a storage difference, not a direct measurement of cache behavior.

### The same input can favor one decomposition

A star gives the clearest example. Removing its center leaves only singleton components. The top-level depth is one, so segment-tree queries also take constant work. The centroid-decomposition method therefore performs $O(n)$ algorithmic work on this star family, rather than attaining its general $O(n\log^2(n+1))$ bound.

To remove the star center's high degree, the edge-decomposition method expands it into a dummy chain with attached leaves. Several balanced edge-decomposition levels are still needed. A shallow original tree does not imply that its expansion can be split into singletons in one round. This interaction between input shape and decomposition cannot be inferred from the ordering of two worst-case bounds alone.

| 300,000-vertex case | Edge-decomposition sum of component sizes | Centroid-decomposition sum of component sizes | Centroid maximum collected depth | Segment-tree query-loop iterations |
| --- | ---: | ---: | ---: | ---: |
| Star | 10,578,542 | 599,999 | 1 | 299,999 |
| Balanced binary tree | 10,586,647 | 4,906,621 | 18 | 10,773,528 |
| Random tree | 10,686,040 | 2,917,867 | 26 | 11,405,052 |

The component-size sum counts the complete component visited when finding each centroid or cut edge. A vertex is counted again in later rounds. Both versions include traversal before their small-component handling. This compares traversal volume directly, but is neither an instruction count nor a count of all pairing work. On the random tree, the edge-decomposition method count is about 3.66 times larger; on the star it is about 17.63 times larger.

The random-tree input is generated by attaching each new vertex to an existing parent and then relabeling. Its shallow depths do not establish the same behavior for every random-tree generator.

### The extra logarithm is often small too

The segment tree is indexed by current collected depth $D_c$ , so its query bound depends on $\log(D_c+2)$ . Length limits, empty windows, and small components reduce the executed work further. The random-tree run averages about 3.91 iterations per endpoint query, rather than the full original tree's maximum logarithmic depth each time. Deep chains with wide windows do increase the loop counts, but must still be compared with expansion and multiple linear passes in the edge-decomposition method.

The edge-decomposition method offers the better **general worst-case bound**. The centroid-decomposition method processes fewer states, shallow depth ranges on these shapes, and avoids some conversions. These are meaningful peer tradeoffs. The [operation-count record](../../../docs/performance-work-P1.json) verifies the work differences; without phase timings or cache profiling, no runtime percentage is assigned to individual causes. A fewfold size increase grows the extra logarithm slowly and may not offset these differences. Other shapes, windows, or platforms can still change the ordering.

### Deep chains and special tree shapes

Targeted inputs include combs, unequal spiders, subdivided binary trees, double brooms, recursive combs, wide windows, windows near powers of two and randomly relabeled chains. They increase depth ranges, decomposition levels or nonempty query counts, or change access order. Centroid decomposition with a segment tree remains faster on the measured inputs.

For a chain with edge-length range $[1,\lfloor(n-1)/3\rfloor-5]$, its runtime is about 0.58, 0.56 and 0.55 times the edge-decomposition runtime at 300,000, 600,000 and 1,200,000 vertices. Random relabeling slows both programs substantially; at 1,200,000 vertices, the relabeled chain still takes 8.143168 seconds for edge decomposition and 4.452477 seconds for the segment-tree method. The larger two sizes are performance experiments only.

On these inputs, the extra logarithm has not outweighed the constants from expansion, traversal and endpoint pairing. The measurements give no basis for excluding the segment-tree method by lowering the limit. This concerns the measured implementations, sizes and input families, not every tree or platform. Stress inputs: Codex (GPT-6). See [tree constructions and performance](../../../docs/树形构造与性能.md) for reproduction and full records.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
