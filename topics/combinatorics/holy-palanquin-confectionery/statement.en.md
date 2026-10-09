# Restocking the Holy Palanquin Ship's Confectionery

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

“Quit this job!” ICG says angrily.

The confectionery operated by the Holy Palanquin Ship is completely out of stock. NYN, the shopkeeper, sends the employees Flour—that is, you—and Milk to buy supplies. NYN gives you $X$ units of money. The supplier has $X$ product types, numbered $1,\ldots,X$ . Type $i$ costs $i$ per item, with $X$ items of each type in stock.

Big Sister SZ has pressured Milk into providing data about the shop's business. You must therefore consider every restocking plan within the budget, add up the money left over in all of them, and report the result modulo $998244353$ .

## Formal Problem Statement

The budget is $X$ units of money. There are $X$ product types numbered $1,\ldots,X$ . Type $i$ costs $i$ per item and has $X$ items in stock.

A plan consists of integer quantities $q_1,\ldots,q_X$ satisfying $0\le q_i\le X$ and $\sum_{i=1}^{X}i q_i\le X$ . Its remaining money is $X-\sum_{i=1}^{X}i q_i$ . Plans differ if any quantity differs; purchase order does not matter.

Find the sum of the remaining money over all plans, modulo $998244353$ . Buying nothing is a valid plan. When the budget is zero, there are no products and the unique empty plan leaves zero money.

## Input Format

The input consists of one integer $X$ .

## Output Format

Print the sum of the remaining money modulo $998244353$ as one integer.

## Samples

### Sample 1

### Input

```text
10
```

### Output

```text
284
```

### Sample 2

### Input

```text
0
```

### Output

```text
0
```

### Sample 3

### Input

```text
3
```

### Output

```text
7
```

## Sample Explanation

The sum in Sample 1 is two hundred and eighty-four. Sample 2 has only the empty plan, with zero remaining money. In Sample 3, the numbers of plans costing zero, one, two, and three units are one, one, two, and three, so the answer is $3+2+2\times1+3\times0=7$ .

## Constraints and Guarantees

For 100% of the data: $0\le X\le80$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
