# Simple Analysis

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A laboratory is estimating how many calls a binary-exponentiation routine makes to its multiplication module. The exponent may be very long and is supplied in binary.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Analyze the complete pseudocode below. All variables represent arbitrary-precision integers. The function `multiply(x,y,m)` returns $xy\bmod m$ . Count calls to `multiply` , rather than elementary operations inside that function.

The initial exponent is a nonnegative integer $e$ , with `index = e` before execution. The auxiliary parameter `modulus` is prime, `base` is coprime to it, and $0\le e<\text{modulus}-1$ .

```text
result = 1
index = index mod (modulus - 1)
while index > 0:
    if index mod 2 == 1:
        result = multiply(result, base, modulus)
    index = floor(index / 2)
    if index > 0:
        base = multiply(base, base, modulus)
return result
```

Each input string represents an initial exponent. The auxiliary parameters are not part of the input; under these guarantees the count depends only on the exponent. Leading zeros do not change it. Notice that no squaring call is made after the exponent becomes zero.

## Input Format

The first line contains a nonnegative query count $Q$ . Each of the next $Q$ lines contains a nonempty string of `0` and `1` , representing an unsigned binary integer.

## Output Format

Print $Q$ lines, each containing the number of `multiply` calls for that exponent. If $Q=0$ , produce no output.

## Examples

### Example 1

### Input

```text
5
0
10011
1111
1
1100
```

### Output

```text
0
7
7
1
5
```

### Example 2

### Input

```text
4
0000
0001
00100
00101
```

### Output

```text
0
1
3
4
```

### Example 3

### Input

```text
3
10
100000
111111
```

### Output

```text
2
6
11
```

## Example Explanation

In the first example, `10011` represents $19$ . The loop processes $19,9,4,2,1$ : three conditional multiplications and four squarings, for seven calls. Exponent `0` never enters the loop; `1` makes one conditional multiplication. The second example shows that leading zeros do not add calls.

## Constraints and Guarantees

All inputs satisfy $0\le Q\le2.1\times10^6$ . Every string is nonempty and their total length is at most $2.1\times10^6$ . Each exponent has auxiliary parameters satisfying the guarantees in the formal statement.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
