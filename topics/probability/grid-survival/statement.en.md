# Survival on a Grid

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A roaming robot lands uniformly at random in a grid of roads and pits. It cannot recognize danger and simply steps in a random direction. Find the probability that it remains safe throughout the required number of steps.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

You are given a grid with $n$ rows and $m$ columns, each cell being a road or a pit. The starting cell is chosen uniformly from all $nm$ cells, including pits. The robot then takes $k$ steps. Each step independently chooses up, down, left, or right with equal probability and moves one cell. Staying still is forbidden. A direction leading outside or into a pit is not retried.

A process succeeds exactly when every visited position, including both endpoints, is a road inside the grid. Write its probability as $p/q$ , where $p\ge0,q>0$ , and output

$$p\cdot q^{-1}\bmod P,\qquad P=7\times2^{50}+1=7881299347898369$$

Here $P$ is prime, and $q^{-1}$ is the multiplicative inverse modulo $P$ . You may use $q=nm\cdot4^k$ directly; the constraints ensure that this denominator is coprime to $P$ .

## Input Format

The first line contains $n,m,k$ . The next $n$ lines each contain a string of $m$ characters from `01` , without spaces. Character `0` denotes a pit and `1` a road.

## Output Format

Print the success probability modulo $P$ as one integer between $0$ and $P-1$ .

## Samples

### Sample 1

### Input

```text
1 1 0
1
```

### Output

```text
1
```

### Sample 2

### Input

```text
2 2 1
11
11
```

### Output

```text
3940649673949185
```

### Sample 3

### Input

```text
2 2 1
10
11
```

### Output

```text
5910974510923777
```

### Sample 4

### Input

```text
3 3 1
111
011
111
```

### Output

```text
3940649673949185
```

### Sample 5

### Input

```text
3 3 3
111
011
111
```

### Output

```text
1067259286694571
```

### Sample 6

### Input

```text
1 1 1
1
```

### Output

```text
0
```

## Sample Explanation

The first sample makes no move and its only cell is a road, so the probability is one. In the second, each start has two safe directions, giving one half. In the third, four of the sixteen equally likely start-and-direction choices are safe, giving one quarter. The fourth also has probability one half. The fifth has $114$ safe three-step processes out of $9\cdot4^3=576$ , giving $19/96$ . In the sixth, every move exits the grid, giving zero.

![The three road cells and bidirectional adjacencies in sample three](assets/grid.svg)

Cell numbers match the input characters. Arrows show successful one-step moves only; each of the other directions still has probability one quarter.

## Constraints and Guarantees

For all inputs, $n,m\ge1$ , $1\le nm\le10^6$ , and $0\le k\le25$ . There may be no roads. When $k=0$ , only the starting cell matters.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
