# Festival Plan

- Indicative time limit: **3.5 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Deployment time limit: measure the reference program in the target environment, multiply the slowest case's median time by 2, and round up to the next 0.5 seconds.
- Memory limit: **512 MB**.

## Story

The festival team has arranged its events in a rooted tree. Following the tree downward gives a continuous program of events. Each event has a value; expensive events may have negative values.

A program must contain a permitted number of events. Any event might become the festival's highlight, so the team wants the best total value of a program containing each event.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

You are given an undirected tree with $n$ vertices numbered $1,\ldots,n$ , rooted at vertex $1$ . Vertex $i$ has weight $v_i$ .

A valid path starts at any vertex and moves to a child at every step. Its **number of vertices**, including both endpoints, is between $L$ and $R$ , inclusive. Its value is the sum of the weights of its vertices.

For each vertex $i$ , independently find the maximum value of a valid path containing $i$ . Paths chosen for different answers may overlap.

## Input Format

The first line contains $n,L,R$ .

The second line contains $n$ integers $v_1,\ldots,v_n$ .

Each of the next $n-1$ lines contains two integers $u,v$ , describing an undirected edge.

## Output Format

Print $n$ lines. Line $i$ contains the answer for vertex $i$ , or `-1061109568` if no valid path contains it. A valid path may have a negative value.

## Sample 1

### Input

```text
5 2 5
-338 971 -35 -221 458
1 2
3 1
3 4
2 5
```

### Output

```text
1091
1429
-256
-256
1429
```

## Sample 2

### Input

```text
1 1 1
-7
```

### Output

```text
-7
```

## Sample 3

### Input

```text
4 3 4
2 -1 4 3
1 2
1 3
1 4
```

### Output

```text
-1061109568
-1061109568
-1061109568
-1061109568
```

## Sample Explanation

In sample 1, path $1\to2\to5$ has value $1091$ , path $2\to5$ has value $1429$ , and path $3\to4$ has value $-256$ . Path $5\to2\to1\to3$ is invalid because it does not always move to a child.

![The sample tree and three valid downward paths](assets/downward-paths.svg)

Vertex IDs appear inside the circles, with weights beside them. Arrows point from parents to children.

Sample 2 permits a single-vertex path. In sample 3, the longest downward path has only two vertices, so every answer is the no-path marker.

## Constraints and Guarantees

For all test cases: $1\le L\le R\le n\le500000$ , $-1000\le v_i\le1000$ , and $1\le u,v\le n$ . The input edges form a tree.

| Score | Additional restrictions |
| --- | --- |
| 100% | None |
