# A Binary Search Tree with an Exact Shape — Direct tree simulation

[The C++17 implementation](alternative-direct.cpp) by Codex (GPT-6) searches from the root, locates a successor down the left spine of the right subtree, and uses an explicit stack for printing.

Duplicate keys change only their count. With two children, move the successor key and its entire count before removing its original node. A chain gives worst-case $O(M^2+P)$ time for $M$ operations and $P$ printed vertices, with $O(M)$ space. This version directly exposes the prescribed tree shape.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
