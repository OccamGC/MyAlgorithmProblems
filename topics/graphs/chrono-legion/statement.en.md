# Chrono Legion

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: twice the reference program's benchmark time on the slowest official input in the target environment, rounded up to a multiple of 0.5 seconds. Round up again if the platform requires a coarser unit.
- Memory limit: 256 MB

## Story

A Chrono Legionnaire infiltrates the game's Soviet base to cut communication links between buildings. An alarm will sound as soon as any two buildings can no longer communicate.

He wants to remove as many links as possible while keeping communication available throughout the operation. The commander also wants to count the possible orders of action.

## Formal Problem Statement

The base occupies an $N$ by $M$ grid and contains $K$ labeled buildings. Building $i$ is at $(X_i,Y_i)$ and has construction time $T_i$ . Construction times are distinct. Different buildings may occupy the same cell and still count as separate buildings.

The region centered at building $i$ with nonnegative integer radius $r$ contains every building $j$ satisfying

$$\max(|X_j-X_i|,|Y_j-Y_i|)\le r$$

The center building itself is included. Radius $0$ is allowed and includes all buildings at the same coordinates.

Building $i$ has $P_i$ thresholds $D_{i1},\ldots,D_{iP_i}$ . For each threshold $D$ , generate a link as follows:

1. Find the smallest radius containing at least $D$ buildings, including building $i$ in the count.
2. Among all buildings within that radius, choose the building $j$ with the greatest construction time. All buildings on the boundary participate, not just the first $D$ entries of a sorted list.
3. If $j\ne i$ , add an undirected link between $i$ and $j$ . If $j=i$ , add no link.

Thresholds may repeat. There is at most one link between any pair, regardless of how many times it is selected. The resulting undirected graph is guaranteed to be connected.

Each action removes one existing link, and the graph must remain connected after every removal. Count action sequences that remove the maximum possible number of links, modulo the input integer $\mathrm{mod}$ . Two sequences differ if the link removed at any step differs. The empty sequence counts as one.

## Input Format

The first line contains four integers $N,M,K,\mathrm{mod}$ .

Each of the next $K$ lines describes a building. Line $i$ contains $X_i,Y_i,T_i,P_i$ , followed by the $P_i$ integers $D_{i1},\ldots,D_{iP_i}$ .

## Output Format

Output one integer: the number of sequences modulo $\mathrm{mod}$ .

## Sample 1

### Input

```text
1 5 3 10
1 1 5 1 2
1 5 1 1 2
1 3 10 1 3
```

### Output

```text
1
```

### Explanation

The first two buildings each link to the third, forming a tree. No link can be removed, so the empty sequence is the only answer.

## Sample 2

### Input

```text
1 4 3 12
1 1 1 2 2 3
1 2 2 1 3
1 4 3 1 3
```

### Output

```text
3
```

### Explanation

The three buildings form a triangle. Exactly one link can be removed, and any of the three links can be chosen.

## Sample 3

### Input

```text
1 2 3 1000000007
1 1 1 2 1 3
1 1 2 1 3
1 2 3 1 3
```

### Output

```text
3
```

### Explanation

Threshold $1$ at the first building gives radius $0$ , containing both the first and second buildings. It therefore links to the second building. The other thresholds add links to the third, producing a triangle.

## Sample 4

### Input

```text
1 1 1 2
1 1 0 1 1
```

### Output

```text
1
```

### Explanation

The single building cannot link to itself. The empty sequence is the only answer.


## Constraints and Guarantees

- $1\le N,M$ , $NM\le10^6$ , and $1\le K\le200$ .
- $1\le X_i\le N$ , $1\le Y_i\le M$ , and $0\le T_i\le10^{18}$ . All $T_i$ are distinct.
- $1\le P_i\le K$ and $1\le D_{ij}\le K$ . Thresholds may repeat.
- $2\le\mathrm{mod}\le1000000500$ ; the modulus need not be prime.
- All input values are integers. The generated link graph is connected; a single building also counts as connected.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $N,M\le100$ , $K\le8$ , $T_i\le200$ , and $\mathrm{mod}$ is prime |
| 30% | $N,M\le1000$ and $\mathrm{mod}$ is prime |
| 10% | $\min(N,M)=1$ and $\mathrm{mod}$ is prime |
| 10% | $\mathrm{mod}$ is prime |
| 20% | No additional conditions |
