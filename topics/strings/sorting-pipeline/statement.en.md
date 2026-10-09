# Factorio: Sorting Pipeline

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

An engineer is building a signal network for a Factorio workshop. Four units emit integers, decimals, uppercase letters and lowercase letters. A sorting pipeline must separate the mixed signal, add the numbers, and change the case of the letters.

## Formal Problem Statement

The string $S$ is formed by concatenating outputs from four kinds of units:

- Type A: a nonnegative decimal integer without a decimal point.
- Type B: a nonnegative decimal number with exactly one decimal point, at most two digits after it, and at least one digit in total. Forms such as ` .1` and `0.` are allowed.
- Type C: one uppercase English letter.
- Type D: one lowercase English letter.

At least one letter separates any two numbers. Thus each maximal contiguous segment of digits and decimal points represents exactly one number. Numbers have no sign and do not use scientific notation.

Find the sum of type A integers and the sum of type B decimals. Collect type C letters in lowercase and type D letters in uppercase, preserving the order within each type.

## Input

The input is one line containing $S$ , without spaces. The line may be empty.

## Output

Output four lines, in this order:

1. The sum of the integers.
2. The sum of the decimals, with exactly two digits after the decimal point and digits on both sides of it.
3. The type C letters converted to lowercase.
4. The type D letters converted to uppercase.

A missing numeric type has sum zero. A missing letter type still requires an empty output line.

## Samples

### Sample 1

### Input

```text
0x3F666.
```

### Output

```text
3
666.00
f
X
```

### Sample 2

### Input

```text
66ccff3f3f3f3f
```

### Output

```text
78
0.00

CCFFFFFF
```

### Sample 3

### Input

```text
.01A.09b0.C999999.99
```

### Output

```text
0
1000000.09
ac
B
```

## Sample Explanation

In sample 1, the integers are $0,3$ , the decimal is $666.$ , and the two letter types contain `F` and `x` .

Sample 2 has no decimals or uppercase letters, so its third output line is empty. In sample 3, the decimal sum is $1000000.09$ ; the bound on an individual number does not apply to the sum.

## Constraints and Guarantees

For 100% of the data: $0\le |S|\le10^5$ , and each number is less than $10^6$ . The string follows the rules above; numbers may have leading zeros.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
