# Restocking the Holy Palanquin Ship's Confectionery: Solution

Problem setter’s solutions: pentagonal-number partition recurrence and nondecreasing purchase search. Codex (GPT-6) organizes the recurrence as a sparse sum, supplies modular handling, proofs and implementation, and adds complete knapsack.

## Group plans by total cost

Let $P_s$ be the number of unordered partitions of integer $s$ into positive parts, with $P_0=1$ . A plan costing $s\le X$ corresponds uniquely to such a partition: each part is an item's price. No part or multiplicity exceeds $X$ , so the stock limits exclude no partition.

$$A=\sum_{s=0}^{X}(X-s)P_s\pmod{998244353}$$

## Pentagonal recurrence

[Euler's pentagonal number theorem](https://dlmf.nist.gov/27.14#E4) and the partition generating function imply

$$P_0=1,\qquad P_s=\sum_{k\ge1}(-1)^{k+1}\left(P_{s-k(3k-1)/2}+P_{s-k(3k+1)/2}\right)$$

Values at negative indices are zero. To derive the formula, multiply the partition generating function by $\prod_{i\ge1}(1-z^i)$ , obtaining one. Expand the product with Euler's theorem, compare positive-degree coefficients, and rearrange. Increasing-cost evaluation therefore computes every count, after which the weighted sum gives the answer.

Enumerate only generalized pentagonal offsets no larger than the current cost. Each term uses an already-computed smaller index. Add the modulus before reducing a subtraction to keep residues nonnegative.

## Complexity and choice

There are $O(\sqrt X)$ relevant offsets per cost, giving $O(X\sqrt X)$ time and $O(X)$ space; zero budget needs constant work. Store weighted products in 64-bit integers. Their maximum after modular reduction is at most $80(998244353-1)$ .

[std.cpp](std.cpp) uses the sparse recurrence. Scanning every smaller index and ignoring zero coefficients gives the same recurrence in $O(X^2)$ time; sparse enumeration avoids these inactive terms.

Two further methods have complete explanations and programs:

- [Complete knapsack](solution-alternative-knapsack.en.md): $O(X^2)$ time and $O(X)$ space, with a direct proof that does not need Euler's theorem. It supports the full input range.
- [Nondecreasing search](solution-alternative-search.en.md): explicitly enumerates purchase plans using $O(X)$ space; its time grows with the number of partitions. It is retained as an enumeration alternative, with performance scope in its explanation. The problem bounds are unchanged.

This is an application of a classical partition identity; Euler's theorem is not an original contribution of this implementation.
