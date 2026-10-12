# Matching in a Four-Neighbour Grid Forest: the Logarithmic Upper Bound

This article preserves the earlier logarithmic bound and its illustrations, explaining the static product inequality and harmonic sum. A later [complete-history charge](research/proofs/cubic-bound.en.md) proves the general cubic bound; the weaker bound here remains valid. See the [editorial](solution.en.md), [std.cpp](std.cpp), and [research overview](complexity-research.en.md) for the algorithm and research history.

## 1. The result and the quantity we must count

Let $n$ be the board side length, $m$ the number of moves, $F$ the road set, and $N=|F|\le n^2$ its size. The induced four-neighbour road graph is a forest.

The algorithm starts with every road cell as a candidate starting point. It scans the current candidates only when the cumulative displacement appears for the first time. Let $W$ be the total number of candidate checks. Then

$$
T=O(n^2+m+W).
$$

Reading the board requires processing its cells; all moves and outputs must also be processed. The remaining work is candidate checking. **We must bound the sum of candidate counts over all rounds, not merely the number of rounds.**

We will prove

$$
\boxed{
W\le N\sum_{j=1}^{L}\min\left\{1,\frac{2n-1}{j}\right\},
\qquad L=\min(m,N).
}
$$

Consequently,

$$
\boxed{
T=O\bigl(n^2+m+nN\log(n+1)\bigr)
\subseteq O\bigl(n^3\log(n+1)+m\bigr).
}
$$

Space is $O(n^2)$. If $N=0$ or $m=0$, then $W=0$, with an empty sum interpreted as zero. Writing $\log(n+1)$ also covers $n=1$.

The prefix-by-prefix sum alone gives only this weaker bound. A legal family gives a lower bound of $\Omega(n^3+m)$ when $m\ge n-1$; the later [general proof](research/proofs/cubic-bound.en.md) closes the logarithmic gap with a matching cubic-plus-moves upper bound.

## 2. Strategy: freeze time, then change how we count

Bounding every round by $N$ candidates and the number of rounds by $N$ only gives a quadratic bound in the road count. A more useful question is:

> Once many distinct positions must match, how many starting points can remain?

Fix the set $P$ of all displacements already visited. It contains the zero displacement and records **every** historical requirement. Its legal starting points are

$$
A(P)=\{a:a+P\subseteq F\}.
$$

We want a product bound expressing that a larger pattern permits fewer copies:

$$
\boxed{|A(P)|\,|P|\le(2n-1)N.}
$$

Comparing all copies directly is difficult because they can overlap heavily. Instead, fix one road cell and count how many copies cover it. A linear bound on that multiplicity, summed over all road cells, gives the desired product bound.

The proof has four steps:

1. Represent copies covering one road cell by anchor points inside the pattern.
2. Use unique paths in a forest to exclude nondegenerate parallelograms among those anchors.
3. Count anchors using one base point per row and a budget of horizontal distances.
4. Double-count to obtain the product bound, then sum a harmonic series over prefix sizes.

The first two steps turn the algorithmic question into a forbidden geometric configuration. The third is elementary counting. Only the last step returns to running time.

**First see how the total cost follows.** Temporarily assume the product bound: doubling the pattern size halves the candidate bound but doubles the possible number of new-position filtering rounds in that scale. Each doubling scale therefore costs at most $O(nN)$. All pattern sizes below $n$ together cost at most the same order; a surviving pattern has at most as many vertices as there are roads, leaving only $O(\log(n+1))$ scales between linear and quadratic size. This gives $O(nN\log(n+1))$ total work. Section 8 supplies the exact sum and a table of costs per scale.

The restriction concerns pattern size times candidate count. It does not claim that a pattern of linear size must leave only linearly many candidates. Nor is the product bound at one instant a bound on all scanning work; the latter still requires summing over prefixes.

## 3. Why a surviving complete prefix is a tree

A prefix here is a set of visited displacements; repeated visits contribute no new point. Each move reaches an adjacent cell, so this set is connected.

If $A(P)\ne\varnothing$, choose a legal start $a$. Translation by $p\mapsto a+p$ embeds the pattern's four-neighbour graph into the road forest. A cycle in the pattern would give a cycle in the roads. Thus the connected pattern is a tree.

The pattern also fits inside the board. If its bounding box has $H$ rows and $B$ columns, then

$$
H\le n,\qquad B\le n.
$$

Displacements may have negative coordinates. That does not affect the number of rows and columns in their bounding box: we are bounding spans, not requiring the pattern's original coordinates to lie on the board.

**Use the tree property only for prefixes with surviving candidates.** The final new displacement that empties the list may create a cycle or make the pattern too wide. We will charge that round using the old pattern, before its new displacement is tested.

## 4. From copies covering a cell to anchors inside the pattern

Fix a road cell $v$ and define

$$
S_v(P)=\{p\in P:v-p\in A(P)\}.
$$

For $p\in S_v(P)$, the starting point $a=v-p$ is legal and its complete copy is

$$
a+P=v-p+P.
$$

This copy aligns the pattern point $p$ with the road cell $v$. We call $p$ an anchor.

| Original object | The new viewpoint |
| --- | --- |
| A complete legal copy covering a fixed road cell | An anchor inside the pattern |
| Overlapping copies in the roads | Several points in one pattern |
| The total size of all copies, with multiplicity | First bound the anchors at each road cell |

For a horizontal-road example, write only column coordinates and omit the common row coordinate. Take $P=\{0,1,2\}$ and $F=\{0,\ldots,8\}$, giving all legal starts $A(P)=\{0,\ldots,6\}$. For fixed $v=4$, exactly the three copies starting at $a=2,3,4$ cover that cell; their corresponding pattern anchors are $p=2,1,0$.

![Three copies of a three-vertex pattern on one nine-vertex road cover the fixed road cell v equal to 4, corresponding to pattern anchors 2, 1, and 0.](assets/forest-bound-anchors.svg)

The lower three rows display copies on the same road at different vertical offsets for clarity; they are not separate roads. The orange circles refer to one physical cell but to different pattern positions in the copies. Once an anchor is chosen, its start is uniquely determined by $a=v-p$.

This anchor set is not the union of successful displacements from different times. Every anchor here represents a copy of **the same complete pattern**. The path comparisons below require that condition.

## 5. Main lemma: anchors cannot form a nondegenerate parallelogram

Take four distinct anchors satisfying

$$
p_0+p_3=p_1+p_2.
$$

We will prove that they are collinear. “Nondegenerate” excludes the collinear case; equally spaced points on a line can certainly occur.

### 5.1 Equal endpoints force identical paths

In the pattern, let $U$ be the unique path from $p_0$ to $p_1$. Compare two paths in the roads:

| Legal copy | Pattern path in the copy | Road start | Road end |
| --- | --- | --- | --- |
| $P-p_1+v$ | $p_0\to p_1$ | $v+p_0-p_1$ | $v$ |
| $P-p_3+v$ | $p_2\to p_3$ | $v+p_2-p_3$ | $v$ |

The parallelogram equality gives

$$
v+p_0-p_1=v+p_2-p_3.
$$

Both simple paths exist in the road forest and have the same start and end. A forest has at most one simple path between two vertices, so these paths agree edge by edge. Translating back into the pattern shows that the path from $p_2$ to $p_3$ is a translate of $U$.

Similarly, let $V$ be the path from $p_0$ to $p_2$. Comparing the copies anchored at $p_2$ and $p_3$ shows that the path from $p_1$ to $p_3$ is a translate of $V$.

Move $p_0$ to the origin and write

$$
u=p_1-p_0,\qquad w=p_2-p_0.
$$

The pattern now contains four paths:

$$
U:0\to u,\quad V:0\to w,\quad
U+w:w\to u+w,\quad V+u:u\to u+w.
$$

They form a closed walk. They may overlap and backtrack, so we cannot simply call this a simple cycle. The next step handles that difficulty.

![A contradiction diagram shows four paths paired by translation. Solid blue and dashed orange paths may overlap, while their four endpoints form a nondegenerate parallelogram.](assets/forest-bound-parallelogram.svg)

The diagram uses $u=(5,0)$ and $w=(2,3)$. Solid blue lines show U and its translate; dashed orange lines show V and its translate, with some shared segments. The shaded quadrilateral represents only the geometry of the endpoints; the actual objects being compared are the polygonal paths. **This depicts the path relations under the contradiction hypothesis, not a legal forest input.**

### 5.2 Signed area handles overlap and backtracking

For planar vectors, define the determinant

$$
\det(x,y)=x_1y_2-x_2y_1.
$$

Give a directed edge $x\to y$ weight $\det(x,y)/2$. Let $I$ be the sum of these weights along a path. Reversing an edge negates its weight.

No advanced area theorem is needed, only two elementary properties.

**Property one: every closed walk in a tree has weight zero.** Removing an edge splits the tree into two parts. A walk returning to its starting point crosses from one part to the other exactly as often as it crosses back. Each edge's two directed contributions therefore cancel.

**Property two: translating a path changes its weight only through its endpoints.** For a path from $a$ to $b$ translated by $t$,

$$
I(\gamma+t)-I(\gamma)=\frac12\det(t,b-a).
$$

Expand one edge:

$$
\det(x+t,y+t)-\det(x,y)=\det(t,y-x).
$$

Summing its displacements cancels all intermediate vertices and leaves only $b-a$.

Traverse $U$, then $V+u$, then the reverse of $U+w$, then the reverse of $V$. The weight is

$$
\begin{aligned}
I(U)+I(V+u)-I(U+w)-I(V)
&=\frac12\det(u,w)-\frac12\det(w,u)\\
&=\det(u,w).
\end{aligned}
$$

The closed walk lies entirely in the pattern tree, so its weight must also be zero. Hence

$$
\det(u,w)=0.
$$

The two displacement directions are parallel, and the four anchors are collinear. This proves the lemma.

In the diagram, $\det(u,w)=5\cdot3-0\cdot2=15$. Even after opposite traversals of overlapping blue and orange segments cancel, the whole closed walk has nonzero weight. If it lay in a tree, its weight would have to be zero. The contradiction comes from computable directed edge weights, not from visually assuming that the paths form a simple cycle.

**The reusable idea:** a forest forces paths with equal endpoints to agree; translation creates four corresponding paths; directed edge weights then turn a possibly overlapping closed walk into an algebraic contradiction. The four paths need not be disjoint.

## 6. Elementary counting: only linearly many anchors

Consider a point set in an $H\times B$ integer rectangle with no nondegenerate parallelogram.

In a nonempty row containing $k$ points, choose the leftmost point as the base. Its positive horizontal distances to the other points give $k-1$ distinct values.

**Different rows cannot use the same positive distance.** Otherwise, choosing one pair at that distance in each row produces a nondegenerate parallelogram with equal horizontal opposite sides.

![Columns 1 and 5 in the upper row and columns 3 and 7 in the lower row both have separation 4, forming a slanted parallelogram.](assets/forest-bound-row-distances.svg)

Both rows use distance $d=4$. The pairs need not be vertically aligned: equal horizontal opposite sides suffice. The dashed blue segments only connect endpoints to show the forbidden geometric configuration; they do not represent paths in the pattern.

The possible positive integer distances are $1,\ldots,B-1$. If there are $r$ nonempty rows with sizes $k_1,\ldots,k_r$, then

$$
\sum_{i=1}^{r}(k_i-1)\le B-1,\qquad r\le H.
$$

Therefore,

$$
|S|=\sum_{i=1}^{r}k_i
=r+\sum_{i=1}^{r}(k_i-1)
\le H+B-1.
$$

Think of one base point per row as free. Every additional point consumes a horizontal distance that no other row may reuse. Both the row budget and the distance budget are linear.

Applying this to the anchors gives

$$
\boxed{|S_v(P)|\le H+B-1\le2n-1.}
$$

This counting argument is the rectangular version of the proof of [Proposition 3.5](https://arxiv.org/html/2601.14465v2#S3.SS2) by Jánosik, Nádor, Nagy, and Simon. The complete argument is included above, so reading that paper is not a prerequisite.

## 7. Double-counting the pattern-copy product

Count all pairs

$$
(a,p)\in A(P)\times P.
$$

Counting by legal starting point gives $|A(P)|\,|P|$ pairs.

Instead, count by the road cell $v=a+p$. For fixed $v$, legal pairs correspond bijectively to anchors in $S_v(P)$: an anchor determines its start uniquely as $a=v-p$. Thus

$$
\boxed{
|A(P)|\,|P|
=\sum_{v\in F}|S_v(P)|
\le(H+B-1)N
\le(2n-1)N.
}
$$

This counts copies with multiplicity, rather than bounding the size of their union. Copies may overlap; we have bounded how often any road cell can be covered.

Return to the horizontal-road example in Section 4. Seven legal starts each carry three pattern vertices, giving twenty-one pairs when counted by copy. From left to right, the road-cell multiplicities are one, two, three, three, three, three, three, two, and one, so

$$
7\cdot3=1+2+3+3+3+3+3+2+1=21.
$$

The union has only nine road vertices, but the double-counted total is twenty-one. Overlap does not remove these pairs.

If $A(P)=\varnothing$, the left side is zero and the inequality still holds.

## 8. Summing all rounds: where the logarithm enters

Number the rounds that actually execute the candidate loop. Let $q_j$ be the new displacement tested in round $j$, and write

$$
q_0=0,\qquad P_{j-1}=\{q_0,\ldots,q_{j-1}\}.
$$

Before round $j$, exactly $j$ distinct displacements have been recorded and the candidates are $A(P_{j-1})$. Apply the product bound and the trivial road-count bound:

$$
|A(P_{j-1})|
\le\min\left\{N,\frac{(2n-1)N}{j}\right\}.
$$

This explains the denominator $j$: the current new displacement is not yet in the old pattern, while the initial zero displacement already is.

Whenever a candidate loop is executed, the old candidate set is nonempty. The old pattern embeds into the roads, so $j\le N$. Every round also requires a move. The number of filtering rounds $K$ therefore satisfies

$$
K\le\min(m,N)=L.
$$

This includes the last filter that may empty the list. When a displacement coordinate reaches the board side length in absolute value, the program clears the list without running the candidate loop. Repeated displacements and moves after the list becomes empty only require constant work each.

Summing the rounds gives

$$
W=\sum_{j=1}^{K}|A(P_{j-1})|
\le N\sum_{j=1}^{L}\min\left\{1,\frac{2n-1}{j}\right\}.
$$

Set $c=2n-1$. If $L\le c$, then $W\le NL\le cN$. If $L>c$,

$$
\begin{aligned}
W
&\le cN+cN\sum_{j=c+1}^{L}\frac1j\\
&\le cN\left(1+\ln\frac{L}{c}\right).
\end{aligned}
$$

Since $L\le N\le n^2$, this yields

$$
W=O(nN\log(n+1)).
$$

The same phenomenon can be viewed in doubling intervals: when the pattern size doubles, the candidate bound halves, but the number of rounds in that interval doubles. Each scale costs at most the road count times the side length, and there are logarithmically many scales. **The logarithm comes from summing scales, not from a graph traversal or a data-structure operation.**

Retaining $c=2n-1$, group the pattern size j before each scan into the following intervals to make that explanation quantitative. Every interval is truncated at the actual number of scanning rounds; empty intervals are ignored.

| Pattern-size interval | Maximum rounds | Maximum candidates per round | Maximum checks in this interval |
| --- | --- | --- | --- |
| $1\le j<c$ | $c-1$ | $N$ | $(c-1)N$ |
| $c\le j<2c$ | $c$ | $N$ | $cN$ |
| $2c\le j<4c$ | $2c$ | $N/2$ | $cN$ |
| $4c\le j<8c$ | $4c$ | $N/4$ | $cN$ |
| $2^r c\le j<2^{r+1}c$, where $r\ge0$ | $2^r c$ | $N/2^r$ | $cN$ |

The last row generalizes the doubling intervals above; it is not an additional interval. Since $c=\Theta(n)$, every interval costs at most $O(nN)$. While candidates survive, the pattern has at most $N\le n^2$ vertices, leaving at most $O(\log(n+1))$ intervals in total. These are upper bounds, not a claim that any input spends the full allowance at every scale.

## 9. The limit of prefix-by-prefix counting and how the logarithm was removed

The product bound applies to each fixed prefix. Summing the worst bound for every prefix may charge the same road resources repeatedly. This static inequality alone does not control the combined cost across prefixes.

Two questions must be distinguished:

- Can one prefix approach the product bound? Yes: legal comb families attain its order at several parameter scales.
- Can one board and one actual query spend a full road-count-times-side-length budget at an increasing number of scales? The later bound on the entire history excludes this cumulative behavior.

Choosing a different input for each scale and adding their costs does not establish a running-time lower bound. Conversely, a decreasing candidate set does not automatically turn the harmonic sum into a constant.

The later [general proof](research/proofs/cubic-bound.en.md) groups all successful checks by horizontal labels and uses each label intersection at most four times, bounding the whole history at once. It does not sharpen each static product inequality separately. The [research overview](complexity-research.en.md) retains the subclass results, counterexamples, and changes of direction that led to this proof.

## 10. Common pitfalls

| Tempting claim | Required correction |
| --- | --- |
| Few distinct displacements imply cubic total time | The sum of candidate counts still needs a bound |
| All historical successful displacements avoid nondegenerate parallelograms | The lemma applies to anchors of one complete pattern |
| The four corresponding paths form a simple cycle | They may overlap; use directed weights on a closed walk |
| No growth of the copy union means no new cost | Successful checks can occur without union growth |
| The final new pattern is still a tree | Only the old pattern with surviving candidates is guaranteed to be a tree |
| A large auxiliary count is an algorithmic counterexample | Actual candidates, complete prefixes, and the real move count must be checked |
| The bitset implementation has the same scan bound | This proof counts list candidates; bitset rounds have a different cost |

The main lessons are to **fix a complete state, change the direction of counting, and turn acyclicity into a geometric restriction that can be counted.**
