# Lexicographically Largest Heap Labels — Ancestor-Set Sorting

Codex (GPT-6) contributes the ancestor-set characterization, correctness proof and implementation using classical persistent segment trees. This is a complete derivation of [alternative.cpp](alternative.cpp). The setter's $O(N\log N)$ interval allocation remains preferred; see the [main solution](solution.en.md).

## Why Assign a Whole Subtree the Largest Labels?

Consider a remaining tree or forest with a consecutive available label interval $[L,R]$ . Let $x$ be its smallest-numbered vertex and let its current subtree have size $s$ .

Its $s-1$ descendants require larger labels, so $a_x\le R-s+1$ . This bound is attainable: give its entire subtree the largest $s$ labels, set $a_x=R-s+1$ , assign the descendants in any valid heap order, and use the smaller labels outside. Any ancestors of $x$ outside the subtree also correctly receive smaller labels.

Vertex $x$ is the next lexicographic priority, so an optimum must attain this bound. This forces its descendants to use all $s-1$ larger labels. The problem splits into the forest inside the subtree after removing $x$ , and the forest remaining after removing the whole subtree. Each has a fixed consecutive label interval and follows the same rule.

This establishes an upper bound, a construction attaining it, and independence of the recursive parts.

## Alternative: Static Sorting of Ancestor Sets

Define a length-$N$ binary key $B_v$ for vertex $v$ : bit $i$ is one exactly when vertex $i$ lies on the root-to-$v$ path. Sort vertices by decreasing lexicographic key, with one preceding zero, and assign labels $N,N-1,\ldots,1$ in that order.

A descendant's ancestor set strictly contains its ancestor's set, so its key and assigned label are larger. For optimality, apply the whole-subtree rule. In a currently undecided group, its smallest-numbered vertex $x$ gives the earliest bit that can distinguish the two parts. Exactly its subtree has that bit, placing all those vertices on the larger-label side. Recursing on each side with the next distinguishing number performs exactly the optimal block allocation. Thus static sorting yields the unique optimal label array.

Represent each key by a persistent segment tree instead of storing all $N$ bits. Vertex $v$ inherits its parent's version and inserts bit $v$ ; a zero pointer means an empty interval. Compare versions by descending left when left pointers differ, otherwise right, until reaching their first differing bit. The nonempty side is larger.

Pointer equality is exact here; there is no hashing. Two root paths share an initial segment and then add disjoint vertex numbers. For any number interval, if neither branch subsequently inserts a number in it, both retain the shared old pointer. If a branch does insert a number there, the sets differ because the other branch cannot insert the same vertex number. Comparing ancestor and descendant versions is the special case where one side inserts nothing further.

Building versions takes $O(N\log N)$ time and space. Each comparison costs $O(\log N)$ , giving $O(N\log^2 N)$ total sorting time. The mathematical description is uniform but incurs an extra sorting logarithm. Prefer the $O(N\log N)$ [std.cpp](std.cpp); [alternative.cpp](alternative.cpp) implements this distinct static approach in full.

## Cantor Rank and Implementation Boundaries

Scan vertex numbers from $N$ down to one. A second Fenwick tree stores labels already seen. Query the number $c_i$ strictly below $a_i$ and add $c_i(N-i)!$ . Maintain the factorial incrementally in this scan direction and accumulate separately for the two moduli. Neither primality nor modular inverses are needed.

This method takes $O(N\log^2 N)$ time and $O(N\log N)$ space. Traverse the original tree iteratively; persistent segment-tree recursion has depth $O(\log N)$ . Use sixty-four-bit modular products.
