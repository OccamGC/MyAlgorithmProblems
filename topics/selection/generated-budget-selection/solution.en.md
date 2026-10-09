# Budget Selection from a Generated Sequence

**Problem setter's solution:** take every nonpositive value, then partition positive values around random pivots and narrow the search using the smaller partition's sum. **Codex (GPT-6) contributions:** full-size dynamic storage, three-way partitioning, safe recurrence arithmetic, and a sorting alternative with proofs.

## Generation and nonpositive values

Evaluate the recurrence in 64 bits. Since the remainder's absolute value is below $|D|$ , each $|x_i|<2\times10^9$ , so generated values fit signed 32-bit storage. Intermediate products have absolute value below $2\times10^{18}$ , and the absolute sum of all values is below $4\times10^{16}$ , both fitting signed 64 bits.

Take every nonpositive value: this increases the count without increasing cost. Subtract their sum from the remaining budget. If the remaining budget is still negative, even the sum of all nonpositive values exceeds the original budget. That is the minimum attainable subset sum, so no feasible subset exists; print zero by convention.

Otherwise, only positive values remain. For any fixed count, the cheapest choice is that many smallest values. Replacing a selected larger value with an unselected smaller value cannot increase cost. Thus an optimal answer can always be a prefix of the sorted values.

## Random three-way partition

Choose pivot $v$ among the remaining positive values. Partition into values smaller than, equal to, and larger than $v$ , recording the smaller partition's sum $s$ .

- If $s>L$ , the desired prefix ends inside the smaller partition; discard the other two and continue there.
- If $s\le L$ , take the entire smaller partition and subtract its cost. Among the $c$ equal values, take $\min(c,\lfloor L/v\rfloor)$ .
- If not all equal values were taken, the maximal prefix is complete. Otherwise, continue in the larger partition.

Three-way partitioning consumes duplicate values together. Nonpositive values have already been handled, so division by $v$ is safe.

## Correctness and complexity

The exchange argument reduces the problem to finding the cheapest prefix. Each branch either restricts the search to the smaller partition containing the endpoint or irrevocably consumes the complete smaller partition and affordable equal values. This preserves the answer and remaining-budget invariant. When the range is exhausted or the equal partition is unaffordable, no cheaper additional value exists, so the selected count is maximal.

Uniform random pivots give expected linear selection time. Including generation, time is expected $O(n)$ and space is $O(n)$ ; worst-case time is $O(n^2)$ . The program uses a fixed pseudorandom seed for reproducibility, which does not give a worst-case linear guarantee for arbitrary inputs. Its index distribution covers the full range, rather than treating a small-range `rand()` result as a uniform large-array index.

The [sorted-prefix alternative](solution-alternative.en.md), with its [program](alternative.cpp), has deterministic $O(n\log n)$ time and a direct sorted representation. It exceeds the estimated limit on full stress data in the reference environment, so it serves as a backup and output cross-check. The standard program uses the setter's partition algorithm.

## Implementation and validation

[Standard program](std.cpp), [generator](tests/generate.py), and [test recipes](tests/plan.json).

The slowest standard-program median in the reference environment is 0.258953 seconds, with peak working set 81.48 MiB, and calibrated limit 1.0 seconds. Each case has five independent timing runs.

See the [evaluation environment](../../../docs/评测环境与性能.md) and [individual timings and hashes](../../../docs/benchmark-R31.json). Measurements apply to that environment; recalibrate on another judge.
