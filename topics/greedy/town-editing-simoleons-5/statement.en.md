# Edit Town and Simoleons 5

Reference time limit: 0.5 seconds; memory limit: 64 MiB. Calibrated at twice the slowest formal-file median, rounded up to 0.5 seconds; see the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

The Sims lets players change a town in Edit Town without spending their own Simoleons, although furnishing their own home still costs money. Besides buildings and interiors, this mode can edit household membership. A departing resident takes an equal per-person share of the household's Simoleons.

Little A is studying household wealth again. This time, the town has a fixed number of household positions, and an empty household keeps its position. Little A wants the original members of household 1 to reunite and own as many Simoleons as possible.

## Formal Problem Statement

The town always has $n$ household positions numbered $1,2,\ldots,n$ . Initially, household $i$ contains $p_i$ people and $m_i$ Simoleons. The original members of household 1 are the target members; their identities never change. Let $k=p_1$ be their number, which is positive.

An edit moves one resident to a different household position. If the source contains $p$ people and $m$ Simoleons immediately before the move, the resident takes $m/p$ Simoleons. The source loses one person and that amount of money; the destination gains both. Money in the destination is shared by all its members, and a later departure takes the new per-person share.

A resident may move into an empty household. An emptied household retains its position and has zero Simoleons. No new position can be created. Household populations during editing and at the end have no upper bound. All money is an exact rational quantity, and moves conserve total money.

Any finite number of edits is allowed, including zero. At the end, all target members must form one household containing no outsiders. This household may occupy any position. Find its maximum total wealth $W$ .

Maximize the exact rational value first, then output it modulo $P=1000000007$ . If $W=u/v$ in lowest terms, its modular value is $u\cdot v^{-1}\bmod P$ , represented in $[0,P-1]$ . Under the guarantees below, the maximum is attained by finitely many edits and its denominator is coprime to $P$ .

The initial state satisfies the following guarantee. Let $a=m_1/k$ . Consider external households, with $i\ge2$ , for which $p_i>0$ and $m_i/p_i>a$ . Their per-person wealth takes at most three distinct exact rational values. Let $g$ be the actual number of these values. Then

$$0\le g\le3,\qquad n\ge k+g+1.$$

For example, $1/3$ and $2/6$ count as the same value. External households no richer than the target household may have any number of distinct means; they do not contribute to $g$ . The input does not provide $g$ separately. There need not be an empty household initially.

![Fixed household positions](assets/example.svg)

Here $T$ denotes a target, $O$ an outsider, and $M$ household wealth. Merge the external households with mean 9, then separate the targets. After processing the outsiders, reunite the targets in A. Only four positions are used; a stage transition may involve several single-resident moves.

## Input Format

The first line contains $n$ . The next $n$ lines each contain $p_i,m_i$ for household $i$ . Each input describes one town.

## Output Format

Print one integer: the modular value of the maximum total wealth.

## Sample 1

### Input

```text
4
2 2
2 18
1 9
1 9
```

### Output

```text
16
```

Here $k=2,g=1,n=4$ , meeting the position bound exactly, with no initial empty household. After the four outsiders interact with the two targets, target wealth is $17/2$ and $15/2$ , totaling 16.

## Sample 2

### Input

```text
6
2 1
1 1
2 3
2 4
0 0
1 0
```

### Output

```text
367187506
```

The richer external means are $1,3/2,2$ , so $g=3$ and $n=k+g+1=6$ .

## Sample 3

### Input

```text
4
3 30
2 10
1 0
0 0
```

### Output

```text
30
```

No external household is richer than the target household, so $g=0$ . Zero edits attain the optimum 30.

## Sample 4

### Input

```text
5
3 1
2 1
4 2
6 3
0 0
```

### Output

```text
835021980
```

All three richer external households have mean $1/2$ , so $g=1$ .

## Sample 5

### Input

```text
2
1 7
0 0
```

### Output

```text
7
```

The other household is empty, giving an optimum of 7.

## Sample 6

### Input

```text
4
1 0
2 1
4 2
6 3
```

### Output

```text
616088872
```

All three external households have the same initial mean. The maximum is $4095/8192$ .

## Constraints and Guarantees

$2\le n\le1000000$ , $1\le p_1\le20$ , and $0\le p_i\le1000000$ for $i\ge2$ . The guarantees $g\le3$ and $n\ge p_1+g+1$ above hold.

All $0\le m_i\le10^9$ . If $p_i=0$ , then $m_i=0$ . These population and wealth bounds apply only to the initial input.

Redesigned by Codex (GPT-6): household positions are fixed and only the maximum wealth after reuniting the targets is requested; richer external households have at most three distinct means, with enough fixed positions.

| Score | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, worth 10% each. [Generation and verification](tests/README.md).
