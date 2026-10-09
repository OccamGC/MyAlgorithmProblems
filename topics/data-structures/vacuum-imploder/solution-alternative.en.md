# Vacuum Imploder — Solution

> Peer method: affine matrices. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.


## Affine transformations

Every operation has the form $v'=Av+t$ , where $v=(x,y)^\mathsf{T}$ , $A$ is a $2\times2$ matrix, and $t$ is a translation vector. Translations use the identity matrix. The four reflection matrices, in operation order, are

$$\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
\begin{pmatrix}-1&0\\0&1\end{pmatrix},\quad
\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\begin{pmatrix}0&-1\\-1&0\end{pmatrix}$$

The counterclockwise rotation matrix is

$$\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$$

Applying $(A_1,t_1)$ first and $(A_2,t_2)$ second gives

$$(A_2A_1,\ A_2t_1+t_2)$$

Order matters. A later rotation or reflection also acts on the translation accumulated earlier.

## Segment tree

Build a segment tree over point IDs. Each node stores an affine transformation that has not yet been propagated. On full coverage, compose the new transformation after the existing tag. Before partial coverage or descent for a query, compose the parent tag after each child's tag, then reset the parent to the identity.

A leaf starts with its initial coordinates as its translation vector, representing the transformation of the origin into that point. After subsequent operations are composed, its translation is the current position. A point query pushes tags along its path; a final traversal prints all leaves in ID order.

## Correctness

The composition formula is exactly equivalent to applying two operations in sequence. Maintain the invariant that a node's tag contains the transformations, in time order, not yet applied to its descendants. Full coverage appends the new operation. Before partial coverage, pushing the older transformations preserves their order. Thus a queried leaf has received all relevant operations in input order and contains the correct position. The same argument applies to the final traversal.

## Precision and complexity

The reference stores six coefficients using `long double` and prints eight decimal places. Each range update or point query takes $O(\log n)$ ; building the tree and printing final coordinates take $O(n)$ . Total time is $O(n+m\log n)$ and space is $O(n)$ .

Compile the supplied `tests/checker.cpp` and invoke it as `checker input reference contestant` . It counts queries from the input and checks all coordinates, missing or extra output, and non-finite values. It uses absolute tolerance $0.05$ per coordinate with a $10^{-6}$ comparison rounding margin.
