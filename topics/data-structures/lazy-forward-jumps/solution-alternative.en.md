# Link-Cut-Tree Alternative

Codex (GPT-6): applies a standard link-cut tree to rooted paths from pads to the exit. This method does not depend on the batch guarantees, but exceeds the reference limit on the current full tests; see the [main comparison](solution.en.md).

## A rooted-tree model

Add an exit vertex. Give pad $i$ parent $i+K_i$ , or the exit if that target is out of bounds. Parent indices always increase, preventing cycles and ensuring that every vertex reaches the exit. A query asks for the number of edges on its path to the exit.

A link-cut tree maintains this rooted tree. An auxiliary splay tree's inorder sequence is a preferred path from ancestor to descendant. Store the number of vertices on that auxiliary path, excluding virtual subtrees. `Access(u)` exposes the path from the exit to $u$ in one auxiliary tree and splays $u$ to its root. The auxiliary size minus one is the required edge count.

To change a parent, first call `Access(u)` . Its left auxiliary subtree contains all ancestors. Detaching it cuts the logical edge from $u$ to its old parent while retaining the edges between ancestors. Set the path-parent pointer of $u$ to the new target. The target has a larger index and cannot be a descendant of $u$ , so linking it creates no cycle.

## Correctness and complexity

Initial parent edges exactly represent the jumps. A cut and link replace only the transition being updated. Thus the represented tree always matches the current jump rules. The exposed path's vertex count gives its edge count and therefore the exact number of jumps to the exit.

The exit is always the root, so no rerooting or path reversal is needed. Standard splay access amortization gives $O(\log n)$ per operation, $O(n+q\log(n+1))$ total time, and $O(n)$ space. Individual operations are not guaranteed logarithmic worst-case time. Initialization sets path-parent pointers directly with singleton auxiliary trees, taking linear time.

The [implementation](alternative.cpp) uses the same output modes and out-of-range query rule as the standard program. Measurements show the constant cost of its greater generality; its asymptotic bound does not imply that it is faster on these batched inputs.
