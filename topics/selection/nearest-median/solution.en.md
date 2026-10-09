# Values Nearest to the Median

**Problem setter's solution:** select the median, then select the first $k$ values ordered by distance and value. **Codex (GPT-6) contributions:** store values in place, use safe 64-bit arithmetic, add sorting-and-merging, and validate both methods.

## Two selections

Let $T=2m$ . For odd size, this is twice the middle value; for even size, it is the sum of the two middle values. Use `nth_element` at zero-based index $\lfloor n/2\rfloor$ . For even size, the maximum of the preceding partition is the other middle value.

Compare values first by $|2a_i-T|$ , then prefer larger $a_i$ . This is exactly the order of $|a_i-m|$ with the specified tie break, without floating-point arithmetic.

Run selection again with this comparator, putting the required elements in the first $k$ positions, and sum them. If $k=n$ , simply sum everything without a second selection.

## Correctness

The first selection's partition property gives the correct middle rank. For even size, the left partition's maximum is the lower middle value, so $T$ is correct. Multiplying all distances by positive two preserves their order, and the second comparison key is precisely the required tie break. The second selection therefore yields the required multiset in its first $k$ positions. Equal values may appear in any order without affecting the sum, which is the required output.

## Complexity and arithmetic

Standard-library selection is linear on average, so the complete method has average time $O(n)$ . The input array occupies $O(n)$ space; auxiliary space depends on the library's selection implementation. This program does not allocate another distance array. The average linear guarantee of `nth_element` is not a worst-case linear guarantee.

Use 64-bit integers for $T$ , distances, and the sum. A doubled distance can approach $4\times10^9$ , while the answer's absolute value is below $10^{15}$ , both fitting 64 bits.

[Sorting and merging outward from the middle](solution-alternative.en.md) gives deterministic $O(n\log n)$ time and a direct ordered structure; see its [program](alternative.cpp). Both programs pass the current full recipes. The setter's average-linear algorithm remains preferred.

## Implementation and validation

[Standard program](std.cpp), [generator](tests/generate.py), and [test recipes](tests/plan.json).

The slowest standard-program median in the reference environment is 0.115108 seconds, with peak working set 12.81 MiB, and calibrated limit 0.5 seconds. Each case has five independent timing runs.

See the [evaluation environment](../../../docs/评测环境与性能.md) and [individual timings and hashes](../../../docs/benchmark-R31.json). Measurements apply to that environment; recalibrate on another judge.
