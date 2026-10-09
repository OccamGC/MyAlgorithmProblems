# Building a Big Star — Solution

## Comparing solutions

The problem setter’s solution stores unreduced symbols and completed star blocks in a doubly linked list. After inserting at one end, it repeatedly forms or merges blocks only at that end and updates the historical maximum. An insertion cannot affect the stable interior. Each block is created and removed only a constant number of times, so the local-reduction proof and amortized argument below also apply to the problem setter’s method.

The implementation used by Codex (GPT-6) replaces the hand-written list with a deque while retaining the block meanings and reduction order. This removes manual link and node-pool management. For initial length $n$ and $m$ operations, both use $O(n+m)$ total time and space. This is a container substitution within the same algorithm; actual speed was not compared.

## Idea

Compress every completed valid, nonempty segment into a neutral block, denoted by `N` (Neutral), retaining its actual length. `N` is only a block-type marker used by the algorithm, not an input character. Keep each unmatched left shell `<` or right shell `>` as a block of length $1$ . A spark `*` is itself a neutral block of length $1$ .

Repeatedly apply three local reductions to the block sequence:

1. Merge `N N` into one neutral block.
2. Merge `< >` into one neutral block.
3. Merge `< N >` into one neutral block.

The new length is the sum of the merged lengths. New marks are added only at the ends, while all old internal blocks are already irreducible. It is therefore enough to apply reductions repeatedly at the modified end. Store blocks in a deque and maintain the largest neutral-block length ever created. That length is the current longest valid segment.

## Correctness

Each reduction combines valid material into an equivalent neutral block and preserves its length. Once all reductions have been applied, adjacent neutral blocks have merged, and an unmatched shell cannot form a valid segment with neighboring blocks. Every valid contiguous substring must lie within a neutral block; otherwise it would cross an unmatched shell, contradicting irreducibility. Hence the longest valid segment has the length of the largest neutral block.

An insertion occurs only at one end. Previously internal blocks cannot acquire a new reduction unless it touches that end. Repeated local reductions therefore restore an irreducible block sequence after each insertion. The maintained answer is correct for the initial sequence and after every operation.

The program stores the largest neutral-block length ever created. This equals the current answer: insertions never remove an existing valid segment, and a merged neutral block only becomes part of a longer neutral block. The answer therefore cannot decrease. If there is no neutral block, the answer is $0$ .

## Complexity

Each input mark creates one block, and every reduction removes at least one block. There are $O(n+m)$ reductions in total, so time and space are both $O(n+m)$ .
