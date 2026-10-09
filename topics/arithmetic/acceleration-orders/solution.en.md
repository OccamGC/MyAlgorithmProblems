# Acceleration Orders: Integer Half-Units

Problem setter's solution: evaluate $d=|at^2|/2$ directly. Codex (GPT-6): an equivalent integer representation, range proof and output boundaries. The formula is unchanged.

## Algorithm and correctness

Let $z=|a|t^2$ . Compute $z$ with a 64-bit integer. Print the integer quotient $z/2$ , followed by `.0` if $z$ is even or `.5` if it is odd.

Since $t^2\ge0$ , we have $|at^2|=|a|t^2=z$ . Halving an even integer has no fractional part; halving an odd integer has fractional part exactly $0.5$ . Thus the printed decimal is the exact formula value. If $a=0$ or $t=0$ , the output is `0.0` , without negative zero.

## Numeric bounds

From $|a|,|t|\le10^4$ , we obtain $0\le z\le10^{12}$ and a maximum answer of $5\cdot10^{11}$ . A 32-bit integer is insufficient. Use 64-bit arithmetic from the first multiplication; reading both inputs as `long long` avoids overflowing a 32-bit intermediate before assignment.

The setter's floating-point implementation is also valid here. Every integer product is at most $10^{12}<2^{53}$ and is exact in the usual IEEE 754 binary64 environment; division by two remains exact. The integer implementation separates the same result into its whole and half-unit parts.

## Complexity and validation

Each order takes $O(1)$ time and $O(1)$ extra space. Total time including input is $O(T+1)$ . An empty batch produces no output.

See [std.cpp](std.cpp). Direct floating-point evaluation, parity handling and integer scaling were considered; all are constant-time evaluations of the same formula, with no distinct better algorithm to publish. The [test plan](tests/plan.json) includes signed parameters, zeros, odd products, extreme absolute values and empty input batches. See the [measurements](../../../docs/评测环境与性能.md).
