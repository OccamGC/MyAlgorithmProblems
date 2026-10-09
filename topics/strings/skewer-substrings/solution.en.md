# Skewer Substrings: KMP Inside Each Interval

Problem setter's solution: extract the query interval, repeatedly search for the pattern, and advance the next starting position by one. Codex (GPT-6): an application of the established KMP algorithm, a linear per-query bound and a proof for overlapping occurrences.

## Preferred solution

Build the prefix function $\pi$ for the current pattern $t$ . The value $\pi_i$ is the length of the longest proper prefix of $t_0\ldots t_i$ that is also its suffix.

Scan from $S_{l-1}$ through $S_{r-1}$ using zero-based indices. Maintain matched length $j$ , initially zero. On a mismatch with $t_j$ , fall back to $j\gets\pi_{j-1}$ . On a match, increase $j$ . When $j=|t|$ , count an occurrence and set $j\gets\pi_{j-1}$ before continuing.

After a complete match, return to the longest proper border instead of zero to preserve overlaps. For example, `aaa` has three starting positions in `aaaaa` . Each query starts with zero matched characters and scans only its own interval, excluding occurrences that extend across a boundary.

## Correctness

The prefix-function chain lists all possible shorter borders. After a mismatch, a previously matched suffix can remain the prefix of a new occurrence only if its length lies on this chain. Following the chain cannot omit a candidate. Extending on a matching character preserves this property. Reaching the pattern length identifies a complete occurrence; falling back to the longest proper border retains all possible overlapping continuations.

Every occurrence is counted exactly when its last character is read. Distinct ending positions correspond to distinct starting positions. Starting at the interval's left endpoint and stopping at its right endpoint counts exactly the occurrences fully contained within it.

## Complexity and comparison

Let $q=r-l+1$ and $L=|t|$ . Building the prefix function takes $O(L)$ time. The matched length increases at most $q$ times, and decreases can be charged to prior increases, giving $O(q)$ scanning time. A query takes $O(q+L)$ time and $O(L)$ extra space beyond storing $S$ . For $N=|S|$ and maximum pattern length $L_{\max}$ , total time is $O(N+M(N+L_{\max}))$ and space is $O(N+L_{\max})$ .

See [std.cpp](std.cpp). [Searching successive starts](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), retains the setter's concise string-library method as a backup and also passes the full data. Character-by-character analysis gives an $O(qL)$ query bound; constants and observed speed depend on the library. KMP is preferred for its explicit linear worst-case bound, not an assumption that measured library runtime equals its worst case.

The [test plan](tests/plan.json) covers overlaps, long patterns, late mismatches, periodic strings, interval boundaries and absent patterns. See the [measurements](../../../docs/评测环境与性能.md).
