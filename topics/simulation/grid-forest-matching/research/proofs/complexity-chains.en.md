# Matching in Four-Neighbor Grid Forests: Accounting Along Root-to-Leaf Paths

This note analyzes the [candidate-list program](../../std.cpp) and supplements the [general bound](../../complexity.en.md). Road trees may branch arbitrarily; the parameters below count leaves in the query tree or the road trees.

## Result and parameters

Let $T$ be **the last complete offset set for which at least one candidate survives**, rooted at the initial zero offset. Its induced graph is a tree that translates into the board. The new offset that eliminates all remaining candidates is excluded from $T$, as are offsets after a direct out-of-range clearing.

Let $L_T$ be its number of rooted leaves, taking $L_T=1$ for a singleton. For each road component $C$, let $\ell_C$ be its number of unrooted leaves, taking $\ell_C=1$ for a singleton. Let $N$ be the total number of road cells.

**Theorem.** The total number of candidate checks satisfies

$$
\boxed{W\le N+3(n-1)\sum_C|C|\min(L_T,\ell_C).}
$$

Thus, if the valid query tree has a constant number of leaves, or each road component has a constant number of leaves, then $W=O(nN)$ and the running time is $O(n^2+m+nN)\subseteq O(n^3+m)$. If $N=0$, then $W=0$ directly, without defining $T$.

Two concrete consequences are:

- If new query offsets extend a path from one endpoint, then $L_T=1$, so $W\le(3n-2)N$, even when the road trees branch arbitrarily.
- If the valid query tree is a path grown from an interior starting point in any interleaving of its two ends, then $L_T\le2$, so $W\le(6n-5)N$. The same bound holds when every road component is a path, improving the constant in the [earlier path-component proof](complexity-paths.en.md).

Both leaf parameters can be large in general forests, so this theorem does not yet remove the logarithm from the general upper bound.

## Successful points on one query root-to-leaf chain

Fix a destination road cell $v$. When a nonzero offset $p$ first appears and the entire current prefix is valid from start $v-p$, call this a successful hit at $v$. Let $H(v)$ count all such successes.

First consider only successful offsets on one query root-to-leaf path, and add the initial zero offset. Ancestor order along this path agrees with first-visit order, even if the actual walk visits other branches between these events.

Take four distinct selected points $a,b,c,d$ in this order.

### The first forbidden configuration

If $a+d=b+c$, the four points must be collinear.

Indeed, use the copies present when anchors $b$ and $d$ succeed. Their translated paths from $a$ to $b$ and from $c$ to $d$ both have endpoints $v+a-b=v+c-d$ and $v$. Uniqueness of paths in the road forest makes these segments translates of each other. Similarly, the paths from $a$ to $c$ and from $b$ to $d$ are translates.

These four segments form a closed walk in the query tree. Set $u=b-a$ and $w=c-a$, and give a directed edge $xy$ weight $\det(x,y)/2$. The closed walk has total weight $\det(u,w)$. A closed walk in a tree traverses every edge equally often in both directions, so its weight is zero and the four points are collinear. This is the area argument from the general proof, using paths already present when their respective anchors succeed.

### The second forbidden configuration

The equality $a+c=b+d$ is impossible, even for collinear points.

Otherwise $a-d=b-c$. In the successful copy for $d$, translate the outer query-chain segment from $a$ to $d$ to end at $v$. In the successful copy for $c$, do the same for the inner segment from $b$ to $c$. Both simple paths have exactly the same endpoints, namely $v+a-d=v+b-c$ and $v$. The unique path between these endpoints in the road forest forces their lengths to agree.

But the four points occur in order along one query chain, so the outer segment strictly contains the inner segment and is strictly longer, a contradiction.

Consequently, if these points form a nondegenerate parallelogram, the only possible diagonal-sum equality is $a+b=c+d$: the earliest two points must be opposite corners.

## Label horizontal distances by visit direction

Let $S$ consist of the selected successful points and the zero offset. Its bounding box has dimensions $h\times w$, where $h,w\le n$.

In each nonempty row containing $k$ points, pair the leftmost point with each of the other points. This gives $k-1$ distinct positive horizontal distances. Label each distance by visit direction: positive if the left endpoint appears first, negative if the right endpoint appears first.

**The same distance with the same visit direction cannot occur in two rows.** Otherwise the two endpoint pairs form a nondegenerate parallelogram. Since both pairs visit their left endpoint first, or both visit their right endpoint first, the earliest two endpoints cannot be opposite corners, contradicting the preceding result.

There are at most $w-1$ positive distances, each with two visit directions, and at most $h$ nonempty rows. Therefore

$$
|S|\le h+2(w-1)\le3n-2.
$$

Removing the added zero offset shows that **each query root-to-leaf chain contributes at most $3n-3$ successful hits at a fixed destination**. Exchanging the coordinates also gives the point-count bound $\min(h+2w,2h+w)-2$.

## Group by query leaves

Assign every nonroot vertex of $T$ to one of its descendant leaves. Each group lies on the corresponding root-to-leaf chain, and every successful offset is assigned once. Add the zero offset to each group and apply the count above to obtain

$$
H(v)\le3(n-1)L_T.
$$

A singleton template has no successful new offsets. For $n=1$, the right-hand side is also zero.

## Duality: grouping only by road leaves also works

Root the road component containing $v$ at $v$, and let $L_v$ be its number of rooted leaves. Assign each original successful start $a=v-p$ to a host root-to-leaf path $R$ containing it.

Fix one such $R$. Exchange the roles of the two trees: use the final valid query tree $T$ as a new host, and follow $R$ outwards from $v$ as a new single-ended path query. At road vertex $x$, the new query offset is $q=x-v$.

For any original start $a$ in this group, choose new start $p=v-a$. When the new query reaches $a$, its translated complete prefix is

$$
R[v,a]-v+p=R[v,a]-a.
$$

The original success guarantees that this is exactly the path from $p$ to the zero offset in the original query tree, so it is entirely contained in $T$. The new query therefore successfully hits the zero offset when $q=a-v$. These events are reordered by depth along $R$; they do not depend on their original visit order.

$T$ translates into a board of the same size, so it is a valid new road tree. Each group satisfies the single-ended path bound already proved. Hence

$$
H(v)\le3(n-1)L_v,
\qquad
H(v)\le3(n-1)\min(L_T,L_v).
$$

The two trees give separate leaf-based bounds; their leaf counts need not be multiplied.

## Total checks

Each start fails at most once, so failed checks total at most $N$. Sum successful checks by destination. Every rooting of a component $C$ has at most $\ell_C$ rooted leaves, yielding

$$
W\le N+\sum_{v\in F}H(v)
\le N+3(n-1)\sum_C|C|\min(L_T,\ell_C).
$$

The final filter that empties the list has no successful checks and is covered by the failure term. Direct out-of-range clearing adds no candidate checks. Revisits to old offsets only affect the input length $m$. This proves the theorem.

## Charge short branches to ancestor vertices

There is an additional bound when the leaf count is large. Choose a connected subtree $K$ of $T$ containing the root, with $b$ rooted leaves. For each vertex $p$, let $\pi(p)$ be the last vertex of $K$ on the path from the root to $p$. Set

$$
\mu=\max_{q\in K}|\{p\in T:\pi(p)=q\}|.
$$

Then

$$
\boxed{W\le\mu[1+3(n-1)b]N.}
$$

**Proof.** Represent every successful check by a pair $(a,p)$, and add all $N$ initially valid pairs $(a,0)$. If there are $S$ successful checks, this set has size $N+S$. Since at most $N$ checks fail, we have $W\le N+S$.

Map $(a,p)$ to $(a,\pi(p))$. If $\pi(p)=p$, the pair is unchanged; otherwise the connected query prefix must visit this proper ancestor first. Thus the image pair is also valid and occurs no later than the original pair. Each image has at most $\mu$ preimages. If $S_K$ counts nonzero successful checks whose offsets lie in $K$, then

$$
N+S\le\mu(N+S_K).
$$

Assign the vertices of $K$ to its $b$ root-to-leaf chains. The earlier chain count gives $S_K\le3(n-1)bN$, proving the result. This argument uses the complete prefixes of the original query; it does not replace that query with a traversal of $K$ alone.

If every vertex has tree distance at most a nonnegative integer $r$ from its ancestor projection, all preimages of a given $q$ lie in the Manhattan ball of radius $r$ around it. Consequently,

$$
\mu\le B_r=2r^2+2r+1,\qquad
W\le B_r[1+3(n-1)b]N.
$$

This allows $T$ to have many leaves, provided its branches outside a subtree with few root-to-leaf paths are sufficiently short.

## Host trees with bounded branches beside a main path

Suppose each road component has a path $R$ such that every vertex in the component has tree distance at most $r$ from $R$. Then every query satisfies

$$
\boxed{W\le(2r^2+2r+1)(6n-5)N.}
$$

It suffices to find the subtree $K$ from the previous section with $b\le2$ and the same distance bound $r$. Take a valid embedding of the final query tree, write $z$ for its root, and call the embedded subtree $Q$.

- If $Q$ intersects the host path $R$, their intersection is a path segment. Take this segment together with the path connecting $z$ to it as $K$. Rooted at $z$, $K$ has at most two leaves. For every query vertex $p$, its last root-path ancestor in $K$ lies on its path towards $R$, so the remaining distance is at most $r$.
- If $Q$ does not intersect $R$, it lies in one attached branch. Let $s$ be the vertex of $Q$ closest to $R$, and take the path from $z$ to $s$ as $K$. Every path from a query vertex towards $R$ goes through $s$, so the same distance bound holds. In this case $K$ has one rooted leaf.

The projection bound therefore applies with $b\le2$, without doubling the distance. Singleton components, singleton queries and $r=0$ are all covered.

For constant $r$, this gives time $O(n^2+m+nN)$. It goes beyond bounded leaf counts: a long serpentine main path can have $\Theta(n^2)$ single-cell leaves while still allowing $r=1$. General branches can be deep, so this additional bound still does not prove the cubic bound for every forest.

## Repeated horizontal markers share a complete prefix

Return to all successful displacements at a fixed target $v$, without restricting them to one query root chain. Include the initial zero displacement. In each row, draw distance markers from the leftmost point to every other point, recording whether the left endpoint was visited first. A given marker occurs at most once per row, but it can now repeat across rows.

For a collection of identical markers, write each pair in visitation order as $(e_i,f_i)$, with the earlier endpoint first. There is a fixed nonzero horizontal vector $\delta$ such that

$$
f_i-e_i=\delta.
$$

**Nesting lemma.** Their time intervals are pairwise strictly nested. To see this, suppose one pair's early endpoint comes first. If the intervals are disjoint or interleaved, the identity

$$
e_i+f_j=f_i+e_j
$$

makes the earliest and latest points sum to the other two points. The markers lie in different rows, so the parallelogram is nondegenerate, contradicting the first general temporal restriction above. The only possible order is

$$
\operatorname{time}(e_i)<\operatorname{time}(e_j)
<\operatorname{time}(f_j)<\operatorname{time}(f_i).
$$

Consequently, let $P$ be the actual complete query prefix just after the last early endpoint in this collection is visited. It contains every early endpoint and no late endpoint. Each candidate that later succeeds already matches this entire prefix, and

$$
a_i=v-f_i,\qquad a_i+e_i=v-\delta.
$$

Thus the early endpoints are static successful anchors of the same complete prefix at the same fixed target. The complete-prefix restrictions in the [general proof](../../complexity.en.md) apply. However, different distances may have different shared prefixes, so this does not yet give a total charging bound.

Moreover, each query path between a marker's endpoints translates, in its later successful copy, to the same host path, with endpoints $v-\delta$ and $v$. These query paths have identical direction words. They need not be edge-disjoint, so their costs cannot simply be assigned to separate unused branches.

Distance one has a stronger boundary case. Two adjacent successful displacements must be query parent and child, with the parent visited first. Let $w$ be the parent's root direction word, let $\varepsilon$ be the parent-to-child direction, and let $k$ be the word length. The two corresponding host starts are adjacent, and their tree distances to the fixed target differ by one. Uniqueness of the host path therefore requires

$$
w\varepsilon=\varepsilon w,\qquad w=\varepsilon^k.
$$

Hence this query edge lies on an initial straight ray from the root. Horizontal distance-one markers occur only in the root's row and cannot repeat across rows. At distance at least two, a single marker can repeat linearly many times in the square's side length. A global allocation of costs across different markers remains missing.
