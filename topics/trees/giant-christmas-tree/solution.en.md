# Giant Christmas Tree — Solution

Setter method: centroid decomposition for diameter maintenance under deletion. Codex (GPT-6): the reverse-time method, plus local Euler intervals, path operations, and iterative construction for the online method.

## Reverse the deletions

A lit edge changes only when it is first extinguished. Root the tree at vertex 1 and preprocess parents, depths, and binary-lifting LCA. Represent each parent edge by its deeper endpoint. A separate skipping disjoint set bypasses consecutive already-dark parent edges; initialize it to skip edges that start dark.

For query $u,v$ , find $w=\operatorname{LCA}(u,v)$ . From each endpoint, call `Find` and, while its depth exceeds that of $w$ , record its parent edge as first deleted by this query, then link it to `Find(parent)` . Each edge is recorded at most once. Test depth after jumping: the returned vertex may already be above $w$ .

Build the lit forest after all operations. Each component stores its size, diameter length, and two diameter endpoints. Process queries backward: **record the current global diameter before restoring edges first deleted by this query**.

## Merge component diameters

For endpoint pairs $(a,b)$ and $(c,d)$ , compare the two old diameters and four cross distances $d(a,c),d(a,d),d(b,c),d(b,d)$ . Depths and LCA give each distance in $O(\log N)$ . Once the components are joined, their unique path in the full tree lies entirely in the new component.

The needed lemma is that, for any diameter endpoints $a,b$ , a farthest vertex from any $z$ can be chosen from $a,b$ . Project vertices onto the diameter of length $D$ . If $x$ projects to coordinate $s$ at height $h$ , maximality of the diameter gives $h\le\min(s,D-s)$ . If $z$ projects to $t$ at height $h_z$ , then $d(z,x)\le h_z+|t-s|+h\le h_z+\max(t,D-t)$ , the maximum distance to the endpoints. Apply this lemma on each side of the connecting edge to obtain the four sufficient cross candidates.

## Correctness

Skipping bypasses only edges already dark, so each query records exactly its newly dark edges. The final forest is correct. Restoring the edges first deleted by query $i$ takes the forest from the state after query $i$ to the state after query $i-1$ ; initially dark edges are never restored. The merge lemma preserves every component diameter. Reverse processing only adds edges, so the global maximum can only increase. Induction proves every recorded answer.

## Complexity and Contributions

Preprocessing, at most $N-1$ merges, and $M$ LCA queries take $O((N+M)\log N)$ time and $O(N\log N+M)$ space. The skipping structure uses path compression, and explicit traversal sequences avoid recursion on deep chains.

Codex (GPT-6) supplied this offline reverse-time method and [std.cpp](std.cpp). The setter's centroid-decomposition idea for deletion and diameter maintenance is retained as the [online alternative](solution-alternative.en.md). Both implementations use and verify the current input specification.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
