# Matching in a Four-Neighbor Grid Forest: Charging Long Branches

This note analyzes the existing candidate-list algorithm. The general bound remains $O(n^2+m+nN\log(n+1))$. We give an additional bound in terms of the distribution of branches, extending the cases with a proved cubic bound. Here $N$ is the number of road cells and $W$ counts actual candidate checks, both successful and failed. Repeated offsets and direct clearing on an out-of-range offset do not add to $W$.

**Current status:** The actual complete-prefix periodic family in the final section disproves both the per-pair and aggregate proposals for paying all repeated markers from historical third-arm capacity. The deletion-time lemma, short-arm windows, and reductions with an explicit remainder remain valid. The general complexity question is still open.

## Results

For a vertex $x$ in a road component $C$, consider each incident direction and the greatest tree distance from $x$ reachable in that direction. Sort these directional heights in decreasing order, and let $t_C(x)$ be the third height, or zero if there are fewer than three directions. For an integer $r\ge1$, write

$$
b_r(C)=|\{x\in C:t_C(x)\ge r\}|,
\qquad \beta_s=2s^2+2s+1.
$$

Then every query satisfies

$$
\boxed{W\le\beta_{r-1}(6n-5)N+\sum_C |C|b_r(C).}
$$

In particular, let $B_C$ count the vertices of degree at least three in a component. Then

$$
\boxed{W\le(6n-5)N+\sum_C |C|B_C.}
$$

Thus, if each road component has $O(n)$ branching vertices, branches of any length and any query order take $O(n^2+m+nN)$ time. More generally, the same conclusion holds if there is a fixed constant $r$ such that each component has only $O(n)$ vertices from which three separate directions each extend at least $r$ steps.

The total branch depth also satisfies

$$
\sum_{r\ge1}b_r(C)=\sum_{x\in C}t_C(x)\le |C|-1.
$$

These parameter bounds do not yet remove the logarithm for general forests.

## After the first branch appears

First consider $r=1$. Let $T$ be the last complete query tree with any surviving candidate. An offset that finally makes every candidate fail is excluded from it.

During the growth of $T$, take the first time a vertex has degree at least three, and call this vertex $q$. The complete prefix before that time is a path, possibly rooted in its interior. By the [root-to-leaf chain proof](complexity-chains.en.md), this first part contributes at most $6n-6$ successful hits to each target road cell $v$.

Starting with this round, including the round itself, if the start $v-p$ succeeds at a new offset $p$, its entire current prefix lies on roads. In particular, $q$ and its three already visited incident edges map to

$$
v+q-p.
$$

This is a branching vertex in the component containing $v$. Distinct new offsets $p$ map to distinct vertices. Hence the remaining hits to $v$ number at most $B_C$. If the effective query never branches, this second part is empty. Therefore

$$
H(v)\le6n-6+B_C.
$$

Each start can fail only once, so there are at most $N$ failed checks. Summing over targets gives the second boxed bound. We fix the three edges already visited at the first branch; other query branches need not be completed.

## Three long arms and distance from a diameter

In a tree, a tripod of length $r$ centered at $x$ consists of three simple paths of length $r$ that share only their center. It exists exactly when $t(x)\ge r$.

Take any diameter path $D$ of the tree. The following equality holds:

$$
\max_{p}\operatorname{dist}(p,D)=\max_x t(x).
$$

**First direction.** Suppose $p$ is at distance $d$ from $D$, with attachment point $q$, and let $u,w$ be the diameter endpoints. The path from $p$ to either endpoint is no longer than the diameter, so

$$
d\le\operatorname{dist}(q,u),\qquad
d\le\operatorname{dist}(q,w).
$$

For $d>0$, the three directions from $q$ towards $p,u,w$ all extend at least $d$ steps, giving $t(q)\ge d$.

**Second direction.** A simple path can enter at most two arms of a tripod. If it avoids the center, it lies entirely in one component after the center is removed. In either case, some arm of length $t(x)$ has its endpoint at distance at least $t(x)$ from the path. Applying this to $D$ proves the other direction.

Consequently, if a tree contains no tripod of length $r$, every vertex is within tree distance $r-1$ of any diameter path.

## Split at the first tripod of the chosen length

Take the first time the effective query contains a tripod of length $r$, and fix this tripod and its center $q$. The second part starts with and includes this round. If no such time exists, the entire effective query is the first part and the second part is empty.

The last complete query tree of the first part has no such tripod, so it is within distance $r-1$ of a diameter path. Take that path together with the connection from the query root as a core. Rooted at the query root, the core has at most two leaves. Every vertex is still within distance $r-1$ of its last core ancestor.

Apply the [short-branch projection proof](complexity-chains.en.md). If the first part has $S_{\mathrm{early}}$ successful checks, then

$$
N+S_{\mathrm{early}}\le\beta_{r-1}(6n-5)N.
$$

We retain the $N$ initial pairs here: the projection proof directly bounds initial pairs plus successful pairs, rather than only actual checks.

In the second part, each offset $p$ that successfully hits $v$ maps the fixed complete tripod into the road component. Thus $v+q-p$ satisfies $t_C(v+q-p)\ge r$. Distinct new offsets again give distinct images, so there are at most $b_r(C)$ such hits to $v$. Adding at most $N$ failed checks gives

$$
W\le N+S_{\mathrm{early}}+\sum_C |C|b_r(C)
\le\beta_{r-1}(6n-5)N+\sum_C |C|b_r(C).
$$

Empty road graphs, singleton components, and singleton queries all satisfy the bound. Direct clearing adds no checks. The final all-failing round is paid for by the failure term and need not be included in the effective query tree.

We can also split checks by the component containing the start. For each component, use the last prefix with a surviving candidate in that component and choose its threshold independently. This gives

$$
W\le\sum_C |C|\min_{r\ge1}\{\beta_{r-1}(6n-5)+b_r(C)\}.
$$

We apply the proof separately and then sum; the split times may differ between components.

## A budget for all branch depths

Choose any root in a road component. At each vertex with children, select a child giving the greatest downward height and call its edge heavy; call the other child edges light.

If $t_C(x)>0$, at least two child directions have height at least $t_C(x)$, since at most one of the three long directions is the parent direction. We can therefore select such a light child edge, take it from $x$, and then follow heavy edges for a total of $t_C(x)$ steps.

The paths chosen for different $x$ have disjoint edges. Their first edges are distinct light edges, and the remainder of each path lies in the heavy chain entered by its first edge. A heavy chain has only one incoming light parent edge. Paths may share endpoints, but cannot share edges.

Charging these paths to the $|C|-1$ edges of the component gives

$$
\sum_x t_C(x)\le |C|-1.
$$

Counting by height gives the budget equality stated above, and also $b_r(C)\le(|C|-1)/r$. Substituting this coarse bound into the main theorem does not improve the existing general logarithmic bound. Its use is to describe further cases with a cubic bound and to support further study of whether different depths can share a charge.

## Balanced attachments outside an already visited connected subtemplate

Subsequent successful checks can be charged to third-longest host arms without multiplying by the longest attachment length. Let $T$ be the last valid query tree, and let $S_{\mathrm{early}}$ count all successful checks before a chosen cut. Select a nonempty connected subtemplate $P\subseteq T$ whose vertices have all been visited by then. It need not equal the entire visited prefix or contain the query root.

After deleting the subtemplate, every remaining component attaches to it through a unique edge. For $q\in P$, let $B_q$ be the union of points attached through it, excluding the attachment vertex itself. Define

$$
L_q=\max_{x\in B_q}\operatorname{dist}_T(q,x),\qquad
V_q(r)=|\{x\in B_q:\operatorname{dist}_T(q,x)\le r\}|.
$$

Empty attachments require no conditions. For each nonempty attachment, assume two different directions within the subtemplate each extend at least $L_q$ steps from its attachment vertex. Also assume, for every positive integer radius,

$$
V_q(r)\le\lambda r.
$$

Each of the two direction heights must suffice individually; their sum is not enough. Write $h_P,w_P$ for the subtemplate's bounding-box height and width, and let

$$
b(P)=h_P+w_P-1\le2n-1.
$$

If the road forest has $c$ nonempty components, successful checks after the cut satisfy

$$
\boxed{
S_{\mathrm{tail}}
\le\lambda b(P)\sum_{z\in F}t_F(z)
\le\lambda b(P)(N-c).
}
$$

Every start fails at most once over the entire run, so

$$
\boxed{
W\le N+S_{\mathrm{early}}+\lambda b(P)(N-c).
}
$$

The early term must include every success before the cut, including previously visited points outside the subtemplate. The failure term is added only once.

### Charge each candidate and attachment vertex once

Fix a candidate start and attachment vertex $(a,q)$. If it has a later success in this attachment, let $s$ be its maximum successful depth. At that success, the complete actual prefix contains the whole subtemplate. The visited set is connected and the final query is a tree, so it also contains the entire path from the attachment vertex to the successful point.

After translation, the host point $z=a+q$ has three paths meeting only at their center. Two come from the visited subtemplate and each has length at least $L_q\ge s$; the third comes from the attachment and has the maximum successful depth. Hence

$$
s\le t_F(a+q).
$$

All subsequent successful points of this candidate in this attachment lie in the depth ball. Their total contribution is therefore at most

$$
V_q(s)\le\lambda s\le\lambda t_F(a+q).
$$

This uses one actual historical success certificate. Later candidate deletion does not invalidate it, and arbitrarily many interleaved visits do not create repeated charges.

Now fix a host point. Each possible attachment vertex uniquely determines the candidate start, and that candidate has already matched the entire subtemplate. Define all legal translations by

$$
\mathcal A(P)=\{a\in\mathbb Z^2:a+P\subseteq F\}.
$$

The corresponding attachment vertices belong to the static anchor set of a fixed complete template,

$$
\{q\in P:z-q\in\mathcal A(P)\},
$$

whose size is at most $b(P)$. The subtemplate need not contain the original query root: translate any of its points to the origin, preserving the anchor count and bounding box. Sum over host points and use the total third-arm budget to obtain both boxed bounds.

If attachment vertices have different growth rates, the weighted form is

$$
S_{\mathrm{tail}}
\le\sum_{z\in F}t_F(z)
\sum_{\substack{q\in P\\z-q\in\mathcal A(P)}}\lambda_q.
$$

Vertices with no remaining attachment may use growth rate zero. This still fixes one subtemplate; it does not settle resource reuse when the subtemplate changes.

## Complete a diameter before growing path attachments in any order

The tail bound gives a cubic subclass without restricting attachment length. Suppose the final valid query tree has a diameter path $P$, and every component left after deleting it is a path. The query root may be anywhere. Require the walk to finish the diameter and the necessary connecting path from the root before visiting any other points. Subsequent path attachments may grow in any interleaving.

The diameter property supplies height balance. With endpoints $u,v$, an attached point at depth $s$ satisfies

$$
s+\operatorname{dist}_P(q,u)\le |E(P)|,\qquad
s+\operatorname{dist}_P(q,v)\le |E(P)|.
$$

Thus each diameter arm is at least as long as the attachment depth.

We can also use $\lambda=2$ uniformly, even if the connecting edge enters the interior of a path component:

- With one attached component, a depth ball has at most $2r-1$ points.
- With two attached components, the attachment vertex has road degree four. A side turn at either entrance would form a unit four-cycle with another occupied neighbor of the attachment vertex. Each entrance must therefore be an endpoint of its path component. Each component contributes at most $r$ points.

The actual early visited set is the diameter plus the root's connecting path. Rooted at the original query root, it has at most two leaves. The chain bound gives at most $6(n-1)N$ early successes. The tail is still charged using the original diameter as the subtemplate. When the root is outside it, any remaining path beyond the root is assigned to its attachment on the diameter; the root is not incorrectly treated as a charging center with only one core arm. Combining the bounds gives

$$
\boxed{
W\le N+6(n-1)N+2(2n-1)(N-c)
\le(10n-7)N.
}
$$

This query class therefore takes $O(n^2+m+nN)$ time in any road forest. Both the diameter and its attachments may bend, and attachment lengths need not have a constant bound. Completing the specified connecting path and diameter first remains essential: this proof does not pay for work before both full arms are available.

## Scope of the fixed-subtemplate bound

For one fixed subtemplate, the tail may be split into any number of batches; maximum successful depth is counted once. With general branching, a batch's new points cannot simply be bounded by the growth rate times the increase in maximum depth, since another branch's shallow points may be filled later. The whole-ball count above avoids this problem.

The growth-rate condition cannot be dropped. A balanced attachment can contain quadratically many comb points while its height and width grow only linearly. Sending all of them to one attachment vertex leaves only a linear third-arm length and cannot pay the cost. A general proof must use internal branch resources and control repeated use of new attachment anchors when the subtemplate expands. The logarithmic gap for general forests remains open.

## Diameter and branching costs under arbitrary orders

Continue to assume that deleting a diameter $P$ from the final valid query tree $T$ leaves path components, but now allow any root and any connected discovery order. The argument below pays for all branching cost and leaves a diameter term that is still uncontrolled.

For each initial candidate $a$, let $T_a$ be its last successfully matched complete prefix; use the singleton tree if its first new point fails. If $S$ is the number of successful checks, then

$$
S=\sum_a(|T_a|-1),\qquad W\le N+S=\sum_a|T_a|.
$$

### Decomposing the size of a tree

For any finite tree $R$ of maximum degree at most four, write $d_R(q)$ for its degrees and $D(R)$ for its diameter in edges. Then

$$
\boxed{|R|-1\le D(R)+\sum_{q\in R}(d_R(q)-2)_+t_R(q).}
$$

Here $(x)_+=\max(x,0)$. Root the tree at one endpoint of any diameter. On the diameter, choose the child edge toward the other endpoint as heavy; elsewhere choose a child of maximum downward height. All other child edges are light.

The diameter property ensures that each nonroot vertex's parent direction is at least as tall as every light child direction. For a point outside the diameter, let $s$ be its distance to the diameter, let $A,B$ be the distances from its projection to the two endpoints, and let $h$ be the height of a child direction. Then

$$
s+h\le\min(A,B),
$$

while the parent direction has height at least $s+\max(A,B)$. On the diameter itself, use the balance between its two arms directly.

Each light edge followed by its heavy chain forms a path whose length is exactly the height of that light child direction. This length is at most the third direction height of its parent, since the parent and heavy child directions are also at least that tall. These paths partition the edges outside the diameter. Each vertex has at most $(d_R(q)-2)_+$ light child edges, proving the boxed inequality. The singleton case also holds.

### Multiplicity of historical anchors

Let $B=6n-5$. For a fixed host point $z$, there are at most $B$ historical pairs satisfying

$$
q\in P\cap T_a,\qquad a+q=z
$$

Indeed, the diameter together with the path from the original root to it has at most two rooted leaves. Its diameter points lie on two original root chains. Each chain has at most $3(n-1)$ noninitial successes at a fixed target, with at most one initial pair added. This uses each candidate's actual successful prefix and does not require a complete diameter match.

A branch vertex outside the diameter can only be an internal entry point $e$ of a path component. It has degree three and is adjacent to a unique diameter point $q$. If $t_{T_a}(e)>0$, all three neighbors belong to that successful prefix, so the diameter neighbor has also succeeded. Split these pairs into the four unit directions $e-q$. Each class injects into the historical diameter pairs at target $z-(e-q)$. Thus there are at most $4B$ such entry pairs at a fixed host point.

Apply the size inequality to every candidate. The coefficient is at most two on the diameter and at most one at an external entry, and

$$
t_{T_a}(q)\le t_F(a+q).
$$

Consequently,

$$
W\le N+\sum_a D(T_a)+6(6n-5)(N-c).
$$

If every path component attaches to the diameter at an endpoint, there are no external internal entries, and the coefficient six can be replaced by two.

### Which actual checks form the diameter term

Let $T_i$ be the complete prefix after the $i$-th valid new displacement. Adding one leaf increases the diameter by zero or one. Define

$$
\Delta_i=D(T_i)-D(T_{i-1})\in\{0,1\},\qquad
S_D=\sum_{i:\Delta_i=1}|A(T_i)|.
$$

This uses the candidate count after filtering, so it counts successful checks. Interchanging the sums over candidates and rounds gives the exact identity

$$
\sum_aD(T_a)=\sum_i\Delta_i|A(T_i)|=S_D.
$$

We obtain the following rigorous reduction for arbitrary discovery orders:

$$
\boxed{W\le N+S_D+6(6n-5)(N-c).}
$$

If all path components attach at their endpoints, then

$$
\boxed{W\le N+S_D+2(6n-5)(N-c).}
$$

Root height is another option. Let $H(T_i)$ be the greatest tree distance from the original root, and let $S_H$ count successful checks when a new root depth is first reached. The same argument gives

$$
\sum_aH(T_a)=S_H,\qquad S_D\le2S_H.
$$

An $O(nN)$ bound on either record total would remove the order requirement for the preceding query class. That term is still uncontrolled: the tree diameter can be $\Theta(n^2)$, and record points can switch between different root chains. This reduction does not prove the cubic bound for arbitrary orders. Failures are still counted only once, and the final all-failing point and revisits are handled as above.

## Completing a local fork does not simplify the general local-hit problem

For any actual execution, let $J(z)$ count historical pairs with the following properties: the center $q$ is a branch vertex of the final query, the last successful prefix of candidate $a$ contains that center and at least three neighbors, and $a+q=z$. Write $H(v)$ for the ordinary local success count. Clearly,

$$
J(z)\le H(z)+1.
$$

There is a reduction in the other direction with constant scale. Set

$$
C=\{(0,0),(1,0),(-1,0),(0,1),(0,-1)\},\qquad
F^\star=\bigcup_{x\in F}(3x+C).
$$

Replace each original point by a five-point cross. Crosses of nonadjacent original points are at least four steps apart; those of adjacent points have exactly one unit edge between them. Each original edge becomes a three-step corridor, and directions missing at an original center become new leaves. The resulting graph is still an induced forest, with

$$
N^\star=5N,\qquad |E(F^\star)|=5N-c,\qquad n^\star\le3n.
$$

Truncate the original query at its last valid prefix, then replace each step by three steps in the same direction. At the initial center and at every newly reached center, first take one step in each of the four unit directions and return. If the truncated walk has length $m_0$ and visits $k$ different points, the new continuous walk has length

$$
m^\star=3m_0+8k.
$$

Candidate $3a$ completes a new query block if and only if candidate $a$ matches the corresponding old prefix. The forward construction uses the valid crosses and corridors. Conversely, a road point whose two coordinates are divisible by three must be a cross center. Whenever that center is valid, its four neighbor excursions are valid too.

Thus every original successful pair becomes a center pair whose four neighbors have all been matched, while preserving the fixed target:

$$
(a,p)\longmapsto(3a,3p),\qquad
J_{F^\star}(3v)\ge H_F(v).
$$

Consequently, proving $J(z)=O(n)$ for all instances is equivalent up to constant scale to proving the general bound $H(v)=O(n)$. A complete local fork certificate may still be useful, but adding it alone does not make this local problem easier. Neither general local bound is currently proved.

## Repeated horizontal markers among root-height records

There is also a strict structural consequence of the order of record depths. Fix a road target $v$. A successful root-height record is a new query offset $p$ that first reaches a previously unseen depth from the query root and succeeds for start $v-p$. The root $p=0$ may be included as an initial record, adding at most one point.

Take pairs $(e_i,f_i)$ whose endpoints are successful root-height records for this same target, with $e_i$ discovered before $f_i$, and with

$$
f_i-e_i=\delta
$$

equal to one fixed nonzero horizontal vector. This fixes both the length and the visit direction. Different pairs must lie in different query rows. The existing temporal parallelogram prohibition rules out disjoint or crossing time intervals, so the intervals are strictly nested. Numbering them from outermost to innermost gives

$$
e_1<e_2<\cdots<e_r<f_r<\cdots<f_2<f_1,
$$

where the inequalities denote first-discovery times.

Put $a_i=v-f_i$ and $w=v-\delta$. When the later endpoint succeeds, start $a_i$ matches the complete actual prefix containing both endpoints. The query paths $e_i\to f_i$ therefore all translate to the same unique host path

$$
R=F[w,v],\qquad \ell=|E(R)|.
$$

This uses complete-prefix success and uniqueness of paths in a forest. Equal endpoint displacement alone would not imply equal paths.

### Projection positions must move strictly forward

Root the query at its original root and write

$$
q_i=\operatorname{LCA}_T(e_i,f_i),\qquad
x_i=\operatorname{dist}_T(e_i,q_i),\qquad
s_i=\operatorname{depth}_T(q_i).
$$

Then

$$
\operatorname{depth}_T(e_i)=s_i+x_i,\qquad
\operatorname{depth}_T(f_i)=s_i+\ell-x_i.
$$

Record depths strictly increase with time. Two consecutive nested intervals give

$$
s_i+x_i<s_{i+1}+x_{i+1},\qquad
s_i-x_i>s_{i+1}-x_{i+1}.
$$

Hence

$$
\boxed{x_{i+1}-x_i>|s_{i+1}-s_i|.}
$$

All quantities are integers. Summing the individual inequalities also bounds the total variation of the root-arm lengths:

$$
\sum_{i=1}^{r-1}|s_{i+1}-s_i|
\le x_r-x_1-(r-1).
$$

Within each pair, the earlier endpoint has smaller depth than the later one, so $\ell-2x_i>0$. Using integrality yields

$$
\boxed{0\le x_1<x_2<\cdots<x_r\le
\left\lfloor\frac{\ell-1}{2}\right\rfloor,
\qquad r\le\left\lceil\frac\ell2\right\rceil.}
$$

Let $z_i=a_i+q_i$. The complete successful prefix also contains the path from the root to $q_i$, which meets $T[e_i,f_i]$ only at $q_i$. Thus $z_i$ is the projection of host start $a_i$ onto $R$, with

$$
\operatorname{dist}_F(w,z_i)=x_i,\qquad
\operatorname{dist}_F(a_i,z_i)=s_i.
$$

The projections move strictly along the common path from $w$ towards $v$ and remain in the half closer to $w$. The root-arm lengths $s_i$ themselves need not be monotone.

### Root arms are disjoint within one marker family

Distinct projections are different vertices of $R$. After deleting $R$, each remaining road component can attach to only one path vertex, since two attachments would create a cycle. The root arms $F[a_i,z_i]$ consequently have disjoint edges. Their half-open vertex sets $[a_i,z_i)_F$ are also pairwise disjoint and outside $R$. Each such set includes its starting vertex, excludes its projection endpoint, and contains exactly $s_i$ vertices; it is empty when $s_i=0$.

If $C$ is the road component containing $R$, then

$$
\boxed{\sum_i s_i\le |C|-|V(R)|=|C|-\ell-1.}
$$

When $x_i>0$ and $s_i>0$, the projection vertex has three distinct arms of lengths at least $x_i$, $\ell-x_i$, and $s_i$. Thus

$$
t_F(z_i)\ge\min\{x_i,s_i\}.
$$

At most one marker can have $x_i=0$. Several may have $s_i=0$, and this latter case cannot be paid for directly by third-longest arms.

These statements concern one family with a fixed target, a fixed horizontal vector, and different query rows. Such a family already has at most $n$ members, while the path length $\ell$ can be $\Theta(n^2)$. Different marker families and different targets can reuse the same root arm, and no global multiplicity bound is known here. The single-family budgets therefore cannot simply be summed over all markers, and they do not yet prove $S_H=O(nN)$.

## A comb whose height records require arbitrarily many root chains

Take integers $k,H\ge1$, use row and column coordinates, and let both the query and host be the following induced tree, rooted at its upper left endpoint:

$$
F=Q=\{(0,c):0\le c\le2k\}
\cup\{(t,2i):1\le t\le H,\ 0\le i\le k\},\qquad r=(0,0).
$$

An empty column separates consecutive vertical teeth, and only the spine connects them, so there are no extra adjacencies or cycles. Visit each tooth to its tip from left to right, returning to the spine before continuing, and stop at the rightmost tip. Every discovery prefix retains the original root as a valid reference candidate. The vertex count, square size, and actual walk length are

$$
N=2k+1+(k+1)H,\qquad n=\max(2k+1,H+1),\qquad
m=2k+(2k+1)H.
$$

Fix the target $v=(H,2k)$. Every point on the first tooth is a height record, and its current vertical prefix can be translated to the end of the rightmost tooth. Each later tooth tip is also a record; its entire current prefix translates to a rightmost subcomb of the host. No other record hits this target: sending an internal point of a later tooth, or a spine point, to the target would move the already completed first tooth below the bottom row. Therefore

$$
H_H(v)=H+k,\qquad
\text{minimum root-chain cover}=k+1.
$$

The second equality follows because the tooth tips are pairwise incomparable, while each path from the root to a tooth tip covers the records on that tooth. Thus a fixed number of original root chains cannot always cover the height records.

Exact counting is also direct. Along the first tooth, each additional step reduces the survivor count by the number of teeth. Each later odd-column spine discovery removes the rightmost candidate; no further candidate is removed before that tooth is completed. Each later block has exactly two height records, including when the teeth have length one. Summing these blocks gives

$$
\begin{aligned}
W&=N+(k+1)\left(\frac{H(H+1)}2-1\right)
 +(H+2)\frac{k(k+1)}2+k,\\
S_H&=(k+1)\frac{H(H+1)}2+k(k+1).
\end{aligned}
$$

Setting $H=2k$ gives

$$
\begin{aligned}
n&=2k+1,&N&=2k^2+4k+1,&m&=4k^2+4k,\\
W&=3k^3+7k^2+6k,&S_H&=2k(k+1)^2,&H_H(v)&=3k.
\end{aligned}
$$

Hence the record success count itself can be $\Theta(nN)=\Theta(n^3)$, and the local record count divided by the square size tends to $3/2$. These are cubic and linear lower bounds; they do not exceed the conjectured upper bounds. The general record total remains unresolved.

## Assign repeated record markers to actual branching pairs

The following exact reduction does not require completing a diameter first. Records that cannot be paid for by row and horizontal-label counts are assigned to branches in actual successful prefixes. The number of charges assigned to one pair is still uncontrolled, so this is not a general cubic proof.

### First-child groups and earliest row centers

Let $T$ be the last valid query tree. Fix a target $v\in F$, and let $S_v$ be its successful root-height records, excluding the initial root. Each record requires start $v-p$ to match the complete actual prefix when the point is discovered. A final all-failing point contributes nothing to $S_H$, while repeated offsets are still counted only in the actual walk length $m$.

Partition the set into at most four groups according to the first child edge on the path from the original query root to each record. In every nonempty query row of each group, choose the earliest-discovered record $e$ as the center and create a marker to every other record $f$ in that row. Its label is the signed horizontal vector $\delta=f-e$.

The center is then always earlier than the other endpoint, and every noncenter record is the later endpoint of exactly one marker. Each group and row contributes at most one marker of a given label. Choosing the earliest record instead of the leftmost point prevents a late center from being the common later endpoint of several edges, which would count the same success repeatedly.

The valid query translates as a whole into the host, so it occupies at most $n$ rows. Each group has at most $2(n-1)$ possible nonzero signed horizontal vectors.

### Keep only the outermost marker free

Fix a group and a label. Its markers lie in different rows and have strictly nested time intervals. Keep only the outermost marker free and call the others charged markers. Let $R_v,L_v,C_v$ count the row centers, free markers, and charged markers at the target, respectively. Then

$$
|S_v|=R_v+L_v+C_v,\qquad
R_v\le4n,\qquad L_v\le8(n-1).
$$

Consequently,

$$
\boxed{H_H(v)=|S_v|\le12n-8+C_v.}
$$

For a charged marker $(e,f)$, define

$$
a=v-f,\qquad q=\operatorname{LCA}_T(e,f).
$$

It is an inner marker of its label, so the strict projection lemma above gives

$$
\operatorname{dist}_T(e,q)>0.
$$

Record depths increase strictly with time, so $q\ne f$. Both endpoints belong to the same first-child group, giving $q\ne0$. When the later endpoint succeeds, the candidate has matched the query root, both endpoints, and all paths between them. The charging vertex therefore already has its parent direction and two different child directions.

Let $T_a$ be the candidate's last successful prefix. This gives the actual historical certificate

$$
\deg_{T_a}(q)\ge3,\qquad
t_{T_a}(q)\ge
\min\{\operatorname{depth}_T(q),\operatorname{dist}_T(e,q)\}\ge1.
$$

Later candidate deletion does not invalidate the certificate. The first-child grouping excludes the case of a query root with only two directions, where no third arm would follow.

### Define the charging multiplicity exactly

Let $M(a,q)$ count charged markers, across all targets, assigned to the same candidate start and the same query LCA. Each later endpoint corresponds to an actual success $(a,f)$, whose target is uniquely determined by $v=a+f$. At that target, it is the later endpoint of only one marker. Thus no actual success is assigned to several charged markers.

By definition,

$$
\sum_v C_v=\sum_{a,q}M(a,q),
$$

and hence

$$
\boxed{S_H\le(12n-8)N+\sum_{a,q}M(a,q).}
$$

Nonzero multiplicities occur only at branches in actual candidate histories. The reduction so far applies to every query in an induced grid forest.

### The available capacity for the path-attachment subclass

Now suppose deleting a diameter $P$ from the final query leaves only path components. Let $c$ be the number of nonempty host components, and put $B=6n-5$. Define the historical capacity without a degree coefficient by

$$
\Psi=\sum_a
\sum_{\substack{q\in T_a\\\deg_{T_a}(q)\ge3}}
t_F(a+q).
$$

The dynamic anchor count gives

$$
\boxed{\Psi\le5B\sum_{z\in F}t_F(z)
\le5(6n-5)(N-c).}
$$

Pairs on the spine have multiplicity at most $B$ at a fixed host point: the diameter is covered by at most two original root paths, allowing one additional initial pair. An off-spine branch can only be an adjacent interior entrance of a path component. When that entrance becomes a prefix branch, its neighboring spine vertex has already succeeded. Splitting by the four entrance directions injects these pairs into historical anchor sets at neighboring points, for multiplicity at most $4B$.

The query root need not lie on the diameter, and the diameter need not have been completely matched at any earlier time. If every path attachment is joined at its endpoint, there are no off-spine interior entrances, and the coefficient five in the capacity bound becomes one.

One proposed capacity relation was the following, for an absolute constant $C$:

$$
\sum_{a,q}M(a,q)\le C\Psi,
$$

If it held, the reduction would prove $S_H=O(nN)$ for this subclass. However, the periodic family in the final section disproves this inequality and the stronger per-pair bound $M(a,q)\le C t_F(a+q)$. The third-arm certificates and preceding valid reductions remain useful, but they cannot pay all repeated charges across labels and targets.

## Deletion times and charges in short directions

This section retains the exact charging definition above. It controls all charges for which at least one endpoint direction is short. Charges between two long directions remain unresolved.

### Exact distances to the outer candidate root

Fix a target $v$, an inner charged marker $(e,f)$, and any outer marker $(e',f')$ of the same label. Their discovery times and displacements satisfy

$$
e'<e<f<f',\qquad f-e=f'-e'=h.
$$

The inequalities indicate first-discovery order. Here $h$ is a nonzero horizontal vector, and the markers lie in different rows. Define

$$
a=v-f,\qquad b=v-f',\qquad q=\operatorname{LCA}_T(e,f),
$$

$$
s=\operatorname{depth}_T(q),\qquad
x=\operatorname{dist}_T(q,e),\qquad
y=\operatorname{dist}_T(q,f),
$$

$$
D_e=\operatorname{depth}_T(e)-\operatorname{depth}_T(e')>0,\qquad
D_f=\operatorname{depth}_T(f')-\operatorname{depth}_T(f)>0.
$$

The two complete-prefix successes at the later endpoints make their translated endpoint paths the same host path $R$, with endpoints $v-h,v$ and length $\ell=x+y$. Write the corresponding outer LCA, root depth, and early-end distance as $q',s',x'$. The endpoint depth relations give

$$
x-x'=\frac{D_e+D_f}{2}>0,\qquad
s'-s=\frac{D_f-D_e}{2}.
$$

Put $z=a+q$ and $z'=b+q'$. These are the projections of the candidate roots onto $R$. The latter lies on the side of the former toward $a+e$, at distance $x-x'$. Root segments with distinct projections are disjoint and, except for their projections, lie outside the common path. Therefore

$$
\operatorname{dist}_F(a,b)=s+(x-x')+s'=2s+D_f,
$$

$$
\boxed{\operatorname{dist}_F(z,b)=(x-x')+s'=s+D_f.}
$$

In particular, $b$ lies in the direction component from $z$ toward the early endpoint. If the maximum height in that direction is $B_E$, then

$$
s+D_f\le B_E.
$$

These identities do not require the inner candidate to survive later.

### The inner late-end candidate is deleted before the outer late endpoint

This fact requires only the four relevant complete-prefix successes, without the additional height-record or earliest-center conditions.

Translate coordinates so that $a=0$, and write

$$
d=e-e'=f-f',\qquad h=f-e=f'-e'.
$$

The markers lie in different rows, so $d$ is nonhorizontal and $\det(d,h)\ne0$. Suppose instead that the zero candidate survives through $f'$. Let $P_p$ denote the full actual prefix when point $p$ is first discovered. The reference candidate, outer late-end candidate, and inner early-end candidate then give

$$
P_{f'}\subseteq F,\qquad
P_{f'}+d\subseteq F,\qquad
P_e+h\subseteq F.
$$

Take directed query paths $U:e'\to e$ and $V:e'\to f'$. Both belong to the reference prefix, and $U\subseteq P_e$. Thus the host contains all four paths

$$
U,\qquad V,\qquad U+h,\qquad V+d.
$$

They form the following closed walk:

$$
U,\quad V+d,\quad -(U+h),\quad -V,
\qquad e'\to e\to f\to f'\to e'.
$$

Their interiors need not be disjoint. For a directed path $L=(z_0,\ldots,z_k)$, define its area sum and translation identity by

$$
\mathcal A(L)=\sum_{i=0}^{k-1}\det(z_i,z_{i+1}),\qquad
\mathcal A(L+t)=\mathcal A(L)+\det(t,z_k-z_0).
$$

The area sum of the closed walk is therefore

$$
\mathcal A(U)+\mathcal A(V+d)-\mathcal A(U+h)-\mathcal A(V)
=\det(d,h)-\det(h,d)=2\det(d,h)\ne0.
$$

Every closed walk in a forest traverses each edge equally often in both directions, so its area sum must be zero. This contradiction proves deletion before the outer late endpoint.

The failure concerns the whole prefix. In fact, $a+f'$ is already a road point supplied by the early-end copy. Failure may occur at another earlier new point; the conclusion does not say that this single endpoint is absent. In particular, a candidate surviving the final valid prefix receives no charged markers.

### All outer markers share one final height window

Let $H_a$ be the original-root height of the candidate's last successful prefix $T_a$. The inner later endpoint succeeds, while the outer later endpoint is a subsequent global height record. Even if the first failure occurs at a nonrecord point, we still have

$$
\operatorname{depth}_T(f)\le H_a
<\operatorname{depth}_T(f')
=\operatorname{depth}_T(f)+D_f.
$$

Equivalently,

$$
H_a-D_f<\operatorname{depth}_T(f)\le H_a.
$$

Different charges may use different outer markers, but share the same $H_a$. If a collection of charges satisfies $D_f\le D$, it has at most $D$ charges: each global record depth has only one record point, and each later endpoint of a fixed candidate is charged only once. No additional factor for labels or centers is needed.

### Total charges involving a short direction

Fix a pair receiving charges and put

$$
z=a+q,\qquad t=t_F(z),\qquad s=\operatorname{depth}_T(q)\ge1.
$$

For each charge, let $B_E,B_F$ be the maximum heights in the two distinct child directions from this host point toward the early and late endpoints.

If $B_F\le t$, the late record depth belongs to $s+1,\ldots,s+t$, so all such charges together number at most $t$.

If $B_E\le t$, the exact root distance gives $1\le D_f\le t-s$. The common final window then bounds all such charges together by $\max(0,t-s)$, including multiple later endpoints associated with the same center.

Let $M_{\mathrm{LL}}(a,q)$ count only charges whose two directions are both strictly longer than the third arm, satisfying both $B_E>t$ and $B_F>t$. Adding the bounds for the first two classes gives

$$
\boxed{M(a,q)\le t+\max(0,t-s)+M_{\mathrm{LL}}(a,q)
\le2t+M_{\mathrm{LL}}(a,q).}
$$

A host vertex has at most two directions strictly longer than its third direction. All remaining charges therefore use the same pair of long directions, with at most two orientations. The query parent direction is short and already contains a root segment of length $s$, so

$$
M_{\mathrm{LL}}(a,q)>0\ \Longrightarrow\ s\le t.
$$

In particular,

$$
\boxed{\operatorname{depth}_T(q)>t_F(a+q)
\ \Longrightarrow\ M(a,q)\le t_F(a+q).}
$$

This classification applies to general queries. For the subclass whose components outside a diameter are paths, the short-direction charges sum to at most $2\Psi$ and are covered by the preceding capacity bound. A bound on the total $M_{\mathrm{LL}}$ remains unproved. This section does not treat that remainder as paid or claim a general cubic bound.

### The actual early arm further reduces the remainder

In the exact projection identity, $x'\ge0$, and the earlier record depth gap satisfies $D_e\ge1$. Hence

$$
D_f=2(x-x')-D_e\le2x-1.
$$

For a fixed pair, all charges with actual early-end distance $x\le t$ therefore lie within the last $2t-1$ height records, regardless of how much farther that host direction extends. Let $M_{x>t}(a,q)$ count only charges with a longer actual early arm. This gives another strict bound:

$$
\boxed{M(a,q)\le2t-1+M_{x>t}(a,q).}
$$

Its unresolved set is smaller; the preceding direction classification can still give a finer bound on the paid portion. Both actual child arms of each remaining charge exceed the third arm, so the parent direction is short. They satisfy

$$
s\le t<x<y.
$$

The total number of these remaining charges is still uncontrolled. The remainder cannot be dropped from the bound.

For the subclass whose components outside a diameter are paths, define the total remainder by

$$
R_{\mathrm{rem}}=\sum_{a,q}M_{x>t}(a,q),\qquad B=6n-5.
$$

The proved parts combine directly to give

$$
\sum_{a,q}M(a,q)\le2\Psi+R_{\mathrm{rem}},\qquad
S_H\le(12n-8)N+2\Psi+R_{\mathrm{rem}}.
$$

Substituting the preceding volume decomposition and capacity bound gives the following exact, unfinished charging reduction:

$$
\begin{aligned}
W&\le N+S_D+6B(N-c)\\
 &\le N+2S_H+6B(N-c)\\
 &\le (24n-15)N+4\Psi+6B(N-c)+2R_{\mathrm{rem}}\\
 &\le\boxed{(24n-15)N+26(6n-5)(N-c)+2R_{\mathrm{rem}}}.
\end{aligned}
$$

Thus all costs except the explicit total remainder are already cubic. A suitable bound on that remainder must still be proved or refuted to finish the arbitrary-order analysis of this query subclass. Processing the actual input moves remains an additional cost.

## A periodic counterexample to charging all markers to historical third arms

The following family retains actual complete prefixes and the exact earliest-center definition. For a multiple of three $H\ge12$, it has

$$
n=H+5,\qquad N=9H+14,\qquad |T|=6H+2,
$$

and a fixed candidate and query fork such that

$$
M(\widehat a,\widehat q)\ge\frac H3,\qquad
t_F(\widehat a+\widehat q)=3,\qquad \Psi=9.
$$

Deleting a query diameter leaves just one path of length three. The family therefore belongs to the path-attachment subclass considered above. It disproves both the per-pair and aggregate capacity proposals, but does not give a supercubic scan lower bound for the original algorithm.

### The query and its actual discovery order

Use geometric coordinates $(x,y)$, with north increasing the second coordinate. Put

$$
U=\mathsf N^H\mathsf E^2\mathsf S^{H-2}\mathsf E^2,
\qquad L=|U|=2H+2.
$$

This path word has displacement $(4,2)$. Take the spine vertex $q=(0,0)$, extend the positive side through a prefix of two copies of the word, and extend the negative side through a prefix of its inverse. Add the short attachment

$$
q\to(0,-1)\to r=(0,-2)\to(-1,-2),
$$

with original query root $r$. First visit the left leaf, then follow the root connector to the spine. Discover the remaining points in the following order, walking along the already visited tree whenever switching arms.

1. Extend the positive arm upward to $(0,H)$.
2. For $y=H-3,H-6,\ldots,3$, extend the negative arm to $e_y=(-4,y)$, then the positive arm to $f_y=(2,y)$.
3. Finally continue the positive arm to $(6,5)$ in the second period.

The final main path runs from $(-4,3)$ through the spine vertex to $(6,5)$, with side lengths $2H-3$ and $4H+1$. It is a diameter, with only the short attachment outside it. The spine vertex is the query's only degree-three vertex; the original root has degree two.

To match the earlier convention that the query root is zero, write the normalized quantities as

$$
\widehat q=q-r=(0,2),\qquad
\widehat a=r=(0,-2),\qquad
\widehat b=r+(-4,-2)=(-4,-4).
$$

Geometric query points and copy translations below still use the original coordinates. Their host locations are unchanged.

### Four complete prefixes and an induced-tree certificate

Let $P_*$ be the final prefix, $P_f$ the prefix after all inner rounds, $P_e$ the prefix after the last extension to the negative endpoint but before the last positive extension, and $P_0$ the prefix after the initial upward run. Define

$$
F=(P_*+(-4,-2))\cup P_f\cup(P_e+(6,0))\cup(P_0+(2,-2)).
$$

Every prefix contains the initial left leaf, root connector, and all previously discovered branches. The host also has the following exact decomposition into one polygonal path, an additional branch, and three short attachments. Include all integer points between consecutive corners.

The main path is

$$
\begin{gathered}
(-8,1)\to(-8,H-4)\to(-6,H-4)\to(-6,-2)\to(-4,-2)\\
\to(-4,H-2)\to(-2,H-2)\to(-2,0)\to(0,0)\\
\to(0,H)\to(2,H)\to(2,-4)\to(1,-4).
\end{gathered}
$$

Attach the following branch at $J=(2,H-2)$:

$$
J\to(4,H-2)\to(4,0)\to(6,0)\to(6,H)\to(8,H)\to(8,6),
$$

and add three attachments of length three:

$$
\begin{gathered}
(-4,-2)\to(-4,-4)\to(-5,-4),\\
(0,0)\to(0,-2)\to(-1,-2),\\
(6,0)\to(6,-2)\to(5,-2).
\end{gathered}
$$

The long vertical segments occupy even columns separated by two. Horizontal connectors occur only at the listed heights. Segments at different heights are separated by at least two rows; nonincident segments at the same height retain empty columns between them. The left leaves of short attachments also retain an empty gap. There are consequently no additional four-neighbor edges. The main path, side branch, and three short attachments have $6H+6$, $3H-2$, and $9$ edges, respectively. The induced graph is a tree with

$$
N=(6H+6)+(3H-2)+9+1=9H+14.
$$

Its coordinate range is $[-8,8]\times[-4,H]$, giving square side length $H+5$.

### Genuine records and earliest centers for all parameters

First take $y\in\{H-3,H-6,\ldots,3\}$. At target $v_y=(2,y)$, consider four query endpoints

$$
e'_y=(0,y+2),\qquad e_y=(-4,y),\qquad
f_y=(2,y),\qquad f'_y=(6,y+2).
$$

Their root depths are

$$
\begin{aligned}
\operatorname{depth}(e'_y)&=y+4, &
\operatorname{depth}(e_y)&=2H+2-y,\\
\operatorname{depth}(f_y)&=2H+4-y, &
\operatorname{depth}(f'_y)&=4H+6-y.
\end{aligned}
$$

The initial upward run reaches height $H+2$. The first inner early endpoint reaches $H+5$. Subsequent early depths increase by three per round, whereas the later endpoint is only two deeper than its early endpoint. Every inner endpoint is therefore a global height record. The outer early endpoints occur on the initial upward run; the outer late endpoints occur in the final positive extension and are also records. Their discovery order is strictly

$$
e'_y<e_y<f_y<f'_y.
$$

The four complete prefixes guarantee success of translation $0$ at the inner late endpoint, translation $(6,0)$ at the inner early endpoint, translation $(-4,-2)$ at the outer late endpoint, and translation $(2,-2)$ at the outer early endpoint. All four hit the same target and use the same first child edge from the original root.

The earliest-center condition still needs checking. Before the inner early endpoint, the only relevant points in its query row are the initial upward point $(0,y)$ and the negative upward point $(-2,y)$. The latter has depth $y+4\le H+1$ and is not a new height record. The former would require translation $(2,0)$ to hit the target. That candidate fails at the initial left leaf because host point $(1,-2)$ is absent. Thus the inner early endpoint is indeed the earliest successful center. The outer early endpoint is the first point discovered in its query row and succeeds.

Both markers have horizontal label $(6,0)$ and lie in different rows. The inner time interval lies strictly inside the outer interval, so it is charged. All these charges go to the same candidate and query fork.

One more row from the first round can be included: $y=H-2$. Its inner early and late depths are $H+4,H+6$, both new records. The point $(-2,H-2)$ only ties the previous maximum. Another earlier record, $(-3,H-2)$, requires translation $(5,0)$, but its initial left-leaf image $(4,-2)$ is also absent. The initial upward point is excluded as before. The corresponding outer early endpoint is $(0,H)$, whose complete initial prefix is supplied.

The number of rigorously charged rows is therefore

$$
\left|\{H-3,H-6,\ldots,3\}\cup\{H-2\}\right|=\frac H3,
$$

proving the general lower bound. Only these charges need be exhibited; the argument does not claim to enumerate every charge.

### Total historical capacity is exactly nine, with no larger receiver arm

The host has only four degree-three vertices. The first three are

$$
z_a=(0,0),\qquad z_b=(-4,-2),\qquad z_c=(6,0).
$$

Each has left, up, and down directions. The downward attachment has length three, and the other two directions are longer, so each third arm has length three. The fourth vertex is the side-branch junction, with up, down, and right directions and third-arm length $H+3$. It lacks the left neighbor required by the query fork and cannot be its successful image.

The query has only one vertex that can become a historical fork. The corresponding prefixes guarantee that all three possible images succeed at some point. Hence, exactly,

$$
\Psi=3+3+3=9.
$$

Every exhibited charge also has

$$
s=2,\qquad x=2H-y,\qquad y_{\mathrm{arm}}=2H+2-y,
\qquad t=3,\qquad D_f=2H+2.
$$

All belong to the actual-long-arm remainder. The candidate receiving the outer complete prefix is always the same, and

$$
t_F(\widehat b+\widehat q)=3=t_F(\widehat a+\widehat q).
$$

The outer LCA is its early endpoint itself. The receiving fork lies on the outer root segment leading to the common endpoint path, outside that path. This configuration is consistent with the exact projection and strict deletion lemmas.

Specifically, after the inner stage, the zero translation still succeeds at $(2,2)$, then fails at the absent point $(3,2)$ before all outer late endpoints.

Thus

$$
\frac{M(\widehat a,\widehat q)}{t_F(\widehat a+\widehat q)}
\ge\frac H9\longrightarrow\infty,\qquad
\frac{\sum_{a,q}M(a,q)}{\Psi}
\ge\frac H{27}\longrightarrow\infty.
$$

Historical third-arm capacity cannot absorb the entire actual-long-arm remainder, and the receiving third arm need not strictly increase.

### Actual scans and moves

This family does not produce a large actual scan complexity. The numbers of surviving candidates after successive new points occur in the following runs:

$$
20\times1,\quad 7\times H,\quad 4\times2,\quad
3\times(3H-7),\quad 2\times4,\quad 1\times(2H+1),
$$

where each term gives a candidate count and its number of new-point rounds. There are $18H+16$ successful checks. Only one candidate remains, giving $9H+13$ failed checks. Therefore

$$
W=27H+29.
$$

Realizing the discovery order by the described walks between arms uses

$$
m=2H^2-\frac{8H}{3}+3
$$

moves. The counterexample therefore disproves this cost allocation, without refuting the original general complexity bound. All fixed parameters $H=12,24,48$ passed exact marker counting, a full-move oracle, and the problem implementation. The first case also passed independent enumeration of complete prefixes, reconstruction of earliest centers, and vertex-deletion BFS for its charges and capacity. The general lower bound and constant capacity follow from the parameter proof above.
