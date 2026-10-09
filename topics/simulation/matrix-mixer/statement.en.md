# Factorio: Matrix Mixer

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A Factorio player is creating a mixer mod. Items sit in a grid, and the machine can swap rows, swap columns, or rotate the grid. To check the mod, record its state after each operation.

## Formal Problem Statement

Initially, the grid has $n$ rows and $m$ columns, with an integer item number in each cell. Rows are numbered top to bottom and columns left to right, starting at $1$ . Process $K$ operations:

- `1 a b` : swap current rows $a$ and $b$ .
- `2 a b` : swap current columns $a$ and $b$ .
- `3` : rotate the entire grid clockwise by $90^\circ$ . Its row and column counts are exchanged, and positions are renumbered accordingly.

If either argument of a swap is outside the currently valid row or column range, the operation is invalid and the grid is unchanged. Swapping a row or column with itself is valid.

After a valid operation, print the whole grid. After an invalid operation, print only an error message.

![The first three operations of the sample](assets/operations.svg)

The panels show the initial state of sample 1, swapping rows $1,2$ , swapping columns $2,3$ , and rotating clockwise.

## Input

The first line contains $n,m,K$ . The next $n$ lines each contain $m$ integers $x_{i,j}$ , describing the initial grid.

Each of the next $K$ lines contains one operation. Operation `3` has no additional arguments; operations `1` and `2` each have two integer arguments.

## Output

Print results in operation order. For each valid operation, print the current grid with adjacent numbers separated by one space. For each invalid operation, print `Invalid arguments!` on one line.

Do not insert blank lines between results, and do not print the initial grid before an operation. Trailing spaces on matrix rows are accepted.

## Samples

### Sample 1

### Input

```text
2 3 6
1 2 3
4 5 6
1 1 2
2 2 3
3
1 1 2
1 1 3
3
```

### Output

```text
4 5 6
1 2 3
4 6 5
1 3 2
1 4
3 6
2 5
3 6
1 4
2 5
2 5
1 4
3 6
3 1 2
6 4 5
```

### Sample 2

### Input

```text
1 2 8
1 2
1 2 1
2 1 2
3
2 1 2
1 1 2
3
1 -1 1
3
```

### Output

```text
Invalid arguments!
2 1
2
1
Invalid arguments!
1
2
2 1
Invalid arguments!
2
1
```

### Sample 3

### Input

```text
1 1 5
0
3
1 1 1
2 1 1
2 30 1
3
```

### Output

```text
0
0
0
Invalid arguments!
0
```

## Sample Explanation

The first three operations of sample 1 are shown above. After rotation, the grid has $3$ rows and $2$ columns; later swaps use these new numbers.

In sample 2, the first operation attempts to swap a nonexistent second row, so it prints only an error. After the first rotation, the grid has only one column, so swapping the second column is also invalid. Invalid operations do not affect later states.

## Constraints and Guarantees

For 100% of the data: $1\le n,m\le20$ , $1\le K\le1000$ , $0\le x_{i,j}\le10^9$ , and $|a|,|b|\le30$ . Operation numbers belong to $\{1,2,3\}$ . Item numbers may repeat. Apart from potentially out-of-range $a,b$ , all input is valid.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
