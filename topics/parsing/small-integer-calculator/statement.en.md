# Integer Calculator

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is twice the slowest per-case median time of the standard program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [evaluation notes](../../../docs/评测环境与性能.md).

## Story

An automated factory needs a small calculator for control expressions. It uses fixed 32-bit integer rules and reports an error when a divisor is zero.

## Formal Problem Statement

Evaluate a valid expression. A numeric literal is exactly one of $0,\ldots,9$ ; multi-digit literals are not allowed. Parentheses `(` and `)` change grouping. The table lists operators from highest to lowest precedence.

| Operators | Meaning | Associativity |
| --- | --- | --- |
| Unary `+ - ~` | Positive, negate, bitwise complement | Right to left |
| Binary `* / %` | Multiply, divide, remainder | Left to right |
| Binary `+ -` | Add, subtract | Left to right |
| Binary `< >` | Less than, greater than | Left to right |

There are no increment or decrement operators. Interpret consecutive signs according to their unary or binary positions. For example, `-~1` means `-(~1)` , and `3<2<1` means `(3<2)<1` .

Every value is a signed 32-bit integer in $[-2^{31},2^{31}-1]$ . Reduce the mathematical result of addition, subtraction, multiplication, or unary negation modulo $2^{32}$ , then interpret it as two's complement. Bitwise complement flips all 32 bits.

Division truncates toward zero. The remainder satisfies $a\bmod b=a-\operatorname{trunc}(a/b)b$ , and is zero or has the dividend's sign. The result of $-2^{31}/(-1)$ also wraps to $-2^{31}$ ; its remainder is zero. Comparisons use signed values and return $0$ or $1$ .

All operands are evaluated. If any division or remainder has a zero divisor, print `Runtime Error` . Otherwise, print the final integer.

## Input

One line contains one expression without spaces. There is exactly one expression in the input.

## Output

Print one line containing the result or `Runtime Error` .

## Examples

### Example 1

### Input

```text
--~~-~(5)+++--(3*(6+7)*4)*2/(2+2)+(1>(((2))))
```

### Output

```text
84
```

### Example 2

### Input

```text
3<2<1
```

### Output

```text
1
```

### Example 3

### Input

```text
9*9*9*9*9*9*9*9*9*9*9
```

### Output

```text
1316288537
```

### Example 4

### Input

```text
5/(7-6-1)
```

### Output

```text
Runtime Error
```

## Example Explanation

Sample 1 evaluates to 84. Sample 2 first evaluates `3<2` to 0, then `0<1` to 1. Sample 3 retains the low 32 bits of $9^{11}$ , obtaining 1316288537. Sample 4 has a zero divisor.

![Two steps of a left-associative comparison](assets/expression.svg)

The result of a comparison can be an operand of the next comparison.

## Constraints and Guarantees

The expression has length $\ell$ , where $1\le\ell\le100000$ . Its syntax is valid. There is no additional bound on parenthesis or unary-operator nesting depth.

Specifications redesigned by Codex (GPT-6): 32-bit wrapping, signed division and remainder, and division of the minimum signed value by minus one are explicit.

| Score | Additional conditions |
| --- | --- |
| 20% | $\ell\le30$ |
| 30% | $\ell\le1000$ |
| 50% | No additional conditions |
