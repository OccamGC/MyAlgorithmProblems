# String Functions in Contiguous Memory

**Problem setter's solution:** locate arrays by prefix sums, simulate contiguous memory, and validate before mutation. **Codex (GPT-6) contributions:** exploit binary-string structure to use a segment tree for first-zero queries and range assignments; provide the complexity proof, safe arithmetic, and tests.

## Addresses and error priority

Use length prefix sums to translate $(x,y)$ to global address $p_x+y$ . Calculate addresses and interval endpoints with 64-bit integers. First check whether every accessed interval lies in $[0,S)$ , then test copy overlap, and finally check each pointer against its named array.

A copy or length query needs the first zero at or after the source. If none exists, it necessarily overflows global memory. Both half-open copy intervals include the terminator; they overlap exactly when the larger start is smaller than the smaller end. Mutate only after all checks succeed. A zero-length write succeeds before any address check.

## Preferred: range assignment and first-zero search

Every byte is zero or one, so a valid string consists of a run of ones followed by zero. After finding its length $t$ , copying requires assigning one to the first $t$ destination bytes and zero to the next byte. Reading each source byte is unnecessary.

A segment tree stores each segment's zero count and a lazy assignment tag. To find the first zero at or after $p$ , skip nodes before $p$ or with zero zero-count, and search the left child first. Range assignment and first-zero search each take $O(\log(S+1))$ time.

## Correctness

Initially, the leaves represent memory exactly. Assignment updates both zero counts and lazy tags, and pushing a tag preserves the correct child contents. First-zero search visits addresses in increasing order and finds the earliest available zero, so the string length is correct.

Each operation checks every required interval in the specified error priority and leaves memory unchanged on rejection. A successful write applies its constant value; a successful copy writes a run of ones and a zero identical to the source string. Warnings are checked against the source and destination arrays separately. Thus every output and mutation is correct, and induction proves the complete sequence correct.

## Complexity and implementation

This implementation builds the tree by point assignments in $O(n+S\log(S+1))$ time. Each operation performs a constant number of queries or assignments, giving total time $O(n+(S+k)\log(S+1))$ and space $O(n+S)$ . Tree recursion has depth $O(\log(S+1))$ , independent of the number of operations.

The setter's prefix-sum and bytewise simulation is also valid. It is direct, uses smaller memory constants, and passes the current full data. See its [explanation](solution-alternative.en.md) and [program](alternative.cpp). The segment tree is preferred for its lower per-operation complexity; range assignment itself is an established technique.

## Implementation and validation

[Standard program](std.cpp), [generator](tests/generate.py), and [test recipes](tests/plan.json).

The slowest standard-program median in the reference environment is 0.042465 seconds, with peak working set 5.37 MiB, and calibrated limit 0.5 seconds. Each case has five independent timing runs.

See the [evaluation environment](../../../docs/评测环境与性能.md) and [individual timings and hashes](../../../docs/benchmark-R31.json). Measurements apply to that environment; recalibrate on another judge.
