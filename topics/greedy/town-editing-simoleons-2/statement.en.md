# Edit Town and Simoleons 2

Reference time limit: 2 s; memory limit: 128 MiB. Calibrate to twice the slowest formal-file median, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

In The Sims, Edit Town lets players change the town without spending their own Simoleons, although furnishing their own home still costs money. Besides buildings and interiors, this mode can edit household membership. When a resident leaves, they take an equal per-person share of the household’s Simoleons.

After discovering this rule, Little A poses a problem: repeatedly edit the town’s households, restore household 1 to its original membership, and make its wealth as large as possible.

This time, household 1 may have several members. Little A only wants to know the maximum number of Simoleons it can eventually own.

## Formal Problem Statement

Initially there are $n$ households. Household $i$ has $p_i$ distinct residents and $m_i$ Simoleons. The $p_1$ residents initially belonging to household 1 are the target members. Their identities never change.

One edit moves a resident out of their current household into another nonempty household or a new single-person household. If the source has $p$ residents and wealth $m$ before the move, the resident takes $m/p$ , leaving $p-1$ residents and wealth $m-m/p$ . All carried wealth is added to the destination. Empty households are deleted immediately. Wealth is an exact rational quantity; residents and Simoleons cannot be created or destroyed.

Any finite number of edits, including zero, is allowed. The number of households may increase or decrease, and household sizes during editing and at the end have no upper bound. Finally, all target members must form one household, called the final household 1, with no other residents. Target members may live apart during editing. Other residents may be grouped arbitrarily at the end.

Find the maximum final wealth $A$ of household 1 and print it modulo $P=1000000007$ . Maximize the exact rational value before taking its residue. If $A=r/s$ in reduced form, its residue is $r\cdot s^{-1}\bmod P$ , represented in $[0,P-1]$ . The maximum is attainable after finitely many edits, and its denominator is coprime to $P$ .

![Two target members average with outsiders and finish with wealth 7 and 5](assets/example.svg)

Here $T_1,T_2$ are the target members and $O_1,O_2$ are outsiders. Each pair initially belongs to one household. First let $O_1$ merge and split with $T_1$ and then $T_2$ , one pair at a time. Repeat with $O_2$ . Finally reunite the target members to obtain $7+5=12$ Simoleons.

## Input Format

The first line contains an integer $n$ .

Each of the next $n$ lines contains two integers $p_i,m_i$ , the initial size and wealth of a household.

## Output Format

Print one integer on one line: the residue of the maximum wealth $A$ .

## Sample 1

### Input

```text
1
3 7
```

### Output

```text
7
```

## Sample 2

### Input

```text
2
2 2
1 9
```

### Output

```text
8
```

The target members can obtain 5 and 3, then reunite with total wealth 8. Merging all three residents at once and removing the outsider yields only $22/3$ .

## Sample 3

### Input

```text
2
2 2
2 18
```

### Output

```text
12
```

## Sample 4

### Input

```text
3
3 6
2 4
1 1
```

### Output

```text
6
```

## Sample 5

### Input

```text
2
2 1
2 3
```

### Output

```text
250000004
```

The maximum wealth is $9/4$ .

## Sample 6

### Input

```text
2
20 1
1000000 1000000
```

### Output

```text
538776497
```

## Constraints and Guarantees

$1\le n\le1000000$ , $1\le p_1\le20$ , $1\le p_i\le1000000$ for $2\le i\le n$ , and $1\le m_i\le1000000$ .

Redesigned by Codex (GPT-6): ask only for maximum target wealth, allow at most 20 initial target members and one million initial members in each other household, and permit arbitrary finite editing with the original target membership restored at the end.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, 10% each. See [test generation and validation](tests/README.md) and [Edit Town and Simoleons](../single-member-household/statement.en.md).
