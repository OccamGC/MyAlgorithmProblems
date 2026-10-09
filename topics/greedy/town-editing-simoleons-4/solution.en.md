# Edit Town and Simoleons 4: Solution

Codex (GPT-6) provides the fixed-position construction, optimality proof, batched formulas, implementations, and verification.

## Personal Wealth and the Averaging Grid

Let $k=p_1$ and $a=m_1/k$ . Define each resident's personal wealth as the mean of their household. A departing person leaves the source's remaining mean unchanged. Joining another household averages the wealth of the mover and all destination residents. Thus every legal move is a complete average of a subset of people.

First relax the position limit to obtain an upper bound for all averaging operations. Then construct a sequence attaining that bound within the fixed positions.

## An Upper Bound for Every Editing Sequence

This argument permits unequal current wealth among target members, so it applies to intermediate states as well.

Sort everyone by nondecreasing wealth, labeling targets $T$ and outsiders $O$ . Whenever adjacent labels are $TO$ , average those two values and exchange their positions in the sorted list. Their values are equal afterward, so the list remains sorted. Continue until all $O$ labels precede all $T$ labels. Let $\Phi$ be the resulting target sum.

**The choice of operations does not affect the result.** Each operation removes one label inversion. Two simultaneously available $TO$ pairs cannot overlap, so their operations commute. Induction on the number of inversions gives the same final wealth vector for every execution order.

**Each operation does not decrease target wealth.** The target in a pair is no richer than the outsider. Thus $\Phi$ is at least the current target sum, and it is reachable in finitely many edits when positions are unrestricted.

**No pairwise average increases $\Phi$ .** Fix the initial wealth ordering. The operations are then a fixed sequence of adjacent averaging matrices, making $\Phi$ linear in the initial coordinates. At the end, the target-sum coefficients in sorted order are

$$0,0,\ldots,0,1,1,\ldots,1.$$

Propagating these coefficients backward averages adjacent coefficients at each step, preserving their nondecreasing order. A richer initial coordinate therefore has a coefficient at least as large as a poorer coordinate.

Now continuously bring any two values $x<y$ toward their mean. On a segment with fixed ordering, their coefficients satisfy $c_x\le c_y$ . Transferring $\delta$ to the poorer coordinate changes the potential by

$$\delta(c_x-c_y)\le0.$$

The function is continuous when the ordering changes. Exchanging equal-valued residents of the same type has no effect. For different types, first perform the zero-change $TO$ operation at equality to obtain the other ordering’s problem. There are finitely many ordering segments, so averaging the pair cannot increase $\Phi$ .

**Averaging a larger group also cannot increase $\Phi$ .** Repeated pairwise averages within that group approach its common mean. Continuity extends the bound to this limit. The limit is used only to prove an upper bound; the strategy attaining it remains finite.

After any edits, the target sum is at most the current $\Phi$ , which is at most its initial value. The adjacent strategy attains that initial value, proving optimality.

## The Recurrence

Every target initially has wealth $a$ . Outsiders no richer than $a$ need not participate. Sort the remaining $r$ initial personal values as $v_1\le\cdots\le v_r$ .

The adjacent averages form a grid:

$$x_{i,0}=a,\qquad x_{0,j}=v_j,\qquad x_{i,j}=\frac{x_{i-1,j}+x_{i,j-1}}2.$$

The optimum is $\sum_{i=1}^k x_{i,r}$ . In column order, one outsider visits targets from currently richest to poorest. In row order, one target visits all outsiders. Both traversals respect the same dependencies and produce the same result: a cell involves only its row's target and its column's outsider, so ready operations in different rows and columns act on disjoint people.

## Why One Empty Position Suffices

Every outsider initially lives alone. Keep the target source household and reserve one initially empty position as a collection household.

Take targets one at a time. Each visits every richer outsider in ascending order of initial wealth, then enters the collection household. Each visit averages exactly two residents; after the target leaves, the outsider is alone again. Targets still in the source each retain wealth $a$ , giving the correct starting value for the next row.

Collected targets never participate again. Mixing them changes individual values but preserves their sum. This exactly evaluates the grid by rows and reunites all targets in the collection household. The source, the outsiders' individual positions, and one collection position suffice regardless of the number of targets.

![Two target visits reunite the targets in D](assets/example.svg)

This finite construction attains the upper bound, so the maximum exists. The algorithm does not execute the potentially $k(r+1)$ moves.

## Processing All Targets at Once

Let $z_j=v_j-a$ be the outsiders' excess wealth, arranged in a nondecreasing column vector $z$ . After one target starting with excess zero visits all outsiders, their excess vector becomes $Bz$ , where

$$B=\frac12(I-L/2)^{-1}.$$

Here $L$ is the $r\times r$ downward shift matrix. The resulting values satisfy $y_i=(y_{i-1}+z_i)/2$ with $y_0=0$ , establishing this matrix expression.

After all $k$ targets, the outsiders' excess vector is $B^kz$ . Since $L^r=0$ , its binomial expansion is finite:

$$B^k=\sum_{d=0}^{r-1}c_d L^d,\qquad c_d=2^{-(k+d)}\binom{k+d-1}{d}.$$

Define $C_d=\sum_{t=0}^d c_t$ . Initial outsider $j$ contributes coefficient $C_{r-j}$ to the final total outsider excess. Conservation of wealth gives

$$W=m_1+\sum_{j=1}^r(v_j-a)(1-C_{r-j}).$$

Scan outsiders from greatest to least wealth and update

$$c_0=2^{-k},\qquad c_d=c_{d-1}\frac{k+d-1}{2d}\quad(d\ge1).$$

After sorting, the answer takes linear time. If $r=0$ , output $m_1$ directly.

## Modular Arithmetic and Complexity

Compare actual integer values: an outsider with wealth $v$ is richer exactly when $vk>m_1$ . Products can reach $10^{15}$ , so use 64-bit integers. Modular values cannot be used for wealth comparisons.

Precompute inverses of $1,\ldots,r$ and use exponentiation for $k^{-1}$ and $2^{-k}$ . Here $k,r<P$ and $k+r-1<P$ , so all divisors in the recurrence are invertible. The attaining construction introduces only the initial denominator $k$ and repeated divisions by 2, making the final denominator coprime to $P$ .

Time is $O(n+r\log r+r+\log P+\log k)$ and space is $O(r)$ , where $r$ counts richer outsiders. The number of targets can be one million. The [reference program](std.cpp) implements this recurrence.

## Verification

Small instances are compared with an exact Fraction grid. A move-by-move simulation checks fixed positions, conservation, and target identity. Large target counts with few outsiders use generic matrix exponentiation; large inputs with few wealth levels use a column-wise tail formula. Tests also include one million distinct wealth values and no beneficial outsider.

One general large input uses a factorial implementation of the same coefficient identity, which is not an independent optimality proof. Correctness rests on the upper bound and attaining construction above. See [measurements](../../../docs/benchmark-R42.json) and [reproduction instructions](tests/README.md).
