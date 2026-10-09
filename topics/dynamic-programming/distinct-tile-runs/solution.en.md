# Partitioning Tiles with Distinct Runs: Solution

Contribution: Codex (GPT-6) developed the finite-state formulation, proof, word-parallel transitions and standard C++17 implementation for this problem. Finite-state dynamic programming is a classical technique.

## Aggregate identical tiles

Sort acquisition records by type and number, then sum counts with equal keys. Types are independent because no group mixes them. Aggregated counts can reach $5\times10^{15}$ , so use sixty-four-bit integers for counts and sorting keys.

A remaining count $c$ can be partitioned into identical triples and quadruples exactly when $c\ge0$ and $c\notin\{1,2,5\}$ . Zero, three and four are immediate. Six, seven and eight are three plus three, three plus four, and four plus four. Every larger integer reduces to one of these by subtracting threes; one, two and five are impossible.

## Six bits describe unfinished runs

Process one type in increasing number order. At most one length-three run and one length-five run may start at each number. Before processing number $i$ , remember whether runs started at:

- $i-1,i-2$ for length three;
- $i-1,i-2,i-3,i-4$ for length five.

These six booleans give $64$ states. If $h(s)$ is the number of set bits of state $s$ , the already open runs require exactly $h(s)$ tiles of the current number.

Choose $u,v\in\{0,1\}$ , indicating a new length-three and length-five run. With current count $c$ , the remainder

$$c-h(s)-u-v$$

must satisfy the identical-group condition. Shift both histories, append $u,v$ , and discard their oldest bits. Encoding the length-three history in the upper two bits and the length-five history in the lower four gives

$$s'=16\bigl((2\lfloor s/16\rfloor+u)\bmod4\bigr)+\bigl(2(s\bmod16)+v\bigr)\bmod16.$$

Initially only empty state zero is possible. At the end of a type, zero must remain possible; otherwise some runs still need future tiles. A gap between occurring numbers has zero tiles, so no unfinished run can cross it. Check for the empty state and reset at a gap instead of scanning absent numbers. Apply the same check when changing types.

![A valid five-tile run and two forbidden copies of one three-tile run](assets/explanation.svg)

Each tuple $(b,c,\ell)$ denotes type, starting number and length. The five different numbers form a length-five run. The two identical length-three runs below cannot both be used.

## Represent the entire state set in one integer

Bit $s$ of an unsigned sixty-four-bit word represents feasibility of state $s$ . At most $6+2=8$ current tiles are required by runs. When $c\ge14$ , every remainder is at least six and therefore feasible. Only count classes $0,\ldots,14$ are needed; larger counts use class fourteen.

Precompute masks $H[c][t]$ selecting states for which $c-h(s)-t$ can form identical groups, where $t=u+v\in\{0,1,2\}$ . Let $P(X)$ shift the histories without starting a new run, merging equal destination states. Then

$$X'=P(X\mathbin{\&}H[c][0])\mathbin{|}\bigl(P(X\mathbin{\&}H[c][1])\ll1\bigr)\mathbin{|}\bigl(P(X\mathbin{\&}H[c][1])\ll16\bigr)\mathbin{|}\bigl(P(X\mathbin{\&}H[c][2])\ll17\bigr).$$

Bitwise OR takes the union of feasible states. To compute $P$ , forget bits three and five of the state index: OR the set with its eight-bit right shift, then OR that result with its thirty-two-bit right shift. Extract the eight-bit sections at positions zero through seven and sixteen through twenty-three. A $256$-entry table expands bit $j$ of each section to bit $2j$ ; shift the expanded upper section left by thirty-two. The two new-run positions remain zero and are filled by the displayed formula. All shifts use unsigned integers, and no destination exceeds bit sixty-three.

## Correctness

Inductively, the state set describes exactly all valid groupings before the current number and their unfinished runs. Every valid partition determines the required old runs and the new choices $u,v$ . Its other tiles must, and can, form identical groups precisely under the remainder test. Thus every valid continuation is considered. Conversely, a transition supplies every open run, uses each start-and-length marker at most once, and records exactly the remaining future requirements. Finishing in state zero is equivalent to completing every run. Since types do not interact, all types are feasible exactly when the complete input is feasible. The word-parallel implementation only merges equal destination states and preserves this recurrence.

## Complexity and choice of method

Let $d\le k$ be the number of distinct aggregated keys. Sorting takes $O(k\log k)$ time, and the DP takes $O(d)$ time. Space is $O(k)$ . Five million sixteen-byte records use about eighty million bytes; sorting is in place. Avoid retaining another equally large record array.

Explicit iteration over sixty-four states implements the same recurrence and is useful for checking. Word-parallel transitions remove the per-number state loop. General matrices or graph search offer no additional advantage here.

Reference program: [std.cpp](std.cpp). Checks include independent enumeration of run subsets, every single-state transition and full-size explicit-state DP. See the [data plan](tests/plan.json), [generator](tests/generate.py) and [measurements](../../../docs/benchmark-R26.json).
