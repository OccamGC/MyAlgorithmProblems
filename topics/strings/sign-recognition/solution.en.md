# Sign Recognition — Solution

## Comparing solutions

The problem setter’s program inserts suffixes from right to left into a treap, comparing their first character and the order label of the following suffix. This is the recursive definition of suffix order. Rotations relabel the affected subtree using floating-point interval midpoints. After obtaining the suffix array and adjacent LCPs, each query scans left and right separately for every source string, finds shared prefixes with other sources, and excludes non-unique lengths. The counting argument is the one below.

Labels must remain strictly ordered; fixed-precision midpoints may coincide, which is a repairable numeric representation issue. After completing an insertion's rotations, the code may relabel an entire subtree, giving a conservative $O(S^2)$ worst-case construction bound. Query scans take $O(qnS)$ and space is $O(S)$ . The implementation used by Codex (GPT-6) uses integer ranks and comparison-sorting doubling, taking $O(S\log^2(S+1))$ to build. It precomputes shared lengths once per source, giving $O((n+q)S)$ scanning and query time, still with $O(S)$ space. The benefits are exact ranks, an explicit construction bound and removal of repeated source scans; suffix-array/LCP counting is inherited.

## Find the longest shared prefix at each start

Fix a starting position $x$ in string $s_i$ . Let $h_x$ be the maximum LCP length between this suffix and any suffix of a **different input string**. Use zero when there is no other string. Let $r_x$ be the number of characters remaining in $s_i$ from $x$ .

Every prefix of length at most $h_x$ appears elsewhere, while every longer prefix does not. The contribution to query $[L,R]$ is therefore

$$\max\bigl(0,\min(R,r_x)-\max(L,h_x+1)+1\bigr)$$

Sum over all starting positions. Do not deduplicate equal content within one string: the problem counts occurrences.

## Suffix array and adjacent LCP values

Concatenate the strings with distinct separators outside the lowercase alphabet. Record each position's source string and $r_x$ , setting $r_x=0$ for separators. Distinct separators prevent a common prefix between different suffixes from crossing an input-string boundary.

The reference builds `Suffix` by doubling. Rank single characters, then sort pairs of ranks for two blocks of length $w$ , doubling $w$ until all suffix ranks differ. It uses integer ranks and comparison sorting, with no floating-point order labels.

Compute adjacent LCP values with the linear scanning algorithm. Let $LCP[j]$ be the LCP of suffixes at positions $j-1$ and $j$ in suffix-array order. The LCP of any two suffixes is the minimum adjacent LCP between them: suffixes sharing a prefix occupy a contiguous lexicographic interval, and its minimum determines the common prefix length.

## Only the nearest different source on each side matters

For each source $i$ , scan the suffix array left to right. If the previous suffix belongs to another source, restart with the current adjacent LCP; otherwise, keep taking the minimum. For suffixes of source $i$ , this yields the LCP with the nearest suffix of another source to the left. Scan backward for the corresponding right-side value and take the maximum.

A farther candidate cannot improve the answer. Its LCP interval contains the interval to the nearest candidate, so its minimum cannot be larger. The two nearest candidates therefore determine $h_x$ . Separator suffixes can count as another source: their LCP with a letter-starting suffix is zero, so they introduce no false shared substring.

## Correctness and complexity

The scans find the longest prefix shared with another string at each start. The contribution formula retains exactly the query lengths that exceed that prefix and fit before the original string ends. Each start and length identifies one occurrence, so summation counts every valid occurrence exactly once.

Let $S$ be the sum of input lengths plus the number of separators. Comparison-sort doubling takes $O(S\log^2(S+1))$ time, LCP construction takes $O(S)$ , and source scans plus queries take $O((n+q)S)$ . Space is $O(S)$ . Use 64-bit integers for answers and query endpoints; very large length bounds are clipped naturally by the formula.

The independent oracle enumerates every position interval, records the source strings for each content, and counts occurrences directly. It covers identical strings, a single string, repeated characters, and very large query bounds.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
