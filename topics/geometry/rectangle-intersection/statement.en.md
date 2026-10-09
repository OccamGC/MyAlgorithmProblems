# Interstellar Orders: Rectangle Intersection

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

After completing its motion-calculation orders, the interstellar computing center is asked to prepare geometry exercises. Some rectangles are flattened into segments or even points. The center must determine whether the resulting shapes have anything in common.

## Formal Problem Statement

Given two closed rectangles $A,B$ in the Cartesian plane, determine whether $A\cap B$ is nonempty. Their sides are parallel to the coordinate axes. Each rectangle is specified by two opposite corners in either order.

A rectangle includes its interior and boundary. Equal coordinates along one axis may make it a segment; equal coordinates along both axes make it a point. A single shared point counts as an intersection.

![Examples with rectangles, contained segments, crossing segments and separated shapes](assets/intersections.svg)

Solid outlines represent $A$ and dashed outlines represent $B$ . The first three pairs intersect; the fourth does not. In the second pair, the segment lies inside the rectangle.

## Input

The first line contains $T$ . Each of the next $T$ lines contains eight integers:

```text
x1 y1 x2 y2 x3 y3 x4 y4
```

The first four numbers specify the opposite corners of $A$ , and the last four those of $B$ .

## Output

For each pair, output `Intersection Found` if the shapes intersect, or `Intersection Not Found` otherwise. Match the capitalization and spaces exactly. For $T=0$ , the output is empty.

## Samples

### Sample 1

### Input

```text
13
0 0 1 1 2 2 3 3
-1 2 2 -1 0 0 1 1
0 0 0 0 0 0 0 0
0 1 0 5 0 2 0 3
0 0 5 5 2 -5 3 0
0 0 5 0 2 -1 2 2
0 0 2 2 -1 -1 1 1
0 0 0 0 5 0 -1 0
-1 -1 -5 -5 -5 0 -5 -2
-1 -1 -5 -5 -2 -1 -2 -2
-2 1 2 -1 1 2 -1 -2
0 0 2 2 0 1 -1 1
0 0 0 0 1 1 1 1
```

### Output

```text
Intersection Not Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Found
Intersection Not Found
```

### Sample 2

### Input

```text
4
0 0 4 4 2 1 2 3
0 2 4 2 2 0 2 4
1 1 1 1 2 2 2 2
-1000000000 -1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000
```

### Output

```text
Intersection Found
Intersection Found
Intersection Not Found
Intersection Found
```

### Sample 3

### Input

```text
0
```

### Output

```text

```

## Sample Explanation

Sample 1 covers disjoint shapes, containment, coincident points, overlapping segments and boundary contact. In sample 2, the first pair is a rectangle containing a segment and the second pair consists of two segments meeting at a point; both intersect. The fourth pair shares a point at the coordinate limit.

## Constraints and Guarantees

For 100% of the data: $0\le T\le1000$ and $|x_i|,|y_i|\le10^9$ for $1\le i\le4$ . Degenerate rectangles and either order of opposite corners are allowed.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
