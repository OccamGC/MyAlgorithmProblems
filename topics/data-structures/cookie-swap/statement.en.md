# The Great Cookie Swap

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 1024 MB

## Story

Every guest at a tea party brings cookies and reports how many they can eat. The host announces, “This is a swap. Please don't just sit down and eat your own box.”

Each cookie must pass directly from its owner to another guest. It cannot be passed on again or take a round trip back to its owner. Guests occasionally revise their quantities or appetites. The host also selects a consecutive group of seats and asks how many cookies that group could distribute internally.

These are planning exercises. After each estimate, not a single cookie has disappeared.

(This story was rewritten by GPT-6 Astra.)

## Formal Problem Statement

There are $n$ participants numbered from $1$ to $n$ . Participant $i$ has receiving capacity $d_i$ (demand) and providing capacity $s_i$ (supply), both measured in items. Each item passes directly from its provider to its recipient; these must be different participants. Both quantities are upper bounds and need not be fully used.

Process $m$ operations in order. Each is one of the following three types:

1. `1 x d` : set $d_x=d$ .
2. `2 x s` : set $s_x=s$ .
3. `3 l r` : allow only participants in $[l,r]$ to exchange items, and find the maximum total delivered.

Formally, for every pair of distinct participants $i,j$ in the queried range, choose a nonnegative integer $f_{ij}$ representing the number of items delivered from $i$ to $j$ . Require $\sum_{j\ne i}f_{ij}\le s_i$ for each provider and $\sum_{i\ne j}f_{ij}\le d_j$ for each recipient, and maximize $\sum_{i\ne j}f_{ij}$ . All indices and sums here are restricted to $[l,r]$ .

A participant may both provide and receive, and two different participants may provide items to each other. Queries do not consume any quantities; only the first two operations change the state.

## Input Format

The first line contains $n,m$ .

The second line contains $2n$ integers $d_1,s_1,d_2,s_2,\ldots,d_n,s_n$ .

Each of the next $m$ lines contains three integers describing an operation.

## Output Format

For each type-3 operation, print one integer on its own line. If there are no type-3 operations, produce no output.

## Sample 1

### Input

```text
3 5
1 1 2 2 2 3
3 1 3
3 1 2
1 1 2
3 1 3
3 1 2
```

### Output

```text
5
2
6
3
```

### Explanation

The first query can deliver $5$ cookies: participant $1$ gives one to $2$ , participant $2$ gives two to $3$ , and participant $3$ gives one each to $1$ and $2$ .

After the update, participant $1$ may receive up to $2$ cookies, and the maximum totals for the two ranges become $6$ and $3$ .

## Sample 2

### Input

```text
2 4
100 100 1 1
3 1 2
3 1 1
1 2 100
3 1 2
```

### Output

```text
2
0
101
```

### Explanation

Initially, each participant can give one cookie to the other, for a total of $2$ . A singleton cannot deliver items to itself, so its answer is $0$ .

After the update, participant $1$ can give $100$ cookies to $2$ , while participant $2$ can still give one to $1$ . The last query therefore has answer $101$ .

## Constraints and Guarantees

- $1\le n,m\le300\,000$ .
- $0\le d_i,s_i,d,s\le1\,000\,000\,000$ , all integers.
- Updates satisfy $1\le x\le n$ .
- Queries satisfy $1\le l\le r\le n$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 10% | $n,m\le10$ ; all quantities are at most $50$ |
| 10% | $n,m\le100$ |
| 20% | $n,m\le300$ |
| 20% | $n,m\le3\,000$ |
| 20% | $n,m\le50\,000$ |
| 20% | No additional conditions |
