# Matching in a Class of Four-Neighbor Grid Forests: A Cubic Bound for Path Components

**Historical research record (updated 2026-10-12).** The [standalone proof](cubic-bound.en.md) now establishes the general cubic bound. The derivations, remainders, and counterexamples below retain their historical order. Statements that a problem is unresolved refer to that stage or local method; stronger auxiliary claims do not automatically follow from the general bound.

This document gives a self-contained analysis of the [candidate-list implementation](../../std.cpp) when every component of the road forest is a path. The proof was prepared by Codex (GPT-6). See the [main complexity proof](../../complexity.en.md) for general forests.

The subsequent [root-to-leaf path proof](complexity-chains.en.md) improves this subclass to $W\le(6n-5)N$ and also covers path queries on branching roads. This document retains the original direction-string border argument and its independent lemma.

## Result and scope

Let $F$ be the set of road cells, with $N\le n^2$ cells. If the road forest has maximum degree at most $2$, so that every component is a path or an isolated vertex, then every input walk satisfies

$$
\boxed{W\le(16n+1)N,\qquad
T=O(n^2+m+nN)\subseteq O(n^3+m),}
$$

where $W$ is the total number of candidate checks.

The query may extend either end of the visited path and may move repeatedly among previously visited offsets. If a new offset creates a branch, no candidate can pass that round: a road path cannot contain a branch.

The disjoint horizontal stripes used for the lower bound in the main complexity proof also belong to this subclass. Consequently, when $m\ge n-1$, its worst-case bounds meet at $\Theta(n^3+m)$.

## A bound on borders of a direction string

Encode a grid path with no repeated vertices as a direction string $w$, whose length $L$ is its number of edges. A nonempty string is a **border** of $w$ if it is both a prefix and a suffix. We include the entire string $w$ and write $B(w)$ for the number of borders.

**Lemma.** If the path can be translated into an $n\times n$ grid, then

$$
B(w)\le4n.
$$

The lemma only requires that the path have no repeated vertices; it need not be an induced path. The following proof does not rely on an external string theorem.

### 1. The shortest period and the longest border

An integer $p\in[1,L]$ is a period of a string if $w_i=w_{i+p}$ whenever both positions are defined. If $p$ is the shortest period, the longest proper border has length $L-p$. This length is zero if there is no nonempty proper border.

All borders can be listed by repeatedly replacing the current string with its longest proper border. Every shorter border is also a border of the longest proper border, and the converse holds. Thus each positive length in this chain represents exactly one nonempty border.

### 2. Prefixes at least twice as long as the period

Suppose the shortest period of $w$ is $p$. Any prefix of length $\ell\ge2p$ certainly has period $p$.

Suppose it also has a period $q<p$. For $0\le i<p$, both positions $i$ and $i+q$ lie within the first $2p$ letters, so

$$
w_i=w_{i+q}=w_{(i+q)\bmod p}.
$$

The period block of length $p$ is therefore unchanged by a cyclic shift of $q$. The infinite string obtained by repeating this block has period $q$, so the original string $w$ also has period $q$, contradicting the choice of the shortest period.

Hence the prefix still has shortest period $p$, and its longest proper border has length $\ell-p$.

### 3. Removing borders in stages

Consider the current string in the border chain. Let its length be $L$ and its shortest period be $p$, and write

$$
k=\left\lfloor\frac Lp\right\rfloor,\qquad
L=kp+t,\quad 0\le t<p.
$$

If $k=1$, the longest proper border has length $L-p<L/2$. This stage removes the entry for the current whole string and at least halves the length. If the remaining length is zero, the chain ends.

If $k\ge2$, the preceding section lets us remove $k-1$ consecutive entries, with lengths

$$
L,L-p,\ldots,2p+t,
$$

leaving a string of length

$$
L'=p+t<2p.
$$

The cost of this stage is $k-1$, while the factor by which the length decreases satisfies

$$
\frac L{L'}=\frac{kp+t}{p+t}\ge\frac{k+1}{2}.
$$

The remaining string is a prefix of the original direction string. It still describes a path with no repeated vertices that fits in the same grid, so all assumptions remain available in later stages.

### 4. The grid bounds the number of period repetitions

Let $d$ be the displacement of the first $p$ steps. Since the path has no repeated vertices, $d\ne0$. Periodicity makes the vertices after

$$
0,p,2p,\ldots,kp
$$

steps form the arithmetic progression

$$
x_0,x_0+d,x_0+2d,\ldots,x_0+kd.
$$

At least one coordinate of the nonzero integer vector $d$ has absolute value at least $1$. All these vertices lie in an $n\times n$ grid, so

$$
k\le n-1.
$$

### 5. Summing the costs of the stages

First suppose $n\ge4$, and set

$$
C_n=\frac{n-2}{\ln(n/2)}.
$$

The function $r/\ln(1+r/2)$ is increasing for $r>0$. Therefore, in a stage with $k\ge2$, setting $r=k-1\le n-2$ gives

$$
k-1\le C_n\ln\frac{k+1}{2}
\le C_n\ln\frac L{L'}.
$$

A stage with $k=1$ and a nonempty remainder costs $1$ and at least halves the length. Since $C_n\ge1/\ln2$, it satisfies the same cost bound.

Charge $1$ separately for the final step from a positive length to zero. Summing the logarithms over all other stages gives

$$
B(w)\le C_n\ln L+1.
$$

A path with no repeated vertices uses at most $n^2$ cells, so $L<n^2$. Using $\ln n\le2\ln(n/2)$ for $n\ge4$, we obtain

$$
B(w)\le\frac{2(n-2)\ln n}{\ln(n/2)}+1
\le4n-7<4n.
$$

For $n\le3$, the direct bound $B(w)\le L\le n^2-1\le4n$ suffices. The empty string has no nonempty borders. This proves the lemma.

## A road path with query growth at one end

First suppose all new query offsets are added consecutively along a simple path from a fixed starting point. Let its direction string be $S$.

Fix a road cell $v$ and a host edge $e$ used to enter $v$. Collect all successful checks that end at $v$ and use $e$ on their last step. Let $j$ be the number of edges added along the query path at such a check.

The host component is a path. Starting at $v$ and following $e$ backwards has a unique continuation, so the host segments for these successful checks are nested by length.

Let $J$ be the largest successful length in this group. The direction string $S[0:J]$ describes a simple path that fits in the road grid. Every shorter successful length $j$ satisfies

$$
S[0:j]=S[J-j:J].
$$

String intervals here include their left endpoint and exclude their right endpoint. Thus every successful length is a border of $S[0:J]$. By the lemma, this group contains at most $4n$ successful checks.

A road path has at most two edges incident to $v$, so growth at one end gives the following bound on the total number of successful checks at each cell:

$$
H(v)\le8n.
$$

## Alternating between both ends and allowing arbitrary walks

As long as a candidate remains, the graph induced by all visited offsets must translate into a host path. It is therefore itself a path. Keeping the initial offset $0$ as a fixed root splits this path into at most two arms extending from the root.

New cells on either arm can only be discovered in order from the root outwards. Let the direction strings of the two arms be $S_1,S_2$. Alternating between the arms, or moving among old cells, does not change the prefix relation on either arm.

Fix $v$, one query arm, and the host edge used to enter $v$. Every successful check of the entire query prefix also satisfies the weaker condition of following only that arm from the root to the newly added cell. Ignoring the other arm can only add valid starting points; it cannot discard any success we need to count.

The successes in this group can therefore be mapped to borders of one arm direction string exactly as in the preceding section. The compared strings are **arm prefixes from the fixed root**, so growth at the other end does not disrupt the prefix–suffix relation.

Each target cell has at most two query arms and two host entry edges, giving four groups. Hence

$$
\boxed{H(v)\le16n.}
$$

If a step makes the offset graph branch, form a cycle, or otherwise fail to fit in a host path, that round has no successful checks and leaves no candidates. Such a step does not increase the number of successful checks.

## Total scanning cost and the boundary of the proof

Each candidate starting point fails and is removed at most once, so there are at most $N$ failed checks. Counting successful checks by their target road cells gives

$$
W\le N+\sum_{v\in F}H(v)\le(16n+1)N.
$$

Adding $O(n^2+m)$ for initialization and input processing proves the stated time bound.

The key property is that, in a host path, extending backwards from a target cell through a fixed entry edge never branches. A general road tree does not have this property: two reverse paths may diverge farther away and need not be nested by length. The proof therefore applies only when the road forest has maximum degree at most two.
