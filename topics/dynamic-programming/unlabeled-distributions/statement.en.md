# Distributing into Unlabeled Containers

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A warehouse places identical items into identical containers. Containers may remain empty and have no capacity limit. Count the distributions for several total numbers of items.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given positive integers $n,m$ , for each $t=1,2,\ldots,n$ distribute exactly $t$ indistinguishable items among $m$ indistinguishable containers. Find the least nonnegative residue of the number of distributions modulo $10^9+7$ .

Each container holds any nonnegative number of items. Two distributions are equal exactly when sorting all $m$ occupancies gives the same sequence. Exchanging containers therefore creates no new distribution. Count each total $t$ independently.

## Input Format

The input is one line containing $n,m$ .

## Output Format

Print $n$ lines. Line $t$ gives the number of ways to distribute exactly $t$ items, modulo $10^9+7$ .

## Samples

### Sample 1

### Input

```text
3 2
```

### Output

```text
1
2
2
```

### Sample 2

### Input

```text
5 1
```

### Output

```text
1
1
1
1
1
```

### Sample 3

### Input

```text
5 5
```

### Output

```text
1
2
3
5
7
```

## Sample Explanation

The first sample has two containers. One item gives only $(1,0)$ ; two items give $(2,0),(1,1)$ ; three give $(3,0),(2,1)$ . Exchanging the entries does not create a different distribution.

The second sample has one container, so each total has one distribution. The third has enough containers to hold all items separately; the first five counts are $1,2,3,5,7$ .

## Constraints and Guarantees

For all inputs, $1\le n,m\le5000$ . Empty containers are allowed.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
