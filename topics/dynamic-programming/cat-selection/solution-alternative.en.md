# Choosing Cats: Subset Search with Feasibility Pruning

Problem setter's subset search and pruning from the teaching notes. Codex (GPT-6): precomputed weights, portable 64-bit types and boundary validation. [alternative.cpp](alternative.cpp) is a backup to [dynamic programming](solution.en.md) and passes the current full data.

## Search state

Track the current zero-based position $p$ , the number already selected $j$ , and their contribution $s$ . If $j=k$ , update the best answer and return. If the remaining $n-p$ cats are fewer than $k-j$ , return. Otherwise branch:

- Select this position and enter $(p+1,j+1,s+v_p3^{k-j-1})$ .
- Skip it and enter $(p+1,j,s)$ .

Precompute powers of three. Initialize the answer below all valid scores, not to zero. For $k=0$ , the first base case immediately returns the empty score zero.

## Correctness and complexity

Each valid index set corresponds to one unique select-or-skip path. Positions increase monotonically, preserving the required order. A new selection is number $j+1$ , so its weight is $3^{k-j-1}$ . Once enough cats have been selected, all remaining positions must be skipped, allowing an immediate answer update. When too few positions remain, no valid completion exists. Neither pruning rule loses an optimal valid selection.

The binary decision tree has at most $O(2^n)$ nodes. After precomputing weights, each node does constant work. Total time is $O(2^n)$ ; the input, powers and recursion stack use $O(n+1)$ space. Negative and repeated scores do not affect enumeration. For larger $n$ , use polynomial-time DP. The runtime acceptance claim applies to the stated bounds and measured data.
