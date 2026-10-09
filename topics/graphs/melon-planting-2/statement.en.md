# Melon Planting 2

- Indicative time limit: 1.0 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); estimate only)
- Actual time limit: twice the reference program's benchmark time on the slowest official input in the target judging environment, rounded up to a multiple of 0.5 seconds. Round up again if the platform only supports a coarser interval.
- Memory limit: 128 MB

## Story

The farmer has built guide frames that let each vine grow toward a few chosen plots. The frames are ready, but the order in which vines grow is still beyond anyone's control. What is the smallest harvest possible when no vine can grow another melon?

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $p$ vines and $q$ initially empty plots, numbered from $1$ to $p$ and from $1$ to $q$ , respectively. Vine $i$ can grow a melon in any plot in its specified set $A_i$ , where $|A_i|\le4$ . These connections have no geometric restrictions, and guide frames do not interfere with each other.

Each vine can grow at most one melon, and each plot can hold at most one melon. A growth step selects a vine $i$ that has not grown a melon and an empty plot in $A_i$ , then places a melon in that plot. The vine cannot grow again, and the plot remains occupied. Vines and plots are two separate kinds of objects.

Growth continues until no legal step remains. Find the minimum number of melons over all possible terminal states. Growth must reach this stopping condition; it cannot stop while another step is possible.

## Input Format

The first line contains two integers $p,q$ .

The next $p$ lines describe the connections. Line $i$ starts with an integer $d_i$ , followed by $d_i$ distinct plot IDs that form $A_i$ . If $d_i=0$ , the line contains only $0$ . If $p=0$ , there are no further lines.

## Output Format

Print one integer: the smallest possible number of melons in a terminal state.

## Sample 1

### Input

```text
2 2
2 1 2
1 2
```

### Output

```text
1
```

## Sample 2

### Input

```text
4 4
1 1
1 2
1 3
1 4
```

### Output

```text
4
```

## Sample 3

### Input

```text
0 3
```

### Output

```text
0
```

## Sample Explanation

In the first sample, vine $1$ can grow in plot $2$ . The only plot available to vine $2$ is now occupied, so growth stops with one melon. If vine $1$ grows in plot $1$ first, a second melon must still grow. The order and choices can therefore change the final harvest.

![Specified plots for two vines and a terminal state with only one melon](assets/guide-frames.svg)

`L1` and `L2` are vines; `R1` and `R2` are plots. Dashed lines indicate allowed connections. The solid arrow indicates the actual growth step, and the circled `M` marks its melon.

In the second sample, each vine has its own exclusive plot, so all four must grow before the process stops. The third sample has no vines, so the answer is zero.

## Constraints and Guarantees

The constraints were strengthened and redesigned by Codex (GPT-6): the vine limit was raised from $18$ to $24$ , with general connections allowing each vine to designate at most four plots.

All inputs satisfy $0\le p\le24$ , $1\le q\le96$ , and $0\le d_i\le\min(4,q)$ . Plot IDs in each list are distinct and belong to $[1,q]$ . A vine may have no designated plot, and a plot may belong to no designated set.

| Score share | Additional conditions |
| --- | --- |
| 20% | $p\le10$ |
| 30% | $p\le18$ |
| 50% | No additional conditions |
