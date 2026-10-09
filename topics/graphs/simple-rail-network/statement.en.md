# Factorio: Simple Rail Network

Estimated time limit: 1.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

You have built production and mining clusters in Factorio. Choose bidirectional rail routes that connect every cluster with the smallest total construction cost.

## Formal Problem Statement

There are $n$ vertices numbered from $1$ to $n$ and $m$ candidate undirected edges. Edge $i$ joins $a_i,b_i$ and has integer cost $w_i$ . Each edge may be selected zero or one time.

The selected edges must connect all vertices. Minimize their total cost. Costs may be negative or zero. Self-loops and distinct parallel edges are allowed. The selected subgraph may contain cycles.

Report impossibility if no connected choice exists. A single vertex is connected even without selected edges, but the total cost must still be minimized.

## Input Format

The first line contains $n,m$ . Each of the next $m$ lines contains $a_i,b_i,w_i$ , describing one candidate edge.

## Output Format

If all vertices cannot be connected, print `bad idea` on one line. Otherwise, print the minimum total cost as one integer.

## Examples

### Example 1

### Input

```text
4 7
1 2 -5
2 3 -4
1 3 -3
1 1 -2
3 4 7
2 4 9
4 4 0
```

### Output

```text
-7
```

### Example 2

### Input

```text
1 2
1 1 -9
1 1 6
```

### Output

```text
-9
```

### Example 3

### Input

```text
3 1
1 2 0
```

### Output

```text
bad idea
```

## Example Explanation

In the first example, select all four negative-cost edges, totaling $-14$ , including a cycle and a self-loop. Add the edge of cost $7$ to connect vertex $4$ , giving $-7$ .

![Negative-cost edges and the positive edge connecting the last vertex](assets/network.svg)

Solid edges are selected in the illustrated solution; dashed edges are omitted. Including or omitting the zero-cost loop does not change the optimum.

The second example has one vertex; choosing its loop of cost $-9$ lowers the total. In the third example, vertex $3$ cannot be connected to the others.

## Constraints and Guarantees

$1\le n\le10^6$ , $0\le m\le2\times10^6$ , $1\le a_i,b_i\le n$ , and $|w_i|\le10^9$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
