# Sign Recognition

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for estimation only)
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 128 MB

## Story

An old village save has lost the meaning of its signs, but their character sequences remain. To compare writing habits, the administrator wants to count fragments that occur on one sign and on no other sign.

## Formal Problem Statement

You are given $n$ nonempty lowercase strings. An occurrence of a substring in $s_i$ is identified by its index interval $[l,r]$ .

An occurrence is exclusive if its content does not occur in any other string $s_j$ with $j\ne i$ . **Occurrences at different positions in the same string count separately, even if their content is identical.** If the content appears in another string, none of its occurrences are exclusive.

For each query $[L,R]$ , count all exclusive substring occurrences, across all strings, whose lengths lie in this inclusive interval.

## Input Format

The first line contains $n,q$ . The next $n$ lines contain the strings. Each of the following $q$ lines contains $L,R$ .

## Output Format

Print one integer answer per query, on $q$ lines.

## Example 1

### Input

```text
2 1
aababab
bbaabaa
2 10
```

### Output

```text
24
```

## Example 2

### Input

```text
2 3
aaa
b
1 1
2 3
4 10000000000
```

### Output

```text
4
3
0
```

## Example 3

### Input

```text
2 1
aaa
aaa
1 3
```

### Output

```text
0
```

## Example Explanation

In example 2, the three occurrences of `a` in `aaa` and the one occurrence of `b` are exclusive, giving $4$ for length $1$ . The substring `aa` occurs twice and `aaa` once. The two strings in example 3 are identical, so no occurrence is exclusive.

## Constraints and Guarantees

All inputs satisfy $1\le n,q\le5$ . Each string has length in $[1,50000]$ and contains only `a` through `z` . Queries satisfy $1\le L\le R\le10^{10}$ . Different input strings may be identical.

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
