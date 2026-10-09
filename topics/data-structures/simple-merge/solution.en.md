# Simple Merge

## Algorithm and attribution

Problem setter's solution: orient each sequence in nondecreasing order and maintain one head per nonempty sequence in a heap. Codex (GPT-6) provides the standard C++17 implementation and verifies duplicates and zero-operation cases. Program: [std.cpp](std.cpp).

The [tournament-tree alternative](solution-alternative-tournament.en.md), with [source](alternative-tournament.cpp), maintains the same candidate set using fixed leaves and minimum winners. The algorithms have the same overall asymptotic bounds. The heap remains preferred; the tournament tree provides a different update structure.

## One head represents each sequence

Let $S=\sum s_i$ . Reverse a sequence if its first element is greater than its last. Otherwise it is already nondecreasing; monotonicity implies that equal endpoints mean every value in the sequence is equal.

The smallest remaining element of each nonempty sequence is at its current head. Hence the global minimum is among these heads.

Insert every head into a min-heap together with its sequence index. Pop and print the minimum, advance that sequence's pointer, and insert its next head if one remains.

## Correctness

Initially, the heap contains exactly one head from each nonempty sequence. If this invariant holds before an operation, its minimum is the global minimum. Removing it changes only one sequence's head. Inserting that sequence's next head restores the invariant. Induction proves every output.

Repeated values retain all their occurrences. The sequence index only breaks ties and does not change the printed value. If $m=0$ , no heap removals are needed after reading the input. If $m=S$ , all elements are removed exactly once.

## Complexity

Reading and normalization take $O(S)$ time. This implementation inserts initial heads one at a time, so heap operations take $O((k+m)\log(k+1))$ . Total time is $O(S+(k+m)\log(k+1))$ , with $O(S+k)$ space for input and heap storage.

The tournament tree builds in $O(k)$ time and updates one leaf in $O(\log(k+1))$ , for total time $O(S+k+m\log(k+1))$ and the same $O(S+k)$ space. Since $k\le S$ , their overall asymptotic bounds agree. Actual timings are reported below.

## Verification and Use

An independent model flattens and sorts all values. It covers mixed monotone directions, duplicates, no removals and removing every element.

The ten input recipes, fixed seeds and purposes are in `tests/plan.json` . After compiling the program, run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs, or use `--case 01` to select one input. Independent checks are in [check_r15.py](../../../tools/check_r15.py). See the [five-round alternating measurements](../../../docs/benchmark-R15.json) and [environment](../../../docs/评测环境与性能.md). Finite tests and timings of these implementations supplement the proofs; they do not establish a time guarantee for every implementation with the same asymptotic bound.

## Measured Results

| Program | Largest per-case median | Peak working set |
| --- | ---: | ---: |
| Reference | 0.176663 s | 9.00 MiB |
| Alternative | 0.159656 s | 9.01 MiB |

The reference limit is 0.5 seconds. Both programs agree on all ten measured formal inputs and finish within this limit. Peak working set includes process overhead; maximum time and memory may come from different inputs.
