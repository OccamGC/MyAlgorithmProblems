# Distributing into Unlabeled Containers: Solution

## Method and contributions

Codex (GPT-6) applies partition conjugation and the standard unbounded-knapsack recurrence in [std.cpp](std.cpp), with proof and implementation. The [pentagonal-number and generating-function alternative](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), reduces the work when the container count is close to the item count. Both support the full range with linear space.

Items and containers are each indistinguishable. Sort the occupancies of nonempty containers in nonincreasing order. A distribution is exactly a partition into at most $m$ positive parts; empty containers fill the remaining slots without adding choices.

## From a part-count bound to a part-size bound

Draw a left-aligned row of cells for each part. Transpose the diagram across its main diagonal. The original row count becomes the length of the first transposed row. Transposition is reversible, giving a bijection between partitions with at most $m$ parts and partitions whose parts are all at most $m$ .

![Transposing a partition exchanges its row-count and row-length bounds](assets/partitions.svg)

The partition $4+1$ has two rows. Its transpose is $2+1+1+1$ , with every row at most two cells long. Both diagrams contain five cells.

## Unbounded-knapsack counting

Let $D_s$ count partitions of sum $s$ using the part sizes processed so far. Initially $D_0=1$ and all other entries are zero. For each size $j=1,\ldots,\min(n,m)$ , process $s=j,j+1,\ldots,n$ in increasing order and set

$$D_s\leftarrow D_s+D_{s-j}\pmod{10^9+7}$$

Increasing order permits repeated use of size $j$ . Processing part sizes in a fixed order avoids counting rearrangements separately. Output $D_1,\ldots,D_n$ .

## Correctness

When processing size $j$ , a partition either uses no $j$ , counted by the old $D_s$ , or uses at least one. Removing one $j$ from the latter gives a partition of $s-j$ using sizes at most $j$ . Increasing order ensures that $D_{s-j}$ already includes every allowed repetition of $j$ . The cases are disjoint and exhaustive, preserving the invariant.

After all sizes, the array counts partitions with maximum part at most $m$ . Conjugation maps these bijectively to distributions using at most $m$ nonempty containers, proving every output correct.

## Complexity and choice

Time is $O(n\min(n,m))$ and space is $O(n)$ . For $m>n$ , larger parts are unusable and the loop stops at $n$ . Entries are always reduced modulo $10^9+7$ ; adding two stays below $2\times(10^9+7)$ and fits a signed 32-bit integer.

The pentagonal method also uses linear space and is faster when $m$ is close to or above $n$ . For small $m$ , unbounded knapsack needs only a few part-size passes, so it remains the reference alongside the alternative's stated use case.
