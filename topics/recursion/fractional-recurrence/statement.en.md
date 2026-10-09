# A Fractional-Power Recurrence

Estimated time limit: 1.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

An evaluation service receives many integer queries. Each answer depends on answers at two smaller arguments. Compute the exact values for all queries.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

The function $F$ maps nonnegative integers to nonnegative integers and satisfies

$$F(x)=3F\left(\max\{\lfloor x^{4/5}\rfloor-1,0\}\right)+2F\left(\left\lfloor\frac{x}{2}\right\rfloor\right)+x$$

The fractional power is taken over the real numbers, and $\lfloor\cdot\rfloor$ means floor. The equation also holds at zero, implying $F(0)=0$ . Given $N$ arguments $a_i$ , compute each exact integer value $F(a_i)$ without taking a modulus.

## Input Format

The first line contains the query count $N$ . The second contains $a_1,\ldots,a_N$ .

## Output Format

Print $N$ space-separated integers on one line, giving answers in query order.

## Samples

### Sample 1

### Input

```text
5
0 1 1000000000 5000 2
```

### Output

```text
0 1 12422138161640 8422275 4
```

### Sample 2

### Input

```text
6
0 0 1 2 3 4
```

### Output

```text
0 0 1 4 8 24
```

## Sample Explanation

In the second sample, $F(1)=1$ , $F(2)=4$ , and $F(3)=8$ . Since $\lfloor4^{4/5}\rfloor-1=2$ , we have $F(4)=3F(2)+2F(2)+4=24$ . Repeated queries at zero all return zero.

## Constraints and Guarantees

For all inputs, $1\le N\le10^5$ and $0\le a_i\le10^9$ . Queries may repeat.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
