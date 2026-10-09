# Danjin's Canisters

- Indicative time limit: **1.5 seconds** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual limit: measure the reference solution on the target system, take the largest median time over test files, multiply by 2, and round up to a multiple of 0.5 seconds.
- Memory limit: **128 MB**.

## Story

“Absolutely none of them are empty!”

“Hehe, surely an empty one now and then is understandable.”

Danjin arranges his canisters in a row, each with a type. To change the display, he may replace the types in a range, reverse a range, or move a whole segment elsewhere. He also wants to know how many consecutive runs of one type appear in a queried range.

## Formal Problem Statement

You are given a sequence of length $n$ , with positions $1,\ldots,n$ and initial types $v_1,\ldots,v_n$ . Process $m$ operations in order:

1. `1 l r v` : set every type in $[l,r]$ to $v$ .
2. `2 l r` : reverse the order of $[l,r]$ .
3. `3 l len nl` : remove the segment of length $\mathrm{len}$ starting at position $l$ , keeping its internal order. Renumber the remaining sequence from $1$ , then insert the removed segment so that it occupies $[\mathrm{nl},\mathrm{nl}+\mathrm{len}-1]$ in the final sequence. Equivalently, insert it after the first $\mathrm{nl}-1$ remaining elements.
4. `4 l r` : output the number of consecutive equal-type runs in $[l,r]$ . Equivalently, the answer is $1$ plus the number of adjacent pairs with different types inside the range.

Every operation uses the current sequence positions. In operation 3, $\mathrm{nl}$ is interpreted relative to the **remaining sequence after removal**, and insertion at either end is allowed. The total length always remains $n$ .

## Input Format

The first line contains $n,m$ . The second line contains $v_1,\ldots,v_n$ . Each of the next $m$ lines contains an operation in the format above.

## Output Format

For each operation 4, output one integer on its own line, in query order.

## Sample 1

### Input

```text
6 6
1 1 2 2 3 3
4 1 6
2 2 3
4 1 6
4 2 3
1 5 5 7
4 1 6
```

### Output

```text
3
5
2
6
```

## Sample 2

### Input

```text
5 7
1 2 2 3 1
3 2 2 4
4 1 5
2 1 5
4 1 3
1 2 4 2
3 1 5 1
4 1 5
```

### Output

```text
4
2
2
```

## Sample 3

### Input

```text
1 5
7
3 1 1 1
2 1 1
1 1 1 9
4 1 1
4 1 1
```

### Output

```text
1
1
```

## Sample Explanation

After the first reversal in sample 1, the sequence is $[1,2,1,2,3,3]$ . It has $5$ runs in total, while positions $2,3$ contain $2$ runs.

Sample 2 first removes the two elements at positions $2,3$ , leaving $[1,3,1]$ . Inserting the removed segment at the end produces $[1,3,1,2,2]$ .

![Two type-2 canisters are removed and inserted after the remaining sequence](assets/segment-move.svg)

Dashed outlines identify the moved segment; numbers indicate types. Sample 3 covers moving, reversing and assigning a sequence with one element.

## Constraints and Guarantees

For all test cases: $1\le n,m\le200000$ , and every initial or assigned type satisfies $1\le v\le10^9$ .

Operations 1, 2 and 4 have $1\le l\le r\le n$ . Operation 3 has $1\le l\le n$ , $1\le\mathrm{len}\le n-l+1$ , and $1\le\mathrm{nl}\le n-\mathrm{len}+1$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
