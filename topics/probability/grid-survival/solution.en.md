# Survival on a Grid: Solution

Problem setter’s solution: count safe paths with rolling DP, then divide once by the number of equally likely processes. Codex (GPT-6) supplies flat storage, portable C++17 modular multiplication without overflow, and the sparse-road alternative.

## Count first and normalize last

Let $D_t(x,y)$ count processes that start at any road cell, take $t$ steps, remain safe, and end at $(x,y)$ . Initially a road cell has value one and a pit has value zero. A road cell's next value is the sum of the previous values of its four neighbors. Pits and positions outside the grid always contribute zero.

Every nonempty safe process has a unique final step. Removing it gives a safe process ending at a neighbor; conversely, each such neighbor process extends uniquely to the current road cell. Thus the recurrence neither omits nor duplicates a process. By induction, $A=\sum_{x,y}D_k(x,y)$ is the number of safe processes. All start-and-direction strings are equally likely, giving probability $A/(nm\cdot4^k)$ .

Store just two consecutive rounds. Overwrite every road value on each round, while both layers remain zero at pits. Use the grid character to recognize roads: a current count of zero does not make a cell a permanent obstacle.

## Numeric bounds and modular arithmetic

For a fixed endpoint, each reversed direction string determines at most one starting cell. Hence $D_t(x,y)\le4^t\le2^{50}$ . Every exact cell count fits 64-bit integers, so the inner recurrence needs no modular reductions. The total may exceed 64-bit range. Accumulate it modulo $P$ one cell at a time: the partial remainder is below $P$ and the next count at most $2^{50}$ , so each addition is safe.

The denominator is nonzero modulo $P$ because $1\le nm<P$ and $P$ is an odd prime. Fermat's little theorem gives the inverse as $q^{P-2}\bmod P$ . Direct multiplication of two residues can overflow. The program instead processes multiplier bits, using modular addition and doubling. Each addition is below $2P<2^{54}$ , so standard 64-bit integers suffice. Binary exponentiation uses this multiplication and needs no extended integer type.

## Complexity and parallel method

Let $B=\lceil\log_2 P\rceil$ be the modulus bit length. Reading and DP take $O(nm(k+1))$ time. Normalization takes $O(B^2)$ fixed-width integer operations, so total time is $O(nm(k+1)+B^2)$ with $O(nm)$ space.

[std.cpp](std.cpp) uses the setter's rolling grid DP. On grids with few roads, the [sparse-road method](solution-alternative.en.md) restricts each round to road cells and stores only their adjacency. It stores more information on a full grid, so it is a parallel method suited to different input shapes. Both programs cover the full range.
