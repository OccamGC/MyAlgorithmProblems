# Chaos Drone

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge only supports coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

Rahn is surrounded by enemy units, and Chaos Drones have arrived to help him escape. Each drone can provoke conflict between two units or cause internal confusion in one unit. The evacuation can begin once every enemy unit is occupied by one of these disruptions. Use as few drones as possible.

## Formal Problem Statement

There are $n$ enemy units and $m$ allowed pairs. One action consumes one Chaos Drone and does one of the following:

- Choose an allowed pair and occupy both units by provoking conflict between them.
- Choose any one unit and occupy it by causing internal confusion.

Find the minimum number of actions needed to occupy all $n$ units. Different actions may involve the same unit, although this is not required.

Units have case-sensitive code names, which appear only in the list of allowed pairs. If the input contains only $d<n$ distinct names, the remaining $n-d$ units have no allowed pair and must each be handled individually.

## Input Format

The first line contains two integers $n,m$ . Each of the next $m$ lines contains two whitespace-separated code names forming an allowed pair.

## Output Format

Print one integer: the minimum number of actions.

## Sample 1

### Input

```text
8 9
100 200
200 300
300 400
300 500
300 600
400 500
600 500
500 -700
501 -700
```

### Output

```text
4
```

### Explanation

Choose the four pairs `100–200` , `300–600` , `400–500` , and `501–-700` . Four actions are optimal because each action occupies at most two units.

## Sample 2

### Input

```text
6 6
1 2
2 3
1 3
3 4
4 5
5 6
```

### Output

```text
3
```

### Explanation

Choose pairs $1$–$2$ , $3$–$4$ , and $5$–$6$ to occupy all units in three actions.

## Sample 3

### Input

```text
5 10
1 2
1 3
1 4
1 5
2 3
2 4
2 5
3 4
3 5
4 5
```

### Output

```text
3
```

### Explanation

Choose two disjoint pairs, then cause internal confusion in the remaining unit.

## Sample 4

### Input

```text
3 0
```

### Output

```text
3
```

### Explanation

No pair is available, so handle all three units separately.

## Constraints and Guarantees

- $1\le n\le300$ and $0\le m\le n(n-1)/2$ .
- There are no duplicate pairs or self-loops. At most $n$ distinct code names occur.
- Each name is a nonempty UTF-8 string of at most $80$ bytes, containing only English letters, digits, underscores, hyphens, or Chinese characters, with no whitespace.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 20% | $n\le10$ , $m\le20$ |
| 20% | The relation graph is a tree or forest |
| 20% | Every connected component has exactly one cycle |
| 10% | The relation graph is complete |
| 30% | No additional conditions |
