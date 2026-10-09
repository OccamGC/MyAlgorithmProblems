# Forward Jumps with Batched Operations

Indicative time limit: 0.5 seconds. Memory limit: 128 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

A farm has a row of spring pads. A sheep landing on a pad jumps forward until it leaves the row. The keeper adjusts springs in batches and asks how many jumps a sheep will make.

## Formal Problem Statement

There is one pad at each integer position $0,1,\ldots,n$ , with initially positive jump lengths $K_0,\ldots,K_n$ . From a position $i\le n$ , a sheep makes one jump to $i+K_i$ . It stops after reaching a position greater than $n$ . A starting position already greater than $n$ requires zero jumps.

Process $q$ operations in order:

- `1 A B` : change the jump length of pad $A$ to $B$ .
- `2 C` : ask how many jumps are needed to stop when starting at $C$ . A query does not change any jump length.

The output mode is $t$ . For $t=2$ , print every query result immediately. For $t=1$ , print three integers after all operations: the XOR of query results at odd-numbered operations, the XOR at even-numbered operations, and the ordinary sum of all query results. **Operation numbering includes updates** and starts at one. The XOR and sum of an empty set are both zero.

![Three jumps after a spring update](assets/example.svg)

After Sample 1 changes $K_2$ to 3, a sheep starting at zero follows $0\to1\to2\to5$ and leaves in three jumps.

## Input Format

The first line contains `n q t` . The second contains $n+1$ integers $K_0,\ldots,K_n$ . Each of the next $q$ lines is an operation.

## Output Format

Follow the selected output mode. For $t=1$ , print three integers on one line. For $t=2$ , print one integer per query; no queries means empty output.

## Sample 1

### Input

```text
4 6 2
1 1 1 1 1
2 0
1 2 3
2 0
2 4
2 9
1 0 1000000000
```

### Output

```text
5
3
1
0
```


## Sample 2

### Input

```text
4 6 1
1 1 1 1 1
2 0
1 2 3
2 0
2 4
2 9
1 0 1000000000
```

### Output

```text
6 1 9
```


## Sample 3

### Input

```text
1 0 1
1 1
```

### Output

```text
0 0 0
```

## Constraints and Scoring

$1\le n\le300000$ , $0\le q\le6000000$ , $t\in\{1,2\}$ , $1\le K_i,B\le10^9$ , $0\le A\le n$ , and $0\le C\le10^9$ .

Completed by Codex (GPT-6) and recorded as a redesign: initial jump lengths are positive, batch conditions are precise, and the memory limit is 128 MiB.

An update interval is a contiguous range containing only updates; a query interval is defined similarly. The intervals in the table may be chosen freely and need not be maximal. In group 4, the segments partition all operations in order without gaps or overlap.

| Score | Additional constraints |
| --- | --- |
| 25% | $t=1$ ; the sum of update positions is $\sum A\le50000000$ |
| 25% | $t=1$ ; at most 100000 updates; at most 100 update intervals cover all but at most 10 updates |
| 25% | $t=2$ ; at most 100000 queries; at most 100 query intervals cover all but at most 10 queries |
| 25% | $t=2$ , $q\le1000000$ ; at most 100 consecutive segments partition all operations, with the maximum and minimum positions $A,C$ in each segment differing by at most 500 |

Group 4 recipes randomly choose operation types and positions within each segment's allowed range. There are eight formal files worth 12.5% each, two per group.

See the [test recipes](tests/README.md).
