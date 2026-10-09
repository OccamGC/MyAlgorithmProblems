# Matrix Mixer: Index Permutations and a Transposition Flag

Codex (GPT-6): a representation by row and column permutations, with a clockwise-rotation rule and proof. [alternative.cpp](alternative.cpp) is a parallel option to [direct matrix maintenance](solution.en.md) and supports the full data.

## Representation and operations

Keep the initial matrix $G$ , row-index array $R$ , column-index array $S$ , and Boolean flag $b$ . Indices are zero-based. Initially both arrays are identity permutations and $b$ is false. The value at current position $(i,j)$ is

$$b=0:\quad G[R_i][S_j],\qquad b=1:\quad G[S_j][R_i]$$

To swap rows, swap two entries of $R$ ; to swap columns, swap two entries of $S$ . Validate arguments against the current array lengths.

For rotation, exchange the arrays, reverse the new column array, and flip $b$ :

$$R' = S,\qquad S' = \operatorname{reverse}(R),\qquad b'=1-b$$

The current row and column counts are exchanged automatically.

## Correctness

Initially the representation is exactly $G$ . Swapping row or column indices swaps exactly the corresponding full rows or columns. Under rotation, new position $(i,j)$ must contain old position $(n-1-j,i)$ . For $b=0$ , this is $G[R_{n-1-j}][S_i]$ . After the update, $b'=1$ and the new representation yields that same value. For $b=1$ , exchanging the coordinate roles proves the same result. Induction shows that the representation always matches the actual matrix.

## Cost

Index swaps take $O(1)$ time. Reversing an array during rotation takes at most $O(n+m)$ time, using the current dimensions. The extra index arrays use $O(n+m)$ space. The initial matrix uses $O(nm)$ space, with no second matrix for rotation. Every valid state must still be printed. Let $C=nm$ and let $V$ count valid operations; total time remains $O(C+K+VC)$ and total space remains $O(C)$ .

Direct matrix maintenance follows the statement more closely. Index maintenance requires care with the meaning of the two arrays under transposition. These bounds include output and do not claim an asymptotic overall speedup from the representation alone.
