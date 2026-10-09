# Transport with Capacities on a Line

Estimated time limit: 2.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $18$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).
This multiplier gives the documented correct alternative at least twofold measured headroom.

## Story

Workstations along a corridor produce items over time. Local storage is limited, while the warehouse at the end has unlimited space. A dispatcher wants the minimum transport distance for every prefix of items.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n+1$ points on a line, ordered from left to right and numbered $1,\ldots,n+1$ . The distance from point $i$ to point $i+1$ is $d_i$ , possibly zero. Points $1,\ldots,n$ have capacities $r_1,\ldots,r_n$ ; point $n+1$ has unlimited capacity.

There are $m$ items, with item $j$ produced at point $p_j$ . Each item must be stored at some point, possibly its production point. A finite-capacity point may store at most that many items. The transport cost of an item is the distance between its production and storage points.

For each $j=1,\ldots,m$ , find the minimum total cost for the first $j$ items. Prefixes are independent: all earlier items may be reassigned when optimizing a new prefix.

## Input Format

The first line contains $n,m$ . The next three lines contain $r_1,\ldots,r_n$ , then $d_1,\ldots,d_n$ , then $p_1,\ldots,p_m$ .

## Output Format

Print $m$ lines. Line $j$ is the minimum total cost for the first $j$ items.

## Samples

### Sample 1

### Input

```text
9 5
1 1 0 1 0 1 0 1 0
1 1 1 1 1 1 1 1 2
3 5 7 2 9
```

### Output

```text
1
2
3
3
5
```

### Sample 2

### Input

```text
8 4
1 0 1 0 1 0 1 0
2 1 1 1 1 1 1 3
4 6 8 2
```

### Output

```text
1
2
3
5
```

### Sample 3

### Input

```text
2 3
0 1
0 5
1 2 1
```

### Output

```text
0
5
10
```

## Sample Explanation

Sample one gives successive minimum costs $1,2,3,3,5$ . Earlier items may be reassigned for each prefix in sample two. In sample three the first two points coincide, but there is only one finite storage slot; each later item adds a warehouse trip of distance five.

## Constraints and Guarantees

$1\le n,m\le100000$ , $0\le r_i\le100000$ . For $i<n$ , $0\le d_i\le2$ ; the final distance satisfies $0\le d_n\le1000000$ . Each request satisfies $1\le p_j\le n$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
