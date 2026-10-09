# Roboport Network: Implicit Treap

Codex (GPT-6): an application of the established implicit treap data structure, representing circular positions by sequence rank, with implementation and proof.

Program: [alternative.cpp](alternative.cpp). This parallel option supports the full data; see the [linked ring](solution.en.md) for comparison.

## Representing a ring as a sequence

Cut the ring at any boundary and list active nodes in direction $0$ . Store the current node as a zero-based rank $q$ . The implicit treap's inorder sequence is this list. Subtree sizes support splitting, merging, and selection by rank. The cut does not change the circular order.

- Insertion: insert the new number after the first $q+1$ entries. Keep $q$ unchanged on a nonempty ring; set $q=0$ when inserting into an empty ring.
- Deletion: split out the one node at rank $q$ , discard it, and merge the two sides. For new size $s'>0$ , set $q\gets q\bmod s'$ to select the removed node's direction-$0$ successor. Set $q=0$ if empty.
- Movement: set $q\gets(q+x)\bmod s$ for direction $0$ , or $q\gets(q-x)\bmod s$ for direction $1$ , then normalize to a nonnegative remainder. Skip empty rings.
- Query: use left-subtree sizes to find the number at rank $q$ ; return `-1` for an empty tree.

## Correctness

Initially, the inorder sequence is $1,2,\ldots,n$ and the current rank is zero. Splitting and merging by rank preserve relative order, so insertion and deletion implement exactly the required circular neighbor changes. Removing the last linear entry wraps its rank to zero, crossing the cut correctly. Modular movement implements wraparound, and selection returns the node at the current rank. Induction therefore shows that the sequence and current position remain correct after every operation.

## Complexity and applicability

Let $M=n+m$ . Under the usual model of independent random priorities, expected tree height is $O(\log M)$ . Building by repeated merges takes expected $O(n\log M)$ time; insertion, deletion and queries take expected $O(\log M)$ time, while movement takes $O(1)$ . Total expected time is $O(M\log M)$ and node arrays use $O(M)$ space. Worst-case tree height and recursion depth can be $O(M)$ , so the logarithmic bound is not deterministic.

The implementation generates reproducible priorities with fixed-seed SplitMix64. This pseudorandom sequence does not guarantee worst-case balance against adversarial inputs. Priorities affect runtime only, never the answer. The program passes the measured full data; use the preferred solution when strict worst-case bounds are required. This option makes large movements independent of ring size, but insertion and deletion lose the linked ring's constant-time bound.
