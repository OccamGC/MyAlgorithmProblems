# Potion Wool

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for estimation only)
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 32 MB

## Story

The farm now keeps potion sheep. Some wool makes its carrier move faster, while other wool slows the carrier down. The village head must shear every flock once and store all the wool in chests. Plan the visits and deposits to minimize the total time.

## Formal Problem Statement

The farm is an $a$ by $b$ grid. `S` is the start, `C` a chest, `E` empty land, `B` an obstacle, and digits $0,\ldots,p-1$ mark the flocks. Each flock appears exactly once. Every cell except obstacles and cells outside the grid can be traversed.

There are $k$ sheep types. Each unit of wool of type $j$ adds $d_j$ to the time for one step. Initially no wool is carried and the base step time is $t$ . With $c_j$ units of type $j$ in the inventory, a move to an orthogonally adjacent cell costs

$$\max\left(1,t+\sum_{j=1}^{k}c_jd_j\right)$$

Flock $i$ contains $w_{i,j}$ sheep of type $j$ . At an unshorn flock, you may pass without shearing or shear the entire flock, gaining one unit of wool per sheep. Each flock may be shorn once. At a chest, you may deposit any quantity of any carried wool, including none. Deposited wool cannot be retrieved. Shearing and depositing take no time; wool cannot be dropped elsewhere.

Find the minimum time to start at `S` , shear all flocks, and deposit all wool in one or more chests. Returning to the start is unnecessary.

## Input Format

The first line contains $a,b,p,k,t$ . The second line contains the $k$ integers $d_j$ . The next $p$ lines describe flocks $0$ through $p-1$ , each with $k$ integers $w_{i,j}$ . The final $a$ lines contain $b$ space-separated characters each, describing the map.

## Output Format

Print the minimum total time as an integer.

## Example 1

### Input

```text
4 4 2 2 10
-5 2
0 1
1 0
1 B C E
E B B E
E E E 0
B B B S
```

### Output

```text
106
```

## Example 2

### Input

```text
4 4 2 2 2
-3 4
1 0
0 1
S E B B
E E 0 B
E 1 B B
E E E C
```

### Output

```text
17
```

## Example 3

### Input

```text
1 10 2 2 1
10 -2
1 1
1 1
S C E 0 E E E 1 E C
```

### Output

```text
41
```

## Example Explanation

In example 1, visit flock $1$ , flock $0$ , then a chest. The cost is $6\times10+5\times5+3\times7=106$ . In example 2, visit flock $0$ , flock $1$ , then a chest, costing $3\times2+2\times1+3\times3=17$ .

For example 3, follow the route below. At the left chest, deposit only the wool that increases step time and retain the wool that decreases it. Deposit everything at the right chest. The four legs cost $3,18,6,14$ , totaling $41$ .

![The four legs in example three, visiting flock zero, the left chest, flock one, and the right chest](assets/deposit-route.svg)

## Constraints and Guarantees

All inputs satisfy $1\le a,b\le10$ , $1\le p\le10$ , $1\le k\le50$ , $1\le t\le10^6$ , $-100\le d_j\le100$ , and $0\le w_{i,j}\le10$ . Each flock contains at least one sheep. There is exactly one start and between $1$ and $10$ chests. Every flock and chest is reachable from the start.

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
