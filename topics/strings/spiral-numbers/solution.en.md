# Spiral Numbers: Solution

Problem setter’s solution: skip leading zeroes and compare opposite digits. Codex (GPT-6) refines boundary handling and implementation and adds arithmetic reversal.

## Two pointers

Advance the left endpoint past leading zeroes while leaving at least one digit. An all-zero input becomes one zero, and every other input becomes its usual decimal representation. Compare the characters at both endpoints and move inward when they agree. A mismatch immediately means the number is not a palindrome.

The already-checked outer digit pairs are equal, while unchecked digits form a contiguous interval. A mismatch violates the definition. Otherwise, when at most one digit remains, every symmetric pair has been checked. The algorithm therefore recognizes exactly the required palindromes.

## Complexity and choice

Let $L$ be the input string length for one case. Time is $O(L)$ . Storing the input requires $O(L)$ space, and the additional state uses $O(1)$ space. Cases are processed sequentially, so total time is the sum of their lengths.

The preferred [std.cpp](std.cpp) follows the digit definition directly and does not rely on the range of a machine integer. [Arithmetic reversal](solution-alternative.en.md) uses a fixed number of integers within this problem's bounds. Both methods support the full input range.
