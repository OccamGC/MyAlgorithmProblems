# Interval Top Half

## Algorithm and attribution

Problem setter's solution: fix a left endpoint, extend the right endpoint, and maintain two sorted parts with heaps. Codex (GPT-6) organizes the implementation, states the size invariants and verifies boundary cases. Program: [std.cpp](std.cpp).

The [sliding-window algorithm](solution-alternative-sliding-window.en.md), with [source](alternative-sliding-window.cpp), is a parallel option: it outputs by length directly, reducing space from $O(n^2)$ to $O(n)$ with the same time bound. It requires ordered multisets supporting deletion. The reference keeps the problem setter's heap algorithm; both time/space choices remain available.

## Two-heap invariant

The lower part has $\lfloor L/2\rfloor$ elements and the upper part has $\lceil L/2\rceil$ . Use a max-heap for the lower part and a min-heap for the upper part. Every lower value must be at most every upper value. Store equal values with their multiplicities.

Insert the new value into the lower heap. If the upper heap needs one more element, move the lower maximum into it. If the lower maximum then exceeds the upper minimum, exchange those two boundary values.

The parts were ordered before insertion, so only the new element can violate the boundary. At most one exchange is needed. Maintain the sum of the upper heap: add any inserted value, and on an exchange add the incoming value minus the outgoing value.

## Correctness

Both heaps start empty. Inductively, insertion and adjustment preserve the required sizes and ordering. Thus the heaps contain precisely the two specified parts of the sorted interval. Their boundaries or maintained sum give the sum of the larger half.

Rebuild the heaps for each left endpoint and extend the right endpoint through every possible position. This visits every nonempty interval exactly once. Store answers indexed by length and left endpoint, then print in the required order.

## Complexity and numeric bounds

There are $n(n+1)/2$ extensions, each performing a constant number of heap operations. Time is $O(n^2\log(n+1))$ . The heaps use $O(n)$ space and the answer table uses $O(n^2)$ . Output alone requires $\Omega(n^2)$ time.

Let $U=\max_i\lvert a_i\rvert$ . The absolute answer is at most $\lceil n/2\rceil U$ , which can reach $5\times10^{11}$ here. Store sums in 64-bit integers. Negative values cannot be discarded; each interval has a fixed number of selected elements.

## Verification and Use

Every sequence of length at most six over a three-value alphabet is checked by sorting each interval, with additional random large and negative values. Formal data cover thousand-element monotone, constant and alternating-extreme sequences.

The ten input recipes, fixed seeds and purposes are in `tests/plan.json` . After compiling the program, run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs, or use `--case 01` to select one input. Independent checks are in [check_r15.py](../../../tools/check_r15.py). See the [five-round alternating measurements](../../../docs/benchmark-R15.json) and [environment](../../../docs/评测环境与性能.md). Finite tests and timings of these implementations supplement the proofs; they do not establish a time guarantee for every implementation with the same asymptotic bound.

## Measured Results

| Program | Largest per-case median | Peak working set |
| --- | ---: | ---: |
| Reference | 0.080116 s | 9.06 MiB |
| Alternative | 0.206423 s | 5.38 MiB |

The reference limit is 0.5 seconds. Both programs agree on all ten measured formal inputs and finish within this limit. Peak working set includes process overhead; maximum time and memory may come from different inputs.
