# A Binary Search Tree with an Exact Shape — Solution

## Methods and Contributions

The setter's method searches the actual tree edge by edge, maintains duplicate counts, and deletes using the inorder successor. Codex (GPT-6) preserves those shape-changing operations and adds an ordered key-to-node index, giving logarithmic worst-case location costs. It also supplies iterative preorder traversal and safe parsing over the full integer range. Binary search trees, ordered maps and successor deletion are classical methods.


The diagram shows sample two before and after deleting four. Nodes show “key × multiplicity”. Both occurrences of five move to the root, and six replaces its original physical position.

![ Worked example ](assets/example.svg)

## Setter's Method: Direct Simulation

Store a key, multiplicity and two children per node. Insertion searches from the root, creates a node at an empty link, or increments the multiplicity of an equal key. Deletion likewise searches first and changes links only when the count reaches zero.

For a node with two children, enter its right child and repeatedly follow left children to find the inorder successor. Exchange the complete key and multiplicity, then delete the physical successor position. That position has no left child: such a child would be a smaller key in the right subtree, contradicting the successor choice. Its right child, if any, can therefore replace it.

The successor is larger than every key in the left subtree and smaller than every other key in the right subtree. Moving it to the target position preserves the search order. The old target key temporarily occupies only the position immediately removed. Multiplicity must move together with the key.

Preorder prints the root, then the left and right subtrees. Let $H$ be the total length of all search and successor-location walks, and $P$ the total number of nodes printed. Direct simulation takes $O(M+H+P)$ time, or $O(M^2+P)$ in the worst case, and $O(M)$ space. The qualitative access promise does not specify a numerical height bound and does not justify claiming logarithmic searches.

## Preferred Implementation: A Separate Ordered Index

The problem tree still stores parent, left child, right child, key and multiplicity, with exactly the prescribed shape changes. Separately, a `std::map` maps each key to its actual node number. Balancing this auxiliary map never changes the problem tree.

### Inserting a New Key

Find its inorder predecessor $p$ and successor $s$ in the index:

1. If $p$ exists and has no right child, attach the new node there.
2. Otherwise, if $s$ exists, attach it as the left child of $s$ .
3. If neither exists, it becomes the root.

This is exactly the empty link reached by an ordinary root search. There is no existing key between two adjacent inorder nodes. If the predecessor has no right child, keys in that gap search into its empty right link. Otherwise the successor is the leftmost node of the predecessor's right subtree; its left link is empty and is the destination. The same argument applies at the current minimum or maximum when one neighbor is absent.

### Deletion and Index Maintenance

Locate the target and reduce its count first. With two children, the next map iterator identifies the successor. Copy its key and multiplicity to the target position, redirect that key's index to the target, and remove the old physical successor. Erase the old target key's index entry. Copying and immediately removing is equivalent to the specified exchange followed by deletion.

Physical removal replaces the position by its only child, possibly empty, updating the relevant parent link or root. Also update the replacement child's parent when nonempty. Deleting an absent key creates neither an index entry nor a negative count.

### Printing and Integer Boundaries

Use an explicit stack, pushing the right child before the left so that the left is processed first. An empty tree emits a newline. Each live node appears once.

Accumulate an input magnitude in a sixty-four-bit integer, apply the sign, and then convert to the key type. Otherwise the magnitude of $-2^{31}$ overflows a signed thirty-two-bit accumulator before negation. Output also promotes to sixty-four bits before taking a negative value's magnitude.

## Correctness and Complexity

Induct on operations. The index maps every live key to its precise position. Insertion chooses the same unique empty link as a root search. Deletion performs the same count update, successor-data move and child transplant. Printing follows the same links. Thus all output agrees with direct simulation.

Each insertion or deletion uses a constant number of $O(\log(M+1))$ index operations and constant link changes. Printing costs $O(P)$ in total. Total time is $O(M\log(M+1)+P)$ and space is $O(M)$ . The index adds storage per live key in exchange for searches independent of the actual tree height, within the unchanged constraints. The [reference program](std.cpp) uses this method.
