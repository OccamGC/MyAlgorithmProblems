# Magic Bread — Bidirectional palindromic trees

[The C++17 implementation](alternative-palindromic-tree.cpp) by Codex (GPT-6) maintain each level along suffix links. Extension is limited to one lap. Store the forward results by ring position and combine them during the reverse scan.

For suffix link $f$, let $B_f(j)$ be the greatest length on its chain repeating a palindromic block of length $j$. When the new length is $B_f(j)+j$, symmetry supplies the same block at the other end, so the whole palindrome qualifies. Otherwise inherit the suffix-link result. Time and space are $O(nK)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
