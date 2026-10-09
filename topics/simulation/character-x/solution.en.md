# Character X: Test Both Diagonal Strips

Problem setter's solutions: test each grid cell, or substitute into a fixed template supplied with the problem. Codex (GPT-6): standard C++17 implementations, explicit output dimensions and whitespace validation.

## Algorithm and proof

Enumerate rows $i=1,\ldots,8$ and columns $j=1,\ldots,10$ . Print the requested character if $j\in[i,i+2]$ or $j\in[9-i,11-i]$ ; otherwise print a space. End each row with a newline.

These closed intervals are exactly the two required diagonal strips. Logical OR takes their union, printing overlapping cells once. Every other cell becomes a space. Increasing row and column order visits every position exactly once in the required order.

## Complexity and implementation

Each pattern prints a fixed $80$ cells and $8$ newlines. Total time is $O(T+1)$ and extra space is $O(1)$ . Parenthesize each strip condition to make the AND/OR grouping clear.

Trailing spaces belong to the rectangle and must be preserved. Do not add blank lines between patterns. When $T=0$ , the loop is skipped and output is empty.

[std.cpp](std.cpp) directly implements the geometric definition and is preferred. The setter's [fixed-template solution](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) avoid reconstructing the pattern cell by cell, but apply to this fixed shape and size. Both programs pass all formal inputs; local timings largely include startup and output.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
