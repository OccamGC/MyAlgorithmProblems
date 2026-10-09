# Danjin's Canisters — Solution

Credits: the implicit splay tree with run counts is the problem setter’s solution. Codex (GPT-6) contributed interval positioning, tag propagation and the run-count merge proof.

## Comparing solutions

### Problem setter’s solution: an implicit splay tree with run counts

The problem setter’s program uses an implicit splay tree with a sentinel at each end. Every subtree stores its size, first and last types, and number of consecutive runs. Merging subtracts duplicate runs at equal-type boundaries. Assigning a whole segment makes its run count one; reversal swaps children and boundary types without changing the run count. Both operations use lazy tags.

Assignments, reversals and queries isolate a segment with two splays. A move removes the corresponding subtree, searches by rank for an insertion gap in the remaining sequence, attaches the subtree and splays it. Ranks refer to the sequence after removal, which defines the insertion position unambiguously. The inorder, run-count and tag invariants and proofs below explain both implementations.

Both initialize in linear time and use a constant number of splay, split or join operations per request. Total amortized time is $O(n+m\log(n+1))$ , with $O(n)$ space.

### Implementation details

The Codex implementation also isolates insertion gaps through their two boundaries, sharing one positioning method between range operations and moves. The splay routine explicitly collects ancestors and pushes their tags, reducing its dependence on callers having done so. Node relationships use array indices, and the explanation includes the merge proof and boundary cases.

Range operations and moves share boundary positioning, and the splay routine handles ancestor-tag propagation. These implementation choices keep the invariants in one place without changing the asymptotic bounds.

## Maintain consecutive runs

For a segment, store its length, first type, last type and run count. Joining two nonempty sequences $A,B$ can merge runs only at their boundary:

$$\operatorname{runs}(AB)=\operatorname{runs}(A)+\operatorname{runs}(B)-[\operatorname{last}(A)=\operatorname{first}(B)]$$

An empty sequence contributes zero runs; its sentinel value must not participate in equality tests. Merge the left subtree, current element and right subtree in order to maintain each subtree's statistics.

## Assignment and reversal

Assigning a nonempty segment to $v$ makes both boundary types equal to $v$ and sets its run count to $1$ , without changing length.

Reversing a segment preserves its run count while exchanging its first and last types and its left and right children. An assignment tag stores the new type not yet propagated to children; a reversal tag stores a pending order reversal. Since these concern type and order, they can coexist. Propagate assignment before reversal, consistently with the reference representation.

Push relevant ancestor tags before finding a position by subtree size or performing rotations; otherwise child direction or boundary types may be stale.

## Isolate and move a segment

Add two sentinel elements outside the sequence. Maintain the sequence as the splay tree's inorder traversal, locating positions by subtree size.

To isolate $[l,r]$ , splay its preceding element to the root and its following element to the root's right child. That child's left subtree is exactly the requested segment. Apply assignments, reversals or queries to this subtree, then update the two ancestors.

For a move, first isolate and detach the segment of length $\mathrm{len}$ . The tree now contains only the remaining sequence and the sentinels. In **this shortened tree**, isolate the empty gap after its first $\mathrm{nl}-1$ real elements and attach the removed subtree there. Its internal order is unchanged, and it occupies exactly the requested final positions.

Even removing the entire sequence leaves both sentinels, so gap insertion remains defined. A single element, either insertion endpoint and reinsertion at the original position need no special rule.

## Correctness and complexity

The inorder sequence always matches the current canister sequence. Isolation changes tree shape without changing inorder order. Range updates change exactly the requested types or order; moving uses positions after removal, and the merge identity preserves statistics. Each query therefore returns the correct number of runs.

Build an initially balanced tree in linear time. Each operation uses a constant number of splay, split or join operations, giving $O(n+m\log(n+1))$ total amortized time and $O(n)$ space. Initialization recursion has only $O(\log(n+1))$ depth; operation-time propagation uses an explicit stack.

See Sleator and Tarjan's [Self-Adjusting Binary Search Trees](https://www.cs.cmu.edu/~sleator/papers/Self-Adjusting.htm) for the amortized analysis. Run statistics and lazy tags add only constant work per visited node.

## Validation

An independent array model applies all operations using slices and counts neighboring unequal types directly. Tests cover whole-sequence moves, repeated reversals, moves after assignment, single elements, matching boundary types and insertion at the end.

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.
