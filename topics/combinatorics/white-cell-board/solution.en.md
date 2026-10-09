# Solution: Boards with No All-Black Line

Problem setter’s solution: precompute the answers on the fixed domain and print them. Codex (GPT-6) verifies the table and supplies an inclusion-exclusion calculator and proof using mirror pairs of rows.

## Fixed answer table (primary)

There is no input, and the output is a fixed list of 21 residues. The [standard program](std.cpp) stores and prints that list. For maximum order $N$ , online time and table space are $O(N)$ ; here $N=20$ . Correctness also requires a derivation of the constants, rather than merely presenting a table.

The [inclusion-exclusion solution](solution-alternative.en.md) proves the formula. Its [calculator](alternative.cpp) regenerates every entry at runtime and agrees with the table. It also passes the full tests. The calculator makes the answers reproducible; the fixed table reduces online work. Both handle $n=0$ separately.

## A column-coverage dynamic program

Another calculation method of the problem setter fills the board row by row. A state set $S$ contains the columns that have not yet received a white cell. Choose a subset $U$ of those columns to receive white in this row, producing $S\setminus U$ . Columns already covered can be colored freely, except that the row must not be all black. If a diagonal is forced black, its cell in this row cannot be white.

Start with all columns in $S$ and finish at $S=\varnothing$ . Enumerating the legal row choices enforces all row and column requirements. Every board has a unique sequence of row choices, so it is counted once. Apply inclusion-exclusion to the two diagonals. Enumerating states and their subsets takes $O(n3^n)$ time and $O(2^n)$ space for one order. This supports small offline calculations, but is not an online reference solution for the complete domain. Grouping mirror pairs avoids this exponential enumeration.

Verification exhausts all boards through $n=4$ and compares all 21 constants with the calculator. See the [test recipes](tests/README.md) and [measurements](../../../docs/benchmark-R36.json).
