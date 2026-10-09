# Lottery Plugin

- Indicative time limit: 8.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for estimation only)
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 512 MB

## Story

The village head is testing a lottery plugin. Participants may leave, or change their lucky number and rejoin. At specified events, the plugin must find the lucky number closest to a target, following precise tie rules.

## Formal Problem Statement

There are $n$ participants, numbered $1$ through $n$ . Initially everyone is active and participant $i$ has lucky number $i$ . Process $m$ events in order.

Let $a_0=A$ . For each event $i$ , compute exactly once

$$a_i=(a_{i-1}B+C)\bmod n+1,\qquad t_i=a_i$$

There are three event types:

1. **Query:** choose an active participant whose lucky number has minimum absolute difference from $t_i$ . Break a distance tie by the smaller lucky number. For equal lucky numbers, choose the smallest participant ID if that number is greater than $t_i$ , and the largest ID otherwise. Return $0$ if nobody is active. A query changes nothing.
2. **Update:** for the specified participant $d_i$ , set the lucky number to $t_i$ and reactivate that participant if necessary.
3. **Leave:** deactivate participant $t_i$ . If already inactive, nothing changes.

The input specifies the positions of the $q$ queries and the positions and participants of the $k$ updates. All other events are leave events. Every event advances the sequence once, including queries and ineffective leave events.

## Input Format

The first line contains $A,B,C$ . The second line contains four integers $n,m,q,k$ . The third line contains the $q$ query event indices in strictly increasing order. The fourth line contains $k$ pairs $p_i,d_i$ , meaning that event $p_i$ updates participant $d_i$ , with $p_i$ strictly increasing. The two sets of event indices are disjoint. The corresponding line is empty if $q=0$ or $k=0$ .

## Output Format

Print one answer per query in event order, on $q$ lines. Print no integers when $q=0$ .

## Example 1

### Input

```text
5 3 3
5 8 4 2
3 6 7 8
2 3 5 3
```

### Output

```text
2
1
2
3
```

## Example 2

### Input

```text
1 13 17
11 30 10 8
5 13 17 18 19 20 23 25 27 30
1 1 8 1 9 1 15 10 21 10 26 4 28 4 29 10
```

### Output

```text
7
4
4
6
8
4
4
7
6
4
```

## Example 3

### Input

```text
1 1 17
11 60 15 8
5 13 17 18 19 20 23 25 27 30 40 45 55 58 60
1 1 8 1 9 1 15 10 21 10 26 4 28 4 29 10
```

### Output

```text
3
3
9
10
2
9
9
9
2
2
2
0
0
0
0
```

## Example Explanation

The targets in example 1 are $4,1,2,5,4,1,2,5$ , and the four query answers are $2,1,2,3$ . Nobody is active for the last four queries of example 3, so those answers are $0$ .

## Constraints and Guarantees

All inputs satisfy $1\le n\le3500000$ , $0\le m\le4000000$ , $0\le q,k\le200000$ , $q+k\le m$ , and $0\le A,B,C\le10^9$ . Event indices are in $[1,m]$ and updated participant IDs are in $[1,n]$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
