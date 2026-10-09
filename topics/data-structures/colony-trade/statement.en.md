# Colony Trade

- Indicative time limit: **2.0 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 256 MB

## Story

A colony on Mars has overcome its initial shortage and now produces and sells goods regularly. Its warehouse sells the most expensive items first, using current prices. Production rates and prices may change. Compute the revenue from each sale.

## Formal Problem Statement

There are $n$ goods types, numbered $1$ through $n$ . Type $i$ initially has unit price $c_i$ and production parameter $p_i$ . All inventories initially contain zero items. Process these operations in order:

- `1 t` : produce $p_it$ additional items of every type $i$ .
- `2 k` : sell up to $k$ items in decreasing order of current unit price, breaking equal-price ties by larger type ID. If fewer than $k$ items exist, sell all of them. Output this sale's revenue modulo $10^9+7$ .
- `3 i p` : change type $i$'s production parameter to $p$ , without changing existing inventory.
- `4 i c` : change type $i$'s unit price to $c$ , including the price of its existing inventory.

Unsold items remain in storage. A sale may sell any number of items of one type; $k$ counts individual items.

## Input Format

The first line contains $n,m$ . The second line contains $n$ pairs $c_i,p_i$ in type order. Each of the next $m$ lines describes one operation in the format above.

## Output Format

For each sale, print its revenue modulo $10^9+7$ on a separate line. Print no integers if there are no sales.

## Example 1

### Input

```text
2 8
1 5 3 1
1 1
2 3
4 1 5
1 1
2 1
3 2 2
1 1
2 13
```

### Output

```text
5
5
63
```

## Example 2

### Input

```text
2 5
5 1 5 1
1 1
2 1
4 2 9
2 1
2 1
```

### Output

```text
5
5
0
```

## Example 3

### Input

```text
1 5
0 0
1 1000
2 0
3 1 100000
1 1000
2 1000000000000000000
```

### Output

```text
0
0
```

## Example Explanation

The first sale in example 1 sells one item priced $3$ and two priced $1$ , earning $5$ . The next two sales earn $5$ and $63$ . In example 2, the first equal-price sale consumes type $2$ , so raising type $2$'s price afterward does not affect the remaining item. All sold items in example 3 have price zero.

## Constraints and Guarantees

All inputs satisfy $1\le n,m\le300000$ . Initial and updated prices satisfy $0\le c_i,c\le10^9$ , and production parameters satisfy $0\le p_i,p\le100000$ . Operations satisfy $0\le t\le1000$ , $0\le k\le10^{18}$ , and $1\le i\le n$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
