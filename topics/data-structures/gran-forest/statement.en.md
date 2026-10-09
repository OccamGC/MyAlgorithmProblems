# Gran Forest

- Indicative time limit: **1.0 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual limit: measure the reference solution on the target system, take the largest median time over test files, multiply by 2, and round up to a multiple of 0.5 seconds.
- Memory limit: **128 MB**.

## Story

After the fire in Gran Forest, the elves are restoring its magical wards. The connections between wards form a forest, and each vertex stores an energy value. Restoration may add to or reset the energy along a path, and the elves need to count and sum the vertices that meet an energy threshold.

## Formal Problem Statement

You are given a forest with $n$ vertices numbered $1,\ldots,n$ and $m$ undirected edges. Vertex $i$ initially has weight $c_i$ .

Process $q$ operations in order. The vertices $a,b$ in every operation belong to the same tree. Their path is the unique simple path between them, **including both endpoints**; if $a=b$ , it contains just that vertex.

- `1 a b c` : add $c$ to the current weight of every vertex on the path.
- `2 a b c` : set the current weight of every vertex on the path to $c$ .
- `3 a b d` : output the number of path vertices whose current weight is at least $d$ .
- `4 a b d` : output the sum of the current weights of those vertices.

Increments, weights and thresholds may be negative. If no vertex meets the threshold, both the count and the sum are $0$ .

## Input Format

The first line contains $n,m,q$ . The second line contains $c_1,\ldots,c_n$ .

Each of the next $m$ lines gives the endpoints of an undirected edge. Each of the next $q$ lines contains four integers describing an operation.

## Output Format

For each operation 3 or 4, output one integer on its own line, in query order.

## Sample 1

### Input

```text
3 2 5
5 5 2
2 1
3 2
3 2 3 4
2 2 3 0
4 1 3 4
1 1 3 5
3 1 3 5
```

### Output

```text
1
5
3
```

## Sample 2

### Input

```text
4 2 7
-2 0 3 -4
1 2
2 3
4 1 3 -2
2 1 3 -3
1 2 3 5
3 1 3 2
4 1 3 -10
4 4 4 -4
3 4 4 0
```

### Output

```text
1
2
1
-4
0
```

## Sample Explanation

In sample 1, the first queried path has weights $5,2$ , so only one vertex has weight at least $4$ . After assignment, the path $1\to3$ has weights $5,0,0$ , whose qualifying sum for threshold $4$ is $5$ . The final addition changes them to $10,5,5$ .

Sample 2 includes an isolated vertex. After assignment and addition, vertices $1,2,3$ have weights $-3,2,2$ , so their qualifying sum for threshold $-10$ is $1$ . A sum for the isolated vertex $4$ may be $-4$ .

## Constraints and Guarantees

For all test cases: $1\le n\le500000$ , $0\le m<n$ , $1\le q\le10000$ , and $|c_i|\le10000$ . In operations 1 and 2, $|c|\le10000$ ; in operations 3 and 4, $|d|\le100000000$ . Vertex identifiers lie in $1,\ldots,n$ . The edges form a forest, and both endpoints of each operation are connected.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
