# Optimal Binary Search Tree: Solution

## Methods and contributions

The problem setter used interval dynamic programming over every root, choosing the smaller root on equal costs. Codex (GPT-6) applied Knuth's optimal-search-tree optimization and iterative preorder reconstruction. [std.cpp](std.cpp) is the reference. Full root enumeration remains in [alternative.cpp](alternative.cpp) with its [editorial](solution-alternative.en.md); it supports the entire problem range.

## Setter's solution: interval DP

Every subtree of a search tree occupies a consecutive identifier interval. Let $D(l,r)$ be its minimum cost when its own root has depth one; an empty interval costs zero. Let $W(l,r)=\sum_{i=l}^r f_i$ . Choosing root $k$ increases every subtree depth by one, hence

$$D(l,r)=W(l,r)+\min_{l\le k\le r}\{D(l,k-1)+D(k+1,r)\}$$

Process intervals by increasing length. Every legal tree has a unique root, and both of its subtrees must be independently optimal. Thus the recurrence covers all possibilities and cannot miss a cheaper tree.

Define $R(l,r)$ as the smallest minimizing root. Preorder prints the root first, so a smaller root wins any cost tie. With that root fixed, choose the smallest preorder in the left subtree and then in the right. Induction gives the lexicographically smallest global answer, including zero frequencies.

## Knuth optimization

Nonnegative interval sums are monotone under containment and satisfy the quadrangle equality. Optimal search tree roots obey

$$R(l,r-1)\le R(l,r)\le R(l+1,r)$$

Only roots between those bounds need examination. This classical result is due to [Knuth, Optimum binary search trees (1971)](https://doi.org/10.1007/BF00264289); unsuccessful-search frequencies are zero in this application.

Smallest-root ties can be used consistently. The DP costs satisfy the quadrangle inequality: extending the right endpoint cannot make a smaller, strictly inferior root catch up with or beat the selected root. The symmetric argument prevents a leftward move when removing the left endpoint. With all frequencies zero, $R(l,r)=l$ , which also satisfies the bounds. Scan roots in ascending order and update only for a strict improvement.

For a fixed interval length, candidate-range widths telescope through differences of neighbouring roots, giving $O(n)$ candidates in total. Across all lengths, time is $O(n^2)$ . The cost table, root table and prefix sums occupy $O(n^2)$ space. Full enumeration uses $O(n^3)$ time and $O(n^2)$ space.

## Reconstruction and implementation

Print $D(1,n)$ . A stack stores pending intervals: print the root and push the right interval before the left interval. Popping then visits root, left, right. Skip empty intervals. This avoids recursion depth issues for chain-shaped answers caused by zero frequencies.

Use 64-bit costs and prefix sums. Any tree costs at most $n^2\max_i f_i\le2.5\times10^{14}$ , safely within signed 64-bit range. Store roots as integer identifiers. Integer lexicographic order must not be replaced by decimal-string order.

## Data generation and validation

Run the Python 3 standard-library script `tests/generate.py --out-dir <directory>` to generate inputs from [plan.json](tests/plan.json). Repeat `--case` to select identifiers; pass `--std <executable>` to generate outputs as well. Compile the desired source as C++17 first. Fixed recipes and seeds reproduce the inputs. Store large generated data outside the problem directory.

[Measurements](../../../docs/benchmark-R30.json) record input and source hashes, five timings per case, and peak working set. All delivered variants pass the full test set. 226 small inputs enumerate all search-tree shapes and independently compare weighted depths and integer preorders. Every official input is cross-checked against full root enumeration.
