# Equipment Amplification Editorial

**Problem setter’s solution: decimal zero-one encoding, a fixed-width prefix table, and a partial-block scan.** Codex (GPT-6) organizes the C++17 implementation, handles the final block, and supplies a table generator that prunes invalid low digits. The query algorithm is preserved.

## 1. Encode the candidate integers

A binary digit is zero or one, so every decimal digit of a successful value must also be zero or one. Let $D$ be the maximum decimal digit count; here $D=30$ . Interpret such a decimal digit string as a binary mask $M$ . Its decimal value is

$$S(M)=\sum_{i=0}^{D-1}M_i10^i$$

The success condition becomes

$$S(M)\mathbin{\&}M=M$$

Only the low $D$ binary bits of $S(M)$ matter: higher decimal digits are all zero. The implementation evaluates powers of ten and sums with unsigned 32-bit integers. Defined reduction modulo $2^{32}$ preserves every required bit. Signed overflow must not be used.

Ordering decimal zero-one strings is equivalent to ordering their masks. To find the largest candidate mask $B$ whose decimal value is at most $N$ , scan from the most significant digit. Copy zeros and ones. At the first digit greater than one, replace it and every following digit by one. That position already makes the result strictly smaller than $N$ , and all-one suffixes maximize the candidate. If there is no such digit, convert directly.

## 2. Prefix table and queries

Choose a block width $L$ . Store $C_t$ , the number of successful masks at most $tL$ , and a final entry for the end of the universe. For an upper bound $B$ , start with $C_{\lfloor B/L\rfloor}$ and enumerate the masks after that boundary up to $B$ , evaluating the success condition.

If consecutive table entries are equal, the block contains no successful masks and can be skipped. The zero mask is already counted by $C_0=1$ and must not be counted again. The final entry corresponds to $2^D-1$ and handles the incomplete last block.

This implementation uses $L=160000$ and 6712 table entries, including the full-domain count 715704. Compile `std.cpp` with `prefix-table.hpp` present. For a judge accepting a single source file, inline the table into the source. The 50 KB limit applies to the submitted program, excluding generation and validation tools.

## 3. Reproduce the prefix table

The problem setter’s direct table-generation method enumerates all $2^D$ masks and checks each in $O(D)$ time.

The supplied `tests/generate-table.cpp` prunes earlier using the same condition. Choose decimal digits from low to high. Once position $i$ has been chosen, every future term $10^j$ with $j>i$ is divisible by $2^{i+1}$ and cannot alter binary bit $i$ . If choosing one produces a zero binary bit at that position, stop the branch. Choosing zero imposes no condition.

Every successful mask is generated exactly once. Every retained prefix can be extended by an all-zero suffix into a successful mask. With $K$ successful masks, the search visits $O(DK)$ states. Sort the masks and scan them to produce the same prefix table. Total time is $O(DK+K\log K+2^D/L)$ and space is $O(K+D+2^D/L)$ . This improvement concerns table generation.

Compile the generator and save its stdout as `prefix-table.hpp` to rebuild the supplied table. It uses no randomness; all overflowing arithmetic is unsigned and defined by C++.

## Correctness and complexity

The encoding covers all possible successful integers and preserves their order. The prefix table and final scan partition all masks $M\le B$ without overlap. Each mask is tested by the equivalent bit condition, so the count is correct.

With the precomputed table, $q$ queries take $O(qDL)$ time and $O(2^D/L+D)$ runtime space. Offline generation costs are given above. This method avoids generating every successful value at each startup and fits the source-size and query-count limits; it is not claimed to be fastest for every parameter choice.

## Data and validation

`tests/generate.py` accepts `--out-dir` , `--case` , and `--std` . Cases cover zero, the maximum integer, decimal zero-one strings, block boundaries, and random bounds. The small-instance oracle enumerates integers and directly compares the digits of both representations; the full table is checked entry by entry. See [environment and measurements](../../../docs/评测环境与性能.md).
