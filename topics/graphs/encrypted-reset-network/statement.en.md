# Encrypted Packets and Network Resets

Indicative time limit: 1.5 seconds. Memory limit: 512 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

A relay station adds a link whenever it receives an encrypted packet. If a route becomes short enough, it clears all links and starts another round. Reproduce the effect of every packet.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Maintain a weighted directed multigraph with $n$ vertices. Parallel edges are allowed; self-loops are forbidden. A **logical edge** is a tuple $(u,v,x,y)$ . If $y=0$ , it provides an arc from $u$ to $v$ of weight $x$ . If $y=1$ , it permits travel in both directions with weight $x$ in either direction. A bidirectional logical edge still counts as one edge.

First add $m$ unencrypted initial logical edges. This does not trigger a reset, even if the shortest distance from vertex 1 to vertex $n$ is already at most the threshold $T$ .

Then process $k$ encrypted packets in order. Decrypt each of the four fields of packet $c$ by

$$a=a'\mathbin{\mathrm{XOR}}\left(((b+3)(c+37))\bmod998244353\right)$$

Here $a'$ is the input field, $a$ is its decoded value, $c$ is numbered from one, and $b$ is the total number of logical edges deleted by all previous resets, initially zero. Use the same key for all four fields to obtain $(u,v,x,y)$ , then add that edge.

If the shortest distance from vertex 1 to vertex $n$ is now at most $T$ , delete every current logical edge, including the new one, increase $b$ by that count, and output 1. Otherwise retain the graph and output 0. An unreachable destination has infinite distance. Initial edges count toward $b$ when a reset deletes them.

![All links are removed when the threshold is reached](assets/example.svg)

The first packet in Sample 1 adds a weight-2 link and completes a route of length $3+2=5$ . Since the threshold is 5, the network resets.

## Input Format

The first line contains `n m k T` . The next $m$ lines contain unencrypted `u v x y` . The following $k$ lines contain four encrypted fields per packet, in packet order.

## Output Format

Print one line of $k$ space-separated zeros or ones, indicating whether each packet triggers a reset.

## Sample 1

### Input

```text
4 1 5 5
1 2 3 0
112 118 112 114
194 199 197 194
201 203 200 200
206 201 200 205
337 340 336 337
```

### Output

```text
1 0 0 1 1
```


## Sample 2

### Input

```text
2 1 2 0
1 2 0 0
112 115 10082 114
194 193 195 194
```

### Output

```text
1 1
```

## Constraints and Scoring

$2\le n\le10^5$ , $1\le m\le10^5$ , $1\le k\le50000$ , and $0\le T\le100$ . Initial and decoded edges satisfy $1\le u,v\le n$ , $u\ne v$ , $0\le x\le10000$ , and $y\in\{0,1\}$ . Encrypted fields belong to $[0,2^{30}-1]$ , and their decoded values are guaranteed legal.

Completed by Codex (GPT-6) and recorded as a redesign: the first line includes $T$ , with $0\le T\le100$ , and logical-edge counting explicitly covers bidirectional and initial edges.

| Score | Additional constraints |
| --- | --- |
| 100% | None |

There are ten formal files worth 10% each.

See the [test recipes](tests/README.md).
