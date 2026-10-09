# Counting End-Position Classes with a Suffix Automaton

Codex (GPT-6): application of suffix-automaton end-position classes, counting, implementation, and verification. This applies an established string algorithm; the automaton itself is not attributed to the model. [alternative.cpp](alternative.cpp) is provided alongside the [primary suffix-array method](solution.en.md).

## Construction and Counts

Extend a suffix automaton one character at a time. A state $v$ represents substrings sharing the same set of ending positions, with lengths exactly

$$\operatorname{len}(\operatorname{link}(v))+1,\ldots,\operatorname{len}(v).$$

Give each newly created terminal state a count of one. A clone only splits an equivalence class and starts at zero. Counting-sort states by length, then propagate counts from longer states to their suffix-link parents. The resulting count is the occurrence count of every substring represented by that state, including overlapping occurrences.

Each noninitial state contributes $\operatorname{len}(v)-\operatorname{len}(\operatorname{link}(v))$ distinct substrings. Add the same contribution to $U$ exactly when the occurrence count is one. Summing gives $D,U$ .

## Correctness

All strings represented by a state have the same ending positions and thus the same occurrence count. Every distinct substring corresponds to exactly one state and one allowed length, so summing length intervals neither omits nor duplicates strings. Each prefix marks its endpoint once; suffix-link propagation sends this contribution to all suffix classes ending there. This counts all ending positions exactly. Selecting count-one states therefore selects precisely the unique substrings.

The expectation is $ND/U$ . Fraction reduction and noninvertible denominators follow the proof in the primary solution and are implemented in [expectation.hpp](expectation.hpp). The full 94-character alphabet is supported.

## Cost and Applicability

There are at most $2n$ states, each with 94 transitions. Time is $O(94n+Q+\log P)$ and space is $O(94n)$ ; for a fixed alphabet, construction is linear in $n$ . This method classifies occurrences directly without suffix sorting or LCPs, at the cost of more memory for dense transitions. It passes all formal inputs and independent small counts within 128 MiB and the current time limit. See the [primary solution](solution.en.md) for measurements.
