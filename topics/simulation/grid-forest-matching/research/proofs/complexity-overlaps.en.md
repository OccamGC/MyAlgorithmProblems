# Matching in a Class of Four-Neighbor Grid Forests — Overlap Across Prefixes

**Historical research record (updated 2026-10-12).** The [standalone proof](cubic-bound.en.md) now establishes the general cubic bound. The derivations, remainders, and counterexamples below retain their historical order. Statements that a problem is unresolved refer to that stage or local method; stronger auxiliary claims do not automatically follow from the general bound.

This note proves overlap constraints across prefixes, collinearity of historical high-overlap components, and a total multiplier budget for changes of high-overlap direction. It then reduces actual candidate checks to a total of root-path matches and bounds some parts of that total. The full total-count bound remains a conjecture; these results have not removed the logarithm from the [general upper bound](../../complexity.en.md).

**Current result: a linear total for unweighted frontiers is false.** The final section gives induced grid trees with a common query and host root whose frontier count is $\Theta(nN)$, with $N=\Theta(n^2)$. This does not refute a cubic bound for the actual algorithm or the direct root-path matching target: many of these frontiers cannot satisfy one actual complete-prefix history. The valid reductions and earlier obstacles remain below, but frontier linearity is no longer an open target.

Let the road set be $F$, with an induced four-neighbor graph that is a forest, and let $N=|F|$. The roads lie in an $n\times n$ grid. Translations preserve orientation; no rotation or reflection is allowed. All set connectivity below means four-neighbor connectivity.

## A unified lemma for two nonparallel partial translations

Take a nonempty finite set $U\subseteq F$ and nonempty connected sets $P,R\subseteq U$. Suppose the integer displacement vectors $d,e$ are linearly independent and

$$
P+d\subseteq F,\qquad R+e\subseteq F.
$$

Then

$$
\boxed{|(P+d)\cap U|+|(R+e)\cap U|\le |U|-1.}
$$

The set $U$ need not be connected, the translation domains need not be nested, and the four connected copies need not belong to the same road component.

### Step one: an area potential on the road forest

Write $\det(x,y)=x_1y_2-x_2y_1$. Choose a root in each road component and sum edge weights along unique root paths to obtain a function $\Phi$ satisfying

$$
\Phi(y)-\Phi(x)=\det(x,y)
$$

on every directed road edge. Root values in different components can be chosen independently. For $x\in P$, define

$$
f_d(x)=\Phi(x+d)-\Phi(x)-\det(d,x).
$$

If $x,y$ are adjacent in $P$, both the original and translated edges are road edges. Hence

$$
f_d(y)-f_d(x)
=\det(x+d,y+d)-\det(x,y)-\det(d,y-x)=0.
$$

Connectivity makes $f_d$ constant on $P$; denote the constant by $c_d$. Similarly obtain a constant $c_e$ on $R$. Every $x\in P$ therefore satisfies

$$
\Phi(x+d)-\Phi(x)=-\det(x,x+d)+c_d.
$$

The endpoints in this identity need not be adjacent road cells.

### Step two: the auxiliary graph is acyclic

Build an auxiliary undirected graph on $U$:

- For $x\in P$ with $x+d\in U$, add the edge $x(x+d)$.
- For $x\in R$ with $x+e\in U$, add the edge $x(x+e)$.

There are no loops or repeated edges, and the edge count is exactly the left side of the lemma. Suppose there is a simple cycle. All its vertices belong to one affine lattice

$$
x_0+\mathbb Z d+\mathbb Z e.
$$

Using $d,e$ as a coordinate basis turns every edge into a unit edge of the integer square grid. Distinct unit edges intersect only at shared endpoints, so a simple cycle bounds a simple polygon of nonzero area. Transforming back preserves nonzero area, giving

$$
\sum_{xy\text{ on the cycle}}\det(x,y)\ne0.
$$

Traversing an edge in its positive translation direction changes the potential by $-\det(x,y)+c_d$; a reverse traversal changes it by $-\det(x,y)-c_d$. The other edge type behaves identically. The cycle has zero total displacement. Linear independence of $d,e$ implies equal positive and negative counts of each edge type, so all constant terms cancel. The potential also telescopes to zero. Thus

$$
0=-\sum_{xy\text{ on the cycle}}\det(x,y),
$$

a contradiction. The auxiliary graph is a forest, with at most $|U|-1$ edges, proving the lemma.

This argument applies to two nonparallel translations. It does not justify combining arbitrarily many translation directions into an acyclic graph.

## Constraints that survive deletion of an old candidate

Let $P\subseteq Q$ be nonempty connected sets, with $P,P+d,Q,Q+e$ all contained in the road forest and $d,e$ nonparallel. Define

$$
I_d(P)=|P\cap(P+d)|.
$$

Set $U=Q$ and $R=Q$ in the unified lemma to obtain

$$
\boxed{|(P+d)\cap Q|+I_e(Q)\le |Q|-1.}
$$

In particular, $I_d(P)+I_e(Q)\le |Q|-1$. The condition $Q+d\subseteq F$ is not required, so the candidate responsible for the old translation may already have been deleted.

If $k>1$ and $I_e(Q)\ge(1-1/k)|Q|$, then

$$
|Q|\ge k\bigl(|(P+d)\cap Q|+1\bigr)
\ge k\bigl(I_d(P)+1\bigr).
$$

If the new base copy contains the entire old translated copy, the intersection term equals $|P|$. Thus deletion alone does not invalidate the old certificate, although its use still requires the same valid base copy.

Alternatively, setting $U=F$ gives a size constraint without any nesting requirement:

$$
\boxed{|P|+|R|\le N-1.}
$$

For the algorithm, fix a surviving start of the last valid prefix as the base. Let another start have displacement $d$ from it, and let $\ell(d)$ be the size of its last successfully matched complete prefix, including the initial zero offset. Nonparallel displacements satisfy

$$
\ell(d)+\ell(e)\le N-1.
$$

Consequently all starts with lifetime greater than $(N-1)/2$ are collinear with the base. Including the base, there are at most $n$ such starts. This pairwise lifetime constraint does not yet bound the sum of all lifetimes.

## All historical high-overlap edges within one size interval

Take $1/2<\alpha<1$, put $\rho=\alpha/(1-\alpha)$, and fix $s\ge1$. Build a historical graph whose vertices are all initial candidates. Whenever a complete query prefix has size $j\in[s,\rho s)$ and two valid copies overlap in at least $\alpha j$ points, add an edge between their starts. Keep the edge even after a candidate is deleted.

**Every nontrivial connected component of this graph lies on a single line and contains at most $n$ starts.**

It suffices to show that two edges sharing a start are parallel. Order them by their appearance times. Write the two prefixes at the common start as $P\subseteq Q$, and let $d,e$ be the displacements to their other starts. The common start survives at the later time, so both base copies are valid. The other start of the old edge may already have been deleted.

If $d,e$ are nonparallel, the previous section gives

$$
\alpha|P|+\alpha|Q|
\le I_d(P)+I_e(Q)\le |Q|-1.
$$

Therefore

$$
|Q|\ge\frac{\alpha|P|+1}{1-\alpha}
>\rho|P|\ge\rho s,
$$

contradicting the interval definition. Apply this along graph paths to obtain collinearity of the whole component. Any line in the square grid contains at most $n$ integer points, proving the size bound.

For example, taking $\alpha=2/3$ retains all historical high-overlap edges within any interval $[s,2s)$. Combining every size interval is not justified: across several scales, the historical graph can have a noncollinear cycle.

This does not prove cubic total time. The remaining issues include charging copies with small overlaps and sharing charges across different intervals.

## The sum of maximum multipliers over direction blocks is less than three side lengths

The previous section fixes an overlap threshold. The following result combines different thresholds and scales, but it still counts only high-overlap certificates, not every successful check.

Let nonempty containers $Q_i\subseteq F$ be nested in chronological order. Each certificate consists of a nonempty connected domain $D_i\subseteq Q_i$ and a nonzero integer displacement $d_i$ satisfying $D_i+d_i\subseteq F$. Define

$$
j_i=|Q_i|,\qquad J_i=|(D_i+d_i)\cap Q_i|,\qquad
\kappa_i=\frac{j_i}{j_i-J_i}.
$$

Domains may vary between certificates and need not be nested. Containers need not be connected either.

Within the container, add the edge $x(x+d_i)$ only when $x\in D_i$ and $x+d_i\in Q_i$. This gives disjoint straight chains, with $J_i$ edges. Each chain has at most $n$ lattice points, so

$$
1\le\kappa_i\le n.
$$

For an earlier and a later certificate with nonparallel displacements, the unified lemma and monotonicity of the containers give

$$
J_i+J_k
\le |(D_i+d_i)\cap Q_k|+|(D_k+d_k)\cap Q_k|
\le j_k-1\qquad(i<k).
$$

At each time keep only certificates with $\kappa_i\ge4$. All such certificates at the same time are parallel: otherwise both overlaps would be at least three quarters of the container size, contradicting the unified lemma. Group consecutive certificates of the same direction, treating opposite displacements as the same direction and skipping times with no high multiplier. In each direction block select a certificate attaining its maximum multiplier, and renumber the selected certificates chronologically as $1,\ldots,r$.

**These representatives satisfy**

$$
\boxed{\sum_{i=1}^{r}\kappa_i<3n.}
$$

With no certificates or one direction block this is immediate. Otherwise there are at least two blocks, and $n\ge4$. Consecutive representatives have nonparallel displacements, so

$$
\frac{j_{i+1}}{\kappa_{i+1}}\ge J_i+1
=\left(1-\frac1{\kappa_i}\right)j_i+1,
\qquad
j_{i+1}>\frac34\kappa_{i+1}j_i.
$$

Taking natural logarithms and summing gives

$$
\sum_{i=2}^{r}\log(3\kappa_i/4)<\log(j_r/j_1).
$$

The function $x/\log(3x/4)$ increases for $x\ge4$, since its derivative has the sign of $\log(3x/4)-1>0$. Using $\kappa_i\le n$, $j_1\ge\kappa_1\ge4$, and $j_r\le n^2$, we obtain

$$
\sum_{i=2}^{r}\kappa_i
<\frac{n}{\log(3n/4)}\log(j_r/j_1)
\le\frac{n\log(n^2/4)}{\log(3n/4)}<2n.
$$

The last step uses $n^2/4<(3n/4)^2$. Adding $\kappa_1\le n$ proves the budget.

For an actual query, fix a surviving start of the last valid prefix as the base. Consider certificates only through that prefix, using the base start's current complete prefix as the container. After another candidate is deleted, its last successful prefix can remain the domain of a certificate. A growing container may later absorb more points of that old copy. The theorem therefore includes history after a candidate has been deleted. Any final check that empties the candidate list remains covered by the original budget of at most $N$ failures.

The theorem bounds only the sum of maximum multipliers over direction blocks. There is currently no proof charging all checks to those blocks; numerous copies with small overlaps still need a separate argument. Nor can disconnected domains with the same displacement simply be merged into one certificate, since the unified lemma requires a connected domain for each certificate.

## Reducing all candidate checks to a total of root-path matches

The following reduction is proved, but the resulting linear total-count bound remains a conjecture.

For nonempty roads, let $T$ be the last complete query tree with surviving candidates, including the initial zero offset. Exclude a final new offset that makes all candidates fail. One may set $Q=T$. Alternatively, choose a surviving start $a_*$ and set $Q=C-a_*$, where $C$ is its entire road component. Either choice is an induced tree rooted at the zero offset and containing $T$.

For each initial start $a\in F$, define

$$
K_a=\operatorname{comp}_0\bigl(Q\cap(F-a)\bigr),
\qquad S(Q,F)=\sum_{a\in F}|K_a|.
$$

Here the component is the one containing zero in the induced intersection graph. Equivalently, $p\in K_a$ precisely when the entire query path from zero to $p$, translated to start at $a$, lies on roads.

If $C_a$ is the road component containing the start, one can also write $K_a=\operatorname{comp}_0(Q\cap(C_a-a))$. The sum still includes every start outside the reference component.

Every actual successful new offset belongs to the corresponding $K_a$, and a start never checks that offset twice. It therefore has at most $|K_a|-1$ successful checks. Each start fails at most once, so there are at most $N$ failed checks in total. Hence

$$
\boxed{W\le N+\sum_{a\in F}(|K_a|-1)=S(Q,F).}
$$

For empty roads, directly use $W=0$. Repeated offsets and immediate clearing after an excessive displacement do not add candidate checks.

**Open conjecture.** Does an absolute constant $c$ exist such that every instance above satisfies

$$
S(Q,F)\le c nN\,?
$$

A proof would give time $O(n^2+m+nN)\subseteq O(n^3+m)$. A linear hit bound at every target cell is unnecessary: this total-count problem permits many root-path matches at a few targets. Even proving only the special case $Q=C-a_*$ above would suffice for the algorithmic upper bound.

Constant one is already false. Take an integer $s\ge1$ and $n=4s+1$. Let the roads consist of a full bottom-row spine and full-height teeth in every even column. Use the midpoint of the central tooth as the reference root, and let $Q$ be the entire component relative to this root. Counting vertical segments and same-height combs gives

$$
N=8s^2+8s+1,\qquad
S(Q,F)=36s^3+34s^2+12s+1.
$$

Thus $S(Q,F)/(nN)\to9/8$. This family neither refutes an absolute constant bound nor gives a supercubic running-time construction.

The exact formula can be checked by groups. Use coordinates $0,\ldots,4s$, with the spine at height zero. A start in an even column at height $y\ne2s$ matches only a vertical segment, of size $2s+1+\min(y,4s-y)$. For a same-height start $(2i,2s)$, put $t=\min(i,2s-i)$. The common spine has $2s+1+2t$ vertices, with $s+1+t$ full teeth contributing $4s$ additional vertices each. A spine start in an odd column matches only the root. Summing these sizes gives the polynomial.

## A proved bound for ancestor starts

Root each road component arbitrarily. In a root-path match, write the road endpoint as $b=a+p$. Count only pairs in which $a$ is an ancestor of $b$, including equality. Their total is at most

$$
(3n-2)N.
$$

Fix the endpoint $b$. Reverse the road path from its component root to it, using this as a new single-ended path query, with $Q$ as the new road tree and zero as the fixed target. Every original valid ancestor start $a$ gives a new query offset $a-b$ and a new start $b-a$. Translating the entire new query prefix to this start gives exactly the path in $Q$ from that vertex back to its root. This is therefore an actual complete-prefix success.

By the [root-to-leaf chain theorem](complexity-chains.en.md), each endpoint admits at most $3n-3$ nonempty successes, or $3n-2$ matches including the empty word. Summing over endpoints proves the bound. The original $Q$ need not embed completely into the host, and the number of road components is unrestricted.

This covers matches moving downward relative to the chosen host roots. Purely upward paths, and paths moving upward before turning downward, still require a combined charge. The general total-count conjecture remains open.

## Adjacent matched endpoints at a fixed target lie on initial straight rays

Fix a host target $b$ and put

$$
A_b=\{q\in Q:\text{the root path to }q\text{ matches a road path ending at }b\}.
$$

If a query parent and child $q,q+\delta$ both belong to $A_b$, where $\delta$ is a unit direction, then the direction word from the root to $q$ consists entirely of repetitions of $\delta$.

To prove this, write that word as $w_q$ and its length as $k$. The two matching starts are

$$
a=b-q,\qquad a'=b-q-\delta=a-\delta.
$$

They are adjacent road cells. Because the host is an induced forest, a road edge joins them, and their unique paths to $b$ have lengths $k$ and $k+1$. Thus the path from $a'$ to $b$ must first take direction $\delta$ to $a$ and then follow the other path. Its direction word is therefore both

$$
\delta w_q=w_q\delta.
$$

Comparing letters gives $w_q=\delta^k$, proving the claim.

If the endpoint $k\delta$ of an initial ray matches at $b$, every shorter endpoint on that ray also matches at $b$: take the corresponding suffix of the host path. Hence the induced query subgraph $Q[A_b]$ consists of a straight cross containing the root and isolated remaining points. The root path of every remaining point changes direction at least once.

The straight cross contains at most $2n-1$ points in the grid. Consequently all matches of straight root paths total at most

$$
(2n-1)N.
$$

This does not bound the total of isolated endpoints with nonstraight root paths. Sparsity of the induced subgraph alone does not prove the full total-count bound.

## A query-frontier reduction for purely upward matches

Root each host component. For every target $b$, let $U_b\subseteq Q$ consist of the query endpoints of purely upward matches: the translated query root path follows host parent pointers from its start to $b$. Include the path of length zero.

In the query ancestor order, let $M_b^Q$ be the points of $U_b$ having no deeper matched descendant. Assign each matched endpoint to one such maximal descendant. Every group lies on one query root chain. Running that chain as a complete one-ended query makes every match in the group a valid hit at the fixed target $b$. By the root-to-leaf chain theorem, each group contains at most $3n-2$ matches, including the empty word. Thus

$$
S_{\mathrm{up}}(Q,F)=\sum_{b\in F}|U_b|
\le(3n-2)\sum_{b\in F}|M_b^Q|.
$$

**This sufficient condition has since been disproved.** The proposed bound $\sum_b|M_b^Q|=O(N+|Q|)$, or even just $O(n^2)$, would have controlled the purely upward part. The parameterized family in the final section disproves both bounds, even for identical query and host trees with a common root. The reduction inequality above remains valid, but unweighted frontier counts cannot complete the total-count proof this way. The full root-path total also includes paths going upward and then downward.

## One complete reference tree with a common root: comparable frontiers

Consider a single road tree, used as both the query and the host, with the same root $r$. Let $N$ be its number of vertices. A purely upward frontier event consists of a host start $a$, a target $b$, and a query endpoint $q\in M_b^Q$, with

$$
b=a+q-r,\qquad
\operatorname{depth}(a)=\operatorname{depth}(b)+\operatorname{depth}(q).
$$

Separate events according to whether the query endpoint is an ancestor of the host start. Call these the comparable and incomparable classes. The depth identity rules out a query endpoint that is a strict descendant of the start, so these two classes cover all events.

**Lemma.** In the comparable class, the query endpoint is an ancestor of the host target, and a strict ancestor when $q\ne r$. Consequently, the number of comparable frontier events satisfies

$$
E_{\mathrm{comp}}\le N.
$$

Proof: the empty query path is immediate. For a nonempty path, let $u$ be the query root word, of length $k$, and let $W$ be the host start's root word, of length $h$. The ancestor condition makes $u$ a prefix, while the upward match makes the inverse word $u^{-1}$ a suffix.

The direction word of a simple tree path has no adjacent inverse letters. These two inverse end segments cannot meet or overlap: if $2k\ge h$, the two central letters are inverse when the length is even, or the central letter equals its own inverse when the length is odd. Either contradicts reduction. Thus

$$
2k<h,\qquad \operatorname{depth}(b)=h-k>k=\operatorname{depth}(q).
$$

Both vertices are ancestors of the start, so the query endpoint is a strict ancestor of the target. For a fixed target, all comparable query endpoints lie on its single root path. A query frontier is an antichain, so it retains at most one of them. Summing over targets proves the lemma.

The incomparable part has no general linear charge, as the final section shows. The comparable-part lemma remains valid, but it neither controls the full frontier nor addresses different host components or different roots.

## A full comb with frontier ratio tending to two: an earlier lower bound

Take even $m\ge2$ and integer $H\ge1$. In row-column coordinates, form the full comb

$$
F=\{(0,c):0\le c\le2m\}
\cup\{(y,2i):1\le y\le H,\ 0\le i\le m\}.
$$

The spine joins all vertical teeth, and adjacent teeth have an empty column between them, so this is an induced tree. Use it as both query and host, rooted at the far tip of the central tooth, $r=(H,m)$. Its size is

$$
N=(m+1)H+2m+1.
$$

Count query frontiers by target type:

- At a positive-height target on a noncentral tooth, a host path can move upward toward the root only by approaching the spine. It matches the initial query chain and has one maximal endpoint.
- At a noncentral spine target, an upward host path approaches from only one side of the spine. Matched query endpoints lie on the chain consisting of the initial tooth and one side of the query spine, so the frontier has size one.
- At the spine center, paths can approach from either side. The two maximal endpoints are the two ends of the query spine, giving frontier size two.
- At a positive-height target $(y,m)$ on the central tooth, each noncentral query tooth in column $c$ gives one maximal endpoint $(y,c)$. Its host start is the reflected tooth tip $(H,2m-c)$: the path reaches the spine, moves to the central column, then follows the central tooth toward the root. These endpoints are exactly the maximal nonempty matches, so the frontier has size $m$.

There are $H$ positive-height targets on the central tooth. Every other target normally contributes one, with one extra at the spine center. Hence

$$
E=\sum_b|M_b^Q|=(N-H)+1+mH=2mH+2m+2.
$$

In particular, set $H=2m$. The bounding square has side $n=2m+1$, and

$$
N=2m^2+4m+1,\qquad
E=4m^2+2m+2,\qquad
\frac EN=2-\frac{6m}{2m^2+4m+1}\longrightarrow2.
$$

Thus this full comb alone shows that any general bound $E\le CN+o(N)$ would require $C\ge2$. The new construction in the final section rules out every such absolute constant. This comb has only linearly many branching vertices in the square's side length, so its actual algorithmic work is already covered by the [long-branch proof](complexity-branches.en.md). The frontier construction is not a supercubic runtime counterexample.

## Restricting a common-root frontier to a connected subtree

Continue using the road tree as both query and host, with common root $r$. Write its frontier total as $E(F,r)$. Take a nonempty connected subtree $K$, and let $c$ be its vertex of minimum original root depth. Uniqueness of tree paths makes it an ancestor of every vertex in the subtree.

Count only original frontier events whose three endpoints $a,b,q$ all belong to the subtree, and call this count $E_F[K]$. Use the subtree as both the new query and the new host, rooted at its shallowest vertex. Then

$$
\boxed{E_F[K]\le E(K,c).}
$$

**Proof.** Let $u$ be the direction word from the original root to the new root, and let $v$ be the word from the new root to the query endpoint. The full original match reads $uv$, and the host reads the same word while following parent pointers from its start to its target. Both host endpoints lie in the connected subtree, so the entire host path lies there. After reading the prefix, its position is

$$
a'=a+c-r\in K.
$$

The remaining word goes from this new start to the original target and is exactly the new query root path. Parent directions inside the subtree are unchanged. This gives a purely upward match in the new instance, with

$$
b=a'+q-c.
$$

Either word may be empty. The new start may differ from the original start, and an originally nonempty query may become empty.

An old query endpoint need not remain maximal: removing the common prefix may introduce more matches. However, at a fixed target the retained old frontier endpoints are still an antichain in the subtree. Each has a maximal new matched descendant. Two different old endpoints cannot choose the same descendant, since they would then be comparable ancestors of one vertex. Thus they inject into the new frontier. Sum over targets to obtain the result.

## Charging to internal paths is equivalent to a linear frontier bound

For each frontier event $e=(a,b,q)$, let

$$
S_e=\operatorname{hull}_F\{a,b,q\}
$$

be the smallest connected subtree containing its three endpoints, including every required internal path vertex. Fix a positive integer $C$. The following statements are equivalent over all complete reference trees with a common root:

1. The frontier total satisfies $E(F,r)\le C|F|$.
2. Each event can be assigned to a vertex of its connecting subtree, with at most $C$ events assigned to each road vertex.

An assignment immediately implies the total bound. Conversely, suppose the total bound holds for every instance. Take any resource set $U\subseteq F$, and let $K_i$ be the connected components of its induced subgraph, with shallowest vertices $c_i$. An event's connecting subtree is contained in the resource set exactly when its three endpoints lie in the same component. The localization lemma gives

$$
\#\{e:S_e\subseteq U\}
=\sum_i E_F[K_i]
\le\sum_i E(K_i,c_i)
\le C\sum_i|K_i|
=C|U|.
$$

Replace each road vertex by as many resource slots as its capacity. For any collection of events, take the union of their permitted resource sets. The inequality ensures that this union supplies at least as many slots as events. Hall's matching theorem therefore gives the required assignment.

This provides a charging target equivalent to the general linear bound; it does not prove that bound. Restricting charges to the three endpoints alone imposes a stronger condition, already refuted by a legal example even with capacity two. The connecting subtree also cannot be replaced by the single path from the start to the query endpoint, since that path need not contain the host target.

## Pay for straight matches before counting nonstraight frontiers

Let $E_{\mathrm{ns}}$ count frontier events whose query root path changes direction at least once; the empty path belongs to the straight class. Every descendant of a nonstraight query vertex is still nonstraight. Assign each nonstraight match to a nonstraight maximal matching descendant. Each group lies on one query root chain and excludes the empty path, so the chain bound gives at most $3n-3$ matches. Together with the bound for all straight matches,

$$
\boxed{S_{\mathrm{up}}(Q,F)\le(2n-1)N+3(n-1)E_{\mathrm{ns}}.}
$$

This holds in the general pure-upward model above; the query and host need not coincide or have the same root. It reduces the unresolved count to nonstraight frontiers without proving that count linear.

In the full comb with a common root, positive-height targets on the central tooth contribute $mH$ nonstraight frontiers, and the spine contributes another $2m$. Thus

$$
E_{\mathrm{ns}}=mH+2m.
$$

However, the general bound $E_{\mathrm{ns}}\le N$ is false: an induced tree with sixty vertices, used as both query and host with a common root, has sixty-three nonstraight frontier events and eighty-nine frontier events in total. This finite example rules out constant one; the final section's parameterized family further disproves a linear nonstraight-frontier bound with any constant.

## A fixed start pays for at most one terminal frontier

Fix a host start $a$. Reading parent pointers gives a unique direction sequence. The query root paths that it can read form an initial segment of one chain; let $q_a$ be the deepest matching endpoint. Call a frontier event terminal if its query endpoint is this deepest point. Each start gives at most one, so

$$
E_{\mathrm{term}}\le N.
$$

A query endpoint that is an actual query leaf cannot continue and is therefore terminal. Frontier events at query leaves also number at most $N$. This bound does not include all frontier events at internal query vertices.

There is also a strict propagation restriction. Suppose $(a,b,q)$ is a frontier event and the next host parent direction is $\delta$. If the query has the corresponding child, the match continues to

$$
b'=b+\delta,\qquad q'=q+\delta.
$$

If the new query endpoint loses frontier status at the new target, take a strictly deeper matching descendant $s$. Let its last step have direction $\varepsilon$. If $\varepsilon=\delta$, deleting that last step from the competing match gives a strict matching descendant of the old query endpoint at the old target, contradicting its frontier status. Hence

$$
\varepsilon\ne\delta.
$$

The competing match enters the new host target from a different child. Losing frontier status while continuing a match therefore requires a host vertex with at least two children. This identifies where a charge could occur, but does not bound how often events can use the same branch.

New frontier events satisfy a dual restriction. Consider a nonempty new frontier whose query predecessor is $q$, new query endpoint is its child $q'$, and old and new host targets are $b,b'$. Removing the last step shows that the predecessor is itself a match. If it was not a frontier, take an old frontier endpoint $s$ strictly below it. If this competitor can also continue in the same direction, it must lie in another query child branch; otherwise its successor would still strictly dominate the new query endpoint. Thus a nonempty frontier appearance involves either a query branch or termination of an old competing frontier.

In particular, if the query predecessor has only one child, all its old frontier dominators must terminate. Charge the new event to any such terminal frontier. This assignment is automatically injective: fixing the old terminal event fixes the old host target and its unique parent as the new target. All possible new query endpoints are ancestors of the same old competing query endpoint, yet lie in the new target's frontier antichain, so there can be at most one. Hence

$$
E_{\mathrm{birth},1}\le E_{\mathrm{term}}\le N,
$$

where the left side counts only nonempty events that change from nonfrontier to frontier and whose query predecessor has exactly one child. Empty query words have no predecessor and are counted separately, at most one per host start. Appearances at query branches and disappearances at host branches still require a general geometric charge.

## Complete historical prefixes do not provide enough direction budget alone

The direction-budget theorem above remains valid. The following legal input family rules out a direct application: multiplying the high-overlap direction budget for complete historical prefix containers by the road size cannot pay for all scans.

Take an odd prime $p\ge3$ and define

$$
D=4p^2,\qquad
B_i=2(2pi+(i^2\bmod p)),\quad 0\le i<p.
$$

These even rows increase strictly, are all below $D$, and have unique nonzero ordered differences. To prove uniqueness, equality of differences first forces equality of index differences because the remaining residue difference has absolute value below $2p$. Reducing modulo the prime then gives equality of index sums. Since two is invertible, the ordered index pairs coincide.

The query root is the origin. Its tree consists of a vertical spine over $[0,4D]$, left teeth of length two on rows $B_i$, and right teeth of length four on even rows in $[2D,4D]$. Finish the left teeth in increasing height order, reach the top of the spine, finish the right teeth in decreasing height order, and return to the root.

The host has two vertical spines and attached teeth:

- The left spine has $x=-4$ and $-4D\le y\le2D$. Its negative even rows have teeth of length two to the left; its nonnegative even rows have teeth of length four to the right.
- The right spine has $x=0$ and $-4D\le y\le0$. Its negative even rows have teeth of length two to the left.

An empty column separates the two groups of teeth below row zero. Only the horizontal path on row zero connects the spines, so the host is an induced tree. The query is also an induced tree, and the walk traverses every edge once in each direction. The exact parameters are

$$
|P|=32p^2+2p+5,\qquad
N=88p^2+5,\qquad
n=24p^2+1,\qquad
m=64p^2+4p+8.
$$

The start $(-4,-2D)$ survives the entire query. Query displacements that successfully hit the origin, including the initial root, are exactly

$$
\{(0,y):0\le y\le4D,\ y\equiv0\pmod2\}
\cup
\{(4,y):2D\le y\le4D,\ y\equiv0\pmod2\}.
$$

Complete prefixes at spine vertices fit the right host comb; complete prefixes at right-tooth tips fit the left host comb. Left-tooth points would require positive host columns, odd rows would require absent odd-row teeth, and interior right-tooth points would require an absent full vertical spine. There are no other hits. Therefore

$$
H(0)=12p^2+1,\qquad
R_4=4p^2+1.
$$

The first expression excludes the initial root; the second counts occurrences of the same directed horizontal distance-four marker.

### All actual prefix overlap factors are at most linear in the parameter

For a complete actual prefix, define

$$
I_d(P_j)=|(P_j+d)\cap P_j|,\qquad
\kappa_j(d)=\frac{|P_j|}{|P_j|-I_d(P_j)}.
$$

We even allow shifts that are illegal in the host. For every nonzero shift,

$$
\kappa_j(d)\le25p.
$$

The vertical argument includes partially constructed teeth. Unique ordered differences of left-tooth rows imply that a nonzero vertical shift has at most two intersection points in negative columns. After all left teeth are complete, at least $2p-2$ points are lost, giving

$$
\kappa_j(d)\le\frac{32p^2+2p+5}{2p-2}\le25p.
$$

While forming the first tooth, a vertical shift has empty intersection. After completing one left tooth but before completing the second, the loss is at least two and the prefix has at most $4p+6$ points. If $t$ left teeth are complete, with $2\le t\le p-1$, allow one point of the next tooth as well. Then

$$
|P_j|\le4pt+2p+2t,\qquad
|P_j|-I_d(P_j)\ge2t-2,\qquad
\kappa_j(d)\le5p+2\le25p.
$$

For nonvertical shifts we can further show $\kappa_j(d)<4$. Before right teeth appear, prefixes occupy only three columns, so each translation chain has at most three points and the factor is at most three. During the right-tooth stage, let $R$ be the number of right-side points already discovered, including a partial tooth. Off-spine sources contribute at most the off-spine point count; spine sources contribute at most the size of one nonzero column. Thus

$$
0\le R\le4D+4,\qquad
|P_j|=4D+1+2p+R,\qquad
I_d(P_j)\le2p+R+D+1.
$$

Consequently,

$$
4I_d(P_j)-3|P_j|\le2p-4D+5<0.
$$

An earlier source domain contained in the current complete prefix has no larger intersection than that prefix's self-intersection. The same bounds therefore cover these historical partial-domain certificates. Only the vertical direction can reach threshold four. Writing $B_{\mathrm{hist}}$ for the sum of block maxima gives

$$
B_{\mathrm{hist}}\le25p.
$$

### Actual scans still cost quadratically in the road size

Right tooth $k$, numbered from zero, is on row $4D-2k$. All starts with even vertical coordinate

$$
(-4,t),\qquad -4D+2k\le t\le-2D
$$

match the entire prefix while that tooth is formed. There are $D-k+1$ such starts, and each tooth introduces four new points. Hence

$$
W\ge4\sum_{k=0}^{D}(D-k+1)
=2(D+1)(D+2)=\Omega(p^4).
$$

The elementary upper bound also gives $W\le N(|P|-1)=O(p^4)$, so

$$
W=\Theta(nN)=\Theta(p^4),
\qquad
N(1+B_{\mathrm{hist}})=O(p^3).
$$

This disproves $W\le CN(1+B_{\mathrm{hist}})$ for every fixed constant. The multiplicity of one marker likewise cannot be bounded linearly by the maximum overlap factor of actual complete historical prefixes. The container restriction matters: this does not exclude a proof using other connected subtemplates, other containers, or additional geometric charges. The family has only linearly many road vertices in the board side length and still satisfies the general cubic target.

Placing copies of the host side by side also rules out adding the board's base cost to this charging proposal. Take

$$
F^\star=\bigcup_{j=0}^{p^2-1}\bigl(F+(8j,0)\bigr).
$$

Each copy occupies seven columns, with one empty column between adjacent copies. The total width is $8p^2-1$ and the height remains $n$, so the forest still fits the original square. Use the same query and actual walk. Every complete query prefix is connected and cannot cross host components, so candidate counts add exactly over components:

$$
N^\star=p^2N=\Theta(p^4),\qquad
W^\star=p^2W=\Theta(p^6),\qquad
n^\star=n,\qquad m^\star=m.
$$

Fix any final surviving reference start. Its complete-prefix containers remain copies of the original template. Candidates in other components obey the same self-intersection bound and cannot add nonvertical high-factor certificates. Thus

$$
B_{\mathrm{hist}}^\star\le25p,\qquad
(n^\star)^2+N^\star(1+B_{\mathrm{hist}}^\star)=O(p^5),
\qquad
W^\star=\Theta((n^\star)^3).
$$

Even after adding the board's base cost, a fixed constant multiple of this budget is insufficient. This is an asymptotic counterexample to the specific charging proposal; the legal forest family's actual complexity agrees with the cubic target.

## A forest of frontier events

Frontier propagation gives a complete forest structure, beyond counts of appearances and disappearances. This works for a general query tree and a host forest rooted separately in each component.

For each continuable frontier event $(a,b,q)$, let its next host target and query child be $b',q'$. If the latter remains a frontier, point to that continuing event. Otherwise, choose any frontier query endpoint $p$ at the new target that strictly dominates it, and point to the corresponding event

$$
(a',b',p),\qquad a'=b'-p+r.
$$

Here $r$ is the query root coordinate. Terminal frontiers have no outgoing edge.

Every arrow moves the host target to its parent, strictly decreasing host depth, while moving the query label to a strict descendant. There is no directed cycle and each event has outdegree at most one, so the underlying graph is a forest. Each tree has exactly one terminal frontier as its root, and there are at most $N$ trees.

### Each event tree projects injectively to a connected host subtree

Fix a host child and its parent. Distinct old frontier query endpoints at that child are incomparable, and each selected new frontier is a descendant of its old endpoint. If two old events pointed to the same new event, both old query endpoints would be ancestors of the same new query endpoint, a contradiction. The frontier map from one host child to its parent is therefore injective.

Expand an event tree downwards from its root. Each host child direction corresponds to at most one event-tree child. Different host children have disjoint descendant subtrees, so the full projection cannot repeat a vertex. Event-tree edges project to host edges, giving a connected subtree $K_\tau$ with

$$
|\text{event tree }\tau|=|K_\tau|.
$$

Along every event arrow, query labels move to strict descendants. If the terminal root has query label $q_\tau$, all query labels in that event tree are its ancestors and lie on one query root chain. The query projection need not be injective.

Writing $\mathcal T$ for all terminal frontiers gives the exact decomposition

$$
\boxed{
E=\sum_{\tau\in\mathcal T}|K_\tau|,
\qquad |\mathcal T|\le N.
}
$$

Host subtrees of different event trees may overlap. Their total overlap remains uncontrolled; injectivity for one tree does not give injectivity for the entire forest.

There is a further restriction: if two different event trees have comparable terminal query labels, including equal labels, their host projections are disjoint. Otherwise, at a shared host point, both frontier query labels lie on one query root chain but belong to the same frontier antichain. They must coincide, putting the same event in two components, a contradiction. Thus, for any query root chain $\Gamma$,

$$
\sum_{\substack{\tau\in\mathcal T\\q_\tau\in\Gamma}}|K_\tau|\le N.
$$

Overlap between components with incomparable terminal query labels remains unpaid.

### Edges that actually replace a frontier

If an arrow comes from frontier loss, the dominating query endpoint is strictly deeper than the original next query endpoint. The pure-upward depth identity gives

$$
\operatorname{depth}(a')
=\operatorname{depth}(b')+\operatorname{depth}(p)
>
\operatorname{depth}(b')+\operatorname{depth}(q')
=\operatorname{depth}(a).
$$

The different-child result above also gives

$$
\operatorname{LCA}(a,a')=b'.
$$

Ordinary continuation preserves the original start. Contracting consecutive frontier states with the same start into one segment still gives a forest; each contracted edge strictly increases start depth.

If there are $R$ consecutive segments, $T_{\mathrm{term}}$ terminal frontiers, and $L_{\mathrm{loss}}$ continuable events that lose frontier status, then

$$
R=T_{\mathrm{term}}+L_{\mathrm{loss}}.
$$

This is an identity for segment counts, not a bound for all frontier events; segment lengths still need to be paid for. The structure does not prove the general linear frontier bound.

## Events with the same source are consecutive within a component

Fix one event tree and one original host source. All purely upward targets from that source lie on its host ancestor chain. If two such events belong to the same component, connectedness and injectivity of the host projection force the event path between them to follow that ancestor chain upward.

Ordinary continuation preserves the original source; a frontier replacement strictly increases its host depth. Since the endpoints have the same source, no replacement can occur between them. Thus events with a fixed source form one consecutive path within a component. Different maximal consecutive segments of the same source belong to different components. Their terminal query labels can still be comparable.

## Frontier monotonicity under connected deletion preserving the root

Here both query and host are the whole tree $F$ with common root $r$. Write $S_b(F,r)$ for all query points matching purely upward at host target $b$, and $M_b(F,r)$ for their maximal points in the query ancestor order. Empty paths are included, so each target has at least one frontier.

If a nonempty connected subtree $K\subseteq F$ contains the root, retained root paths and ancestor relations are unchanged. For every $b\in K$,

$$
S_b(K,r)\subseteq S_b(F,r),\qquad
|M_b(K,r)|\le|M_b(F,r)|.
$$

The second inequality requires an injection between maximal points; it does not assert that all old maximal points survive. For each new maximal point, choose an old maximal descendant. New maximal points are incomparable and therefore cannot choose the same descendant. This injection accounts for replacement frontiers newly exposed by deletion.

Summing over targets gives

$$
E(F,r)-E(K,r)\ge |F\setminus K|.
$$

### Adaptive choice of one maximal pendant path still has no constant cost

A maximal nonroot pendant path starts at a nonroot leaf and follows degree-two vertices inward. Delete the points before the first branch or root, retaining that branch or root. Even when the cheapest such path may be chosen, there is no uniform constant bound on frontier loss per deleted point.

Use coordinates $(x,y)$. Take integers $g,H\ge2$, put $L=H+2$, and choose root $r=(0,0)$. Form the road tree from the integer points on these segments:

- Left stem: $x=-g$, $-H\le y\le H$.
- Right stem: $x=g$, $-L\le y\le L$.
- Central bridge: $y=0$, $-g\le x\le g$.
- Left end bars: $y=\pm H$, $-2g\le x\le0$.
- Right end bars: $y=\pm L$, $0\le x\le2g$.

The central bridge joins the two stems, and two horizontal arms attach at each of their four endpoints. End bars on different stems are separated by two rows; other parts without a designated connection are at least two grid steps apart. There are no extra four-neighbor edges, so this is an induced tree. Its eight nonroot leaves give exactly eight maximal pendant paths, namely the arms, each containing $g$ removable points. The number of vertices and the required box side are

$$
N=4H+10g+5,\qquad n=\max(4g+1,2H+5).
$$

Delete any arm $P$. Write its retained attachment as $(x_s,y_s)$ and let $\sigma=\operatorname{sgn}(y_s)$. Consider the $H$ retained host targets

$$
b_t=(x_s,y_s-\sigma t),\qquad 0\le t<H.
$$

They lie outside the central bridge. Their descendants occupy only the stem toward the corresponding endpoint and its two arms. Every nonempty query root path starts horizontally; if it turns, its initial run must have length $g$. When $t>0$, a nonempty root word matching upward to the target can start only at the two arm tips. When $t=0$, other arm sources give only ancestors on the same horizontal query chain. The old frontier therefore consists exactly of two points in different root branches:

$$
M_{b_t}(F,r)=\{(-g,-\sigma t),(g,-\sigma t)\}.
$$

Deleting one arm removes exactly one of these sources. Both query points lie at $|y|<H$ and remain in the tree. The other arm tip still supplies a match, and no other descendant source can replace the removed one. Each of these targets consequently has exactly one new frontier. Monotonicity prevents a net increase at other retained targets. Including the deleted targets gives

$$
\boxed{E(F,r)-E(F\setminus P,r)\ge H+g.}
$$

This holds for all eight arms. Fixing $g=2$, every removable path has cost ratio at least $1+H/2$, which has no absolute constant bound. This disproves the adaptive pruning condition, not the overall linear frontier bound, and it is not a supercubic counterexample to the algorithm.

## Two event components can share arbitrarily many branches

The intersection of host subtrees is connected, but need not be a path. The following valid family disproves that shape restriction; it does not give a superlinear frontier lower bound.

Use row-column coordinates and directions $\mathrm N,\mathrm S,\mathrm E,\mathrm W$. Take an integer $h\ge1$ and root $r=(-4,4)$. The union of the following four classes of complete grid paths is the tree used by both query and host:

$$
\begin{array}{c|c}
\text{start}&\text{word}\\
(0,0)&\mathrm S^{4j}\mathrm W^2\mathrm S^2\mathrm W^4\quad(0\le j\le h)\\
(0,0)&\mathrm E^4\mathrm N^4\\
r&\mathrm N^2\mathrm E^2\mathrm N^{4h}\mathrm E^2\\
r&\mathrm E^4\mathrm N^2\mathrm E^2\mathrm N^{4h}\mathrm E^2
\end{array}
$$

The first class creates bent teeth spaced four rows apart. The long vertical parts of the two query root branches are four columns apart. Apart from designated prefixes and junctions, there are no extra four-neighbor edges. The graph is therefore an induced tree with

$$
N=20h+33.
$$

Write $U=\mathrm N^2\mathrm E^2$ and $B=\mathrm E^4$. Choose two query leaves and corresponding host sources:

$$
q_1^*=(-4h-6,8),\quad q_2^*=(-4h-6,12),\qquad
a_1^*=(4h+2,-2),\quad a_2^*=(4h+2,-6).
$$

Their purely upward paths to $(0,2)$ read the two query leaf words and give terminal events. Let their component host projections be $K_1,K_2$. Both contain the subtree

$$
\begin{aligned}
I_h={}&\{(y,0):0\le y\le4h\}\cup\{(0,1),(0,2)\}\\
&\cup\{(4j,-2),(4j,-1),(4j+1,-2):0\le j\le h\}.
\end{aligned}
$$

The event certificate is listed below. The table gives the query word and original source for the first component. For the second, prepend $B$ to the query word and shift the source four columns left.

| Host target | First query word | First original source |
| --- | --- | --- |
| $(4j+1,-2)$ | $\mathrm N$ | $(4j+2,-2)$ |
| $(4j,-2)$ | $\mathrm N^2$ | $(4j+2,-2)$ |
| $(4j,-1)$ | $\mathrm N^2\mathrm E$ | $(4j+2,-2)$ |
| $(y,0)$, $0\le y\le4h$ | $U\mathrm N^{4h-y}$ | $(4h+2,-2)$ |
| $(0,s)$, $s=1,2$ | $U\mathrm N^{4h}\mathrm E^s$ | $(4h+2,-2)$ |

Every listed query point is a frontier. A deeper query-chain match on the trunk would require a source beyond the lowest host tooth. On a tooth, a deeper match would require either a nonroad source or one whose upward path starts east, contradicting the first direction of that query chain. The second query chain has the same argument after removing its fixed initial horizontal run.

These events continue ordinarily along parent edges except at $(4j,-1)\to(4j,0)$ for $j<h$. There, the next query word is strictly dominated by the deeper frontier on its corresponding chain, and that dominator is unique. Following the remaining parent edges reaches the designated terminal event. Hence

$$
I_h\subseteq K_1\cap K_2,\qquad |I_h|=7h+6.
$$

This common subtree has $h$ degree-three branches at $(4j,0)$ for $0\le j<h$. Two components can therefore share arbitrarily many branch vertices as well as turns. Their terminal query labels are incomparable, consistent with the earlier disjointness lemma.

## A shared host ancestor segment requires disjoint query paths

Suppose host point $b$ is an ancestor of $c$ at distance $\ell$, and $k$ different event components contain both. Each component has a connected, injective host projection, so its events follow the entire segment from $c$ upward to $b$. Write $q_i(c),q_i(b)$ for the query labels at its endpoints in component $i$.

Every event arrow moves the query label to a strict descendant, hence

$$
q_i(c)\preceq q_i(b),\qquad
\operatorname{depth}_Q(q_i(b))-\operatorname{depth}_Q(q_i(c))\ge\ell.
$$

The points $q_i(c)$ are distinct members of the same frontier antichain $M_c$. Their descendant subtrees in the query are disjoint, so the query paths $Q[q_i(c),q_i(b)]$ are vertex-disjoint. Therefore

$$
\boxed{
\sum_{i=1}^k
\bigl(\operatorname{depth}_Q(q_i(b))-\operatorname{depth}_Q(q_i(c))+1\bigr)
\le |Q|,
\qquad k(\ell+1)\le |Q|.
}
$$

The case $b=c$, $\ell=0$ is allowed and simply counts distinct frontier points. More generally, suppose $k$ components contain a common nonempty connected subtree $K$. If the tree distance from the point of $K$ nearest the host root to its farthest point is $D$, then

$$
\boxed{k(D+1)\le |Q|.}
$$

Here $D$ is tree distance, not coordinate height. The result holds for any valid rule for choosing a dominating frontier.

It pays only for one fixed shared host segment or for the height of one common subtree. Query paths obtained from different host segments may reuse the same query points, so these inequalities cannot simply be summed. The full branching volume of the intersection is also unpaid. This local resource bound therefore does not establish the total frontier bound $E=O(N)$.

## Arbitrarily many components can share arbitrarily many branches

The earlier two-component family extends to two independent parameters. Again use row-column coordinates. Take integers $k,h\ge1$ and root $r=(-4,4)$. Query and host both use the union of these complete paths:

$$
\begin{array}{c|c}
\text{start}&\text{word}\\
(0,0)&\mathrm S^{4j}\mathrm W^2\mathrm S^2\mathrm W^{4(k-1)}\quad(0\le j\le h)\\
(0,0)&\mathrm E^4\mathrm N^4\\
r&\mathrm E^{4i}\mathrm N^2\mathrm E^2\mathrm N^{4h}\mathrm E^2\quad(0\le i<k)
\end{array}
$$

Host teeth are spaced four rows apart, and long query teeth are spaced four columns apart. Gaps at their turns prevent extra four-neighbor edges outside the designated junctions. The second path joins the upper and lower parts, so the union is still an induced tree. The three parts add $(4h+1)+4k(h+1)$, $8$, and $4(k-1)+k(4h+6)$ vertices, respectively. Thus

$$
N=8kh+4h+14k+5.
$$

The bounding box has height $8h+9$ and width $8k+3$. Write $U=\mathrm N^2\mathrm E^2$ and $B_i=\mathrm E^{4i}$. Choose query leaves and host sources

$$
q_i^*=(-4h-6,8+4i),\qquad
a_i^*=(4h+2,-2-4i),\qquad 0\le i<k.
$$

Their purely upward paths all end at $b_*=(0,2)$ and read the query root words $B_iU\mathrm N^{4h}\mathrm E^2$. The query points are leaves, giving $k$ distinct terminal events. Denote their component host projections by $K_i$.

Use the subtree $I_h$ defined above. For every $i$, the certificate on the common subtree is:

| Host target | Query word | Original source |
| --- | --- | --- |
| $(4j+1,-2)$ | $B_i\mathrm N$ | $(4j+2,-2-4i)$ |
| $(4j,-2)$ | $B_i\mathrm N^2$ | $(4j+2,-2-4i)$ |
| $(4j,-1)$ | $B_i\mathrm N^2\mathrm E$ | $(4j+2,-2-4i)$ |
| $(y,0)$, $0\le y\le4h$ | $B_iU\mathrm N^{4h-y}$ | $a_i^*$ |
| $(0,s)$, $s=1,2$ | $B_iU\mathrm N^{4h}\mathrm E^s$ | $a_i^*$ |

The extended bottom horizontal teeth contain all required sources. Each query tooth remains a chain. On the trunk, the lowest host tooth realizes the greatest matching depth; on a tooth, the listed source realizes it. A deeper match would require a missing source or an incompatible initial direction. Every listed query point is therefore a frontier.

Replacement occurs only at $(4j,-1)\to(4j,0)$ for $j<h$: the unique deeper frontier $B_iU\mathrm N^{4(h-j)}$ on the same query tooth dominates $B_iU$. Other edges continue ordinarily, and all listed events reach their designated terminal event. Consequently

$$
\boxed{
I_h\subseteq\bigcap_{i=0}^{k-1}K_i,
\qquad |I_h|=7h+6,
\qquad E\ge k(7h+6).
}
$$

The common subtree still has $h$ degree-three branches. Neither the number of sharing components nor the number of shared branches has an absolute constant bound. The construction also uses $\Theta(kh+k+h)$ road points, however, and supplies no superlinear frontier lower bound.

It also shows where the shared-segment resource bound is paid. Take $c=(4h+1,-2)$ and $b_*$, whose host distance is $4h+5$. The corresponding $k$ query paths run from the first northward vertex of each query tooth to its leaf. Each contains exactly $4h+6$ vertices, and the paths are disjoint. These separate query teeth pay for the long shared segment; reuse of query resources across different host segments remains unresolved.

## The general linear frontier bound is false

Take integers $k,h\ge1$, use row and column coordinates, and root the tree at $(0,0)$. The right comb consists of

$$
\{(y,0):0\le y\le2k-2\}
\cup\{(2i,x):0\le i<k,\ 1\le x\le2h\}.
$$

Go three steps left from the root to a trunk in column minus three, extending down to row $2(k+h)$. For each $1\le j\le h$, at row $y_j=2(k+j)$ attach a horizontal segment of length $2j$ to the left, then an upward arm of length $2(k-1)$ at its left endpoint. Use all roads as both query and host.

A later hook's vertical arm is at least two columns beyond every earlier horizontal segment's left endpoint, and its horizontal segment is at least two rows below every earlier vertical arm's bottom. All arm tops are in row four or below, away from the bridge in row zero. There are no extra four-neighbor edges or cycles. Counting gives

$$
N=4kh+h^2+4k+h+2,\qquad
n=\max\{2(k+h)+1,4h+4\}.
$$

On horizontal segment $j$, take

$$
\begin{aligned}
b_{j,\ell}&=(y_j,-3-2j+\ell),&1\le\ell\le2j,\\
q_{i,\ell}&=(2i,\ell),&0\le i<k,\\
a_{i,j}&=(y_j-2i,-3-2j).
\end{aligned}
$$

The host source-to-target path moves entirely toward the root and reads the query word $\mathrm S^{2i}\mathrm E^\ell$. These query points lie on different teeth and are incomparable. A strict descendant can only continue right. Its longer horizontal suffix would pass through the point one step left of the current hook's left endpoint, which is empty. Thus all these points are maximal frontiers, giving

$$
E\ge kh(h+1),\qquad E_{\mathrm{ns}}\ge(k-1)h(h+1).
$$

The second inequality counts only nonstraight frontiers that move down and then right. In fact these are exactly the frontiers at the designated horizontal targets. Other targets on left arms, trunk sections without teeth, the bridge, and the right comb away from the root each have one frontier; the root has two. Hence

$$
E=N+(k-1)h(h+1)+1.
$$

Setting $k=h=t$ gives

$$
n=4t+4,\qquad N=5t^2+5t+2,\qquad
E=t^3+5t^2+4t+3=\Theta(nN).
$$

The general bounds $E=O(N)$, $E_{\mathrm{ns}}=O(N)$, and even $E=O(n^2)$ are therefore false. Every fixed-capacity internal-path charging scheme equivalent to frontier linearity is also disproved.

### Complete prefixes and actual checks

Once a nonzero-column point of another query tooth has been visited, its whole root path has been visited too. Placing a current tooth point at a designated target makes a shallower old tooth require an early right turn on the left arm, whose first step is empty; an inner hook starts at least two columns farther right. A deeper old tooth requires a step past the hook's bottom, which is also empty; an outer hook lies at least two rows lower. Therefore all designated successful events in any actual discovery order come from one tooth index and number at most $h(h+1)$. Visiting one root-to-tip path first attains this count.

The direct pure-upward matching count also stays within the target scale. Each host source contributes its longest readable query prefix length plus one. A left-arm source reads to the hook's bottom, then along the horizontal segment if that distance is even. A horizontal source reads its remaining rightward segment. A right-comb tooth source reads at most three steps left. The three bridge sources read six steps in total. Summing for balanced parameters $t\ge2$ gives exactly

$$
S_{\mathrm{up}}=\frac{11}{3}t^3+\frac{19}{2}t^2+\frac{17}{6}t+8
=\Theta(nN).
$$

There are also exactly $k+h-2$ branch vertices. The existing long-branch bound gives, for every actual discovery order,

$$
W\le(6n+k+h-7)N=O(nN).
$$

This family thus closes the auxiliary route through linear unweighted frontier counts. The general direct root-path total and actual complete-prefix check total remain unresolved, as does the original logarithmic complexity gap.
