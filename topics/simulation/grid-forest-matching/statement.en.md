# Matching in a Class of Four-Neighbor Grid Forests

Research update (2026-10-12): the cubic upper-bound conjecture in the story now has a [general proof and result summary](research/results/cubic-bound.en.md). The problem and input/output requirements retain their original definitions.

Estimated time limit: 1 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $11$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).
This multiplier gives the documented correct alternative at least twofold measured headroom.

## Story

After slacking off for far too long, a devious problem setter decides to investigate a problem. Someone may already have studied it, but he has never heard of it.

He gives you an $n\times n$ four-neighbor grid in which each cell is either a road or an obstacle. The road cells, connected whenever they are adjacent above, below, to the left, or to the right, form a forest: a collection of trees, possibly with no road cells at all.

The questioner reports $m$ moves, one at a time, each moving one cell in a specified direction. Initially and after every move, count the starting cells from which the entire sequence reported so far could have been followed. Once a start would have led onto an obstacle or outside the map, it remains invalid even if later moves return to a road.

For $m>n$, the setter conjectures that his method has a time upper bound of $O(\max(n^3,m))$ and has tried to construct inputs requiring the same order of work. His arguments for both bounds are still informal. If you can provide a rigorous proof or find a flaw, he would love to hear your thoughts.

## Formal Problem Statement

An $n\times n$ grid contains road cells and obstacles. Orthogonally adjacent road cells are joined by edges. The graph of all road cells and these edges is a forest: a disjoint union of trees, possibly empty.

You receive $m$ directions, each specifying a move by one cell. A start is valid exactly when it is a road cell and every step of the entire movement prefix remains on a road cell inside the grid. A start that has ever left the grid or reached an obstacle is permanently invalid, even if later moves return to a road.

Report the number of valid starts initially and after each step. Rows go from top to bottom and columns from left to right. Directions zero, one, two and three mean up, down, left and right, respectively.

## Input Format

The first line contains $n,m$ . Each of the next $n$ lines is a string of length $n$ : one denotes a road and zero an obstacle. Each of the next $m$ lines contains a direction integer $d$ .

## Output Format

Print $m+1$ lines. The first is the initial number of valid starts; the next $m$ lines give the counts after the first one through $m$ moves.

## Samples

### Sample 1

### Input

```text
4 6
1110
0010
1110
0000
3
3
1
0
2
2
```

### Output

```text
7
4
2
1
1
1
1
```

### Sample 2

### Input

```text
2 2
00
00
0
3
```

### Output

```text
0
0
0
```

### Sample 3

### Input

```text
3 0
101
010
101
```

### Output

```text
5
```

## Sample Explanation

Sample one starts with seven road cells. Two moves right leave two starts; the downward move leaves only the top-left start, which also survives the last three moves. Sample two has no roads, so every answer is zero. Sample three has no moves and reports its five road cells.

## Constraints and Guarantees

$1\le n\le400$ , $0\le m\le10^6$ , $d\in\{0,1,2,3\}$ . The four-neighbour road graph is guaranteed to be a forest.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
