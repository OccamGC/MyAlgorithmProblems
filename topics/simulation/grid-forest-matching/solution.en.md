# Matching in a Class of Four-Neighbor Grid Forests — Solution

## Method and contribution

Use the problem setter's candidate filtering with repeated cumulative offsets skipped. Codex (GPT-6) supplies the set invariant, explicit bounds, provable workload analysis and standard C++17 implementation. The [candidate-list program](std.cpp) is preferred. The [bitset explanation](solution-alternative-bitsets.en.md) and [program](alternative-bitsets.cpp) process several starts in each machine word.

## The set of offsets determines validity

Let $(x_t,y_t)$ be the cumulative displacement after $t$ moves, with initial offset $(0,0)$ . Start $(r,c)$ is valid exactly when
$$
(r+x_i,c+y_i)
$$
is an in-bounds road cell for every $0\le i\le t$ . Each step adds one required road position.

The circles in the figure mark valid starting cells for successive prefixes of sample one. Their counts $Q_t$ are seven, four, two and one. They mark starts, not current positions.

![Filtering the starting cells in sample one](assets/example.svg)

If an offset has appeared before, its condition has already been tested and cannot eliminate another candidate. It is the two-dimensional cumulative offset that matters, not whether the direction has been repeated.

## Filter a candidate list

Initialize the list with all road cells and mark the zero offset visited. After reading a direction, update the offset:

1. If the list is empty, continue reading directions and print zero.
2. If either coordinate has absolute value at least $n$ , every start is out of bounds; clear the list.
3. On the first visit to an offset, test each candidate translated by that offset. Compact the list in place, retaining only in-bounds road cells.
4. Print the list length.

Deleted starts are never reinserted, so returning to a road later cannot restore them. Shift signed offset coordinates by a fixed origin in the visited array, and access that array only while candidates remain and the offset is within its safe range.

**Invariant.** Initially the list contains precisely the valid starts. A new offset adds exactly the current road-cell condition; an old offset adds no condition. Induction proves that the list always represents validity for the entire prefix.

## Proved complexity

Let $N\le n^2$ be the road count and $W$ the total number of actual candidate checks. The list implementation takes
$$
O(n^2+m+W)
$$
time and $O(n^2)$ space. Board reading, moves, and output have been accounted for separately; the main quantity is the sum of candidate counts over all rounds.

The following scan bound is now proved for the entire history:
$$
\boxed{W\le(5n-3)N},\qquad
\boxed{T=O(n^2+m+nN)\subseteq O(n^3+m)}.
$$

Group successful checks by host target and query row, pairing every later check with the group's earliest success, called its star. A pair's horizontal displacement is its label $h$. Its complete early prefix supplies a resource inside the intersection $G_h=F\cap(F-h)$.

For one label, pay its common-cut class with one intersection budget. In each remaining intersection component, choose a reference class with latest early endpoint and pay it with one more budget. Every remaining resource spans less than one label length on the host axis, whereas different copies of the same early endpoint are farther apart than that length. Bin resource projection left endpoints: each bin has distinct early endpoints and a unit allocation, while a road vertex participates in at most two bins. Thus four intersection budgets suffice per label:
$$
\widetilde M_h\le4|G_h|,\qquad
\sum_{h=(0,d),\ d\ne0}|G_h|
=\sum_r k_r(k_r-1)\le(n-1)N.
$$
Here $k_r$ is the road count in row $r$. Add at most $nN$ stars and one failed check per candidate to obtain the scan bound. The key separation lemma uses two actual complete reference late prefixes and covers straight axes, curved axes, and all powers.

- [Complete general cubic proof](research/proofs/cubic-bound.en.md): the counting strategy, common cut, finite second-axis lemma, capacity-two bins, and sum over labels.
- [Earlier product bound and logarithmic proof](complexity.en.md): retained anchor diagrams, geometric lemmas, and harmonic summation explain where the old logarithm came from.
- [Research overview](complexity-research.en.md) and [directory](research/README.md): completion of the general proof, valid subclass results, failed approaches, and verification scripts.

For short move sequences, combine this with at most one full-road scan per move:
$$
O(n^2+m+N\min(m,n)).
$$
The bitset implementation scans machine words each round; see its [separate editorial](solution-alternative-bitsets.en.md). It does not inherit the candidate-check bound directly. Reproducible measurements are in the [performance record](../../../docs/benchmark-R28.json); measurements do not replace complexity proofs.

## A rigorous cubic lower bound

Make every odd-numbered row entirely road and every even-numbered row entirely obstacles. The road graph consists of $r=\lceil n/2\rceil$ disjoint paths of $n$ vertices each, so it is a forest. For $n\ge2$, first move right $n-1$ times. If more moves are needed, alternate left and right between the last two offsets already visited.

Before the $j$-th right move, each path still supplies $n-j+1$ candidates, and the new offset has never appeared before. The first $n-1$ moves therefore perform exactly
$$
\sum_{j=1}^{n-1}r(n-j+1)
=r\left(\frac{n(n+1)}2-1\right)
=\Theta(n^3)
$$
candidate checks. Later moves require no new filters, but input and output still take $\Omega(m)$ time. Hence, for $m\ge n-1$, this valid family gives a worst-case time lower bound of $\Omega(n^3+m)$, matching the general $O(n^3+m)$ upper bound.

## Why acyclicity matters

If cycles are allowed, make the entire grid road and visit every offset in $\{0,\ldots,k\}^2$, where $k=\lfloor n/2\rfloor$. A row-by-row serpentine route uses $(k+1)^2-1=\Theta(n^2)$ moves, with a different offset at every step.

Every offset stays inside this small square, so at least $(n-k)^2=\Theta(n^2)$ candidates remain throughout. The total number of checks is therefore $\Theta(n^4)$. This attains the quartic bound for general grids. The grid contains cycles and is not a counterexample to the original conjecture.

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables are kept outside the published package. See the [reference measurements](../../../docs/benchmark-R28.json) for runtime and memory.
