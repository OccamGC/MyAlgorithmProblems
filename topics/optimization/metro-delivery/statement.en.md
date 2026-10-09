# Metro Delivery

- Indicative time limit: **0.5 seconds** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: twice the reference program's median runtime on the slowest test file in the target environment, rounded up to a multiple of 0.5 seconds.
- Memory limit: **512 MB**.

## Story

Qingchuan Town is building its third metro line. The head of Creekvale Village also works as a planner for the Transit Office and has taken charge of delivering construction resources along the line.

Each station produces resources for stations farther along the route. The freight train cannot turn around easily, so it only moves forward; automated loading and unloading take negligible time. The village head can also use command blocks to shorten travel times between adjacent stations and wants the resources delivered as early as possible.

## Formal Problem Statement

There are $n$ stations in order, numbered $1,2,\ldots,n$ . A freight train with unlimited capacity starts at station $1$ at time $0$ . It can only travel from station $i$ to station $i+1$ and cannot return.

For each $1\le i<n$ , station $i$ produces $\mathrm{Num}_i$ resources for **each** station $j>i$ . All these resources become available at time $T_i$ and cannot be loaded before then. Station $i$ produces $(n-i)\mathrm{Num}_i$ resources in total, each with a fixed destination.

The train may wait at a station, and loading and unloading take no time. Traveling from station $i$ to station $i+1$ initially takes $D_i$ time units. You may use at most $K$ command blocks. Each use reduces the travel time of one segment between adjacent stations by $1$ . A segment may be chosen multiple times, but its travel time must remain nonnegative.

The delivery task is complete when **all resources have reached their respective destinations**. The time spent by a resource is its arrival time at its destination minus its production completion time. Allocate the command blocks and schedule the deliveries to minimize the sum of these times over all resources.

Minimize the total time first, then take the result modulo $10^9+9$ . If there are no resources, the total time is $0$ .

## Input Format

The first line contains two integers $n,K$ .

The next $n-1$ lines describe stations $1$ through $n-1$ . Line $i$ contains three integers $\mathrm{Num}_i,T_i,D_i$ : the number of resources produced for each later station, their production completion time, and the original travel time to station $i+1$ .

## Output Format

Print one integer: the minimum total time modulo $10^9+9$ .

## Sample 1

### Input

```text
3 2
2 1 2
3 2 1
```

### Output

```text
4
```

## Sample 2

### Input

```text
5 7
2 1 2
3 2 1
5 5 3
1 4 3
```

### Output

```text
44
```

## Sample 3

### Input

```text
10 17
2 1 2
3 2 1
5 5 3
1 4 3
3 3 3
4 4 4
6 6 6
3 1 4
4 5 2
```

### Output

```text
669
```

## Sample 4

### Input

```text
3 0
1 0 1
0 100 1
```

### Output

```text
3
```

## Sample Explanation

In sample 1, reduce the two travel times from $2,1$ to $1,0$ . The train leaves station $1$ at time $1$ and reaches both station $2$ and station $3$ at time $2$ . Each of the four resources produced at station $1$ spends $1$ time unit, and each of the three resources produced at station $2$ spends $0$ time units. The total is $4$ .

![The three-station route in sample 1: travel times decrease from 2 and 1 to 1 and 0, and both delivery times are 2](assets/delivery-route.svg)

Here $D$ denotes a reduced travel time and $A$ an arrival time. The blue numbers are the actual travel times in this schedule.

In sample 4, two resources must be delivered, and the minimum total time is $3$ .

## Constraints and Guarantees

For all test cases: $1\le n\le10^5$ and $0\le K\le5\times10^8$ . For every $1\le i<n$ , $0\le\mathrm{Num}_i,D_i\le10^5$ and $0\le T_i\le10^9$ . All input values are integers.

| Score | Additional constraints |
| --- | --- |
| 10% | $K=0$ |
| 20% | $K\le1$ |
| 10% | $n\le50$ , $\mathrm{Num}_i\le50$ , $T_i\le500$ , $K\le50$ , $D_i\le100$ |
| 20% | $n\le2000$ , $K\le2000$ |
| 40% | No additional constraints |
