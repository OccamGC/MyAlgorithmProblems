# Optimal Binary Search Tree: Alternative solution

## Full root enumeration: the setter's solution

For every nonempty interval, [alternative.cpp](alternative.cpp) examines every root $k\in[l,r]$ and minimizes $D(l,k-1)+D(k+1,r)+W(l,r)$ . Empty intervals cost zero and singletons cost their frequencies. Process intervals by increasing length; prefix sums provide $W$ in constant time.

Scan roots in ascending order and update only for a strictly lower cost. The smallest root survives a tie. Root-left-right reconstruction applies the same rule independently at every subtree and therefore yields the smallest preorder; see the [main editorial](solution.en.md) for its proof and explicit-stack reconstruction. Every legal tree's root and subtrees are considered, proving optimality.

Time is $O(n^3)$ and space $O(n^2)$ . This method needs no root-monotonicity property, making its recurrence and tie rules easy to inspect. It passes the full data; the reference Knuth algorithm reduces time to quadratic. Codex (GPT-6) retained the setter's enumeration and root choice, with input-sized arrays and iterative output.
