# Psychic Commando Solution

## Comparing solutions

The problem setter’s method partitions rows into blocks. Each row has a lazy segment tree over columns. Each block additionally stores the aggregate of its rows' base values and column-range tags applied uniformly to the whole block. A rectangle operation uses block trees for complete blocks and handles rows individually in boundary blocks, updating the block aggregate as needed. A cell's base value plus its block tag is its actual value, so summing these disjoint pieces gives the rectangle sum.

For $H$ rows, $W$ columns and block length $B$ , an operation costs $O((H/B+B)\log(W+1))$ , with $O(HW)$ space. The implementation used by Codex (GPT-6) uses four two-dimensional Fenwick trees for weighted differences, giving $O(\log(H+1)\log(W+1))$ time per operation and the same $O(HW)$ space. It removes row-block enumeration but performs four weighted prefix computations. The expansion and proof follow below.

## Split each bombardment into rectangles

For $r=1$ , update one cell. For $r\ge2$ , the central rectangle is $[x-r+1,x+r-1]\times[y-r+1,y+r-1]$ , accompanied by four one-cell-wide fringe rectangles. For example, the left strip is $\{x-r\}\times[y-r+2,y+r-2]$ . These five pieces are disjoint and gain $p$ or $\lceil p/4\rceil$ .

Intersect every rectangle with the recorded region first. Skip an empty update or return zero for an empty query. Translate the intersection to local coordinates starting at $1$ . Using local coordinates in weighted sums avoids unnecessarily large products.

## Four two-dimensional Fenwick trees

Use translated local coordinates throughout. Let $A$ be the cell-value array, with row $0$ and column $0$ defined as zero. Its two-dimensional difference array is

$$D_{i,j}=A_{i,j}-A_{i-1,j}-A_{i,j-1}+A_{i-1,j-1}$$

Adding $\Delta$ to the closed rectangle $[x_1,x_2]\times[y_1,y_2]$ is equivalent to these four point updates:

| Difference position | Increment |
| --- | --- |
| $(x_1,y_1)$ | $\Delta$ |
| $(x_1,y_2+1)$ | $-\Delta$ |
| $(x_2+1,y_1)$ | $-\Delta$ |
| $(x_2+1,y_2+1)$ | $\Delta$ |

Difference positions outside the recorded region need not be stored. Let $S(x,y)$ be the sum of all cells in $[1,x]\times[1,y]$ , or zero if $x=0$ or $y=0$ . The difference value $D_{i,j}$ contributes to $(x-i+1)(y-j+1)$ cells within this prefix, giving

$$S(x,y)=\sum_{i\le x,j\le y}D_{i,j}(x-i+1)(y-j+1)$$

Expanding gives

$$S(x,y)=xy\sum D-y\sum(i-1)D-x\sum(j-1)D+\sum(i-1)(j-1)D$$

Each sum ranges over $1\le i\le x,1\le j\le y$ . Maintain the prefix sums of $D$ , $(i-1)D$ , $(j-1)D$ , and $(i-1)(j-1)D$ in four Fenwick trees. A difference-point update adds the corresponding weight to each tree.

The sum of an arbitrary closed rectangle is

$$S(x_2,y_2)-S(x_1-1,y_2)-S(x_2,y_1-1)+S(x_1-1,y_1-1)$$

The implementation stores the four weights for each position together and processes them in the same traversal.

## Correctness

The disjoint rectangle decomposition matches the bombardment definition cell by cell. Clipping removes only cells the problem does not record. Four difference updates reproduce each rectangle addition. The expanded prefix formula counts exactly how many cells each difference value affects. Inclusion-exclusion then selects precisely the query rectangle, proving every answer correct.

## Complexity and integer bounds

Let the recorded width and height be $W,H\le1001$ . Time is $O(WH+m\log(W+1)\log(H+1))$ and space is $O(WH)$ . A bombardment makes at most five rectangle updates.

One operation changes a cell by at most $10^4$ in absolute value. Each cell therefore has absolute value at most $3\times10^8$ , and a region sum at most $3\times10^8WH$ . For a conservative bound on intermediates, each operation produces at most $20$ difference-point updates, and each weight gains a factor of at most $WH$ . The prefix formula combines four terms, and rectangle inclusion-exclusion combines four prefixes. Thus intermediates are bounded by $320m\cdot10^4WH<10^{17}$ in absolute value, within signed 64-bit range.

Preserve negative values. Radius one, a single row or column, disjoint rectangles, and zero power all fit the same data structure.
