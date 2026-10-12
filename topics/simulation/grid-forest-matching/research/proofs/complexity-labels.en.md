# Intersection forests for fixed horizontal labels

**Historical research record (updated 2026-10-12).** The [standalone proof](cubic-bound.en.md) now establishes the general cubic bound. The derivations, remainders, and counterexamples below retain their historical order. Statements that a problem is unresolved refer to that stage or local method; stronger auxiliary claims do not automatically follow from the general bound.

An area potential proves $W\le2nN$ when every nonempty horizontal translation intersection of the query is connected. This covers straight comb queries with arbitrary roots and discovery orders. Section 15 also proves a host subclass with unrestricted queries: a constant bound on the multiplicity of vertical-edge column differences between consecutive rows gives $O(nN)$ scans. At the time of this investigation, the bound for general labels was unproved and general worst-case complexity lay between $\Omega(n^3+m)$ and $O(n^3\log(n+1)+m)$; the later general proof closes this gap.

## 1. Successful events and earliest stars

Let the induced road forest be $F$, with $N$ vertices in a board of side length $n$. The query root is zero, and its connected prefixes grow in first-discovery order. Write these prefixes as $P_j$. A candidate succeeds at time $j$ only when its entire translated prefix lies in the road set.

For each road target $v$, retain all successful nonroot query points and group them by:

- the first child edge from the query root;
- the row of the query point.

The earliest successful point of a group is its star $e$. Each later successful point $f$ forms a marker with that star. Define its label and late candidate by

$$
h=f-e=(0,d),\quad d\ne0,\qquad a=v-f.
$$

Alternatively, retain only global root-height records and choose the stars again. This gives the height-record variant. It does not count all successful events and must not be confused with the all-success variant.

## 2. The intersection forest and its total resource

For a fixed nonzero horizontal label, define

$$
G_h=F\cap(F-h)=\{z\in F:z+h\in F\}.
$$

This is an induced forest. The two successful prefixes of a genuine marker give

$$
a+P_f\subseteq F,\qquad a+h+P_e\subseteq F.
$$

Here a query-point subscript denotes the prefix ending at its first discovery. Since the early prefix is contained in the late prefix,

$$
\boxed{a+P_e\subseteq G_h.}
$$

Thus a marker can be associated with the directed edge $a\to a+e$ and the unique tree path joining its endpoints in the intersection forest. The entire early prefix is in the intersection, including its other branches. The associated edge need not be a grid edge.

If row $r$ contains $k_r$ road vertices, summing over all signed horizontal labels counts exactly the ordered pairs of distinct road vertices in the same row:

$$
\boxed{\sum_{d\ne0}|G_{(0,d)}|
=\sum_r k_r(k_r-1)\le(n-1)N.}
$$

Let $M_h$ be the number of markers with label $h$ in the all-success variant, and let $S$ be the total number of successful checks. There are at most four times the board side length stars per target, and each candidate fails at most once. Therefore

$$
W\le N+S\le(4n+1)N+\sum_hM_h.
$$

Consequently, a uniform constant satisfying

$$
M_h\le C|G_h|
$$

would imply

$$
W\le[4n+1+C(n-1)]N.
$$

**This fixed-label inequality remains a conjecture.** The representation and total-resource identity do not themselves bound the marker multiplicity.

## 3. An exact local condition for path capacity

Allow each marker to be assigned to any vertex of its associated path, with at most a positive integer $C$ markers assigned to each vertex. Such an assignment exists if and only if, for every nonempty connected vertex set $K$ of the intersection forest, the number of markers whose entire paths lie in $K$ is at most $C|K|$.

Necessity is immediate. For sufficiency, take any subset of markers and split the union of their paths into connected components. Each path is contained in one component, and every component is a connected subtree of the intersection forest. Applying the stated condition in each component shows that the total available vertex capacity is at least the number of markers in the subset. Replace each vertex by $C$ copies and apply Hall's theorem.

This is an equivalent formulation, not a proof of the local density bound. It is also stronger than the global inequality $M_h\le C|G_h|$: failure of local capacity need not disprove the global count. Section 9 disproves a general constant path capacity for all-success markers. That counterexample does not disprove the unit-label result or the height-record variant.

## 4. Unit horizontal displacements can be paid rigorously

**Proposition.** For $h=(0,1)$ and $h=(0,-1)$, both variants can assign their markers to distinct source vertices. Thus both satisfy unit capacity on the complete associated paths.

It suffices to prove the positive case. The intersection forest cannot contain a vertical edge: that edge and its translate one column to the right would form a unit square cycle in the road forest. Hence every intersection component is a horizontal path.

Consider a marker. Since its entire early prefix is connected, that prefix must be a horizontal interval. Write

$$
e=(0,k),\qquad f=(0,k+1).
$$

The late point is discovered later and belongs to the same first-child group, so $k\ge1$ and both points lie in the right root branch. Write the early prefix as $[-L,k]$.

For the all-success variant, take $j=1$. For the height-record variant, let $(0,j)$ be the first global root-height record in the right root branch. Since the early point is selected, this point exists and satisfies $1\le j\le k$. At its discovery, the prefix is $[-L_j,j]$, where $L_j\le L$.

Set

$$
b=v-(0,j)=a+(0,k+1-j).
$$

On the horizontal line containing these points, this candidate's entire prefix image is

$$
[a_x+k+1-j-L_j,\ a_x+k+1],
$$

which lies inside the interval already covered by the successful late candidate:

$$
[a_x-L,\ a_x+k+1].
$$

Thus this candidate genuinely succeeds at query point $(0,j)$. The event belongs to the same target, first-child group, and row as the original early event. The earliest-star condition forces $k=j$.

For the whole fixed positive unit label, the early point and the late point are therefore fixed query points. A source cannot produce two different markers. Assign each marker to its source, which lies on its associated path. Horizontal reflection gives the negative case.

This pays only the two unit labels. It does not establish the bound for other horizontal displacements.

## 5. The association graph can have arbitrarily many cycles

Acyclicity of the intersection forest does not imply acyclicity of the association graph. In the periodic family from the [historical third-arm counterexample](complexity-branches.en.md), take a multiple of three $H\ge12$. In the normalized row-column coordinates, set

$$
h=(0,6),\quad A=(-2,0),\quad B=(-4,-4),\quad w_y=(y,-4).
$$

The previously verified inner and outer markers produce

$$
A\to w_y,\qquad B\to w_y.
$$

For the height-record variant, one can take

$$
y\in\{H-2\}\cup\{H-3,H-6,\ldots,3\},
$$

giving a copy of $K_{2,H/3}$. The all-success variant works for every $3\le y\le H-2$, giving $K_{2,H-4}$.

For the all-success variant, one must additionally exclude an earlier point that is not a height record. In the original Cartesian coordinates, point $(-2,y)$ would hit $(2,y)$ using translation $(4,0)$, but the query root image $(4,-2)$ is absent. The earlier point on the zero column requires translation $(2,0)$ and misses the leaf beside the root; the extra earlier point on the top row requires translation $(5,0)$ and also misses that leaf image. The early star therefore does not move earlier. The outer early point is still the first discovered point in its row, and the complete prefixes are those of the original family.

Since $K_{2,k}$ has $2k$ edges and $k+2$ active vertices, these association graphs are neither forests nor pseudoforests as the parameter grows. Assigning each edge only to one of its two endpoints, with unit capacity, also fails. However, the same family satisfies

$$
|G_{(0,6)}|=6H.
$$

Thus it does not disprove constant linear capacity using all intersection vertices, nor the cubic conjecture for the original algorithm.

Duplicate directed edges are impossible for a fixed label: the source and endpoint uniquely determine the early point, late point, and road target. In the height-record variant, an edge and its reverse cannot both occur either. Their two root paths would have to be the same host path in opposite directions, making the distinct early points have equal root depths. Global height records have strictly increasing depths. These restrictions still allow the undirected cycles above.

## 6. Area potentials and query overlap components

Let $Q$ be the last complete query prefix with a surviving candidate, excluding a possible final point that empties the list. It is a tree that fits in a translated board. Define

$$
J_h=Q\cap(Q-h).
$$

For a grid-embedded forest $X$, choose an arbitrary potential constant in each component and define it along edges by

$$
\Phi_X(y)-\Phi_X(x)=\det(x,y).
$$

Acyclicity makes the potential well-defined. At intersection vertices, set

$$
c_h^X(z)=\Phi_X(z+h)-\Phi_X(z)-\det(h,z).
$$

Along an intersection edge, the difference between the increments of the first two terms equals the increment of the last term. Thus this value is constant on each connected component of $X\cap(X-h)$.

A marker's associated host endpoint is $w=a+e$. Its late candidate's complete prefix contains the path between the early and late points. Summing determinants along the translated path gives

$$
\boxed{c_h^F(w)=c_h^Q(e)-2\det(h,a).}
$$

The candidate need not embed the whole query intersection component. The host may be disconnected, but a successful prefix connects the relevant points, so the component potential constant cancels.

For a fixed host intersection component and query potential value, the sources lie in one horizontal row. Fixing the host endpoint and first-child group also fixes the query early point's row. The earliest star for that target, group, and row is unique, so these markers inject into their host endpoints. Different query intersection components with the same potential value can be combined in this injection.

A further fact does not require earliest stars: for a fixed candidate and label, all its marker early points lie in one query intersection component. Take two early points and their respective late points. The early candidate survives both early points, and the late candidate survives both late points. The translated images of the two connecting query paths have the same host endpoints and must coincide. Hence the whole path between the early points and its label translate belong to the query tree. That path lies in the query intersection.

## 7. A new subclass: queries with connected horizontal intersections

This section defines a separate all-success variant that groups only by query row: each target and row has one earliest successful star, without first-child splitting. Write its marker count as $\widetilde M_h$ and the number of distinct query intersection potential values as $\kappa_h$, with zero for an empty intersection. These are not the earlier four-group marker counts.

The potential argument does not require first-child grouping. Fixing a query potential value and host endpoint fixes the query early point's row. The earliest star for that target and row is unique. Therefore

$$
\boxed{\widetilde M_h\le\kappa_h|G_h|.}
$$

There are now at most the board side length stars per target, so

$$
\boxed{W\le(n+1)N+\sum_h\kappa_h|G_h|.}
$$

If every nonempty query intersection $J_h$ is connected, then $\kappa_h=1$, yielding

$$
\boxed{W\le2nN.}
$$

More generally, if every nonempty query intersection has at most $b$ potential values, then

$$
W\le[n+1+b(n-1)]N.
$$

A uniform constant bound on the number of connected components is sufficient. These conditions concern the final effective query tree. They allow any root and discovery order, and the host forest may branch arbitrarily.

For a concrete example, take a complete horizontal spine with arbitrarily long straight teeth extending upward or downward in its columns, subject to the induced-tree requirement. Each column is an integer interval containing the spine row. The column range of a horizontal intersection is the overlap of the two spines, and each intersection of vertical intervals still contains the spine row. Thus every nonempty intersection is connected.

These straight comb queries satisfy the cubic bound on every road forest, regardless of the starting point or how visits to the spine and teeth are interleaved. Every connected subtree is again such a comb or a single straight tooth, so failure after a partial visit does not invalidate the result. Rotating coordinates and using vertical labels with column stars gives the corresponding vertical-spine subclass.

Events count only first discoveries of nonroot points; revisits contribute to the move count. A final check that empties the candidate list is included in the allowance of at most one failure per candidate. The bound also holds directly when there are no successful nonroot events.

## 8. Resources on both sides and the remaining gap

The query side has a total-resource bound as well:

$$
\sum_{d\ne0}|J_{(0,d)}|\le(n-1)|Q|\le(n-1)N.
$$

Each marker may be represented by a bipartite edge from its early query point to its associated host endpoint. A constant bound using all intersection vertices on both sides would also remove the general logarithmic gap. This total bound remains unproved.

The bipartite graph need not be a forest: in the periodic family, one host endpoint already has two query early points. Duplicate the host into two nonadjacent road components while keeping the query unchanged. This gives a four-cycle. Complete prefixes are connected, so successful candidates for an old target must remain in its original component, preserving the earliest stars. This counterexample does not disprove the total bound using all intersection resources on both sides.

Another sufficient, weaker form is

$$
M_{(0,d)}\le C N\left(1+\log\frac n{|d|}\right),
\qquad 1\le|d|\le n-1.
$$

Indeed,

$$
\sum_{d=1}^{n-1}\log\frac nd
=n\log n-\log(n!)\le n-1,
$$

so the total over positive and negative labels would still be at most $4C(n-1)N$. This scale-dependent form is also unproved.

Complete-path assignments succeeded on the earlier fixed examples, but the infinite family in Section 9 disproves a general constant path capacity. Assignments using each marker's entire early prefix, or direct bounds on the whole label resource, remain possible directions. These reductions do not change the scanning algorithm or the problem constraints.

The two resource targets are asymptotically equivalent: the final effective query has a complete valid translate, so

$$
a_0+Q\subseteq F\quad\Longrightarrow\quad
a_0+J_h\subseteq G_h,\qquad |J_h|+|G_h|\le2|G_h|.
$$

Resources on both sides may help construct an assignment, but they do not weaken the whole-label counting target.

## 9. No uniform complete-path capacity for all-success markers

This section uses Cartesian coordinates. Take integers
$$
k\ge2,\qquad H=2k,\qquad d=2k+2,\qquad h=(d,0).
$$

The query root is the origin. A vertical spine has long teeth at positive even heights:
$$
Q=\{(0,y):0\le y\le H\}
\cup\{(x,2i):1\le i\le k,\ 0\le x\le d+k\}.
$$

First visit the teeth from bottom to top: move two steps up the spine, move right by $k$ steps, and return. At the top, visit the teeth from top to bottom, traversing each full tooth and returning to the spine before moving two steps down. The walk ends at the root. The roads are
$$
\begin{aligned}
F={}&\{(0,y):-H\le y\le H\}
\cup\{(d,y):-H\le y\le0\}\\
&\cup\{(x,-2i):1\le i\le k,\ 0\le x\le k\}\\
&\cup\{(x,-2i):1\le i\le k,\ d\le x\le d+k\}\\
&\cup\{(x,2i):0\le i<k,\ 0\le x\le d+k\}.
\end{aligned}
$$

The two spines are joined only by the long tooth at height zero. The left and right short teeth have a gap between them on negative even rows, and there is no right spine at positive heights. Consecutive teeth have an empty row between them. Thus the listed edges form an induced tree, with no extra adjacency creating a cycle. The query is also an induced tree. Including every return step gives
$$
N=5k^2+8k+1,\quad |Q|=3k^2+4k+1,\quad
n=4k+1,\quad m=8k^2+8k.
$$

Shifting the final query down two steps embeds it in the roads, so a candidate survives throughout. Define
$$
\begin{aligned}
1\le i\le k,\quad&0\le j\le k,\\
e_{ij}=(j,2i),\quad& f_{ij}=(d+j,2i),\\
a_i=(0,-2i),\quad&c_i=(d,-2i),\\
w_j=(j,0),\quad&v_j=(d+j,0).
\end{aligned}
$$

At the early point, the early candidate maps the current spine into the right spine, lower short teeth into negative even right teeth, and the current tooth to height zero. At the late point, the late candidate maps the full spine into the left spine and every short tooth into a corresponding short or long tooth. Previously extended higher teeth land on positive even long teeth, and the current tooth lands at height zero. Both **complete historical prefixes** are valid.

Earlier points in the same query row lie strictly to the left of the designated early point. To hit the same target, their candidate roots would lie strictly beyond the right spine at negative even height. The first query step goes up to a missing negative odd row, so those candidates have failed. The designated early point is the genuine earliest star. The root has one child, so both the row-only and old four-group variants produce these markers.

Each associated path goes from its source up the left spine to height zero, then right to its associated endpoint. Their union is
$$
K=\{(0,y):-2k\le y\le0\}\cup\{(x,0):1\le x\le k\},
\qquad |K|=3k+1.
$$
Consequently,
$$
C\ge\frac{k(k+1)}{3k+1}\longrightarrow\infty.
$$

This disproves any uniform constant capacity restricted to each marker's own complete path. It does not disprove the whole-label bound: row counts and candidate spine restrictions give
$$
\widetilde M_h=M_h=k(k+1),\qquad |G_h|=2k^2+3k.
$$

A late candidate's spine must lie on the left spine. The early prefix requires a downward shift of at least the current tooth index, while the late prefix requires at most that index. Each query pair is therefore produced by exactly the specified candidate.

This family even admits a unit assignment to the entire early prefixes:
$$
z_{ij}=(j,2-2i)=a_i+(j,2)\in a_i+P_{e_{ij}}\subseteq G_h.
$$

At the current early discovery, the relevant part of the first tooth has been visited. Different index pairs give different road vertices. These resources include old teeth outside the associated paths. A general capacity theorem for entire early prefixes remains unproved.

The family does not produce the same number of global height-record markers. Nor does it disprove the original algorithm's bound: its query is a vertical comb covered by the rotated theorem of Section 7. See the [research certificate](../examples/local-path-capacity.zh.md) for the general construction and fixed-input validation.

## 10. Even the smaller of the two potential budgets can be quartic

The inequality in Section 7 is valid, but its potential-weighted budget has no uniform cubic bound. Return to row-column coordinates and take
$$
k\ge2,\qquad b=2k+4.
$$

Construct two orthogonal combs:
$$
\begin{aligned}
A={}&\{(r,0):0\le r\le2k\}
\cup\{(2i,c):0\le i\le k,\ 0\le c\le2k\},\\
B={}&\{(b,c):b\le c\le4k+4\}
\cup\{(r,b+2i):0\le i\le k,\ b\le r\le4k+4\}.
\end{aligned}
$$

Join the bottom of the first comb to the left end of the second by a vertical segment followed by a horizontal segment:
$$
(2k,0)\longrightarrow(b,0)\longrightarrow(b,b).
$$

The combs are separated by four grid units, and the connector meets each only at its endpoint. The result is an induced tree. Use it as both query and road tree, root it at the origin, and follow any complete depth-first traversal. Then
$$
n=4k+5,\qquad N=4k^2+10k+9,\qquad m=2(N-1).
$$

Each positive horizontal displacement gives distinct potential values on the first comb's horizontal teeth. The second comb's vertical teeth give the analogous result for vertical displacements. Specifically,
$$
1\le d\le k:\qquad
\kappa_{(0,d)}\ge k+1,\quad |G_{(0,d)}|\ge(k+1)(2k-d+1).
$$

A horizontal tooth lies at twice its index, and its potential value is four times its index times the displacement. These values are distinct. Swapping coordinates gives distinct values in the vertical case too; the common path to the second comb adds only a potential constant.

Write the horizontal and vertical budgets as
$$
B_H=\sum_{d\ne0}\kappa_{(0,d)}|G_{(0,d)}|,
\qquad B_V=\sum_{d\ne0}\kappa_{(d,0)}|G_{(d,0)}|.
$$

Positive and negative labels pair up, so
$$
B_H,\ B_V\ge
2(k+1)^2\sum_{d=1}^k(2k-d+1)
=k(3k+1)(k+1)^2=\Omega(k^4),
\qquad nN=\Theta(k^3).
$$

Choosing the smaller directional budget cannot remove this extra factor. This disproves only the bound on the coarse budget, not the cubic bound on actual scans. Full counts are in the [orthogonal double-comb certificate](../examples/orthogonal-combs.zh.md).

## 11. Genuine time restrictions across query components

Use the row-only all-success variant of Section 7 throughout the following sections. Let $t(q)$ be a query point's discovery index. For any genuine marker,
$$
R_{e,f}=P_{t(e)}\cap(P_{t(f)}-h)
$$
is connected and contains the early point. To prove it, translate:
$$
(a+h)+R_{e,f}
=((a+h)+P_{t(e)})\cap(a+P_{t(f)}).
$$

Both valid host subtrees on the right contain the target. Unique paths in the forest make their intersection connected. Thus every translated query pair whose early and late indices are no greater than this marker's corresponding indices belongs to the same final query intersection component.

In particular, any two markers with the same label but different intersection components satisfy strict reverse order:
$$
t(e_1)<t(e_2)\quad\Longrightarrow\quad
t(e_1)<t(e_2)<t(f_2)<t(f_1).
$$

This applies across targets and candidates and does not require height records. There is no such restriction within one component, so it does not make all markers one nested chain.

Once the query first reaches the signed displacement point, the root belongs to the prefix intersection too. Thus, if the displacement lies in the query and the late index is at least its discovery index, the early point belongs to the root component of the query intersection. All root-component markers jointly inject into host endpoints. Nonroot-component markers must finish before the first visit to that displacement. The opposite displacement cannot replace this cutoff.

## 12. A common cut leaves two fixed disjoint query subtrees

Fix a label with at least one marker. Take the latest-discovered early point and define
$$
t_*=\max_{\text{markers}}t(e),\qquad P=P_{t_*},
\qquad I=P\cap(P-h).
$$

Both candidates of a marker realizing this latest early point match the entire common prefix. The union of the prefix and its translated copy therefore embeds in the roads and is an induced forest. Their intersection is connected or empty, and so is the old intersection.

If a late point already lies in the common prefix, its early point lies in the old intersection. For a marker crossing the cut, suppose the late candidate's common-prefix image meets the early candidate's early-prefix image. There is then a point with
$$
x\in P_{t(e)},\qquad x+h\in P.
$$

The two complete valid host prefixes contain both the intersection point and the marker target. Unique paths force the query path from that point to the early point, and its translated copy, to exist. Hence the early point connects to the final query component containing the old intersection. Completed markers and these touching markers **together** cost only one host-intersection size.

The touching condition is independent of the candidate position: it holds exactly when the early prefix meets the old intersection. Define
$$
\tau=
\begin{cases}
\min_{q\in I}t(q),& I\ne\varnothing,\\
t_*+1,&I=\varnothing,
\end{cases}
\qquad R=P_{\tau-1},
$$
where the prefix with index minus one is empty. Every unpaid marker satisfies
$$
\boxed{
e\in R\subseteq P,\quad f=e+h\in R+h,\quad
P\cap(R+h)=\varnothing,\quad t(e)\le t_*<t(f).
}
$$

All late candidates still match the same common prefix; early candidates may have died before the cut. Denoting the remaining marker count gives
$$
\boxed{\widetilde M_h\le |G_h|+\widetilde M_h^{\rm separated}.}
$$

If the signed displacement lies in the common prefix, the old intersection contains the root and the remaining prefix is empty. Thus
$$
h\in P\quad\Longrightarrow\quad \widetilde M_h\le |G_h|.
$$

In general, the static template product bound yields only
$$
|R|\le |P|-|I|,\qquad
\widetilde M_h^{\rm separated}
\le |A(P)|\,|R|
\le (2n-1)N\frac{|R|}{|P|}.
$$

A joint bound for these remainders across labels is still missing. Section 9 shows that road resources must allow old branches outside the associated paths. Section 10 shows that paying the entire intersection separately for each potential type is too coarse. The general logarithmic gap remains.

## 13. Entire early prefixes and families without repeated early points

Continue using row-only all-success markers. Each marker may now use its entire early prefix:
$$
S_{a,e}=a+P_{t(e)}\subseteq G_h.
$$

This is a connected subtree. The Hall argument from Section 3 gives an exact condition for a positive integer capacity: the number of resources wholly contained in any nonempty connected subtree must not exceed its total capacity:
$$
\#\{(a,e,f):S_{a,e}\subseteq U\}\le C|U|
\qquad\text{for every connected }U\subseteq G_h.
$$
This is stronger than bounding the marker count for the whole label. The general statement remains unproved.

A useful rigorous case is that **any marker family with distinct query early points admits unit capacity**. Take any subset. The complete prefix of its latest early point already contains all the selected distinct nonroot early points and the root. That one resource has strictly more vertices than the subset has markers. Every subset satisfies Hall's condition.

Markers from one source have distinct early points. Markers of one query potential type inject directly into host endpoints. Difficulty must therefore involve multiple sources, multiple types, and repeated early points simultaneously. These features are not mutually exclusive within one host intersection component: a legal mixed example is given in the [construction certificate](../examples/mixed-types.zh.md).

## 14. Vertical edges per row bound entire-prefix capacity

Use row-column coordinates. For a nonempty connected subtree, define the largest number of vertical edges between consecutive rows:
$$
b(U)=\max_r\#\{c:(r,c),(r+1,c)\in U\}.
$$

**Theorem.** Genuine markers whose entire resources lie in this subtree admit capacity at most
$$
1+b(U).
$$

Let the first vertical-edge time be the first discovery outside the root's horizontal row. Before that time, every complete query prefix lies on the root row. All these early points have query row zero. Earliest row stars make their associated host endpoints distinct, giving unit capacity for this part.

The first vertical edge and its endpoints are fixed:
$$
q\longrightarrow q+\delta,\qquad
\delta\in\{(1,0),(-1,0)\},\qquad q_r=0.
$$
From that time onward, every early prefix contains this edge. Fix a query early point. Since the resources lie in one host intersection component, the area identity
$$
c_h^F(a+e)=c_h^Q(e)-2\det(h,a)
$$
uniquely determines the row of every corresponding source. The host image of the first vertical edge,
$$
a+q\longrightarrow a+q+\delta,
$$
must therefore start on the same host row in the same direction. The number of choices is at most the subtree's vertical-edge parameter. The image edge uniquely determines the candidate source and marker. Each early point consequently occurs at most that many times in this second part.

Split the second part by occurrence rank of each early point, making each group have distinct early points. Section 13 gives unit capacity per group. Adding the first part proves the theorem. If the first query step is vertical, the first part is empty and the capacity improves to
$$
b(U).
$$

The proof retains the original complete prefixes and genuine stars. It never deletes late history outside the subtree. An empty part costs no capacity. A horizontal straight path has only the first part, and a vertical straight path has only the second; both admit unit capacity. A vertically monotone path crossing each pair of consecutive rows at most once admits capacity at most two. An arbitrary path with repeated row crossings has no such parameter restriction.

Each resource lies wholly in one host intersection component, so
$$
\widetilde M_h\le
\sum_{K\in\operatorname{comp}(G_h)}[1+b(K)]|K|.
$$
The parameter can grow on general forests, so this does not settle the general bound.

## 15. A new host subclass: bounded multiplicity of vertical-edge column differences

For each pair of consecutive road rows, collect the columns of the vertical edges joining them:
$$
C_r=\{c:(r,c),(r+1,c)\in F\}.
$$
Suppose that for every row and every nonzero signed column difference,
$$
|C_r\cap(C_r-d)|\le b\qquad(d\ne0).
$$
This constant bound concerns the roads. It does not restrict the query root, discovery order, or branching.

For a fixed horizontal label, the vertical-edge columns of the host intersection are exactly the translated column-set intersection:
$$
h=(0,d),\qquad
\{c:(r,c),(r+1,c)\in G_h\}=C_r\cap(C_r-d).
$$
Thus every intersection component has vertical-edge parameter at most the given constant. Apply Section 14 and sum over all signed labels:
$$
\boxed{
\widetilde M_h\le(b+1)|G_h|,\qquad
W\le[(b+2)n-b]N.
}
$$
This proves cubic time for arbitrary queries on this host subclass. If the first query step is vertical, the stronger bound is
$$
W\le[n+1+b(n-1)]N.
$$
A final check that empties the list is still paid by at most one failure per candidate. Revisits count toward the actual move count.

### A dense tree family with more than linearly many forks

Take any odd prime and define
$$
p\ge3,\quad
a_i=2pi+(i^2\bmod p)\quad(0\le i<p),\quad
H=2p^2,\quad w=p-1.
$$
The roads consist of a horizontal base in row zero, full vertical spines in these columns, and short rightward teeth on positive even rows:
$$
\begin{aligned}
F={}&\{(0,c):0\le c\le2p^2-p\}\\
&\cup\{(r,a_i):0\le i<p,\ 0\le r\le H\}\\
&\cup\{(2j,a_i+x):0\le i<p,\ 1\le j\le p^2,\ 1\le x\le w\}.
\end{aligned}
$$
Consecutive spines are separated by at least the prime plus one grid units. Each tooth has length the prime minus one, leaving an empty column before the next spine. Teeth have an empty row between them. The base joins the spines only at their bottom endpoints. The result is an induced tree.

Nonzero differences of spine columns are unique. If two column differences agree, the difference of their remainder terms has absolute value less than twice the prime. The index differences must first agree. Reducing modulo the prime and using the nonzero difference and invertibility of two then determines both indices:
$$
a_i-a_j=a_u-a_v,\quad i\ne j
\ \Longrightarrow\
i-j=u-v,\quad
(i-j)(i+j)\equiv(u-v)(u+v)\pmod p
\ \Longrightarrow\ (i,j)=(u,v).
$$

Every consecutive row pair has exactly these spine columns as its vertical-edge set, so the multiplicity parameter is one. The exact sizes are
$$
n=2p^2+1,\qquad
N=p^4+p^3+2p^2-p+1,\qquad
B=p^3-1.
$$
Count road vertices as the base, new spine vertices, and new tooth vertices. Count forks at the positive even nontop rows of every spine, plus the base junctions at every spine except the first.

Consequently,
$$
N=\Theta(n^2),\qquad B=\Theta(n^{3/2}),\qquad
W\le(3n-1)N.
$$
This is a dense single road component beyond the earlier condition of only linearly many forks per component. The bound holds for all queries, independently of any example traversal.

## 16. Early points on one connected vertical query segment admit unit capacity

Fix one connected vertical segment of the query tree and take only markers with early points on it. Use the smaller resources
$$
T_{a,e}=a+(P_{t(e)}\cap V)\subseteq S_{a,e}.
$$
The query prefix and the segment are connected subtrees of a tree. Their intersection contains the early point and is therefore a nonempty vertical segment.

Keep only vertical edges in the host intersection and split it into disjoint vertical segments. Each smaller resource lies wholly in one segment. Fixing that host segment and a query early point fixes the source row by the area identity. Subtracting the query segment's column from the host segment's column fixes the source column as well. Thus an early point occurs at most once in that host segment.

Take any subset of its markers. The prefix intersection for the latest early point contains every selected distinct early point. Its resource has at least as many vertices as the subset has markers, proving Hall's condition. Different host segments are disjoint, so combining their assignments preserves unit capacity. The query root need not lie on the chosen segment, and all old branches remain part of the success conditions.

Early points in one query horizontal row inject directly into host endpoints. Hence if the early points can be covered by $u$ query horizontal rows and $v$ connected query vertical segments, entire-prefix capacity is at most the number of covering pieces:
$$
C\le u+v.
$$
For overlapping covers, first assign each marker to one piece. This parameter can grow on general queries and is not a uniform constant.

## 17. Collinear candidate sources admit unit capacity

Fix a horizontal label. Any genuine marker family whose candidate sources are collinear admits a unit assignment using entire early prefixes.

First restrict to one host intersection component. If the source line is horizontal, the area identity makes all query potential types equal, so the row-only endpoint injection from Section 7 gives the assignment. If the line is not horizontal, fixing an early point fixes the source row by the area identity. The line meets that row at most once. Early points are therefore distinct, and Section 13 proves unit Hall.

Resources in different host intersection components are disjoint, so their assignments combine. The line need not be parallel to a grid axis, and early points on the root row are allowed. However, splitting arbitrary sources into multiple lines can reuse the same resources. A bound allowing the costs of all such groups to be added is still missing.

## 18. Connected resource intersection graphs can still mix types

The mixed behavior in Section 13 persists even when actual resources connect through shared vertices. One fixed valid instance has
$$
n=30,\qquad N=118,\qquad |Q|=60,\qquad m=126,\qquad W=421.
$$
In row-column coordinates, its label and counts are
$$
h=(0,20),\qquad \widetilde M_h=14,\qquad
\left|\bigcup S_{a,e}\right|=31.
$$
It has two query potential types and three early points occurring twice each. One resource shares a vertex with every other resource, giving a spanning star in their intersection graph. Thus even a connected component of this graph cannot always be classified as having one type or having no repeated early points.

The fourteen markers still admit assignments to fourteen distinct vertices in their own resources. This example therefore disproves neither entire-prefix Hall nor the cubic algorithm bound. The [construction proof](../examples/connected-resources.zh.md) gives all road coordinates, the actual walk, genuine earliest stars, and an explicit assignment.

## 19. Commutation and axis length for a repeated early point

Fix a host intersection component and take two genuine markers with the same early and late points but different sources:
$$
K\in\operatorname{comp}(G_h),\qquad
(a,e,f),\ (b,e,f),\qquad a\ne b.
$$
All relevant roads belong to one host tree. Complete late prefixes connect their early and late endpoints, while their resources attach to the same intersection component.

### Direction words imply commutation

Record road paths using east-west and north-south inverse letter pairs. A simple tree path has no immediate reversal, so its direction word is reduced. Rooting at one host vertex embeds the road tree isometrically in the free group's Cayley tree. A direction-preserving translation between connected road subtrees is represented by one left multiplication.

Let one left multiplication represent the horizontal translation of the intersection component and another the translation between the complete late prefixes:
$$
g:K\longrightarrow K+h,\qquad
T:a+P_f\longrightarrow b+P_f.
$$
The complete prefixes supply all four corners at the early image:
$$
w=a+e,\qquad
gT(w)=b+f=Tg(w).
$$
Left multiplications agreeing at one vertex have the same group element. Hence
$$
\boxed{Tg=gT.}
$$
The query root belongs to each complete prefix, so also
$$
T(a)=b.
$$
Their grid displacements are the nonzero horizontal label and the nonzero source difference. Both maps are therefore nonidentity. This proof uses no private endpoint and is unaffected by the root-row exception.

### Sources for one early point require distinct axis projections

A nonidentity free-group left multiplication has a unique doubly infinite translation axis, denoted by $L$. Write its element as a conjugate of a nonempty cyclically reduced word. Repeat this word in both directions, then left-translate by the conjugating prefix to obtain the original map's axis. A vertex's displacement length equals the axial translation length plus twice its distance from the axis, which also proves uniqueness.

Commutation makes the map between sources preserve this axis. It cannot reflect the axis, since reflection reverses a nonzero translation. It cannot fix the axis pointwise, since a free left multiplication fixing a vertex is the identity. Thus it translates the axis by a nonzero integer distance. Different sources for the same early point have equal distances from the axis and distinct projections onto it.

Take at least two such markers whose complete resources lie in one connected subtree. Write their common distance from the axis and the span of their projections as
$$
k\ge2,\qquad S_{a,e}\subseteq U\subseteq K,\qquad
r_e=\operatorname{dist}(a,L),\qquad
D=\max_{a,b}\operatorname{dist}(\pi_L(a),\pi_L(b)).
$$
A connected subtree contains the unique path between any two sources. The entire axis need not belong to the roads, but these paths force the axis segment between projections and each source-to-axis segment to lie in the subtree. Off-axis segments attached at distinct projections are disjoint. Consequently,
$$
\boxed{|U|\ge k r_e+D+1\ge k(r_e+1).}
$$
The requirement of at least two markers is necessary: a single source need not have its source-to-axis segment contained in the resource.

This bounds repetitions of one fixed early point only. Different early points may reuse the same source-to-axis segment, so their bounds cannot yet be added. General entire-prefix capacity and a linear total for each fixed label remain unproved.

## 20. Bounded axial repetition gives constant capacity for the remainder

Section 27 improves the constant by grouping resource left endpoints instead of source projections. The original proof is retained here.

Section 12 splits the markers for one label into one intersection cost and a remainder after a common cut. Every remaining marker has an entire early resource disjoint from its label translate:
$$
S\cap(S+h)=\varnothing.
$$
Its early point lies in the earlier prefix, so its entire early prefix lies there too. The translate of that earlier prefix is disjoint from the common late prefix. All candidate history is retained.

### The shortest axial period and the groups

Fix a host intersection component containing remaining markers. Give the axis from Section 19 integer coordinates with the map translating in the positive direction. The signed axial displacements of all free-group left multiplications commuting with this map form a nonzero subgroup of the integers. A zero displacement fixes an axis vertex and hence is the identity. Thus a smallest positive axial displacement exists, and
$$
\ell_g=q_K\ell_0,\qquad q_K\in\mathbb Z_{\ge1}.
$$
This integer is the power exponent of the translation word, not its horizontal grid distance. The appropriate power of the left multiplication with the smallest positive displacement agrees with the original map on the axis and therefore equals it. Summing grid displacements also gives
$$
q_K\mid |d|,\qquad 1\le q_K\le |d|
\qquad\text{when }h=(0,d).
$$
A general instance therefore does not automatically have bounded power exponents.

Group candidate sources by half-open intervals of their axis projections:
$$
[j\ell_0,(j+1)\ell_0),\qquad j\in\mathbb Z.
$$
Different sources for the same early point have projection differences equal to nonzero integer multiples of the shortest axial displacement. Each group therefore has distinct early points. Section 13 gives a unit assignment within each group using entire resources.

### A road vertex can be used by only a bounded number of groups

If a connected resource misses the axis, its projection is one vertex. If it meets the axis, its projection equals its intersection with the axis. Disjointness from its translate gives, in either case,
$$
\operatorname{diam}\pi_L(S)\le\ell_g-1=q_K\ell_0-1.
$$
The source itself belongs to the resource. Thus any road vertex in that resource satisfies
$$
z\in S_{a,e}\quad\Longrightarrow\quad
|\pi_L(z)-\pi_L(a)|\le q_K\ell_0-1.
$$
The allowed source-projection interval meets at most
$$
2q_K+1
$$
group intervals. Each group already has a unit assignment, so summing the assignments bounds the load at this vertex by the same number. The whole axis need not lie in the roads; only vertices of the resources receive charges.

Remaining markers in this component consequently admit that capacity. Taking the smaller value with the vertical-edge capacity from Section 14 gives
$$
\boxed{
\widetilde M_h
\le |G_h|+
\sum_{K\in\operatorname{comp}(G_h)}
\min\{1+b(K),\,2q_K+1\}|K|.
}
$$
Only components containing remaining markers need to be included in the sum; take the summand as zero for the others. The single intersection cost still jointly pays for completed markers and markers touching the common prefix.

In particular, if the exponents for all relevant labels and components have a uniform constant bound, then
$$
q_K\le q_0
\quad\Longrightarrow\quad
\widetilde M_h\le(2q_0+2)|G_h|,\qquad
W\le[(2q_0+3)n-(2q_0+1)]N.
$$
If none of the relevant translation words is a nontrivial power of a shorter word as a free-group element, this gives
$$
q_0=1\quad\Longrightarrow\quad W\le(5n-3)N.
$$
This is a rigorous conditional bound. Both the exponent and the vertical-edge parameter can grow in general. The weighted sum of their smaller values remains uncontrolled. In particular, arbitrary horizontal translations must not be assumed to have exponent one.

## 21. Entire early resources inside any local path admit capacity four

**Theorem.** Fix a label and a host intersection component. Restrict to genuine markers whose entire early resources lie inside one nonempty simple path. Then
$$
U\subseteq K\in\operatorname{comp}(G_h),\qquad
S_{a,e}\subseteq U
\quad\Longrightarrow\quad C_U\le4.
$$
The path may repeatedly change direction, and the query root may lie inside the prefix. Resources need not be disjoint from their label translates, and the axial exponent is unrestricted. The condition concerns the entire early prefix, so the counterexample in Section 9 for associated root paths does not apply.

Give the common axis from Sections 19–20 integer coordinates and write its smallest positive period as
$$
p=\ell_0.
$$
Maps between different sources for the same early point preserve this axis and translate it by nonzero integer multiples of the smallest period.

### Two off-axis tails each cost one unit

If the whole path projects to a single axis vertex, two different sources for one early point cannot both lie in it. All early points are distinct, so Section 13 gives unit capacity.

Otherwise the intersection with the axis is a nondegenerate interval. There are at most two off-axis tails, attached at its endpoints. Resources touching the same tail cannot repeat an early point. Otherwise a nonzero axial translation maps one resource to the other, and their nonempty sets of off-axis projections satisfy
$$
A,\ A+\Delta\subseteq\{\alpha,\beta\},\qquad
\Delta\ne0,
$$
while sharing the chosen tail's attachment point. For a singleton, sharing a point forces zero translation. A two-element set cannot translate nontrivially while remaining in the same two-element set either.

Assign off-axis resources to their touched tails, choosing one if both are touched. Each of the two groups has distinct early points and a unit assignment using entire resources. Together they cost capacity two. These assignments may use the resources' axial parts.

### Short axial resources cost one unit

All remaining resources lie on the axis. Their first-discovery indices satisfy
$$
j=t(e)=|P_{t(e)}|-1\ge1.
$$
This is also the number of axis edges in the resource. First take the short-resource family $\mathcal S_{<p}$ and count it inside an arbitrary axis interval:
$$
j<p,\qquad |V|=\nu.
$$
For a fixed early point, all copies have the same axis orientation and the same relative source position. Fitting the resource in this interval allows a source interval with
$$
\nu-j\qquad(j<\nu)
$$
vertices. Different sources for that early point are separated by nonzero multiples of the smallest period, so their count is at most the ceiling of this quantity divided by the period. Each first-discovery index identifies at most one early point. Thus
$$
\#\{S\in\mathcal S_{<p}:S\subseteq V\}
\le\sum_{j=1}^{\min(p-1,\nu-1)}
\left\lceil\frac{\nu-j}{p}\right\rceil
=\nu-\left\lceil\frac{\nu}{p}\right\rceil
\le\nu-1.
$$
The class is empty when the period is one. Any subfamily's union splits into disjoint axis intervals. Applying the bound in each interval proves Hall and unit capacity.

### Long axial resources have sources on one row and cost one more unit

For the remaining long resources, take the marker with the earliest discovery index and its prefix. Every later long resource contains a complete copy of that prefix, and all these copies lie on the same axis:
$$
j\ge p,\qquad a_*+P_*\subseteq L,\qquad a+P_*\subseteq L.
$$
The left multiplication between copies makes the axis and its image share at least one full period of consecutive edges. Both doubly infinite direction sequences have that period. Reading the shared segment in one direction, agreement for a full period uniquely determines both infinite extensions. Hence
$$
T(L)=L.
$$
This argument also covers oppositely oriented copies. An axis-preserving left multiplication cannot reflect it: reflection would fix a vertex or reverse an edge, both impossible for this free-group action. It therefore translates the axis and commutes with the label map. The grid displacement of the smallest axial period is horizontal, so all these sources lie on one row. Section 17 gives unit capacity.

Adding the four group assignments proves capacity four. Resources lying entirely on the axis need only capacity two. The proof retains early points on the root row and uses no private-endpoint assumption.

If every intersection component for one label is a path, then
$$
\widetilde M_h\le4|G_h|.
$$
If this holds for all labels, then
$$
W\le(5n-3)N.
$$
That host condition already falls within the earlier linear-fork subclass. There can be at most four fork vertices in each row: there are only four triples of neighbor directions, and two vertices in one row sharing a triple would create a fork in their displacement intersection. The new result here is the capacity bound for an arbitrary local path; the all-label corollary must not be presented as a new subclass with superlinearly many forks.

General branching resources cannot simply be split up to apply this section, because the pieces may no longer contain complete early prefixes.

## 22. Unions of axial groups cannot simply be added

The separate assignments in Section 20 may count resources repeatedly. Take a positive even parameter and use horizontal-vertical coordinates:
$$
s\ge4,\qquad h=(2s,0).
$$
The roads are the full horizontal axis from zero to five times the parameter, with one upward leaf at each even horizontal coordinate from the parameter to five times it. The actual query walk and sizes are
$$
E^sNS\,E^{2s}N,\qquad
N=7s+2,\qquad m=3s+3.
$$
The leaves have empty columns between them, so there is no induced cycle.

The first point in the new row and the second leaf form a genuine early-late pair. Every even source from zero to twice the parameter matches both complete prefixes. Its resource is a horizontal interval with one leaf:
$$
e=(s,1),\quad f=(3s,1),\quad
a=(j,0),\quad j\in\{0,2,\ldots,2s\}.
$$
This subfamily already has the parameter plus one markers. The complete row-only count must also include root-row markers, giving
$$
\widetilde M_h=\frac{5s}{2}+1,\qquad |G_h|=4s+2.
$$
The smallest axial period is one, and different sources belong to different groups. Write the resource union in group $j$ as $\mathcal R_j$. The largest number of groups using one road vertex and the sum of their resource-union sizes are
$$
\max_z\#\{j:z\in\mathcal R_j\}=\frac s2+1,\qquad
\sum_j|\mathcal R_j|=s^2+4s.
$$
The number of participating groups at one vertex has no constant bound, and the sum of group resource unions is not bounded by a constant times the actual resource total.

However, all sources lie on one row, so the genuine markers inject directly into distinct associated endpoints. The family still admits unit capacity, and its exact scan count is
$$
W=\frac{15s^2+21s+6}{2}.
$$
It disproves only the coarse group cost, not general Hall or the algorithm bound. The [construction certificate](../examples/overlapping-bands.zh.md) checks complete prefixes, earliest stars, the original program, and independent answers for three fixed parameters.

## 23. A budget for high-power components and the general remainder

### An intersection component is a complete translated intersection of one road tree

Fix a host intersection component containing genuine markers. It and its label translate belong to the same road tree. Embed that tree in the direction-word Cayley tree and denote it as below. The common label left multiplication satisfies
$$
K=C\cap g^{-1}C.
$$
The right side is a nonempty intersection of two convex subtrees and is therefore connected. It contains the original component. Every vertex in it also has its left-multiplied image in the roads, with grid displacement equal to the label. Thus all these vertices belong to that same host intersection component, proving equality.

Let the left multiplication's axis meet the road tree in a finite interval. Then
$$
A=C\cap L,\qquad
\pi_L(K)=K\cap L=A\cap g^{-1}A.
$$
Indeed, the unique road path between an intersection vertex and its image contains their two source-to-axis paths and the intervening axis segment. The two source-to-axis paths are themselves left translates, so the original one lies entirely in the intersection. Every intersection vertex therefore has its axis projection in the intersection.

Consequently, a road tree, an axis with horizontal grid period, and a signed power exponent determine at most one such component. If the axis intersection is one vertex, all sources have the same projection. Early points cannot repeat, giving unit capacity for the whole component.

### Distinct long axes have a linear repetition budget

We use an existing result: in a deterministic edge-labeled rooted tree with at least one edge, the sum of exponents of maximal repetitions along ancestor-descendant paths is less than three times the number of edges. A repetition contains at least two shortest periods; isolated vertices have no repetitions and contribute zero. [Sugahara et al., Computing Runs on a Trie, Corollary 6](https://drops.dagstuhl.de/storage/00lipics/lipics-vol128-cpm2019/LIPIcs.CPM.2019.23/LIPIcs.CPM.2019.23.pdf)

Root each road tree arbitrarily and label edges by their direction toward the parent. Different children of one parent have distinct labels, meeting the determinism requirement. The forest has
$$
N-c
$$
edges, with isolated vertices included in the component count.

Consider axes with nonzero horizontal grid periods and at least four shortest periods present in the roads:
$$
p_L\ge1,\qquad
A_L=C\cap L,\qquad
\rho_L=\frac{|E(A_L)|}{p_L}\ge4.
$$
Axes are distinguished by road component. Split the finite axis segment at its shallowest vertex into at most two ancestor-descendant paths. The longer path contains at least half the original segment and hence at least two periods. Its shortest period is still the axial period: a shorter period of two consecutive copies would impose a smaller cyclic period on the original period word, contradicting minimality.

Extend that ancestor-descendant path to a maximal repetition of the same period. Deterministic labels make the extension unique. One shortest period and its starting vertex also determine the entire doubly infinite labeled axis. Distinct axes therefore cannot map to the same maximal repetition. Applying the exponent-sum result gives
$$
\boxed{\sum_L\rho_L\le6(N-c).}
$$
The factor two comes from selecting at least half the axis segment. This budget merges all labels on the same axis; it must not be charged again for each label.

### The count and exponent sum of high-power components

The shortest axial period has nonzero horizontal grid displacement. If an axis segment contains several complete periods, their endpoints differ horizontally by that many period displacements. Thus
$$
\lfloor\rho_L\rfloor\le n-1.
$$
Each positive or negative signed exponent determines at most one component. Define the following set using only label components containing genuine markers with exponent at least four:
$$
\mathcal H=\{(h,K):q_K\ge4\}.
$$
Then
$$
\boxed{
|\mathcal H|\le12(N-c),\qquad
\sum_{(h,K)\in\mathcal H}q_K
\le12(n-1)(N-c).
}
$$
The constant twelve already includes both signs of horizontal labels. No component-size-weighted exponent sum is bounded here.

### Which markers remain in the general problem

Use the common cut from Section 12 for each label. First pay jointly for completed markers and those touching the common prefix, at a cost of at most one intersection size. Among remaining markers, these components can also be paid:

- Exponent at most three: Section 20 gives capacity at most seven.
- The component itself is a path: Section 21 gives capacity four.
- Its axis intersection is one vertex: distinct early points give unit capacity.

Among label components containing remaining markers, the unpaid set must satisfy all of
$$
\mathcal C=\{(h,K):
q_K\ge4,\quad
K\text{ has a fork},\quad
|E(K\cap L)|\ge1\}.
$$
Its count and exponent sum obey the budgets above. Denote the remaining markers after the common cut in these components by
$$
\widetilde M^{\rm separated}_{h,K}.
$$
Adding row stars, at most one failure per candidate, the common-cut payment, and capacities of the noncritical components gives
$$
\boxed{
W\le(9n-7)N+
\sum_{(h,K)\in\mathcal C}
\widetilde M^{\rm separated}_{h,K}.
}
$$
The coefficient comes from row stars and failures plus eight times the total intersection budget over labels.

**This final remainder is still uncontrolled.** A linear number of components and a cubically bounded exponent sum do not themselves bound actual marker counts. Resources may still be reused across forks.

## 24. Distinct early endpoints and axial projections narrow the remainder

Fix a host intersection component with shortest axial period $p$. A marker subfamily using at most $r\ge1$ distinct early endpoints has complete early-resource capacity
$$
\boxed{C_r=\max\left\{1,\left\lceil\frac{2r}{p+1}\right\rceil\right\}.}
$$
The endpoints need not be consecutive or discovered early. Resources need not be paths or disjoint from their translates. An empty family needs no assignment.

Take any connected subtree and retain the markers whose entire resources it contains. Put
$$
U\subseteq K,\qquad D=\operatorname{diam}\pi_L(U).
$$
If $D<p$, two sources for the same early endpoint cannot both occur: their projections differ by a nonzero multiple of the period. Early endpoints are therefore distinct, and Section 13 gives unit capacity.

If $D\ge p$, put $k=\lfloor D/p\rfloor\ge1$. Each early endpoint occurs at most $k+1$ times. The subtree contains the axial segment between its extreme projections, so
$$
|U|\ge D+1\ge kp+1,\qquad
\frac{k+1}{kp+1}\le\frac2{p+1}.
$$
The last inequality is equivalent to $(k-1)(p-1)\ge0$. Thus there are at most $2r|U|/(p+1)$ resources. Summing over connected components of each resource union gives the claimed capacity version of Hall's condition.

In particular,
$$
r\le\left\lfloor\frac{p+1}{2}\right\rfloor\ \Longrightarrow\ C_r=1,\qquad
r\le p+1\ \Longrightarrow\ C_r\le2.
$$
Resources with $t(e)<p$ use at most $p-1$ early endpoints and have capacity two; this class is empty when the period is one. The resources no longer need to lie on the axis.

A second class has unit capacity even after all its groups are combined:
$$
\operatorname{diam}\pi_L(S_{a,e})=0.
$$
Group by the unique projection point. Within a group, no early endpoint repeats, so complete resources admit a unit assignment. Different groups lie in disjoint projection fibers, allowing their assignments to be combined. A resource may lie entirely off the axis or branch at its single axial point.

### A smaller remainder with the same coefficient

Use the critical components of Section 23. Within each component, let $r_{h,K}$ count distinct early endpoints among all markers remaining after the common cut. If
$$
2r_{h,K}\le7(p_K+1),
$$
capacity seven pays for the entire component. In other critical components, first pay for short discovery indices and then for single-point projections, using total capacity at most three. These components and the noncritical ones form disjoint classes, so all payments still fit the existing capacity-seven budget.

Let $R_{h,K}$ count only remaining markers satisfying
$$
2r_{h,K}>7(p_K+1),\qquad
t(e)\ge p_K,\qquad |E(S_{a,e}\cap L)|\ge1.
$$
Their components must still satisfy the high-exponent, fork, and nondegenerate-axis-intersection conditions of Section 23. Then
$$
\boxed{W\le(9n-7)N+\sum_{(h,K)\in\mathcal C}R_{h,K}.}
$$
A summand is zero when its component fails the early-endpoint count condition. The coefficient is unchanged, but the final sum remains uncontrolled.

## 25. Query-side periodic axes and a common-period length budget

Root the query at the identity and write $w_x$ for the free-group root word of a query vertex; write $a$ for the host source vertex in the free group. For a fixed host label component, let its left multiplication be $g=u^q$, with shortest period $p$. Every actual marker satisfies
$$
g(a w_e)=a w_f,\qquad
a^{-1}ga=w_f w_e^{-1}.
$$
Thus each early endpoint determines a query axis,
$$
I_e=\operatorname{Axis}(w_f w_e^{-1})=a^{-1}L.
$$
This does not depend on which source is chosen for that early endpoint. All sources in one query-axis class send that axis to the host axis. Their relative left multiplications preserve the host axis and are powers of its shortest translation. All such sources lie in one row, giving unit capacity for this class.

The complete late prefix contains the path between the early and late endpoints, whose central axial segment has length
$$
|E(P_{t(f)}\cap I_e)|\ge qp.
$$
The late prefix cannot be replaced by the early prefix here.

### Total length of axes with a common period

Let $T$ be a finite Cayley subtree. Take distinct axes whose bidirectional direction words all have the same positive integer period $p$, with
$$
A_I=T\cap I,\qquad |E(A_I)|\ge4p.
$$
Then
$$
\boxed{\sum_I|E(A_I)|\le4|T|.}
$$

First, if two such axes share $p$ consecutive edges, reading that full period in one common direction determines every letter in both directions. Direction-labeled continuation is unique, so the axes coincide.

Choose any tree root. Split each axial segment at its shallowest vertex and take the longer ancestor-descendant piece, of length $b_I$. Then
$$
b_I\ge\frac{|E(A_I)|}{2}\ge2p.
$$
From its deeper endpoint, take the first $\lfloor b_I/2\rfloor$ edges and their endpoints, forming a closed half-segment $H_I$. If two half-segments share a vertex, both original pieces still have at least $p$ edges toward the root from that vertex. Their axes share a full period, a contradiction. Hence the half-segments are vertex-disjoint, and
$$
|H_I|=\left\lfloor\frac{b_I}{2}\right\rfloor+1
\ge\frac{|E(A_I)|}{4}.
$$
Summing proves the budget. The period length is fixed; this argument does not sum axes of different periods together.

For a fixed host label component with $q\ge4$, every actual query axis leaves at least $qp$ edges in the final valid query. Therefore
$$
\sum_I|E(Q\cap I)|\le4|Q|,\qquad
\#\{I\}\le\frac{4|Q|}{qp}.
$$
Multiple markers on one axis do not count as multiple axes.

### Reversed order across axes bounds candidate counts

Take distinct query axes $I,J$ and fix a marker $(e_J,f_J)$ of the latter class. Let $\mathcal A$ be the distinct late sources that produced a marker of the former class with early endpoint discovered before $e_J$. Distinct query axes belong to different query intersection components, so the reversal rule gives
$$
t(e)<t(e_J)<t(f_J)<t(f).
$$
Each source matches the whole of $P_{t(f_J)}$, leaving at least $qp$ edges of the axis $aJ$ inside the same host tree $C$.

Different sources give different axes $aJ$. Otherwise their relative left multiplication preserves both $I,J$, whereas a nonidentity free-group left multiplication cannot preserve two distinct translation axes. The length budget above yields
$$
\boxed{|\mathcal A|\le\frac{4|C|}{qp}\le\frac{4N}{qp}.}
$$
This counts distinct sources only. One source may contribute multiple early endpoints, and different query-axis classes can reuse resources. It does not yet bound all markers.

## 26. Extending a periodic axis in the actual plane

This section adds a geometric property absent from abstract free trees. Suppose the roads already contain at least two consecutive shortest periods of an axis. Let its period length be $p$ edges and its grid displacement a nonzero horizontal integer vector $\delta$. The critical components in Section 23 satisfy this condition.

### The infinite extension remains an induced grid path

Take one period as a polygonal arc $\alpha$. Two adjacent periods already lie on a simple road path, so $\alpha$ and $\alpha+\delta$ share only their joining endpoint. Brouwer's translation-arc lemma implies that such an arc for a nonzero planar translation cannot intersect nonadjacent iterates. An intersection would give a Jordan curve with fixed-point index one, whereas the translation's displacement field is a nonzero constant vector and has index zero. [Ortega, Translation arcs and stability in two dimensions, Sections 3–4](https://www.ugr.es/~ecuadif/files/arc.pdf)

Consequently,
$$
\Gamma=\bigcup_{k\in\mathbb Z}(\alpha+k\delta)
$$
is a simple doubly infinite polygonal curve. The fundamental arc is compact and the displacement is nonzero, so both directions leave every bounded region. The curve separates the plane into two sides. Translation preserves the curve's orientation and the plane's orientation, and hence each side.

Index consecutive grid vertices so that
$$
\lambda_{i+p}=\lambda_i+\delta.
$$
Suppose an extra unit grid edge joins nonconsecutive axis vertices indexed $i<j$. If $2\le j-i\le p$, translating by whole periods places both endpoints inside the known two-period road segment, contradicting the induced-forest condition.

If $j-i>p$, that unit edge and its period translate have strictly alternating endpoints along the axis:
$$
i<i+p<j<j+p.
$$
An open unit grid edge cannot cross another grid edge, so both chords avoid the axis in their interiors. Translation puts them on the same side. The two unit edges are parallel with distinct endpoints and therefore disjoint. This contradicts Jordan separation, which forces same-side chords with alternating endpoints to intersect.

Thus the infinite axis vertices form an induced path. An abstract Cayley axis alone does not justify skipping this planar argument.

### Off-axis parts of the complete domain avoid the virtual extension

Again take a complete intersection domain containing actual markers. Orient the axis so that
$$
K=C\cap g^{-1}C,\qquad
A=C\cap L=[l,r],\qquad
g\text{ shifts }L\text{ by }\ell>0.
$$
Suppose an off-axis component, starting from its actual attachment $\beta$, first meets the infinite physical axis at index $t$. Take this road arc and its label translate. Both lie in the same host tree, attach at $\beta,\beta+\ell$, and belong to distinct abstract projection fibers. They are disjoint.

Neither meeting point can lie on the actual axial segment: otherwise two distinct abstract vertices of one road tree would have identical grid coordinates. Hence
$$
t\notin[l,r],\qquad t+\ell\notin[l,r].
$$
Both attachments lie on that segment, so $r-l\ge\ell$. A meeting point on the right or on the left respectively gives
$$
\beta<\beta+\ell<t<t+\ell,
\qquad\text{or}\qquad
t<t+\ell<\beta<\beta+\ell.
$$
The two open arcs avoid the axis and translation places them on the same side. Alternating endpoints force an intersection, a contradiction. Each off-axis component therefore lies entirely on one side of the infinite axis.

There is no extra unit adjacency to the virtual axis either. If the adjacent axis point is in the actual segment, inducedness immediately creates a cycle. Otherwise append the unit edge to the road arc just used. If its translated endpoint enters the actual segment, it again creates a cycle; if it remains outside, the endpoints still alternate on the same side. Unit grid edges cannot introduce interior crossings, giving the same contradiction.

Thus
$$
\boxed{K\cup\Gamma\text{ is an induced grid tree}.}
$$
This tree is infinite. The conclusion concerns the complete intersection domain, not arbitrary off-axis parts of the host tree. Both translated road arcs must belong to the same host tree.

### A geometric bound on the shortest period

Suppose one period uses $H$ distinct rows. The $p$ vertices of a half-open period have distinct pairs consisting of their row and their column modulo the absolute horizontal period displacement. Otherwise two different indices of the infinite axis would have the same physical grid coordinates. There are only $|\delta|$ residues per row, so
$$
\boxed{p\le H|\delta|\le n|\delta|,\qquad
\ell_g=qp\le H|h|\le n|h|.}
$$
Displacement magnitudes here mean absolute horizontal integer displacements; axial lengths count edges. This property preserves actual grid geometry, but has not paid for the marker remainder in Section 24.

## 27. Grouping resource left endpoints improves the period capacity

Fix a host label component containing actual markers. Give its common axis integer coordinates, with shortest period $p$. Take any subfamily of complete early resources whose projection spans satisfy
$$
\operatorname{diam}\pi_L(S)\le B,\qquad B\in\mathbb Z_{\ge0}.
$$
This subfamily admits complete-resource capacity
$$
\boxed{C_B\le1+\left\lceil\frac Bp\right\rceil.}
$$
Resources need not be paths, lie on the axis, or be disjoint from their label translates.

Write the smallest projection coordinate of each resource as
$$
\lambda(S)=\min\pi_L(S).
$$
Two different resources for the same early endpoint are related by a left multiplication commuting with the label map. It preserves the common axis and shifts it by a nonzero integer multiple of the shortest period. The resources' smallest projections therefore differ by a nonzero integer multiple of that period. Group resources by
$$
\lambda(S)\in[jp,(j+1)p),\qquad j\in\mathbb Z.
$$
Each group has distinct early endpoints and thus a unit assignment by Section 13.

If a road vertex belongs to a resource, the resource's left endpoint lies in a bounded interval to the left of the vertex's projection:
$$
z\in S,\quad x=\pi_L(z)
\quad\Longrightarrow\quad \lambda(S)\in[x-B,x].
$$
This closed integer interval meets at most
$$
1+\left\lceil\frac Bp\right\rceil
$$
groups. Combining their unit assignments proves the claim. Grouping resource left endpoints instead of candidate sources avoids extending the allowed range in both directions.

Resources remaining after the common cut are disjoint from their label translates, so
$$
B\le qp-1
\quad\Longrightarrow\quad C_B\le q+1.
$$
This improves the capacity in Section 20 to
$$
\boxed{
\widetilde M_h\le |G_h|+
\sum_{K\in\operatorname{comp}(G_h)}
\min\{1+b(K),\,q_K+1\}|K|.
}
$$
Only components with remaining markers contribute. Uniformly bounded relevant exponents now give the smaller conditional bound
$$
q_K\le q_0
\quad\Longrightarrow\quad
W\le[(q_0+3)n-(q_0+1)]N.
$$
In particular,
$$
q_0=1\quad\Longrightarrow\quad W\le(4n-2)N.
$$

A further consequence, requiring no common-cut separation, is
$$
\operatorname{diam}\pi_L(S)<2p
\quad\Longrightarrow\quad C\le3.
$$
This includes single-point projections and short discovery indices. The resources themselves may be large and branch arbitrarily off the axis.

## 28. Long early prefixes separate different query axes in the plane

Fix one host label component with
$$
g=u^q,\qquad q\ge4,\qquad p=\ell_0,\qquad \delta=h/q.
$$
Each query axis has at least one label length in its complete late prefix and extends to an infinite induced grid path by Section 26. Take two markers satisfying
$$
t(e_i)<t(e_j),\qquad I_i\ne I_j,\qquad
|E(P_{t(e_i)}\cap I_i)|\ge2p.
$$
Their infinite physical query axes $\Gamma_i,\Gamma_j$ are disjoint, with no unit grid edge joining them.

**Disjointness.** The later marker's complete early resource contains the translated earlier prefix:
$$
a_j+P_{t(e_i)}\subseteq a_j+P_{t(e_j)}\subseteq K.
$$
This includes at least two periods of the earlier axis. Both infinite axes have the same horizontal period displacement. Any intersection therefore repeats by that displacement, and this actual segment contains two such intersections separated by one full axial period.

Section 26 says that the complete domain together with the virtual host axis is an induced tree. The actual path between these two intersections must therefore follow the host axis, without passing through its off-axis parts. The translated earlier axis and the host axis share an entire period, so Section 25 forces the abstract axes to coincide. Applying the later source's inverse then makes the two query axes equal, a contradiction.

**No grid adjacency.** Suppose a unit grid edge joins the infinite axes. Repeating it by the common period gives two such joining edges whose endpoints lie on the earlier actual two-period segment. That segment is already disjoint from the virtual host axis. The two edges and the connecting segments along the earlier and host axes form a cycle. The completion is induced, so the joining grid edges must be present, contradicting that it is a tree.

The hypothesis concerns the earlier **early prefix**. The long axial segment automatically present in every late prefix cannot replace it.

### Counting classes with long early prefixes

Count only distinct query axes for which some marker's early prefix contains two periods, and denote their number by $k$. Order each class by its first early endpoint satisfying the condition. The result above makes their infinite physical axes pairwise disjoint and nonadjacent.

Each axis has at least one label length in the final valid query, and their actual vertex sets are disjoint. Thus
$$
\boxed{k(qp+1)\le |Q|.}
$$
If the query spans $H_Q$ consecutive integer rows, the row and column-residue keys within one period are distinct on each axis and across axes. Consequently,
$$
\boxed{kp\le H_Q|\delta|.}
$$
The full period's row range already occurs in the query, so virtual extension does not introduce extra rows into this budget.

Alternatively, fix any vertical line with half-integer horizontal coordinate and choose one horizontal crossing edge from each infinite axis. Such an edge exists because a nonzero horizontal period extends the axis infinitely in both horizontal directions. The chosen edges from different axes differ in row by at least two; otherwise they have an extra grid adjacency. Hence
$$
\boxed{k\le\left\lceil\frac{H_Q}{2}\right\rceil.}
$$

Each axis class still has unit capacity by Section 25, but host resources from different classes may overlap. These bounds count axis classes; they do not give unit capacity to all long resources together.

## 29. Keeping capacity seven leaves at least five long early-axis classes

For each label, first pay one intersection size for the part removed by the common cut. In a host component of the remaining markers, let $r_{h,K}$ count distinct early endpoints and $k_{h,K}$ count classes with long early prefixes. Any of these conditions allows capacity seven to pay for the entire component:

- The exponent is at most six, using Section 27.
- The component is a path, or its axis intersection is one vertex, using Sections 21 and 23.
- Its early-endpoint count satisfies the capacity-seven condition of Section 24.
- It has at most four long early-axis classes: resources spanning less than two periods cost capacity three, and each long class costs one.

It therefore suffices to retain components satisfying
$$
\mathcal D=
\{(h,K):q_K\ge7,\ k_{h,K}\ge5,\
2r_{h,K}>7(p_K+1),\
K\text{ has a fork},\ |E(K\cap L)|\ge1\}.
$$
In each such component, pay for all short-span resources and any four long axis classes; choosing the four largest classes is allowed. Define the unpaid count as
$$
R^{(24)}_{h,K}
=\#\{(a,e):\operatorname{diam}\pi_L(S_{a,e})\ge2p_K,\
I_e\text{ is outside the four selected classes}\}.
$$
Only actual markers remaining after the common cut are counted. The capacity already paid in every component is still at most seven, giving
$$
\boxed{
W\le(9n-7)N+\sum_{(h,K)\in\mathcal D}R^{(24)}_{h,K}.
}
$$
The new remainder is contained in that of Section 24: a span of two periods also ensures a sufficiently large discovery index and a nondegenerate axial intersection. Existing unit-capacity criteria, such as distinct early endpoints or collinear sources, remain available.

**The final sum is still uncontrolled.** The number of long axis classes can grow with the instance. Counting axes has not removed reuse of host resources across classes. Checks on the old fixtures and one new curved fixture cover 3,430 actual markers; the new rules pay for all their previous remainders. 

## 30. Another periodic axis separates copies with the same axis image

Take two different abstract query axes with the same shortest horizontal period displacement, the first having shortest edge period $p$, whose infinite physical axes are induced paths by Section 26. Two complete-prefix maps satisfy
$$
I\ne J,\qquad aI=bI,\qquad a\ne b,
$$
and both map an actual query-axis path $A\subseteq J$ into the same road tree. Then
$$
\boxed{aA\cap bA=\varnothing.}
$$
Intersection here first means intersection at actual grid vertices. Two copies already lying in the same road tree share an actual vertex exactly when they share a direction-word tree vertex.

The relative left multiplication preserves the common axis image and translates it by a nonzero integer multiple of the shortest period. Its physical displacement is therefore
$$
\Delta_{\rm grid}=s\delta,\qquad
\Delta_{\rm axis}=sp,\qquad s\in\mathbb Z\setminus\{0\}.
$$
The other infinite physical axis has that same horizontal period, so its two infinite physical images coincide. If the actual finite copies share a vertex, their full bidirectional direction continuations agree there. Directional continuation from a Cayley-tree vertex is unique, so the abstract axis images coincide as well. The relative left multiplication would preserve two distinct axes, contradicting uniqueness of the translation axis of a nonidentity free-group left multiplication.

If both query axes also have the same edge period $p$, the finite copies are shifted by the corresponding number of edges along one physical axis. Their disjointness implies
$$
\boxed{|\Delta_{\rm axis}|>|E(A)|.}
$$
Within one host label component, sources of one query-axis class have the same axis image, so this applies directly. The next section also allows different intersection components, requiring only that the chosen reference-axis image coincide. Both sources must genuinely match the entire segment being used.

## 31. On-axis early endpoints in one conjugacy class fit reference-axis blocks

Fix a horizontal label and its actual common cut. Use the common late prefix and smaller early tree from Section 12:
$$
R\subseteq P,\qquad P\cap(R+h)=\varnothing.
$$
Every remaining early endpoint belongs to the smaller early tree, and every late candidate matches the entire common late prefix.

Group query-side label left multiplications by free-group conjugacy class. Their cyclically reduced words differ only by cyclic rotation, so the shortest edge period, exponent, and horizontal period displacement agree within a class. Consider any subfamily of remaining markers in one such class whose early endpoints themselves lie on their query axes:
$$
q\ge4,\qquad e\in I_e.
$$
This differs from requiring the early resource to contain a long axial segment. The early endpoint may lie off the axis, so this does not cover the entire remainder.

### Choose a reference marker

Take a marker with the latest early endpoint in this family, and write its axis as
$$
(e_*,f_*),\qquad J_*=I_{e_*}.
$$
The reference query-axis class lies in one query translation-intersection component. The potential injection from Section 6 charges its markers to distinct host intersection endpoints. Denote its count by $E_{\rm ref}$.

Other axis classes belong to different query intersection components. Global reversal gives
$$
t(e)<t(e_*)<t(f_*)<t(f).
$$
Every nonreference source therefore matches the entire reference late prefix, which has at least one label length on the reference axis:
$$
|E(P_{t(f_*)}\cap J_*)|\ge qp.
$$

### A common block length bounds the markers per source

Intersect each nonreference query axis with the common early tree. It contains the relevant early endpoint and is nonempty. Put
$$
B=\max_{I\ne J_*}|E(R\cap I)|.
$$
The maximum uses only nonreference axes appearing in this subfamily. If there are no nonreference markers, the following cost is zero. Translating an infinite physical axis by the label moves one label length along it. Common-cut disjointness therefore gives
$$
0\le B\le qp-1.
$$
Otherwise the actual early tree would contain two axial vertices differing by the label, contradicting the cut condition.

A fixed source belongs to only one query intersection component, so all its early endpoints under consideration belong to the same axial intersection. Its markers have distinct early endpoints. Thus each nonreference source contributes at most
$$
B+1
$$
markers. Fix one segment $V$ of the reference late axis satisfying
$$
V\subseteq P_{t(f_*)}\cap J_*,
\qquad |E(V)|=B,\qquad |V|=B+1.
$$
Every nonreference source maps this entire segment into the host.

### Blocks within the same axis image are disjoint

Group nonreference sources by their reference-axis images:
$$
\Lambda=aJ_*.
$$
For different sources in one group, use the nonreference query axis attaining the maximum span. Both sources match the entire common early tree, so Section 30 applies. Their relative displacement along the reference axis exceeds the block's edge length. Consequently,
$$
aJ_*=bJ_*,\quad a\ne b
\quad\Longrightarrow\quad aV\cap bV=\varnothing.
$$
Each source's marker count fits in its own block. This payment uses road vertices from the reference late axis; **it does not assert that they belong to the original marker's complete early resource**. It is therefore not a new complete-resource Hall theorem.

Let $\mathcal A$ be the distinct actual reference-axis images, distinguished by road component. Each has at least one label length in its road tree. The common-period packing bound from Section 25 gives
$$
T_{h,\mathfrak c}
=\sum_{\Lambda\in\mathcal A}|C_\Lambda\cap\Lambda|,
\qquad
M^{\rm on}_{h,\mathfrak c}\le E_{\rm ref}+T_{h,\mathfrak c},
$$
$$
\sum_{\Lambda\in\mathcal A}|E(C_\Lambda\cap\Lambda)|\le4N,\qquad
|\mathcal A|\,qp\le
\sum_{\Lambda\in\mathcal A}|E(C_\Lambda\cap\Lambda)|.
$$
Hence
$$
\boxed{T_{h,\mathfrak c}\le4\left(1+\frac1{qp}\right)N\le5N.}
$$

### Different conjugacy classes still need a shared budget

For a fixed label, an actual host axis and its horizontal period displacement determine the exponent and conjugacy class. Different classes therefore do not list the same host axis twice. Their reference endpoint injections also combine: the label left multiplication at one host intersection vertex is unique, as is its conjugacy class. Thus
$$
\boxed{
M_h^{\rm on}\le |G_h|+\sum_{\mathfrak c}T_{h,\mathfrak c}.
}
$$
Only the selected high-exponent, strictly separated subfamily with on-axis early endpoints is counted.

Paying the entire road count again for every conjugacy class does not prove a linear total. Classes may have different shortest periods, so the fixed-common-period length bound cannot simply be summed across them. The exponent-sum bound of Section 23 is not an axis-length-sum bound either. Markers with off-axis early endpoints remain unpaid by this section. This is a new counting reduction; the general logarithmic gap remains.


## 32. Many repeating axis classes can coexist in connected resources

The number of axis classes with repeated early endpoints cannot be assumed constant. An explicit induced-tree family has $k$ long early axes, with $t$ occurrences of each early endpoint in every upper class and more repetitions in the bottom class. The union of all complete early resources remains connected. Parameters can satisfy
$$
k\ge2,\quad t\ge1,\quad t(k-1)\ge2,\quad
d\ge10,\quad 5\mid d.
$$
Upper candidate columns are spaced by $d+10$, and bottom candidates occur every five columns. Write
$$
P=(d+10)(t(k-1)-1),\qquad b=P/5+1.
$$
The genuine marker count, complete-resource union size, and count left by the previous round's rules when selecting the four largest long-axis classes are
$$
\widetilde M_h=3t(k-1)+6b+1,\qquad
|\mathcal U|=b(6k+4)+1,
$$
$$
R^{(24)}_{h,K}=(k-4)t\qquad(k\ge5).
$$
All markers have an explicit unit assignment: short-tooth early endpoints use the corresponding point of the first visited short tooth; the bottom row's two extra phases and final endpoint use their own endpoints; the off-axis hook also uses its own endpoint. Different heights, column residues modulo five, and the final endpoint's range make these assigned vertices distinct.

The family therefore rules out only a bounded number of repeating axis classes. It is not an algorithm counterexample. Its query size is at most twice the board side, so the generic per-prefix bound already gives
$$
|Q|\le2n,\qquad W\le2nN.
$$
The fixed six-axis instance has 307 markers, every class repeats, and the complete-resource union has 1,841 vertices. The original program and independent answers agree. The [family proof and explicit assignment](../examples/repeated-axis-classes.zh.md) record the construction, general formulas, and finite verification scope.

## 33. All early endpoints on straight axes can be paid for together

The fixed-conjugacy-class bound of Section 31 strengthens further for straight axes. A shortest period of one with horizontal displacement has a cyclic primitive word consisting of one horizontal step toward the label. Thus, for a fixed nonzero horizontal label,
$$
p=1,\qquad q=|h|,
$$
there is only one possible oriented conjugacy class.

The actual road intersections of its different reference-axis images are horizontal paths. If two such axes in one road tree share an actual vertex, unique horizontal continuation in both directions forces the abstract axes to coincide. Different road components share no vertices. The actual road vertex sets of distinct reference-axis images are therefore pairwise disjoint, improving the cost in Section 31 to
$$
T_{h,\rm straight}\le N.
$$
For any high-exponent subfamily remaining after the strict common cut, retain only straight axes with on-axis early endpoints. Then
$$
\boxed{M_{h,\rm straight}^{\rm on}\le |G_h|+N.}
$$
There is no restriction on the number of query-axis classes, repetitions of an early endpoint, or connectivity of the resource union.

There are at most twice the board side minus two signed horizontal labels. Combining their intersection budget gives
$$
\boxed{
\sum_h M_{h,\rm straight}^{\rm on}
\le3(n-1)N.
}
$$
The road count is not charged separately for every host intersection component. Section 31 already treats all components for one label together.

Apply this to the entire unpaid subfamily from Section 29. Remove all markers with straight axes and on-axis early endpoints, and denote the remaining count by
$$
R_{\rm curved/off}^{(25)}
=\#\{(h,K,a,e)\text{ in the Section 29 remainder}:
p_K>1\text{ or }a+e\notin L_K\}.
$$
The general scan count then has the rigorous reduction
$$
\boxed{
W\le(12n-10)N+R_{\rm curved/off}^{(25)}.
}
$$
All other earlier conditions remain, including the actual common cut, high exponent, sufficiently many long early axes, and at least two periods in every unpaid resource. This remainder is still uncontrolled. However, all period-one markers with on-axis early endpoints now fit a shared target-scale budget.

Similarly, restricting on-axis early endpoints to axes whose shortest edge periods have a fixed constant upper bound leaves only finitely many primitive direction-word conjugacy types. Their Section 31 costs also combine into a constant multiple of the target budget, with the constant depending on the period bound. Growing curved-period types and markers with off-axis early endpoints still need to be handled in general.

## 34. The entire intersection domain cannot be completed periodically

Section 26 only proves that an entire intersection domain together with its infinite axis is an induced tree. It does not permit adding every label translate of that domain simultaneously.

Coordinates below are row and column. Uppercase direction letters denote unit moves down, right, and left. Set
$$
h=(0,10),\qquad
B_{\rm L}=D^2W^2D^3E^2,\qquad
B_{\rm R}=D^2E^2D^3W^2.
$$
Both paths start at the origin and have the same endpoint, but take opposite routes. The road contains row zero from columns zero through forty. Attach the left path at columns zero and ten, and the right path at columns thirty and forty. The four branches are separated, so the road is an induced tree. Its intersection domain is exactly
$$
K=\{(0,c):0\le c\le30\}\cup B_{\rm L}
  \cup\bigl(B_{\rm R}+(0,30)\bigr),
$$
where a direction word in a union denotes all its vertices, including its starting point. Directly,
$$
N=77,\quad |K|=49,\quad p=1,\quad q=10,\quad K\cup(K+h)=F.
$$
However, translating the left branch three times aligns it with the original right branch at column thirty. They form a fourteen-edge cycle. Thus
$$
\bigcup_{j=0}^{3}(K+jh)
$$
is already not a forest.

The domain does carry genuine markers. The query first walks two axis edges right and returns, visits the entire left branch and returns along it, then walks ten edges right and visits the second left branch. Recomputing stars over all candidates gives nine strict common-cut markers. All their early endpoints are off the axis, and all their early resources have axis span two. The actual parameters are
$$
n=45,\quad |Q|=29,\quad m=41,\quad W=228.
$$
The standard program and independent answer oracle both pass. The union of resources used by this query has only twelve vertices and does not use the right branch. This example therefore does not refute a stronger property of active resources, and is not an algorithmic complexity counterexample.

## 35. All label translates of one cut resource still form an induced forest

Unlike the preceding domain, a genuine cut resource satisfies an additional disjointness condition. This section requires neither a large exponent nor an early endpoint on the axis.

### A connected grid set injects into the cylinder

Suppose a finite connected grid set and a nonzero horizontal integer translation satisfy
$$
S\cap(S+h)=\varnothing,\qquad h=(0,d),\qquad d>0.
$$
Reflection handles negative labels. Taking the horizontal coordinate modulo the label length gives the cylinder projection
$$
\pi_d(r,c)=(r,[c]_d).
$$
This projection is injective on the grid set. Equivalently,
$$
\boxed{(S+ih)\cap(S+jh)=\varnothing\quad(i\ne j).}
$$

To prove this, suppose two vertices have the same projection. Take a simple path between them in the connected grid set, then a shortest subpath whose endpoints have the same projection. Its cylinder projection is a simple closed curve. Unit grid-edge interiors cannot acquire crossings under the projection: lifting such a crossing would produce intersecting grid edges without a common grid vertex.

The lift of this closed curve has endpoints differing by a nonzero integer multiple of the label. Identifying the cylinder with the punctured plane, this integer is its winding number about the missing origin. A simple closed curve has winding number zero, one, or minus one. The original vertices therefore differ by one positive or negative label, contradicting the assumed disjointness. The winding-number fact is stated in [Theorem 1 of the NTNU notes](https://www.math.ntnu.no/emner/TMA4175/2011v/continuousLogs2.pdf).

For label lengths one or two, the cylinder grid may contain loops or parallel edges. They must be retained as the actual embedded edges rather than collapsed to a simple quotient graph. This does not affect the simple-curve argument.

### Extra grid adjacency cannot skip a copy

Under the same assumptions, any unit grid edge between distinct copies joins consecutive copy indices:
$$
\boxed{
\{x,y+kh\}\text{ is a unit grid edge},\quad x,y\in S,\quad k\ne0
\ \Longrightarrow\ |k|=1.
}
$$
Take a simple path inside the grid set between the two representative vertices. The injectivity just proved makes its projection a simple path. Adding the edge between copies forms a simple closed curve whose winding number is their index difference, so its absolute value is one. If both representative vertices are equal, the path is empty and the added edge itself is a simple closed curve; the conclusion still holds.

In particular, if the set and its first translate are not grid-adjacent, no two distinct integer translates are grid-adjacent.

### From two actual copies to every copy

Assume additionally that the original grid set is an induced tree and its union with its first translate is an induced forest. The two disjoint nonempty connected trees have at most one unit edge between them. The previous arguments exclude every collision and adjacency between nonconsecutive copies, so
$$
\boxed{\mathcal P_h(S)=\bigcup_{j\in\mathbb Z}(S+jh)
\text{ is an induced grid forest}.}
$$
If the first two copies have no connecting edge, the copies are separate components. If they have one, the copies join in integer order and the entire union is an induced tree.

A genuine strict common-cut marker satisfies
$$
S=a+P_{t(e)},\qquad
S\cap(S+h)=\varnothing,\qquad
S\cup(S+h)\subseteq F.
$$
Thus the conclusion applies to each complete early resource. It also applies to an entire fibre of a fixed axis-projection vertex in a high-exponent intersection domain. The fibre and its first label translate have different axis attachments, at axis distance at least two. In the actual road tree they are therefore disjoint and nonadjacent. All distinct label translates of this fibre remain disjoint and nonadjacent.

Injectivity also gives a size bound. Writing the number of covered rows as the height,
$$
\boxed{|S|\le H(S)\,d.}
$$
The actual common early tree is also disjoint from its first translate, so it satisfies this size bound too. However, its two translates need not be matched simultaneously by one candidate; the induced-forest conclusion cannot be applied to it on that basis.

These statements concern all translates of one resource. Different resources may overlap. They do not establish unit Hall capacity for a resource family, nor justify summing resource sizes to pay for scans.

## 36. The reference axis class can also pay for its off-axis early endpoints

The reference marker in Section 31 can be chosen from all selected high-exponent strict markers of one conjugacy class, rather than only those with early endpoints on their axes. Again choose a marker with the latest early discovery time and write its reference axis as
$$
J_*=I_{e_*}.
$$
Now pay for every marker in the reference axis class, together with the on-axis early endpoints in other axis classes. The potential-based endpoint injection for the reference class did not require early endpoints to be on the axis. The nonreference part still has on-axis early endpoints, so its reversed time order, per-source count, and reference late-axis block argument all remain valid. Consequently,
$$
M^{\rm paid}_{h,\mathfrak c}
=\#\{(a,e):I_e=J_*\text{ or }e\in I_e\},
$$
$$
\boxed{
M^{\rm paid}_{h,\mathfrak c}\le E_{\rm ref}+T_{h,\mathfrak c},
\qquad T_{h,\mathfrak c}\le5N.
}
$$
The set is counted only within the selected conjugacy-class family. The maximum block span is taken only over nonreference axes with on-axis early endpoints that are actually being paid. Allowing the reference early endpoint to be off its axis does not change the nonemptiness of those intersections. Reference endpoints from different conjugacy classes still inject jointly.

For the period-one subfamily, the disjoint actual horizontal axis intersections from Section 33 still give
$$
\boxed{
M^{\rm paid}_{h,\rm straight}\le |G_h|+N,\qquad
\sum_h M^{\rm paid}_{h,\rm straight}\le3(n-1)N.
}
$$
The same budget therefore additionally removes every off-axis early endpoint in the reference axis class.

Specifically, inside the Section 29 remainder, choose the reference query axis by this rule for each label's period-one subfamily. An empty subfamily needs no choice. After removing all on-axis early endpoints and the chosen reference class, define
$$
R^{(26)}
=\#\{(h,K,a,e)\text{ in the Section 29 remainder}:
p_K>1\text{ or }(a+e\notin L_K,\ I_e\ne J_{h,*})\}.
$$
The reference axis is used only in the period-one branch. Rigorously,
$$
\boxed{
W\le(12n-10)N+R^{(26)},\qquad
R^{(26)}\le R_{\rm curved/off}^{(25)}.
}
$$

Off-axis early endpoints in other axis classes can genuinely occur. A fixed six-axis instance with added short hooks has 317 markers, including 56 with off-axis early endpoints. The enlarged reference class pays for 46 of these; each of the other five classes leaves two. These markers also have an explicit unit resource assignment, so this instance is still not an algorithmic counterexample.


## 37. A common late prefix enlarges each source block to a full label length

Fix a horizontal label, its actual common cut, and any strict marker subfamily in one high-exponent conjugacy class. Use the latest-early reference marker and its query axis from Section 36. Write the label's axis length as
$$
\ell=qp,\qquad q\ge4,\qquad J_*=I_{e_*}.
$$
The entire reference query-axis class still injects into distinct host intersection endpoints. Below, consider the other axis classes, allowing off-axis early endpoints.

### Every nonreference source shares a later complete prefix

If the nonreference family is nonempty, choose its marker with the earliest late discovery:
$$
(a_\dagger,e_\dagger,f_\dagger),\qquad
t_\dagger=\min_{\rm nonref}t(f),\qquad I_\dagger=I_{e_\dagger}\ne J_*.
$$
Every nonreference source has a marker whose late time is at least this minimum. It therefore matches this entire prefix. The reversed time order between reference and nonreference markers also gives
$$
t(f_*)<t_\dagger,\qquad
a+P_{t_\dagger}\subseteq F\quad\text{for every nonreference source }a.
$$
This common late prefix contains at least a full label length on the second query axis. Set
$$
A=P_{t_\dagger}\cap I_\dagger,\qquad |E(A)|\ge\ell.
$$

Group sources by their actual reference-axis images. If two distinct sources have the same reference-axis image in the same road tree, Section 30 applies to this commonly matched complete axis segment:
$$
aJ_*=bJ_*,\quad a\ne b
\quad\Longrightarrow\quad
|\Delta_{\rm axis}|>|E(A)|\ge\ell.
$$
Their own markers need not belong to the same query-axis class. The required facts are that both sources actually match this second axis segment, and that the second axis differs from the reference axis.

### One block can pay for arbitrary early endpoints

The reference late prefix also contains a full label length on its axis. Fix a segment
$$
V\subseteq P_{t(f_*)}\cap J_*,
\qquad |E(V)|=\ell,\qquad |V|=\ell+1.
$$
Every nonreference source matches it completely. The preceding separation makes these blocks pairwise disjoint within each actual reference-axis image.

For each source, any set of markers no larger than its block can be charged to that block. Write the source count and the sum of road vertices on distinct actual reference-axis images as
$$
r_a=\#\{\text{selected nonreference markers with source }a\},\qquad
T_{h,\mathfrak c}=\sum_{\Lambda\in\mathcal A}|C_\Lambda\cap\Lambda|.
$$
Then
$$
\boxed{
\sum_a\min\{r_a,\ell+1\}\le
|\{\text{nonreference sources}\}|(\ell+1)
\le T_{h,\mathfrak c}\le5N.
}
$$
The reference class is paid separately by intersection endpoints. Early endpoints may be anywhere off the axis, making this stronger than Section 36's payment of only nonreference on-axis early endpoints.

The new rule retains every old payment. A source's on-axis early endpoints are distinct and lie in the common early tree's intersection with its query axis. Cut disjointness limits that intersection to at most one label length of vertices. Pay for those endpoints first, then use the remaining block positions for off-axis endpoints.

The cost still uses actual reference late-axis vertices, without requiring them to lie in the original early resources. No Hall capacity inside those resources is asserted.

### Complete common-early-tree copies are disjoint within one image

The same separation has an independent geometric consequence. The common early tree has reference-axis projection span
$$
\operatorname{diam}\pi_{J_*}(R)\le\ell-1.
$$
If the early tree misses this axis, its projection is one vertex. If it meets the axis, its projection is the actual intersection segment, whose span is limited by cut disjointness. The sources' relative axis displacement exceeds one label length, so their entire projection intervals are disjoint. Axis projection is unique in a road tree. Hence
$$
\boxed{
aJ_*=bJ_*,\quad a\ne b
\quad\Longrightarrow\quad
(a+R)\cap(b+R)=\varnothing
}
$$
for these nonreference sources. Different actual reference-axis images may still reuse road branches. Summing their complete-copy unions across images cannot replace the axis-vertex budget above.

## 38. Only the excess per source remains for straight axes

For period one, a fixed label has one conjugacy class, and the road intersections of distinct actual reference axes are disjoint. The preceding block cost is therefore at most the number of road vertices. Reference-class and source-block payments still combine across labels within the existing Section 33 budget.

Apply this rule to the original Section 29 remainder. Let its total number of curved-period markers be
$$
R_{\rm curved}^{(24)}
=\#\{(h,K,a,e)\text{ in the Section 29 remainder}:p_K>1\}.
$$
For each label's period-one subfamily, choose the latest-early reference query axis and pay its whole class. Denote each remaining source count by
$$
r_{h,a}.
$$
An empty family needs no reference choice. Reference-class sources do not enter the inner sum below. Then
$$
R^{(27)}
=R_{\rm curved}^{(24)}
+\sum_h\sum_a\bigl(r_{h,a}-(|h|+1)\bigr)_+,
$$
$$
\boxed{
W\le(12n-10)N+R^{(27)},\qquad
R^{(27)}\le R^{(26)}.
}
$$
The comparison uses the same Section 29 remainder and reference rule, prioritizing the on-axis markers paid previously. The new remainder is still uncontrolled. However, its period-one part counts only the excess beyond each source block, rather than all nonreference off-axis endpoints.

### The excess cannot simply be omitted

Change the six-axis example of Section 36 to hook depth twenty and query-axis row spacing twenty-three. This gives a prescribed input within the official limits:
$$
n=274,\quad N=16808,\quad |Q|=504,\quad m=1030,\quad W=325690.
$$
It has 1,381 strict markers, including 1,120 off-axis early endpoints. In the entire high-exponent strict family, the reference class contains 1,151 markers. Each of the other ten sources has twenty-three markers, while its block capacity is sixteen.

This example also undergoes the actual Section 29 filtering. Its six long-early-axis classes contain 1,059 markers in the bottom class and forty-two in each upper class. Paying the four largest classes leaves two classes with eighty-four markers. Choosing the reference class anew in this remainder pays forty-two; each of the other two sources has twenty-one markers and a block paying sixteen. Ten markers still remain.

These ten markers also have an explicit unit resource assignment: the first previously visited deep hook of the same candidate provides distinct vertices at the corresponding depths. The complete assignment for every marker, genuine stars, induced forest, standard program, and independent answers all pass. The example establishes that excess can occur; it does not refute the algorithmic complexity.


## 39. Summing complete resources across reference images can overcount without bound

Section 37 separates complete early-tree copies within one reference image. It does not provide a linear road budget for their sum across images. This remains false after paying the four largest long-axis classes and the reference class, even if each remaining source contributes only the largest early resource it actually uses.

### A family of nested combs

Choose
$$
k\ge6,\quad t\ge1,\quad w\ge3,\quad
D=6w,\quad R=D+3,\quad s=2w+5,\quad d=3s,\quad h=(0,d),
$$
$$
B=2w^2+6w,\qquad b=5(t-1)+1.
$$
Each comb descends to the specified depth and has a horizontal tooth of the specified width every third row. Its number of nonroot vertices is the comb size above.

The query descends one level at a time and fully visits a right-pointing comb two columns to the right of each level. At the bottom it visits a left-pointing comb at one phase, then another one label farther right. It then processes the upper levels in reverse order, extending each arm to the label length plus two and visiting a right-pointing comb there. Each excursion returns to the main stem, and the walk ends at the origin.

The upper sources are
$$
a_{i,j}=(-iR,5sj),\quad 1\le i<k,\quad0\le j<t;
$$
the bottom sources are
$$
(-kR,c),\quad c\in\{0,s,\ldots,5s(t-1)\}.
$$
For an upper source, the designated early endpoint is the last tooth tip of its corresponding upper comb. For a bottom source, it is the last tooth tip of the first special left comb. The late endpoint is one label to the right. The roads are the union of the complete late prefixes at these sources and the complete early prefixes at their label-shifted sources.

Expanding this union gives main stems at phase columns and short right combs in the negative rows; a horizontal spine joining them and carrying special left combs at row zero; and separate positive-row blocks at every fifth phase. Each block has a main stem, long arms, and alternating right and left combs. Neighboring right and left tooth intervals are three columns apart, consecutive levels are three rows apart, and column blocks are separated by a phase. Pieces meet only at their prescribed roots or common stems. There are no additional grid edges, so the roads form an induced tree.

The negative rows contain a number of disjoint complete combs proportional to the product of the number of axis classes and column groups. The entire decomposition contains only that order of pieces. Hence
$$
N=\Theta(ktB),\qquad
n=\max\{(2k-1)R+D+1,\ (5t-1)s+1\},
$$
$$
|Q|=1+kR+kd+2(k-1)+s+(2k+1)B,\qquad
m=2|Q|-2+4k.
$$

The initial full-level descent and two right steps force relevant candidates to start at phase columns and level rows. Completing the initial main stem further restricts upper sources to the designated column groups. A label-shifted source cannot descend another full level in the positive rows, so its early endpoint must lie in its own query level. Negative rows have no long arms, which excludes late endpoints in earlier query levels.

An earlier same-row comb point could replace a star only by moving the source to a nonphase column. The separated phase intervals of right and left teeth also prevent such replacement between comb types. Bottom-axis points are classified modulo the phase; only the rightmost bottom source retains the extra star at the root of the first special comb. The complete genuine marker count is
$$
\widetilde M_h=(k-1)t(B+3)+b(B+s)+1.
$$
All markers pass the strict common cut and have shortest period one. Each upper class has the comb size plus one long-early marker per source; the bottom class is largest. Pay the bottom class and the three lowest upper classes, then choose the latest early class in the remainder as reference. This gives
$$
R^{(24)}=(k-4)t(B+1),\qquad
R^{(27)}=(k-5)t(B-d)=(k-5)t(2w^2-15).
$$
Paying later levels first among equal-sized classes is an allowed choice in Section 29.

### The unbounded overcount

The remaining nonreference sources occupy the earlier levels. Their largest actual early resources have total size
$$
\sum_{i=1}^{k-5}\sum_{j=0}^{t-1}|S^{\max}_{i,j}|
=t\left((k-5)+(R+2+B)\frac{(k-5)(k-4)}2\right)
=\Theta(tk^2B).
$$
Different source levels have reference images in different rows. Within one row, arms in different column groups are disconnected horizontal segments and belong to different axes in the host tree. Taking the resource union within each reference image therefore leaves this sum unchanged. Its ratio to the road count grows with the number of axis classes. The within-image disjointness from Section 37 remains valid.

All markers still admit a unit assignment: move each upper marker to the corresponding point in that source's first visited short arm or right comb; treat the first three bottom-axis points the same way; use the early endpoint image for the other bottom markers. Separate height bands, column groups, and left/right tooth phases prevent collisions.

After the initial descent and right turn, only a number of candidates proportional to the product of the axis and column-group counts remain. The designated sources also all survive the initial comb stage. Consequently,
$$
W=\Theta(k^2tB).
$$
In particular,
$$
k=t=w\to\infty:\qquad
N=\Theta(n^2),\quad
\sum|S^{\max}_{i,j}|=\Theta(n^{5/2}),\quad
W=\Theta(n^{5/2}),\quad m=\Theta(n^{3/2}).
$$
This refutes the coarse resource budget, without refuting the target complexity. The exact road decomposition, exclusion of other stars, and assignment checks are detailed in the [parameter proof](../examples/nested-combs.zh.md).

## 40. A nonreference source's label translate fails by the reference early endpoint

Fix a label, the actual common cut, and a selected family in one high-power conjugacy class. Choose the reference marker by its latest early endpoint as before. Every nonreference source satisfies
$$
a+P_{t(f_*)}\subseteq F,\qquad
a+h+P_{t(e_*)}\not\subseteq F.
$$
The first inclusion follows from temporal reversal. For the second, suppose instead that the shifted source also matches the whole reference early prefix. Then
$$
a+P_{t(e_*)}\subseteq G_h.
$$
This connected prefix contains the source, so it lies entirely in that source's original label component. The component's uniform translation word would therefore also send the reference early image to the reference late image. Pulling it back to the query tree makes the nonreference and reference translation words equal, a contradiction.

Thus each nonreference source has a first failure index for its label-shifted candidate:
$$
j_a=\min\{j:a+h+q_j\notin F\}.
$$
For all selected markers at that source,
$$
\max_{e\ {\rm at}\ a}t(e)<j_a\le t(e_*).
$$
The late source still matches this prefix. Let the parent of the failed query vertex be its unique earlier neighbor in the discovery tree. There is an actual road edge
$$
x=a+\operatorname{parent}(q_{j_a})\in K,\qquad
y=a+q_{j_a}\in F\setminus G_h.
$$
This gives each nonreference source an edge leaving its label intersection domain. Subsequent work proves that a single edge can carry linearly many remaining sources and unbounded excess even after the existing payments. Constant charging per edge is therefore insufficient; see the parameter proof in [Section 1 of the ten-round follow-up](reference-followup.en.md).

Opposite early arms now refute connected-union disjointness after reference deletion. The obstruction still has distinct early endpoints, so it does not refute unit capacity itself. See the [continuation record](reference-capacity.en.md) for the construction and replacement capacity-two draft. The subsequent audit replaces the key step with a finite second-axis lemma, removes the high-power restriction, and completes the [general cubic proof](cubic-bound.en.md). Finite allocation checks are retained separately as supporting verification.

The earlier [axis-projection equivalence lemma](reference-followup.en.md) expresses disjointness exactly as a resource component's projected span being shorter than the axis translation length, and proves this property for nested combs in their original order. The lemma and restricted-family result remain valid; the general strict span claim is refuted by the new obstruction.
