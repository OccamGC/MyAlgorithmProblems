# Gnome Sort

- Indicative time limit: 0.5 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

A gnome walks along a row of cells, each containing a two-dimensional vector. When neighboring vectors are out of order, he swaps them and takes one step left. You want to count how many times he executes the comparison step.

## Formal Problem Statement

Given $n$ pairwise distinct two-dimensional vectors $v_i=(x_i,y_i)$ arranged from left to right, compare them lexicographically: compare the first coordinate, then the second coordinate if the first coordinates are equal.

The gnome starts at cell $1$ . He follows these steps until the task ends:

```text
(0) If the current position is 1, move one cell right. Then execute (1).
(1) Check whether the current vector is smaller than its left neighbor.
    If so, swap the two vectors, move one cell left, and return to (0).
    Otherwise execute (2).
(2) If the current position is n, stop. Otherwise execute (3).
(3) Move one cell right and return to (1).
```

Count all executions of step `(1)` , whether its condition holds or not.

## Input Format

The first line contains $n$ . Each of the next $n$ lines contains $x_i,y_i$ .

## Output Format

Output one integer: the number of executions of step `(1)` .

## Samples

### Sample 1

### Input

```text
3
0 0
0 1
1 -1
```

### Output

```text
2
```

### Sample 2

### Input

```text
4
4 0
3 0
2 0
1 0
```

### Output

```text
12
```

### Sample 3

### Input

```text
5
0 2
-1 8
0 -5
2 -8
-1 7
```

### Output

```text
14
```

## Sample Explanation

Sample 1 is already sorted, requiring two checks. In sample 2, inserting each next vector takes the gnome back to the first cell; there are $12$ checks in total.

## Constraints and Guarantees

For **100% of the data**:

$2\le n\le5\times10^5$ ; $|x_i|,|y_i|\le10^9$ . Vectors are pairwise distinct, but individual coordinates may be equal.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
