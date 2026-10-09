# Edit Town and Simoleons 4

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

Initially, every nonempty household other than household 1 has exactly one member, and at least one household is empty. Household 1 may have many members.

![Fixed household positions](assets/example.svg)

Here $T_1,T_2$ are targets, $O_1,O_2$ are outsiders, and $M$ is household wealth. Each target visits B and C, then joins D. All stages use the same four positions.

## Input Format

The first line contains $n$ . The next $n$ lines each contain $p_i,m_i$ for household $i$ . Each input describes one town.

## Output Format

Print one integer: the modular value of the maximum total wealth.

## Sample 1

### Input

```text
4
2 2
1 9
1 9
0 0
```

### Output

```text
12
```

The targets bring 7 and 5 Simoleons into D, for an optimal total of 12.

## Sample 2

### Input

```text
4
3 1
1 1
1 2
0 0
```

### Output

```text
916666676
```

The maximum is $35/12$ , whose modular value is 916666676.

## Sample 3

### Input

```text
4
1 5
1 3
1 5
0 0
```

### Output

```text
5
```

No outsider is richer than the target household. Zero edits attain the optimum 5.

## Sample 4

### Input

```text
3
1000000 1
1 1
0 0
```

### Output

```text
502232024
```

There are one million target members, but only three household positions are needed.

## Sample 5

### Input

```text
3
4 7
0 0
0 0
```

### Output

```text
7
```

There are no outsiders, so all money belongs to the targets.

## Sample 6

### Input

```text
4
2 0
1 0
1 1
0 0
```

### Output

```text
750000006
```

The maximum is $3/4$ , whose modular value is 750000006.

## Constraints and Guarantees

$2\le n\le1000000$ , $1\le p_1\le1000000$ , and $p_i\in\{0,1\}$ for $i\ge2$ . At least one $p_i=0$ .

All $0\le m_i\le10^9$ . If $p_i=0$ , then $m_i=0$ . These population and wealth bounds apply only to the initial input.

Redesigned by Codex (GPT-6): household positions are fixed and only the maximum wealth after reuniting the targets is requested; all external households initially contain at most one person, with at least one empty position.

| Score | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, worth 10% each. [Generation and verification](tests/README.md).
