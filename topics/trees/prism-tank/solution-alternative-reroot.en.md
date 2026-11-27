# Prism Tank — Rerooting DP

[The C++17 implementation](alternative-reroot.cpp) by Codex (GPT-6) defines a message from $u$ to $v$ as the optimum on the $u$ side after a hit from $v$. It depends only on messages from the other neighbors. Postorder and preorder compute both directions. Using all incoming values evaluates $u$ as a firing root.

Without blocking, subtract the excluded value from the sum and use the remaining count, giving $O(n)$ total time. With blocking, sort incoming values $x_0,\ldots,x_{d-1}$ in descending order. Let $S_k$ be the first-$k$ sum and $c_k=p+(1-p)/k$. After excluding index $j$, taking $k\le j$ neighbors gives $c_k S_k$, handled by prefix maxima including the empty choice. For $k>j$ the contribution is $c_k(S_{k+1}-x_j)$. Scanning $j$ backwards adds one line $y=c_k z+c_k S_{k+1}$ at a time and queries the maximum at $z=-x_j$. Insertions have nondecreasing slopes. An upper hull removes middle lines with out-of-order intersections, retains the larger intercept for equal slopes, and supports binary search. Total time with blocking is $O(n\log(n+1))$ and space is $O(n)$.

On formal input `maximum-random`, the median of three runs was 0.0277 s for this implementation and 0.0871 s for the reference. Separately measured peak process working sets were 5.02 and 5.38 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
