# Wheat Field — Solution

## Comparing solutions

The problem setter’s method enumerates two horizontal support lines determined by obstacles and field boundaries. Within their strip, it scans blocking points in horizontal order and takes the largest square fitting between consecutive blockers. An optimal empty square can be moved or expanded until boundaries or obstacles constrain it, so these support strips suffice. Boundary contacts follow the statement's convention.

The implementation by Codex (GPT-6) enumerates vertical supports and scans vertical gaps. Swapping axes yields the horizontal scan above, with the same support-line proof. With $k$ obstacles, both take $O(k^3)$ time and $O(k)$ space.

## Enumerate the left and right boundaries

The grid is large but has few buildings. Collect all building column coordinates together with virtual boundaries $0,m+1$ , then sort and deduplicate them. For every pair $l<r$ , consider the strip strictly between these columns, of width $w=r-l-1$ .

Take buildings inside the strip, sort their row coordinates, and add $0,n+1$ at the ends. Between consecutive row coordinates $a,b$ , the strip contains an empty rectangle of height $h=b-a-1$ and width $w$ . It contains a square of side $\min(h,w)$ .

Sort all buildings by row once. For each boundary pair, scan that list and filter by column instead of sorting again. Repeated building records only introduce empty gaps and cannot increase the answer.

## Correctness

Every rectangle considered by the algorithm is empty, so the square using its shorter side is feasible.

Conversely, take any feasible square. Keep its row interval fixed and expand left and right as far as possible. Expansion stops at a grid boundary or a building in that row interval. Both outer column boundaries therefore belong to the enumerated set. For this pair, one gap between consecutive building rows contains the square's entire row interval. Both that gap's height and the strip's width are at least the square's side length. The algorithm finds an answer at least as large as any feasible square; combined with feasibility, this proves optimality.

## Complexity

There are at most $k+2$ candidate column boundaries, and each pair scans $k$ buildings. Time is $O((k+1)^3)$ and space is $O(k+1)$ , including the case $k=0$ . Grid dimensions affect only coordinates and the answer; no $n\times m$ array is needed.
