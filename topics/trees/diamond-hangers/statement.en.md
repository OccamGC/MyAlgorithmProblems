# Arranging Diamond Hangers

- Reference time limit: 0.5 seconds (environment R30; estimate only).
- Actual time limit: twice the standard program’s baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB

## Story

Diamond-shaped hangers can be attached below or to the right of other hangers, forming one connected arrangement. List their identifiers from top to bottom, and from left to right within each row.

## Formal Problem Statement

Hangers are numbered $1,\ldots,n$ . Hanger $i$ has a lower child $d_i$ and a right child $r_i$ ; zero means no child. All nonzero connections form one rooted tree, with at most one child of each kind. The root is uniquely determined by the input.

The root has level zero. A lower edge increases the level by one without changing the horizontal coordinate of the centre. A right edge preserves the level. Smaller levels are higher.

To define horizontal order precisely, let $B=2n+1$ . Every hanger at level $h$ has horizontal half-diagonal $B^{-h}$ . The root's centre has coordinate zero; a right child's centre is $2B^{-h}$ to the right of its parent's. Vertical diagonals have equal length and a lower attachment descends exactly one level. Thus higher hangers are much wider than lower ones. Coordinates need not be calculated or printed: output the identifiers in each nonempty level from left to right.

## Input Format

The first line contains $n$ . The next $n$ lines contain $d_i,r_i$ in identifier order.

## Output Format

Print one line per nonempty level in increasing level order. List that level’s identifiers in increasing horizontal-coordinate order, separated by spaces. Each identifier occurs exactly once.

## Sample 1

### Input

```text
6
2 3
4 5
6 0
0 0
0 0
0 0
```

### Output

```text
1 3
2 5 6
4
```

### Explanation

The top row is one and three; the next row is two, five and six; the last contains four.

![Width differences between levels are compressed for readability; attachments and identifier order match the rules.](assets/example.svg)

Width differences between levels are compressed for readability; attachments and identifier order match the rules.

## Sample 2

### Input

```text
1
0 0
```

### Output

```text
1
```

### Explanation

There is only one hanger.

## Sample 3

### Input

```text
3
0 0
0 1
0 2
```

### Output

```text
3 2 1
```

### Explanation

Hanger three is the root. All three are connected horizontally in one row.

## Constraints and Guarantees

$1\le n\le10^5$ , $0\le d_i,r_i\le n$ . The connections satisfy the rooted-tree conditions above.

Codex (GPT-6) completed the specification by defining the size limit, valid-tree guarantee, equal widths within a level, width ratio between levels, and output as hanger identifiers.

### Test Groups

| Score | Additional restriction |
| --- | --- |
| 20% | $n\le20$ |
| 30% | $n\le1000$ |
| 50% | No additional restriction |

[Reference environment and measurements](../../../docs/评测环境与性能.md)
