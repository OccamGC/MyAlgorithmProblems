# Just a Little More

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 8 MB

## Story

The radio station writes its opening jingle as lowercase letters, one letter per beat. The jingle is finally ready. Just as the host says “That will do,” the editor copies the first fifth of the current version onto its end, rounding the number of beats up.

The second version comes back with the same request: “Just a little more.” The third and fourth versions receive the same treatment. The jingle keeps growing, while the host is still waiting to say hello.

Print the requested versions of the jingle.

(This story was rewritten by GPT-6 Astra.)

## Formal Problem Statement

You are given a nonempty string $s_1$ . For every $k\ge2$ , define

$$s_k=s_{k-1}+\operatorname{prefix}\!\left(s_{k-1},\left\lceil\frac{|s_{k-1}|}{5}\right\rceil\right)$$

where $+$ denotes concatenation and $\operatorname{prefix}(s,t)$ denotes the first $t$ characters of $s$ .

There are $Q$ queries. Each gives a version index $x$ and asks for the entire string $s_x$ . Queries may repeat and need not be sorted.

## Input Format

The first line contains $s_1$ , consisting only of lowercase English letters.

The second line contains $Q$ . Each of the next $Q$ lines contains one integer $x$ .

## Output Format

Print $Q$ lines, each containing the entire requested string in query order.

## Sample 1

### Input

```text
abbbcd
5
1
2
3
4
5
```

### Output

```text
abbbcd
abbbcdab
abbbcdabab
abbbcdababab
abbbcdababababb
```

### Explanation

From the first version to the second, copy the first $\lceil6/5\rceil=2$ characters, namely `ab` .

## Sample 2

### Input

```text
a
4
1
3
2
2
```

### Output

```text
a
aaa
aa
aa
```

### Explanation

Queries may be out of order or repeated; each refers to the version defined above.

## Constraints and Guarantees

- $1\le |s_1|\le10$ ; $s_1$ contains only lowercase English letters.
- $1\le Q\le10$ .
- Every query satisfies $1\le x\le70$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | Every query has $x\le30$ |
| 20% | Every query has $x\le50$ |
| 50% | No additional conditions |
