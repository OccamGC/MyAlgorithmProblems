# Permuting Grilled Cuttlefish: Solution

Problem setter’s solution: decompose the permutation into cycles, factor their lengths, and retain maximum prime exponents. Codex (GPT-6) organizes the single-case interface, boundaries, proof, and C++17 implementation. The square-root trial-division cutoff also appears in the setter's accompanying explanation.

## The return count is an LCM

Every position has exactly one successor and one predecessor, so the permutation consists of disjoint cycles. On a cycle of length $\ell$ , each element moves forward one position per operation. Since elements are distinct, the whole cycle returns exactly after multiples of $\ell$ operations. The smallest positive simultaneous return count is therefore the least common multiple of all cycle lengths.

Start at each unvisited position and follow successors, counting vertices until reaching a visited position. The program marks a vertex by replacing its successor with zero. Save the successor before clearing it so traversal can continue. Each position is visited exactly once; a fixed point is a cycle of length one.

## Preserve prime information before taking a remainder

If $\ell=\prod p^{e_p}$ , the exponent of $p$ in the LCM is the maximum $e_p$ over all cycle lengths. Store these maxima in an array, then multiply in the required prime factors modulo $998244353$ . Taking remainders of lengths or intermediate LCMs before another LCM operation is invalid: a remainder does not preserve divisibility.

Trial division starts at two. Divide each candidate out completely and record its exponent. Stop when the remaining number is smaller than the candidate's square. A remaining value greater than one must be prime and contributes exponent one. Smaller prime factors have already been removed, so composite candidates cannot introduce spurious factors. The product of maximum prime powers is divisible by every cycle length and divides every common multiple, proving that it is the LCM. Reducing only this product gives the required answer.

## Complexity and choice

The cycle lengths sum to $N$ . Trial divisions and factor removals for a length $\ell$ have a conservative $O(\ell)$ bound, so all factorizations together take $O(N)$ time. Including cycle traversal and the exponent-array scan, total time and space are $O(N)$ . Even trial division scanning up to the remaining length has this linear aggregate bound; the square-root cutoff avoids unnecessary trials without changing that overall order.

Before multiplication, the answer is below the modulus and a factor is at most $N$ , so the product is below $10^{15}$ and fits 64-bit integers. When every cycle has length one, the product stays one, as required for a positive return count.

[std.cpp](std.cpp) implements this method. Direct simulation may depend on an enormous true answer. A smallest-prime-factor sieve adds preprocessing without improving the existing linear aggregate bound. Arbitrary-precision LCM is useful as an independent oracle, but is not an improvement to the fixed-width implementation.
