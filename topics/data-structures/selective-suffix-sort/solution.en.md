# Sorting Selected Suffix Elements: Solution

**Problem setter’s solution: active inversion contributions and two segment-tree layers. GPT-6 supplies the invariant proof, the inactive-pivot boundary repair, and a standard C++17 implementation.**

## 1. Contributions that disappear permanently

Let $c_i$ count inversions whose left endpoint is position $i$ . The answer is $\sum_i c_i$ . Call a position active when $c_i>0$ .

After an operation, every selected position is a suffix minimum. Later selected values are at least its new value, and later unselected values are at least the original pivot. Thus its contribution becomes zero.

A suffix minimum never becomes active again:

- An operation starting to its right preserves the multiset of its suffix.
- If it is selected again, the same argument makes it a suffix minimum.
- If an earlier operation leaves it unselected, its value is at least the pivot. No smaller selected value can lie after it, because that would contradict the suffix-minimum property. Therefore no selected value is moved into its suffix.

Each position becomes inactive at most once. Every active position still contains its initial value, so there is no need to maintain the actual reordered array.

## 2. The exact effect of an operation

If $c_k=0$ , the selected set contains only $k$ ; skip the operation. Otherwise let $P$ be its initial value.

1. Clear position $k$ and every active position $i>k$ whose initial value is below $P$ .
2. Subtract one from each remaining active position $i>k$ whose initial value equals $P$ .
3. Leave all other contributions unchanged.

The first rule follows from selected positions becoming suffix minima. For an unselected active position after $k$ , a value above $P$ sees the same number of selected slots to its right, all containing smaller values. A value equal to $P$ loses exactly one inversion: the one selected value equal to $P$ moves from $k$ to the last selected slot. Activity guarantees a smaller value to this position’s right, so that last slot is indeed to its right. Positions before $k$ see an unchanged suffix multiset.

In sample two, only position $2$ contributes one after the first operation. Selecting position $1$ again must be skipped; using its stale initial value $2$ would incorrectly change another contribution.

## 3. Two segment-tree layers

Compress the initial values. A Fenwick tree scanning from right to left computes all initial contributions.

A global segment tree over positions stores the smallest initial value among active positions, or infinity when none remain. When clearing a suffix below $P$ , discard any whole interval whose minimum is at least $P$ .

For each distinct initial value, build another segment tree over its original positions. Store:

- the smallest positive contribution, treating zero as infinity;
- the number of active positions;
- a lazy subtraction applied to all active contributions.

Before clearing a single position, push its group’s lazy tags and subtract its true contribution from the answer. To subtract one from a suffix of an equal-value group, lazily process a fully covered node if its minimum exceeds one, reducing the answer by its active count. Otherwise descend to the leaves that become zero and remove them from the global tree. Empty nodes ignore lazy updates.

## 4. Correctness and complexity

The Fenwick initialization is exact. Section two proves the exact change to every contribution, and inactive positions remain inactive. Induction therefore proves every output, including the previous answer used by encoded instructions.

Ordinary range boundaries cost logarithmic time. Extra descents that clear positions or locate new zero contributions are charged to permanently removed positions. Each position is removed once and touches both trees logarithmically. Total time is $O((n+m)\log n)$ and space is $O(n)$ ; all value-group trees together have linear size.

The answer can reach $n(n-1)/2$ , so use signed 64-bit arithmetic. Normalize negative remainders into $0,\ldots,n-1$ . Explicitly sorting selected array elements repeatedly may revisit too many inactive positions for the full range.

[Reference program](std.cpp).

## Illustration

In the figure, $a(0),a(1)$ are the arrays before and after the first sort. Circles show values; $c$ below each circle is that position’s outgoing inversion contribution. Blue positions are selected, and the contribution sum drops from five to one.

![Algorithm illustration](assets/example.svg)

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables stay outside the published package. See the [reference measurements](../../../docs/benchmark-R29.json) for runtime and memory.
