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

For any complete set $P$ of already visited displacements, let $A(P)$ be its legal translation starts. The proved product bound is
$$
|A(P)|\,|P|\le(2n-1)N.
$$
Its key idea is to fix a road target and represent complete copies covering it as anchors inside the pattern. Unique paths in the forest exclude nondegenerate parallelograms, and elementary row-distance counting bounds the anchors linearly.

Before filtering round $j$, the old pattern has exactly $j$ points. There are at most $L=\min(m,N)$ filtering rounds, giving
$$
W\le N\sum_{j=1}^{L}\min\left\{1,\frac{2n-1}{j}\right\}.
$$
Hence the general upper bound is
$$
\boxed{O(n^2+m+nN\log(n+1))\subseteq O(n^3\log(n+1)+m)}.
$$

- [Detailed proof](complexity.en.md): the counting strategy, geometric lemma, double counting, and harmonic sum.
- [Research overview](complexity-research.en.md): solved subclasses, refuted auxiliary claims, the current remainder, and open directions.
- [Research directory](research/README.md): detailed proofs, constructions, representative inputs, and a verification script.

A general cubic upper bound remains unproved. The striped input below gives a cubic lower bound. Subclasses already without the logarithm include bounded leaf counts, path roads, some branching restrictions, and straight comb queries.

For short move sequences, the generic bound is also available:
$$
O(n^2+m+N\min(m,N)).
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
candidate checks. Later moves require no new filters, but input and output still take $\Omega(m)$ time. Hence, for $m\ge n-1$, this valid family gives a worst-case time lower bound of $\Omega(n^3+m)$. It establishes the cubic lower bound; an $O(n^3+m)$ upper bound for general $m$ still requires a separate proof.

## Why acyclicity matters

If cycles are allowed, make the entire grid road and visit every offset in $\{0,\ldots,k\}^2$, where $k=\lfloor n/2\rfloor$. A row-by-row serpentine route uses $(k+1)^2-1=\Theta(n^2)$ moves, with a different offset at every step.

Every offset stays inside this small square, so at least $(n-k)^2=\Theta(n^2)$ candidates remain throughout. The total number of checks is therefore $\Theta(n^4)$. This attains the quartic bound for general grids. The grid contains cycles and is not a counterexample to the original conjecture.

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables are kept outside the published package. See the [reference measurements](../../../docs/benchmark-R28.json) for runtime and memory.
