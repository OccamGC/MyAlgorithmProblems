# Nomadism — Night

- Indicative time limit: 1.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); estimate only)
- Actual time limit: twice the reference program's benchmark time on the slowest official input in the target judging environment, rounded up to a multiple of 0.5 seconds. If the platform only supports a coarser resolution, round up again to a supported value.
- Memory limit: 256 MB

## Story

A wandering farmer does not yet own any fields. Each day, the farmer starts at a farm near home, visits the other farms to help with cultivation, and finally returns to the starting farm. At night, travel is restricted to the four cardinal directions to avoid getting lost. The farms are spread across a large map, so the farmer needs a tour with a reasonably small total cost.

## Formal Problem Statement

There are $n$ farms in the plane, numbered from $1$ to $n$ . Farm $i$ has coordinates $(x_i,y_i)$ . Farms with different numbers may occupy the same coordinates.

The cost of travel from farm $i$ to farm $j$ is:

$$d(i,j)=|x_i-x_j|+|y_i-y_j|$$

Choose some undirected connections between farms so that all farms are connected. Every endpoint must be one of the given farms, and each connection costs the distance defined above. Crossings do not create additional connection points. Let $M$ be the minimum possible total cost of these connections. For $n=1$ , define $M=0$ .

Construct a tour that starts at farm $1$ , visits every other farm exactly once, and returns to farm $1$ . If its total cost is $C$ , it is accepted precisely when:

$$C\le 2.001M+0.001$$

Visits are determined by the output sequence of farm numbers. Passing through another farm's coordinates during a leg does not count as an additional visit. You need not output $C$ or $M$ , or find a shortest tour.

## Input

The first line contains an integer $n$ .

Each of the next $n$ lines contains two integers $x_i,y_i$ , the coordinates of farm $i$ .

## Output

Print $n+1$ integers $p_0,p_1,\ldots,p_n$ on one line.

- $p_0=p_n=1$ must hold.
- $p_0,p_1,\ldots,p_{n-1}$ must be a permutation of $1,2,\ldots,n$ .
- $C=\sum_{i=0}^{n-1}d(p_i,p_{i+1})$ must satisfy the bound above.
- For $n=1$ , print `1 1` .

A special checker is used. Any tour satisfying these requirements is accepted; it need not match the sample output.

## Sample 1

### Input

```text
3
5 3
1 7
7 7
```

### Output

```text
1 3 2 1
```

### Explanation

The minimum connection cost is $M=12$ . The sample tour costs $C=20$ and satisfies $C\le2.001M+0.001$ .

## Sample 2

### Input

```text
5
7 3
1 0
-5 3
7 9
9 10
```

### Output

```text
1 4 5 2 3 1
```

### Explanation

The minimum connection cost is $M=27$ . The sample tour costs $C=48$ and satisfies $C\le2.001M+0.001$ .

## Sample 3

### Input

```text
10
15 616
15 7
1 6794
13 245
1233 44
15 6
97 94
123 321
3020 100
456 987
```

### Output

```text
1 4 8 7 2 6 5 9 10 3 1
```

### Explanation

The minimum connection cost is $M=10997$ . The sample tour costs $C=19986$ and satisfies $C\le2.001M+0.001$ .

## Sample 4

### Input

```text
1
0 0
```

### Output

```text
1 1
```

### Explanation

There is only one farm. The tour starts and ends there, with $M=C=0$ .

## Sample 5

### Input

```text
4
0 0
0 0
3 4
3 4
```

### Output

```text
1 2 3 4 1
```

### Explanation

Farms $1,2$ share one position and farms $3,4$ share another, but each farm number must still be visited. The distance between the positions is $7$ , so $M=7$ and the sample tour costs $C=14$ .

## Constraints and Guarantees

- $1\le n\le400000$ .
- $-10000\le x_i,y_i\le10000$ , and all coordinates are integers.
- Coincident farms, entirely collinear inputs, and cocircular points are allowed.

### Test Groups

| Score | Additional constraints |
| --- | --- |
| 100% | None |
