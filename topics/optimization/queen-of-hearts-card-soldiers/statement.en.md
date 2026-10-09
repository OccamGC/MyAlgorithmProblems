# The Queen of Hearts' Card Soldiers

Estimated time limit: 1 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

Luolina, the Queen of Hearts, does not like being called the Queen of the Heart Organ.

She has many card soldiers, belonging to exactly four suits: spades, hearts, diamonds, and clubs. There are no jokers or advertising cards. Each soldier has two integer attributes, attack and defense. Soldier $B$ is no weaker than soldier $A$ if both of $B$'s attributes are at least the corresponding attributes of $A$.

The queen plans to arrange her soldiers on several steps. Her throne occupies the top step, so the soldiers must stand on the second step from the top or below. Naturally, every soldier wants a place on the second step.

A soldier feels threatened by any other soldier who is no weaker. If soldier $A$ finds such a soldier $B$ on the same step, $A$ will use “market competition” to force $B$ out. This is hardly in the interests of the step as a whole. The second step is stable if no soldier will be forced out in this way. The queen wants to select as many soldiers as possible while keeping that step stable.

The four suits remind her of the four quadrants. An intersection of half-planes can form a convex hull, while a union of quarter-planes facing the same direction forms a staircase-shaped outline that includes their corner points. The Chebyshev distance between two points is $\max(|x_i-x_j|,|y_i-y_j|)$. Although that distance has little to do with the problem, she names this staircase structure a “Chebyshev convex hull.”

Puzzled by how to divide the soldiers among the steps, the queen calls upon the great wizard Dilworth.

## Formal Problem Statement

There are $n$ soldiers, each with integer attributes $Attack$ and $Armor$ . Soldier $B$ is no weaker than soldier $A$ when both of $B$'s attributes are at least the corresponding attributes of $A$ .

Choose a subset with no pair of distinct soldiers in which one has both attributes at least those of the other. Find the maximum subset size. Soldiers with identical attributes are still distinct soldiers and cannot both be selected. The empty subset is allowed.

## Input Format

The first line contains $n$ . Each of the next $n$ lines contains $Attack,Armor$ for one soldier, in input order.

## Output Format

Print the maximum size of a stable lineup on one line.

## Samples

### Sample 1

### Input

```text
6
1 1
2 2
3 3
4 2
5 1
6 0
```

### Output

```text
4
```

### Sample 2

### Input

```text
0
```

### Output

```text
0
```

### Sample 3

### Input

```text
5
-1 3
-1 2
0 2
1 1
1 1
```

### Output

```text
3
```

## Sample Explanation

In the first sample, choose soldiers $3,4,5,6$ . Their attacks strictly increase while their armor values strictly decrease, so neither soldier in a pair dominates the other in both attributes. The second sample has no soldiers and gives zero. In the third, choose $(-1,3),(0,2),(1,1)$ for an answer of three.

![The six sample attribute points and a stable group of four](assets/lineup.svg)

The horizontal axis $A$ is attack and the vertical axis $D$ is armor. Outer rings mark one optimal group; labels beside points are input indices.

## Constraints and Guarantees

For all inputs, $0\le n\le10^6$ and $|Attack|,|Armor|\le10^9$ . Attributes may be negative, and soldiers may have identical attributes.

| Score share | Additional conditions |
| --- | --- |
| 30% | $n\le20$ |
| 40% | $n\le2000$ |
| 30% | None |
