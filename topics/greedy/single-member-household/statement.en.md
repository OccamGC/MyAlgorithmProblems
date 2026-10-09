# Edit Town and Simoleons

Reference time limit: 1.5 s; memory limit: 128 MiB. Calibrate to twice the slowest formal-file median, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

In The Sims, Edit Town lets players change the town without spending their own Simoleons, although furnishing their own home still costs money. Besides buildings and interiors, this mode can edit household membership. When a resident leaves, they take an equal per-person share of the household’s Simoleons.

After discovering this rule, Little A poses a problem. The town has several households, and household 1 initially has one resident. Edit the households repeatedly, restore household 1 to its original membership, and make its wealth as large as possible. Subject to this maximum, Little A also wants to know the wealth gaps and whether household 1 can become the wealthiest household.

## Formal Problem Statement

Initially there are $n$ households. Household $i$ has $p_i$ distinct residents and wealth $m_i$ . Household 1 has exactly one resident, called the target resident.

One edit moves a resident out of their current household into another nonempty household or a new single-person household. If the old household has $p$ residents and wealth $m$ before the move, the resident takes $m/p$ , leaving $p-1$ residents and wealth $m-m/p$ . All carried wealth is added to the destination household. Delete empty households immediately. Wealth is an exact rational number; residents and wealth cannot be created or destroyed.

Any finite number of edits is allowed. At the end the target resident must live alone in the target household. Other residents may be grouped arbitrarily. Household sizes during editing and at the end have no upper bound.

First maximize the target household's wealth, obtaining $A$ . Among arrangements attaining $A$ , independently determine:

1. The target wealth $A$ .
2. The largest household wealth gap: maximum minus minimum wealth over all nonempty households.
3. The largest per-capita wealth gap: maximum minus minimum per-person wealth over all nonempty households.
4. Whether some arrangement makes the target at least as wealthy as every other household.
5. Whether some arrangement makes the target strictly wealthier than every other household.
6. Whether some arrangement makes the target at least as wealthy per person as every other household.
7. Whether some arrangement makes the target strictly wealthier per person than every other household.

Items 2 through 7 are independent and may use different final groupings. With only one household, both gaps are zero and all four predicates are true.

Print the first three values modulo $P=1000000007$ . For an exact rational number $x=r/s$ in reduced form, its residue is $r\cdot s^{-1}\bmod P$ , represented in $[0,P-1]$ . The denominators of the three required optimal values are coprime to $P$ .

![The target sequentially averages with two wealthier residents](assets/example.svg)

The target starts with wealth 1 and averages with residents holding 9 and 13, reaching 5 and then 9. The other two end with 5 and 9. Grouping them into a household of wealth 14 gives a household wealth gap of 5.

## Input Format

The first line contains $n$ . Each of the next $n$ lines contains $p_i,m_i$ for one initial household.

## Output Format

Print seven lines in the order above. The first three are rational residues; each of the last four is 1 for true or 0 for false.

## Sample 1

### Input

```text
1
1 7
```

### Output

```text
7
0
0
1
1
1
1
```

## Sample 2

### Input

```text
2
1 2
1 10
```

### Output

```text
6
0
0
1
0
1
0
```

## Sample 3

### Input

```text
3
1 1
1 9
1 13
```

### Output

```text
9
5
4
1
1
1
1
```

## Sample 4

### Input

```text
3
1 3
1 2
1 5
```

### Output

```text
4
2
2
1
1
1
1
```

## Sample 5

### Input

```text
3
1 10
2 6
1 2
```

### Output

```text
10
8
8
1
1
1
1
```

## Sample 6

### Input

```text
4
1 2
1 2
2 4
1 2
```

### Output

```text
2
6
0
1
0
1
0
```

## Sample 7

### Input

```text
2
1 1
3 4
```

### Output

```text
291666670
416666672
125000001
1
1
1
1
```

## Constraints and Guarantees

$1\le n\le1000000$ , $p_1=1$ , $1\le p_i\le20$ , $1\le m_i\le1000000$ .

Redesigned by Codex (GPT-6): the target initially has one resident and every initial household has at most 20 residents. The one-million-household limit, arbitrary editing rules, and seven outputs are preserved. Empty households, rational residues, and independent optimization of the outputs are specified.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, 10% each. See [test generation and validation](tests/README.md).

See [Edit Town and Simoleons 2](../town-editing-simoleons-2/statement.en.md) for the multiple-member variant.
