# Integer Calculator

**Problem setter's solution:** convert infix to postfix with an operator stack, then evaluate with a value stack. **Codex (GPT-6) contributions:** explicit portable 32-bit wrapping, boundary validation, and correctness details.

## Infix to postfix

Track whether the next position expects an operand. The start, an opening parenthesis, or an operator expects one, so a sign there is unary. After a digit or a closing parenthesis, a sign is binary. Use distinct internal tokens for unary and binary signs.

Append digits directly to the postfix sequence. Push opening parentheses. A closing parenthesis pops operators until its matching opening parenthesis, which is discarded. Before pushing an operator, pop operators with higher precedence; at equal precedence, pop only if the incoming operator is left-associative. Finally, pop all remaining operators.

This places tighter subexpressions before their outer operations. At equal precedence, left associativity emits the left operation first, while right associativity delays it until the right operation has run. The postfix sequence therefore preserves the expression's syntax-tree order.

## Value stack and integer semantics

Push each digit. A unary operator pops one operand; a binary operator pops its right operand first and its left operand second. Push the result. In postfix order, each operation's children are already evaluated, so induction shows that every stack value is correct.

Store bit patterns in `uint32_t` . Addition, subtraction, and complement retain the low 32 bits; multiplication first uses `uint64_t` and is then truncated. For comparisons, division, and remainder, convert the pattern to a signed 64-bit value, subtracting $2^{32}$ when its top bit is set. Even minimum-signed-value divided by minus one is then safe in 64 bits before conversion back to the low 32 bits.

Report a zero divisor immediately. There are no short-circuit operators, so an error in any subexpression makes the entire expression erroneous. Early termination cannot discard a valid result. C++ signed overflow must not be used to implement wrapping; it does not supply the required semantics.

## Complexity and choice

Each character is pushed and popped at most once, giving $O(\ell)$ time and space. Both stages are iterative and handle deeply nested parentheses and unary chains. Evaluating as operators are popped is a fused form of the same stack algorithm. Recursive parsing needs separate protection against excessive depth. The setter's two-stage algorithm remains preferred; a change of organization alone does not warrant another implementation.

## Implementation and validation

[Standard program](std.cpp), [generator](tests/generate.py), and [test recipes](tests/plan.json).

The slowest standard-program median in the reference environment is 0.030337 seconds, with peak working set 5.52 MiB, and calibrated limit 0.5 seconds. Each case has five independent timing runs.

See the [evaluation environment](../../../docs/评测环境与性能.md) and [individual timings and hashes](../../../docs/benchmark-R31.json). Measurements apply to that environment; recalibrate on another judge.
