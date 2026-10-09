# An Upgrade Plan for Battles

Estimated time limit: 3 seconds. Memory limit: 512 MB.

The deployed limit is the standard program’s largest input median in the target environment multiplied by $2$ and rounded up to a multiple of $0.5$ seconds. See the [benchmark notes](../../../docs/评测环境与性能.md).

## Story

An expedition must pass a series of guards. A workshop sells three kinds of upgrades, and the captain wants the smallest badge budget that keeps the fighter alive through every battle.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

The fighter initially has health $H_0$ , defence $D_0$ , and attack $A_0$ . Enemy type $i$ contains $k_i$ enemies, each starting with health $h_i$ , defence $d_i$ , and attack $a_i$ , for $i=1,\ldots,n$ .

Fight one enemy at a time. Both sides attack simultaneously in each round. An attack greater than the opponent’s defence reduces health by their difference; otherwise it causes no damage. After a round, combat ends if either health is nonpositive. A side with nonpositive health loses; both may lose in the same round. The fighter’s health does not recover between battles. Each new enemy starts with its full initial health.

Before fighting, you may perform any number of these upgrades:

- Spend $C_H$ badges to increase health by $1$ .
- Spend $C_D$ badges to increase defence by $V_D$ .
- Spend $C_A$ badges to increase attack by $V_A$ .

Defeat all $\sum_i k_i$ enemies and finish with strictly positive health. Find the minimum cost and the attributes $(H,D,A)$ immediately after upgrading and before any battle. Among minimum-cost solutions, choose the lexicographically smallest triple, comparing $H$ , then $D$ , then $A$ .

## Input

The first line contains $n$ . The second contains $H_0,D_0,A_0$ . The third contains $C_H,C_D,V_D,C_A,V_A$ . Each of the next $n$ lines contains $k_i,h_i,d_i,a_i$ .

## Output

If completion is impossible, print $-1$ . Otherwise, print the minimum cost on the first line and $H,D,A$ on the second. Positive upgrade steps guarantee a feasible solution in this problem.

## Samples

### Sample 1

### Input

```text
1
10 5 7
7 3 1 2 9
6 8 7 1
```

### Output

```text
2
10 5 16
```

### Sample 2

### Input

```text
1
1 1 2
1 1 1 1 1
1 1 1 2
```

### Output

```text
1
1 2 2
```

### Sample 3

### Input

```text
1
4 8 2
2 3 1 4 3
2 4 7 5
```

### Output

```text
8
4 8 8
```

## Sample explanations

In sample one, spending $2$ raises attack from $7$ to $16$ , allowing every enemy to be defeated without damage. In sample two, adding one health or one defence both cost $1$ ; $(1,2,2)$ wins because its upgraded health is smaller. In sample three, enemies cannot cause damage, but attack must still exceed their defence. The cheapest attainable attack is $8$ , costing $8$ .

## Constraints and guarantees

$1\le n,k_i\le5000$ . Initial attributes, enemy attributes, and both upgrade steps lie in $1,\ldots,5000000$ . Also, $1\le C_H,C_D,C_A\le1000000000$ . All input values are integers.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
