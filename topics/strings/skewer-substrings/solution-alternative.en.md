# Skewer Substrings: Searching Successive Starts

Problem setter's solution: extract the interval and repeatedly call `string::find` . Codex (GPT-6): C++17 formatting and boundary validation, preserving overlap handling. [alternative.cpp](alternative.cpp) is a backup to [KMP](solution.en.md) and passes the full data.

Extract $U=S_{l-1}\ldots S_{r-1}$ . Call `U.find(t, pos)` starting from zero. If it returns position $p$ , increase the answer and continue from $p+1$ . Stop when it returns `string::npos` .

Each search returns the earliest occurrence at or after the requested position. Strictly increasing this position prevents duplicate counting and never skips an earlier uncounted occurrence. Advancing by one permits overlaps. Advancing by $|t|$ would miss one of the two occurrences of `aa` in `aaa` . Extracting the interval first ensures that every complete returned match lies within the query boundaries.

Let $q=|U|$ and $L=|t|$ . In the model comparing at most $L$ characters at each candidate start, the total comparisons are $O(qL)$ . Extracting the interval costs $O(q)$ , which is included because $L\ge1$ . Query temporary space is $O(q+L)$ , or $O(|S|+L)$ including the original string. A library may perform better; this analysis does not rely on an additional linear-time library guarantee.

This method expresses “find every occurrence” directly through a library operation and is useful for learning and validation. KMP explicitly reuses matched prefixes and provides a stronger worst-case time bound.
