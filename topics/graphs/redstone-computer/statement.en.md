# Redstone Computer

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 512 MB

## Story

The village chief is debugging a prototype redstone computer. To check whether its recorded results are consistent, find a set of inputs that produces all of them, or report that no such inputs exist.

## Formal Problem Statement

There are $n$ unknown $k$-bit binary numbers $x_1,\ldots,x_n$ . You are given $m$ relations of the form

$$x_a\mathbin{\mathrm{op}}x_b=C$$

where the operator is bitwise XOR `^` , AND `&` , or OR `|` , and $C$ is a given $k$-bit binary number. A relation may have $a=b$ , and relations may be repeated or contradictory.

Construct values satisfying all relations. Any valid assignment is accepted. If none exists, output `No` . Binary strings are written most significant bit first and may contain leading zeros.

## Input Format

The first line contains $n,m,k$ . Each of the next $m$ lines contains $a,\mathrm{op},b,C$ , separated by spaces.

## Output Format

If no assignment exists, print `No` on one line. Otherwise print $n$ lines, each with exactly $k$ characters `0` or `1` ; line $i$ gives $x_i$ .

When $n=0$ , necessarily $m=0$ . The empty assignment is valid and the output is empty. Any valid assignment is accepted. Whitespace separators are ignored, but extra non-whitespace content is rejected.

## Sample 1

### Input

```text
3 3 3
1 ^ 2 000
3 & 3 101
2 ^ 1 000
```

### Output

```text
111
111
101
```

### Explanation

The assignment $x_1=x_2=111$ , $x_3=101$ satisfies all relations. Other valid assignments are also accepted.

## Sample 2

### Input

```text
2 2 3
1 | 2 111
1 & 2 000
```

### Output

```text
000
111
```

### Explanation

Exactly one of the two numbers has a set bit at each position. Swapping the two output numbers is also valid.

## Sample 3

### Input

```text
1 1 1
1 ^ 1 1
```

### Output

```text
No
```

### Explanation

A number XOR itself is always zero, so this relation is impossible.

## Sample 4

### Input

```text
0 0 2
```

### Output

```text

```

### Explanation

There are no unknowns or relations, so the output is empty.

## Constraints and Guarantees

- $0\le n\le500$ , $0\le m\le10000$ , and $1\le k\le150$ .
- Every relation has $1\le a,b\le n$ and a binary string $C$ of exactly $k$ characters.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 10% | $k=1$ , $n\le20$ |
| 20% | $k=1$ , $n\le50$ |
| 70% | No additional conditions |
