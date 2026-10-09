# Counting Sublattices: Alternative Solution

## Direct enumeration for checking

The setter supplied the subset-enumeration approach. Codex (GPT-6) organized it as standard C++17 [brute.cpp](brute.cpp). The reference search is in the [main solution](solution.en.md).

Enumerate every mask from one through $2^n-1$ . For each pair of distinct included elements, check that both operation results are included. Reject if either is missing; otherwise count the set. Idempotence handles diagonal pairs automatically, and both operations are commutative, so each distinct pair need only be checked once.

Every nonempty subset appears once, and the test is exactly the definition of a sublattice, proving the count correct. Time is $O(n^2\cdot2^n)$ . Auxiliary space beyond the operation table is constant, giving $O(n^2)$ total space.

This program illustrates the definition and provides independent checks. It finished every formal input, with a largest median of about $0.777$ seconds and about $1.29$ times headroom under the $1$-second limit. This falls short of the reference solution's twofold calibration margin. It is not a full-range acceptance guarantee on the target judge; use the reference search or subset DP for production solving.
