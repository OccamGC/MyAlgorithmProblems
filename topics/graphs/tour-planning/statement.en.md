# Tour Planning

- Indicative time limit: **6.0 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Deployment time limit: measure the reference program in the target environment, multiply the slowest case's median time by 2, and round up to the next 0.5 seconds.
- Memory limit: **128 MB**.

## Story

A block-built town is organizing trips between its villages. Residents are interested only in nearby villages, and each village has limited visitor capacity. Excessive spending also slows down the server, so the organizers first want as many people as possible to travel, then want to minimize their total spending.

Some tourist roads support time travel and may have negative recorded lengths. Check for negative cycles before arranging the trips.

## Formal Problem Statement

There are $n$ villages and $m$ directed roads. A road $u\to v$ has length $w$ . If a directed cycle of negative total length exists anywhere in the road graph, report it immediately.

Otherwise, let $d(i,j)$ be the shortest-path distance from village $i$ to village $j$ . Its candidate destinations are all reachable villages other than $i$ . Sort them in ascending lexicographic order of

$$\bigl(d(i,j),\lvert i-j\rvert\bigr)$$

Thus distance is compared first, then the absolute difference between village IDs. Residents of village $i$ are interested in the first $k_i$ candidates. Include all candidates tied on both quantities at the cutoff. If fewer than $k_i$ candidates exist, include all of them; if $k_i=0$ , include none.

Village $i$ has $V_i$ residents who would like to travel, each making $C_i$ purchases on a trip. Village $j$ can host at most $H_j$ visitors and charges $P_j$ per purchase. Sending one resident from $i$ to $j$ therefore costs $C_iP_j$ .

Each resident may visit at most one destination they are interested in. Residents who stay home use no visitor capacity and incur no cost. Roads determine destination rankings only; they impose no flow capacities or additional charges.

Maximize the number of travelers, and among such arrangements minimize total cost.

## Input Format

The first line contains $n,m$ .

Each of the next $m$ lines contains $u,v,w$ , describing a directed road from $u$ to $v$ .

Each of the next $n$ lines contains $k_i,V_i,C_i,H_i,P_i$ for village $i$ .

## Output Format

If the road graph contains a negative cycle, print `Negative loop found.` on one line, including the final period. Otherwise print the minimum total cost among arrangements with the maximum number of travelers. Print $0$ if nobody can travel.

## Sample 1

### Input

```text
4 6
1 2 1
1 3 2
1 4 3
2 3 -1
2 4 3
3 4 7
3 3 2 0 0
2 2 3 2 5
1 4 1 2 3
0 0 0 1 10
```

### Output

```text
45
```

## Sample 2

### Input

```text
2 2
1 2 1
2 1 -2
3 3 2 0 0
2 2 3 2 5
```

### Output

```text
Negative loop found.
```

## Sample 3

### Input

```text
3 2
2 1 1
2 3 1
0 0 0 1 7
1 2 1 0 0
0 0 0 1 11
```

### Output

```text
18
```

## Sample Explanation

In sample 1, total visitor capacity is $5$ . Send two residents from village $1$ to $2$ , one from $1$ to $3$ , one from $2$ to $3$ , and one from $3$ to $4$ . This sends $5$ travelers at total cost $20+6+9+10=45$ .

In sample 2, cycle $1\to2\to1$ has total length $-1$ .

In sample 3, villages $1$ and $3$ have identical ranking keys for village $2$ . Both are included even though $k_2=1$ . One traveler visits each destination, for total cost $7+11=18$ .

## Constraints and Guarantees

For all test cases: $1\le n\le1000$ , $1\le m\le5000$ . Each road satisfies $1\le u,v\le n$ , $u\ne v$ , and $-10^9\le w\le10^9$ . Parallel directed roads are allowed.

For each village: $0\le k_i\le10$ , $0\le V_i,H_i\le10^9$ , and $0\le C_i,P_i\le30$ . All input values are integers.

| Score | Additional restrictions |
| --- | --- |
| 100% | None |
