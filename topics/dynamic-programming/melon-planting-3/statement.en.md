# Melon Planting 3

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); estimate only)
- Actual time limit: twice the reference program's benchmark time on the slowest official input in the target judging environment, rounded up to a multiple of 0.5 seconds. Round up again if the platform only supports a coarser interval.
- Memory limit: 128 MB

## Story

The farmer has planted a long, narrow field beside the village path. Vines compete for nearby empty cells, and neither their growing order nor their direction can be controlled. What is the smallest harvest possible once no new melon can grow anywhere in the field?

(This story was rewritten by GPT-6.)

## Formal Problem Statement

The field is an $n$-row, $m$-column grid. Initially, each cell is a vine `l` , empty land `o` , or an obstacle `x` ; cells outside the grid are obstacles. The field is narrow: $\min(n,m)\le8$ . There is no additional bound on the number of vines.

Each vine can grow at most one melon. A growth step chooses any vine that has not grown a melon and has an empty cell immediately above, below, left, or right. A melon grows in one such empty cell, which remains occupied and cannot receive another melon. The vine's own cell remains a vine and cannot receive a melon.

Growth continues until no vine can grow another melon. Find the minimum number of melons over all possible terminal states. Growth must reach this stopping condition; it cannot stop while another step is possible.

## Input Format

The first line contains two integers $n,m$ . The next $n$ lines each contain a string of length $m$ describing the field.

## Output Format

Print one integer: the smallest possible number of melons in a terminal state.

## Sample 1

### Input

```text
2 5
xlolx
xolox
```

### Output

```text
2
```

## Sample 2

### Input

```text
1 6
lololo
```

### Output

```text
2
```

## Sample 3

### Input

```text
1 3
lxl
```

### Output

```text
0
```

## Sample 4

### Input

```text
4 1
l
o
l
o
```

### Output

```text
1
```

## Sample Explanation

In the first sample, the upper-left vine can grow into the upper-middle empty cell, and the lower vine can grow into the cell to its right. The remaining vine has no empty neighbor, giving a terminal harvest of two melons. One melon cannot stop every vine.

![The terminal state with two melons in the first sample](assets/terminal-field.svg)

Arrows point from vines to their melons. A circled `M` represents a melon; the other letters have the same meanings as the input characters.

In the second sample, the vine in cell $1$ can grow into cell $2$ , and the vine in cell $5$ into cell $4$ . The vine in cell $3$ then cannot grow, giving the answer $2$ . The third sample has no empty cells, so its answer is zero. In the fourth sample, the vine in cell $3$ can grow into cell $2$ , stopping growth with just $1$ melon.

## Constraints and Guarantees

The constraints were strengthened and redesigned by Codex (GPT-6): the area limit for the minimum-harvest problem was raised from $100$ to $5000$ , the additional limit of $18$ vines was removed, and the shorter dimension is restricted to at most $8$ .

All inputs satisfy $n,m\ge1$ , $nm\le5000$ , and $\min(n,m)\le8$ . Every grid character is `l` , `o` , or `x` . The grid may contain no vines or no empty cells, and may have disconnected regions.

| Score share | Additional conditions |
| --- | --- |
| 20% | $\min(n,m)=1$ |
| 30% | $\min(n,m)\le4$ |
| 50% | No additional conditions |
