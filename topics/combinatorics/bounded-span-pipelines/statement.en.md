# Pipelines with Bounded Span

Reference time limit: 1.5 s; memory limit: 1024 MiB. Use twice the slowest formal-file median on the target platform, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

An engineer lays pipes between a row of towers. Each pipe runs from a higher tower to a lower one, and some old pipes may be reversed. How many arrangements preserve the required connections?

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n$ positions on a horizontal baseline, numbered $1,\ldots,n$ . At each position, either build no tower or build a vertical tower of an integer height from $1$ through $K$ . Each tower top is the endpoint of exactly one pipe.

A pipe is the straight segment joining two tower tops at different positions and different heights. It is directed from the higher endpoint to the lower one. Its endpoints $u,v$ must satisfy $|u-v|\le K$ . Pipes may neither cross nor touch each other. A pipe may not touch or pass through any tower except at its own endpoints, but it may pass strictly above another tower.

There are $M$ required pipes, given as $(u_i,v_i,e_i)$ . Their endpoints are occupied and must remain paired with each other. If $e_i=1$ , the direction is fixed as $u_i\to v_i$ ; if $e_i=0$ , either direction is allowed. All tower heights may be chosen again. Additional towers and pipes may be built at unoccupied positions.

An arrangement is identified by its **set of ordered endpoint pairs**. Different height assignments alone do not count as different arrangements. Count the arrangements realizable with legal heights, modulo $998244353$ .

![Nested pipes and forbidden interleaving endpoints](assets/example.svg)

## Input Format

The first line contains `n K M` . Each of the next $M$ lines contains `u_i v_i e_i` .

## Output Format

Print the number of arrangements modulo $998244353$ .


## Example 1

### Input

```text
13 9 2
2 3 1
5 7 0
```

### Output

```text
2662
```

## Example 2

### Input

```text
6 5 2
1 6 0
2 3 1
```

### Output

```text
6
```

## Example 3

### Input

```text
2 2 1
1 2 1
```

### Output

```text
1
```


## Constraints and Guarantees

$2\le n\le10^6$ , $1\le K\le18$ , $1\le M\le\lfloor n/2\rfloor$ , $1\le u_i,v_i\le n$ , $u_i\ne v_i$ , $|u_i-v_i|\le K$ , and $e_i\in\{0,1\}$ .

All required endpoints are distinct, and some legal height assignment realizes the required pipes. Consequently, every valid input has $K\ge2$ : when $K=1$ , no pipe can have endpoints of different heights.

Redesign by Codex (GPT-6): clarify that required endpoints remain paired, all heights may be reassigned, unused positions may stay empty, and contact is forbidden. Supply missing sample outputs. The original bounds, modulus, and memory limit are retained.

| Score | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, worth 10% each. [Generation guide](tests/README.md).
