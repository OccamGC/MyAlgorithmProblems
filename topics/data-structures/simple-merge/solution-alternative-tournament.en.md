# Simple Merge: Tournament Tree

Codex (GPT-6) applies the established tournament-tree technique to this multiway merge. Program: [alternative-tournament.cpp](alternative-tournament.cpp). See the [main editorial](solution.en.md) for the heap algorithm and shared model.

## Selection with fixed leaves

Orient every sequence in nondecreasing order. Build a complete binary tree whose real leaves store the current sequence heads and their indices. Pad to the smallest power of two at least $k$ . Padded leaves and exhausted sequences use an infinite sentinel.

Each internal node stores the smaller of its two children's entries. The root is the smallest sequence head. Print the winner, advance its sequence pointer, update that leaf, and recompute minima along its path to the root.

## Correctness

Leaves represent the current candidates correctly. Induction on tree height shows that each internal node holds the minimum of all leaves below it, so the root is the minimum head. Changing one leaf affects only its ancestor chain; recomputing that chain restores the property. The head argument in the main editorial then proves every removal is correct.

## Complexity and applicability

Let $S=\sum s_i$ . Input and initialization take $O(S+k)$ time; each removal takes $O(\log(k+1))$ . Space is $O(S+k)$ . When $k=1$ , the root is itself a leaf and the ancestor-update loop is empty.

The tournament tree replaces a fixed leaf on each operation, whereas the heap uses the standard library directly. Both are valid throughout the constraints. Use a 64-bit sentinel greater than every legal input value, rather than reserving a legal value to mean an empty sequence. See the [main measurements](solution.en.md#verification-and-use) for timing applicability.
