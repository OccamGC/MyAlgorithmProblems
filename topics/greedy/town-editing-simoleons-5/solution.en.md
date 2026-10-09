# Edit Town and Simoleons 5: Solution

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

## Attaining the Bound with Fixed Positions

First merge richer external households having the same initial mean. Both ends of every such move have equal means, so personal wealth is unchanged. Only $g$ richer source households remain.

Merge all external households no richer than the targets into one collection household. These people never participate in the grid; their merged mean remains at most $a$ , leaving the upper bound unchanged. If there are no such residents, reserve an empty collection position instead. Split the targets into $k$ single-person households.

This needs $k+g+1$ positions. Merging frees positions, leaving enough empties before targets are separated. The stated position bound makes preparation possible even if every position is initially occupied.

Process richer source households in ascending mean order. Take one resident at a time, visit every target household, and then enter the collection household. Each visit averages exactly two people, and residents left in the source retain its initial mean. Visit targets in grid row order, which is their current descending wealth order. The collection household is never used again.

After all outsiders have been processed, merge the targets. Their sum is unchanged and equals the grid's upper bound. Every move has used an existing position.

![Merging equal-mean households frees positions; targets finish with 16](assets/example.svg)

## Contributions by Wealth Level

Expanding all residents is infeasible: total population can approach $10^{12}$ . Subtract $a$ from all values so that targets start at zero. An outsider followed by $s$ later outsiders has coefficient

$$w_s=\sum_{i=1}^k\binom{s+i-1}{i-1}2^{-(s+i)}$$

in the final target sum. Grid paths from this column's upper boundary to row $i$ in the last column number $\binom{s+i-1}{i-1}$ , each containing $s+i$ halvings.

Define $F(s)=\sum_{t=s}^{\infty}w_t$ . Then

$$F(0)=k,\qquad F(s)=2^{-s}\sum_{j=0}^{k-1}(k-j)\binom{s+j-1}{j}2^{-j}\quad(s\ge1).$$

For a proof, fix $i$ . The probability of exactly $t$ tails before the $i$-th head of fair coin flips is $\binom{t+i-1}{i-1}2^{-(t+i)}$ . At least $s$ tails occur exactly when there are $j<i$ heads before the $s$-th tail. Sum over those $j$ , then over $i$; each $j$ occurs $k-j$ times. This probability argument derives a rational identity. The program evaluates only the finite expression modulo $P$ .

Group richer outsiders by initial mean and scan groups from highest to lowest. If $s$ people have been processed and the current group has $c$ people of mean $v$ , its contribution is

$$(v-a)\bigl(F(s)-F(s+c)\bigr).$$

Add these contributions to $m_1$ . Each tail takes $O(k)$ operations, using

$$\binom{s+j-1}{j}=\binom{s+j-2}{j-1}\frac{s+j-1}{j}.$$

## Exact Grouping and Counts beyond the Modulus

While reading, compare $m_i k>m_1p_i$ using 64-bit products, then compare against at most three existing groups using $m_i p_{\mathrm{rep}}=m_{\mathrm{rep}}p_i$ . No million-element sort or floating-point comparison is needed.

Store each group's total count and one initial representative's $p_{\mathrm{rep}},m_{\mathrm{rep}}$ . Compute the mean as $m_{\mathrm{rep}}/p_{\mathrm{rep}}$ . Do not invert the aggregated population: it may be a multiple of $P$ . Initial household populations are at most one million and therefore invertible.

Use 64-bit total counts and keep the full exponent $s$ . The binomial recurrence divides only by $1,\ldots,k-1<P$ , so it remains valid when $s\ge P$ . Reduce $s+j-1$ modulo $P$ before multiplying to prevent 64-bit overflow. Update $2^{-s}$ by multiplying by $2^{-c}$ , computed by exponentiation for each group.

The attaining strategy changes target personal values through initial population denominators and two-person averages. Final merging preserves their total. Thus the answer's denominator is coprime to $P$ .

## Complexity, Alternatives, and Verification

Let $Q$ be the total richer outsider population. Grouping takes $O(n(g+1))$ time, calculation takes $O(k+g(k+\log P+\log(Q+1)))$ , and space is $O(k+g)$ . With $g\le3,k\le20$ , input dominates. The [reference](std.cpp) uses this tail method.

The [forward convolution method](solution-alternative-forward.en.md) updates individual targets in $O(k^2)$ per group. It also passes the full constraints and supplies another calculation method. Both share the optimality proof, while evaluating the grid in different directions.

Small inputs use an exact Fraction grid. Large inputs are checked by generic matrix exponentiation, with the matrix built directly from single-person averages. Legal move simulations cover initially full towns, tight position bounds, equivalent fractions, and counts crossing the modulus. See [testing instructions](tests/README.md) and [measurements](../../../docs/benchmark-R42.json).
