# Routes with Limited Energy

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A survey robot follows mountain roads. Moving downhill costs no energy, while level and uphill moves do. Count the routes it can take with a given initial energy budget.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n$ vertices labelled $1,\ldots,n$ , with integer heights $h_1,\ldots,h_n$ . Each of $m$ undirected roads joins $u_i,v_i$ . Every move must use exactly one road.

The cost of moving from $u$ to $v$ is

$$c(u,v)=\begin{cases}0,&h_v<h_u,\\1,&h_v=h_u,\\2,&h_v>h_u.\end{cases}$$

Start at any vertex with energy $E$ . The total cost must not exceed $E$ . You may stop at any time, including before making a move. Vertices and roads may be revisited.

A route is the vertex sequence consisting of its start and its position after each move. Only different vertex sequences count as different routes. Parallel roads do not create additional copies of the same sequence. Traversing a self-loop appends the current vertex again and costs one energy unit.

Count the routes modulo $998244353$ , returning the least nonnegative residue. There are no routes when $n=0$ .

## Input Format

The first line contains $n,m,E$ . The second contains $h_1,\ldots,h_n$ . Each of the next $m$ lines contains $u_i,v_i$ . If $n=0$ , the height line is empty and $m=0$ .

## Output Format

Print the route count modulo the specified modulus.

## Samples

### Sample 1

### Input

```text
2 1 2
0 1
1 2
```

### Output

```text
7
```

### Sample 2

### Input

```text
2 3 1
0 0
1 2
1 2
1 1
```

### Output

```text
5
```

### Sample 3

### Input

```text
0 0 30
```

### Output

```text
0
```

## Sample Explanation

The first sample has $(1)$ , $(1,2)$ and $(1,2,1)$ starting at vertex one, and $(2)$ , $(2,1)$ , $(2,1,2)$ and $(2,1,2,1)$ starting at vertex two. The second has the five sequences $(1)$ , $(2)$ , $(1,2)$ , $(2,1)$ and $(1,1)$ ; its parallel roads add no new vertex sequences. The third has no routes.

![Seven routes with energy at most two](assets/example.en.svg)

## Constraints and Guarantees

$0\le n,m\le10^5$ , $-10^5\le h_i\le10^5$ , $0\le E\le30$ , $1\le u_i,v_i\le n$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
