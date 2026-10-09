# Interstellar Orders: Acceleration

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

An interstellar computing center receives a batch of motion-calculation orders. Each model comes with two integer parameters, and the customer asks for distances in a consistent output format.

## Formal Problem Statement

For each order, given integers $a,t$ , calculate

$$d=\left|\frac{at^2}{2}\right|$$

Here $a$ is the acceleration parameter and $t$ is the time parameter. Both may be negative. The answer is defined exactly by this formula and is nonnegative.

## Input

The first line contains the number of orders $T$ . Each of the next $T$ lines contains two integers $a,t$ .

## Output

Output $T$ lines, each containing $d$ with exactly one digit after the decimal point. For $T=0$ , the output is empty.

## Samples

### Sample 1

### Input

```text
6
0 0
1 1
-1 1
2 -3
-3 -3
10000 10000
```

### Output

```text
0.0
0.5
0.5
9.0
13.5
500000000000.0
```

### Sample 2

### Input

```text
4
-10000 -10000
9999 9999
1 -10000
-10000 0
```

### Output

```text
500000000000.0
499850014999.5
50000000.0
0.0
```

### Sample 3

### Input

```text
0
```

### Output

```text

```

## Sample Explanation

The first three answers in sample 1 are $0.0,0.5,0.5$ . When $a=-3,t=-3$ , the answer is $d=13.5$ . Its final order gives $500000000000.0$ . Sample 3 has no orders and hence no output.

## Constraints and Guarantees

For 100% of the data: $0\le T\le10^4$ and $|a|,|t|\le10^4$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
