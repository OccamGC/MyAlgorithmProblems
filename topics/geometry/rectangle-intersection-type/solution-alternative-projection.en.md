# Intersection Types: Symmetric Projections

The projection method appears in the problem setter's teaching notes. Codex (GPT-6): complete implementation, degenerate boundaries and dimension proof. This is a parallel option to the [top-edge method](solution.en.md), supporting the full data. Program: [alternative-projection.cpp](alternative-projection.cpp).

Represent the shapes as $[l_A,r_A]\times[b_A,t_A]$ and $[l_B,r_B]\times[b_B,t_B]$ . Define

$$L=\max(l_A,l_B),\quad R=\min(r_A,r_B)$$

$$D=\max(b_A,b_B),\quad U=\min(t_A,t_B)$$

Their intersection is $[L,R]\times[D,U]$ . If $L>R$ or $D>U$ , one interval is empty, making the intersection empty; otherwise it is nonempty. A point belongs to both shapes exactly when each coordinate belongs to both corresponding closed intervals, proving the formula.

For a nonempty intersection, $L<R$ means positive horizontal length and $D<U$ means positive vertical length. Two true conditions give area, one gives a segment, and zero gives a point. The Boolean task only needs emptiness; the classification task uses this dimension. A zero-length interval is not empty.

Each pair requires a constant number of comparisons, giving $O(1)$ time and $O(1)$ extra space, or $O(T+1)$ total time. The symmetric formula directly describes the intersection. It has no asymptotic time or space advantage over the top-edge method, and floating-point arithmetic is unnecessary.
