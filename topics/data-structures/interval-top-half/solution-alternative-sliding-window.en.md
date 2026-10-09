# Interval Top Half: Sliding Windows by Length

Codex (GPT-6) applies two ordered multisets to sliding windows, allowing answers to be generated directly in output order. Program: [alternative-sliding-window.cpp](alternative-sliding-window.cpp). Compare it with the problem setter's heaps in the [main editorial](solution.en.md).

## Method

Process lengths $L$ in increasing order. Build the first window, then repeatedly remove its leftmost value and insert the new rightmost value. Two `multiset` containers hold the lower and upper parts. The lower part contains exactly $\lfloor L/2\rfloor$ elements, all at most every upper value.

Insert a new value into the lower part. Fix the sizes by moving its maximum or the upper minimum between parts; exchange boundary elements if they are out of order. For the first window, start with all values in the lower part and move the largest values upward. Later windows remove and insert only one occurrence, so a constant number of moves and exchanges restores the invariant.

Remove only one occurrence of a duplicate using an iterator. If the value occurs in both parts, deleting one copy from either part and rebalancing represents the same window multiset.

## Correctness and output

The first window has exactly the correct multiset. Removing the outgoing occurrence and inserting the incoming occurrence preserves that property for each next window. The size and ordering invariants identify the required parts of its sorted values. Maintain the upper sum during every insertion, removal and transfer. It is the required answer. Print windows from left to right for each length, then advance the length. No two-dimensional answer table is needed.

## Complexity and tradeoffs

For each length, initialization costs $O(L\log(L+1))$ and sliding costs $O((n-L)\log(L+1))$ . Total time is $O(n^2\log(n+1))$ , with $O(n)$ space. The program uses 64-bit values and sums.

This is a parallel option with the same time bound and less memory than the heap algorithm. Multiset allocation and deletion add constant costs, so a space improvement does not imply faster execution. It suits memory-sensitive use or direct output. See the [main measurements](solution.en.md#verification-and-use) for timing applicability.
