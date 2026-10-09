# Side-Scrolling Field Theory: Solution

Problem setter’s solution: determine the sign from the facing direction and maintain the holder with modular arithmetic. Codex (GPT-6) refines input handling, modular boundaries, and the correctness explanation.

## Convert relative directions

Use a zero-based holder index $c$ internally, and reindex the facing and label arrays in the same way. A student facing away has their right toward increasing indices. A student facing the observer has their left toward increasing indices. Thus indices increase exactly when $d\ne f_c$ .

Set $r=p\bmod N$ . An increasing move becomes $c\leftarrow(c+r)\bmod N$ ; a decreasing move becomes $c\leftarrow(c-r+N)\bmod N$ . Since $0\le c,r<N$ , the latter dividend is nonnegative. Print the new label, and use the new holder's facing direction for the next operation.

A complete lap returns to the same student, so reducing the step count preserves the destination. The sign rule matches both possible facing directions. Starting with student one, induction on the operations shows that the stored index is always the true holder; every output is therefore correct.

## Complexity and alternatives

Reading the students takes $O(N)$ time, and each operation takes $O(1)$ . Total time is $O(N+M)$ and space is $O(N)$ . Zero steps, complete laps, and a one-student row need no special cases.

Step-by-step simulation takes $O(N+\sum p)$ time and is useful as a small-case oracle, but has no space advantage. Walking through a doubly linked list has the same drawback. Precomputing direction signs is only another representation of this formula, so it is not a separate algorithm. See [std.cpp](std.cpp).
