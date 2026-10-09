# Values Nearest to the Median — Alternative

**Codex (GPT-6) alternative: sorting and a two-sided merge.** Sort all values in ascending order. With zero-based indexing, twice the median is $T=b_{\lfloor(n-1)/2\rfloor}+b_{\lfloor n/2\rfloor}$ .

Start the right pointer at $\lfloor n/2\rfloor$ and the left pointer immediately before it. Moving left makes values smaller and their distance from the median nondecreasing. Moving right also makes distances nondecreasing. Each side is therefore already sorted by distance.

Compare the current candidates by $|2b_i-T|$ and choose the smaller distance. On a tie, choose the right candidate, whose value is at least the left candidate's. If a side is exhausted, take from the other. Repeating this $k$ times produces the first $k$ elements of the merge, proving both selection and tie-breaking correct.

Sorting takes $O(n\log n)$ time, followed by $O(k)$ merging. The array uses $O(n)$ space, with additional call-stack space depending on the sorting implementation. All arithmetic uses 64-bit integers.

This [program](alternative.cpp) provides a deterministic sorting bound and a clear two-sided ordered structure, and passes the full data. Its average asymptotic time is higher than the [preferred selection algorithm](solution.en.md); different organization alone does not imply greater speed.
