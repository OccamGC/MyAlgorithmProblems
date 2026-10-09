# A Certain Unscientific Repeated Prefix Sum

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

You are given positive integers $n,m$ , a nonnegative integer $k$ , and coefficients $a_0,\ldots,a_k$ . Define

$$F_0(x)=\sum_{i=0}^{k}a_ix^i$$

For positive integers $t,x$ , recursively define

$$F_t(x)=\sum_{y=1}^{x}F_{t-1}(y)$$

Find the least nonnegative residue of $F_m(n)$ modulo $2147483647$ . Each summation includes both one and $x$ . For $k=0$ , the initial function is the constant $a_0$ .

## Input Format

The first line contains $n,m,k$ . The second contains $k+1$ integers $a_0,a_1,\ldots,a_k$ in that order.

## Output Format

Print one integer in $[0,2147483646]$ , the required answer.

## Samples

### Sample 1

### Input

```text
3 2 2
1 2 1
```

### Output

```text
46
```

### Sample 2

### Input

```text
5 3 0
7
```

### Output

```text
245
```

### Sample 3

### Input

```text
1 7 3
1 2 3 4
```

### Output

```text
10
```

## Sample Explanation

In the first sample, the first three initial values are $4,9,16$ . One round gives $4,13,29$ , and the third position after the second round is $4+13+29=46$ .

In the second sample, every initial value is seven. The first five values after two rounds are $7,21,42,70,105$ , whose sum is $245$ . The third sample asks only about the first position, which stays $1+2+3+4=10$ after every round.

## Constraints and Guarantees

For all inputs, $1\le n\le2\times10^9$ , $1\le m\le10^7$ , $0\le k\le300$ , and $1\le a_i\le2\times10^9$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
