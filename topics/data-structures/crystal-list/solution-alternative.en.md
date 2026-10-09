# Crystal List — Solution

> Alternative: an ordered interval map. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.

Solution contribution: Codex (GPT-6) supplied an ordered interval map as an alternative, proved an amortized bound by counting deleted intervals and handled an empty list. The original uniform-tag segment tree has the same asymptotic bounds. Interval partitioning and balanced search trees are established methods.


## Partition by type

Store each interval's starting position and type in an ordered map, with a sentinel at $n+1$ . The difference between consecutive starting positions is the preceding interval's length. Initially merge adjacent positions of the same type.

Partition by type, not energy. Distinct types with equal current energy may receive different future updates and must remain distinguishable.

Keep energies in a separate array $e_c$ . Operation 1 changes only this array; interval type identifiers remain unchanged.

## Perform a replacement

Split existing intervals at $r+1$ and $l$ , so that the replaced range consists exactly of complete map entries. Splitting changes no position's type.

For each covered interval of length $t$ and type $a$ , add

$$t\cdot|e_a-e_c|$$

Then erase all covered entries and insert one interval starting at $l$ with type $c$ . Perform the replacement even if its score is zero. The implementation does not require adjacent equal-type intervals to be merged again: they still describe the sequence correctly and satisfy the bound below.

## Bound the total traversal

Initially there are at most $n$ intervals. A replacement splits at most two endpoint intervals and inserts at most one replacement interval. Only $O(n+m)$ map entries are therefore created over the whole execution.

Every entry traversed for scoring is immediately erased. The same map entry cannot be traversed and erased again, so all such work totals $O(n+m)$ , independent of input randomness. One replacement may take linear time, but the complete sequence has an amortized guarantee.

Build the initial map in increasing order with correct insertion hints in $O(n)$ time. Each replacement additionally performs a constant number of $O(\log(n+2))$ searches and insertions; range erasure costs the search overhead plus the number of erased entries. Total time is $O(n+k+m\log(n+2))$ and space is $O(n+k)$ .

A score is at most $49999n$ and needs 64-bit storage. When $n=0$ , only the sentinel exists and valid input contains no replacements. When $k=0$ , there are no energy updates either.

## Correctness and validation

Each interval represents equal-type positions, and the energy lookup gives their current energy. Interval contributions equal position-by-position contributions; splitting and replacement exactly implement the operation. An independent array model covers different types with equal energy, zero-score replacements, later energy changes, single-position ranges, empty instances and long ranges.

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.
