# Time Management and Team Sports — Solution

## Method and contribution

Use the problem setter's exponential weight encoding and KM weighted-matching approach. Codex (GPT-6) supplies a directly justified positional encoding, a Hungarian implementation retaining its alternating tree, portable fixed-width arithmetic and verification. KM, the Hungarian algorithm and their duality argument are classical methods.

## Encode the histogram exactly

Choose a base $B>n$ ; the program uses $B=512=2^9$ . Give grade $g$ weight $B^g$ . A perfect matching then has weight
$$
\sum_{g=0}^{70}c_gB^g.
$$
Every digit is at most $n<B$ , so there are no carries. At the highest differing grade $g$ , one unit of $B^g$ exceeds every possible difference in lower digits. Maximizing the exact weight is therefore equivalent to maximizing the required histogram lexicographically. Simply summing grades would not give this priority.

The figure shows an optimal assignment for sample three, with grades $70,69,70$ .

![An optimal matching between slots and contests](assets/example.svg)

Set the minimization cost to $C_{ij}=-B^{a_{ij}}$ .

## Alternating trees and dual potentials

Maintain row potentials $u_i$ and column potentials $v_j$ satisfying
$$
u_i+v_j\le C_{ij}
$$
for all rows already introduced. The slack is $C_{ij}-u_i-v_j$ . Every matched edge has zero slack and is called tight.

Introduce one new row and grow an alternating tree: travel from rows to columns on tight edges and from matched columns to their matched rows. Each column outside the tree stores its minimum slack from a tree row and the corresponding predecessor.

If no zero-slack column can extend the tree, take the smallest stored slack $\Delta$ . Add $\Delta$ to potentials of tree rows, subtract it from potentials of tree columns, and reduce stored slacks outside the tree by $\Delta$ . Sums within the tree stay unchanged. Edges leaving the tree remain feasible, while edges entering it only gain slack. At least one additional column becomes reachable on a tight edge.

A newly introduced row starts with potential zero and is not yet required to be feasible. Its first adjustment, involving only that row and the dummy column zero, may have negative $\Delta$ and makes the row feasible. Later adjustments are nonnegative. Upon reaching a free column, reverse the matching along the predecessor path. The matching grows by one and its edges remain tight.

At completion, every perfect matching costs at least $\sum_i u_i+\sum_j v_j$ . The current perfect matching attains this bound because all its edges are tight. It is therefore minimum-cost, and the positional encoding gives the required optimal histogram.

## Preserve the search state

One augmentation adds at most $n$ columns to the alternating tree. Each addition scans a row and updates linearly many potentials and slacks, requiring $O(n^2)$ wide-integer operations. Restarting a DFS after each potential adjustment may rescan the same edges; retaining the tree and column slacks gives $O(n^3)$ operations overall.

## Portable wide integers

Let $G$ be the number of grades, seventy-one here, and $W$ the machine-word width, sixty-four in the implementation. The required bit length is $O(G\log B+\log(n+1))$ ; let $L$ be the corresponding number of words. The program uses twelve unsigned 64-bit words, or 768 bits, with two's-complement addition, subtraction and signed comparison. Overflow within an individual unsigned word follows standard C++ rules. Each weight is a single bit at position $9g$ , so no wide multiplication is needed.

The largest weight is $H=B^{70}=2^{630}$ , and all costs lie in $[-H,-1]$ . Real column potentials start at zero and only decrease. Before an augmentation finishes, a free column still has potential zero, so dual feasibility keeps real row potentials negative. Tight matched edges, together with a new row starting at no less than $-H$ , bound real row and column potentials in $[-H,0]$ . Finite slacks are only a constant multiple of $H$ . The dummy column accumulates a value of magnitude at most $nH<2^{639}$ . Infinity uses bit740 and the sign uses bit767, leaving ample room.

Store the grade matrix and only $G$ wide costs instead of a full wide-cost matrix. Time is $O(n^3L)$ and space is $O(n^2+(n+G)L)$ . When $n=0$ , all output counts are zero.

[Reference program](std.cpp). A matching and its potentials form an independently checkable certificate: use arbitrary-precision integers to verify the bijection, every dual inequality, equality on every matched edge and the resulting histogram. No independent repetition of the matching search is required.

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables are kept outside the published package. See the [reference measurements](../../../docs/benchmark-R28.json) for runtime and memory.
