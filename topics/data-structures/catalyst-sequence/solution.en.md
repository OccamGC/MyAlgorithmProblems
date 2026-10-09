# Catalyst Sequence Editorial

**Problem setter’s solution: split by minimum gap, with sliding windows and an eight-way bit tree.** Codex (GPT-6) provides the proof organization and C++17 implementation, including explicit singleton and zero-gap handling. The core algorithm is preserved.

## 1. Large gaps imply short intervals

Let $U=\max a_i$ and $T=\lfloor\sqrt U\rfloor+1$ . An interval with minimum gap greater than $T$ contains distinct values. After sorting them, consecutive values differ by at least $T+1$ , so its length is at most

$$1+\left\lfloor\frac{U-1}{T+1}\right\rfloor$$

For every left endpoint, extend the interval to the right while maintaining its minimum gap. Stop as soon as the gap becomes at most $T$ . Each start therefore processes $O(U/T+1)$ elements.

When inserting $x$ into an ordered set, only its predecessor and successor can create a new minimum gap. If $x$ already exists, the new gap is zero. Record the actual gap of every interval of length at least two, including the interval that first crosses the threshold.

For each right endpoint $r$ , also record the earliest start $L_{T+1}(r)$ satisfying the gap bound $T+1$ . For this auxiliary definition, a singleton satisfies every lower bound but cannot update the final answer.

## 2. Sliding windows for small gaps

For $d=T,T-1,\ldots,1$ , compute $L_d(r)$ from left to right: the earliest start of a window ending at $r$ whose pairwise differences are all at least $d$ .

Before inserting the new value, remove elements from the left while its distance to the current predecessor or successor is less than $d$ . Deletion cannot decrease any remaining pairwise distance, so this process finds the earliest valid start. Each pointer moves at most $n$ times.

We need a gap of **exactly** $d$ . Since $L_d(r)\le L_{d+1}(r)$ :

- If the inequality is strict, the window starting at $L_d(r)$ satisfies bound $d$ but fails bound $d+1$ . All values are integers, so its minimum gap is exactly $d$ . Update the answer with its length.
- If the starts are equal, the longest window already satisfies bound $d+1$ , as does every suffix. No interval ending at $r$ has minimum gap exactly $d$ .

Reuse one array, replacing $L_{T+1}$ by $L_T,L_{T-1},\ldots$ in order. A strictly earlier start also ensures that any recorded interval has at least two elements.

For gap zero, the answer is the whole sequence length if any value repeats, and zero otherwise.

## 3. Eight-way bit tree

Represent the integer universe by a complete eight-way tree. Each internal node has an eight-bit mask identifying its nonempty children; a separate array records present values. Insertions and deletions update masks along one path. A predecessor or successor search climbs to a suitable neighboring nonempty branch and then descends through its last or first nonempty children. Precompute the first and last set bit for every eight-bit mask.

Here $U\le250000$ , so $8^6$ leaves suffice. In general, the height and operation cost are $O(\log(U+1))$ , with $O(U)$ space. Windows for positive thresholds contain distinct values, so multiplicities are unnecessary.

## Correctness and complexity

The short-interval enumeration covers every gap greater than the threshold. The strict-start-change criterion covers every positive small gap, and the repeated-value check handles zero. Every recorded candidate corresponds to a real valid interval, so the maximum lengths are correct.

Time is $O(n(T+U/T+1)\log(U+1)+U)$ , or $O(n\sqrt U\log(U+1)+U)$ with the chosen threshold. Space is $O(n+U)$ .

`std.cpp` uses the eight-way bit tree. A balanced tree has the same asymptotic bound, but allocations and pointer accesses affect constants and should be measured on the target judge.

## Usage and validation

Compile `std.cpp` , then run `python tests/generate.py --out-dir <directory> --std <program>` . The plan covers singletons, duplicates, alternating values, spaced values, permutations, and random sequences. The independent small-instance checker enumerates every pair inside every interval. See [environment and measurements](../../../docs/评测环境与性能.md) for calibration.
