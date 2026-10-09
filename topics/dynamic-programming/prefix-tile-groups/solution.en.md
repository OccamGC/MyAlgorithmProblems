# Feasible Tile Partitions of Prefixes: Solution

Contribution: Codex (GPT-6) developed the canonical run-count proof, prefix states, transition tables and standard C++17 implementation. Finite-state DP and lookup tables are classical tools.

## At most two runs need start at each number

Three identical length-three runs use three tiles of each of three consecutive numbers. Replace them with three identical triples. Repeating this replacement leaves at most two runs at each starting number. It neither changes the tiles used nor affects a pair. Therefore a feasible partition always has such a canonical form.

![Three identical runs regrouped into three identical triples](assets/explanation.svg)

Both sides use exactly three tiles each of numbers one, two and three.

## Eighteen states

Before number $i$ , let $x,y\in\{0,1,2\}$ be the numbers of runs starting at $i-2,i-1$ . Let $p\in\{0,1\}$ indicate whether the unique pair has been used. Initially only $(0,0,0)$ is possible.

The current count is $c=a_i$ . Choose $q\in\{0,1\}$ to indicate a new pair here, with $p+q\le1$ . Choose $z\in\{0,1,2\}$ runs starting here. Existing runs need $x+y$ tiles, so require

$$c-x-y-z-2q\ge0,\qquad c-x-y-z-2q\equiv0\pmod3.$$

All remaining tiles form identical triples. For a fixed state and $q$ , the residue condition uniquely determines $z$ : it is the least nonnegative residue of $c-x-y-2q$ modulo three. The new state is $(y,z,p+q)$ .

After reading a number, feasibility of $(0,0,0)$ gives the first answer, and feasibility of $(0,0,1)$ gives the second. Both open-run counts must be zero; future tiles cannot complete the current prefix.

## Constant work per number

Use nine-bit masks $X_0,X_1$ for states without and with a pair, using bit index $3x+y$ . Precompute:

- $T_c[X]$ , the union of destinations when no new pair is placed;
- $U_c[X]$ , the union of destinations when a new pair is placed.

There are only $512$ masks $X$ . Since $x+y+z+2q\le8$ , counts $c\ge8$ matter only through their residue modulo three. The eleven classes use exact counts zero through seven and representatives eight, nine and ten. Update

$$X'_0=T_c[X_0],\qquad X'_1=T_c[X_1]\mathbin{|}U_c[X_0].$$

Compute both from the preceding masks. The lowest bit of each new mask gives its answer.

## Correctness

The canonical-form lemma preserves every feasible partition while limiting each start to two runs. The state records all information needed by later numbers: only runs from the preceding two starts remain open, and the pair requires only a used/not-used flag. A transition is feasible exactly when current tiles can complete their obligations, start the chosen runs, optionally form the pair, and leave a multiple of three for identical triples. Induction over numbers proves that the state set is exact. A prefix is feasible precisely when no run remains open and the pair flag has the required value. Lookup tables exhaustively implement this finite recurrence.

## Complexity and implementation

The two tables of eleven classes and nine-bit masks have fixed initialization cost and use about twenty-two thousand bytes. Total time is $O(n)$ and auxiliary space is $O(1)$ . Read and output incrementally without storing the sequence. Counts, state indices and remainders fit in thirty-two-bit integers.

Direct eighteen-state DP has the same formulation and verifies every formal prefix; changing its encoding is not presented as a separate solution. Independent small checks recursively take the smallest remaining number and try a run, an identical triple or the unique pair.

Reference: [std.cpp](std.cpp). See the [plan](tests/plan.json), [generator](tests/generate.py) and [measurements](../../../docs/benchmark-R26.json).
