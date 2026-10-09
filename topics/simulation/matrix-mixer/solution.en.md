# Matrix Mixer: Direct Matrix Maintenance

Problem setter's solution: swap rows or columns and rotate into a temporary matrix using a coordinate map. Codex (GPT-6): standard C++17 implementation, boundary validation and a row/column-index alternative.

## Operations and correctness

First check swap arguments against the current row or column count. If either is invalid, print only the error line and leave the matrix unchanged.

Swap the two rows for a row operation. For a column operation, swap the corresponding entries in every row. With zero-based coordinates, clockwise rotation is

$$\mathrm{new}[j][n-1-i]=\mathrm{old}[i][j]$$

The new matrix has $m$ rows and $n$ columns. Fill an independent temporary matrix, then replace the current matrix and exchange its dimensions. This avoids overwriting cells that still need to be read.

Row and column swaps change exactly the specified positions. The rotation sends the upper-left corner to the new upper-right corner and turns the downward direction into the leftward direction. It maps all $nm$ cells bijectively, exactly implementing a clockwise rotation. Invalid operations preserve the state. Induction over operations therefore proves every printed state correct.

## Complexity

Let $C=nm$ be the number of cells, invariant under rotation, and let $V$ be the number of valid operations. Printing after each valid operation already needs $\Theta(C)$ value outputs. Including initialization and invalid operations, total time is $O(C+K+VC)$ and space is $O(C)$ , with another $O(C)$ temporary matrix for rotation. The implementation swaps whole row containers and performs column swaps row by row.

## Alternative and usage

[std.cpp](std.cpp) directly follows the operation definitions and remains preferred. The [index-based method](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), preserves the initial matrix and changes only row/column permutations and a transposition flag. It is a parallel option; both programs pass the full data. It reduces maintenance work, but printing every state remains necessary, so total complexity cannot be claimed below the output size.

Tests include thin grids, four consecutive rotations, maximum matrices, negative and zero arguments, changing dimensions, and state preservation after invalid operations. See the [test plan](tests/plan.json) and [measurements](../../../docs/评测环境与性能.md).
