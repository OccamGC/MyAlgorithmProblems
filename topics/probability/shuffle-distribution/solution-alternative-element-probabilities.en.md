# Random Analysis: Element-Location Probabilities

Problem setter's element-location recurrence. Codex (GPT-6) supplies a C++17 implementation with rolling arrays and aggregates final probabilities by value into a matrix. Program: [alternative-element-probabilities.cpp](alternative-element-probabilities.cpp). See the [main editorial](solution.en.md) for the preferred method and comparison.

## Track one original element

Write $M=998244353$ .

Temporarily distinguish elements by original index, even when their values coincide. Fix the element initially at $s$ , and let $q_j$ be its current probability of occupying position $j$ . Initially $q_s=1$ and all other entries are zero.

In round $i$ , save $c=q_i$ . For $j\ne i$ , an element already at $j$ remains there with probability $(n-1)/n$ ; one at $i$ moves to $j$ with probability $1/n$ . These events are disjoint, giving

$$q'_j=(n-1)n^{-1}q_j+n^{-1}c\pmod M$$

Its probability of ending this round at position $i$ is

$$q'_i=n^{-1}\sum_jq_j=n^{-1}$$

because the element occupies exactly one position. The argument holds for every preceding state, so induction gives the correct final distribution.

## Form the answer

Write this distribution as $q_{s,j}$ . For each original element, add $q_{s,j}$ to entry $P_{j,a_s}$ . Exactly one element occupies position $j$ at the end, so the corresponding events are disjoint and probabilities from equal-valued elements add. Columns represent values, not original indices.

## Complexity and tradeoffs

Each original element runs $n$ rounds with $n$ updates, giving $O(n^3+\log M)$ time. Its distribution uses $O(n)$ rolling space. The output matrix uses $O(n^2)$ , so total space is $O(n^2)$ .

This method directly describes each element's destination and provides an independent comparison for faster recurrences. It is a correct backup; see the [main timing results](solution.en.md#measured-results). Always use the saved old $c$ within a round.
