# Nano Computer Mainframe

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge only supports coarser increments, round up again to a supported value.
- Memory limit: 64 MB

## Story

Imperial researchers use a Nano Computer Mainframe to study drone upgrades. Their research log is a sequence of nonnegative integers, and every consecutive combination has an XOR value. Records can change, and researchers ask for the sum of XOR values of all consecutive combinations within a chosen interval. Help the mainframe answer these queries.

## Formal Problem Statement

Maintain a nonnegative integer array $a_1,\ldots,a_n$ under $q$ operations:

- `1 l r` : sum the XOR values of all nonempty subarrays $[i,j]$ with $l\le i\le j\le r$ , namely

$$\sum_{i=l}^{r}\sum_{j=i}^{r}(a_i\oplus a_{i+1}\oplus\cdots\oplus a_j)$$

- `2 p v` : assign $v$ to $a_p$ ; this is not an increment.

Here $\oplus$ denotes bitwise XOR. The outer sums use ordinary integer addition, with no further XOR and no modulus. Each query uses the current array.

## Input Format

The first line contains $n,q$ . The second contains the $n$ initial values. The next $q$ lines describe operations in the formats above.

## Output Format

For each operation `1` , print one integer on its own line. If there are no queries, print nothing.

## Sample 1

### Input

```text
10 10
10 3 8 2 6 10 7 6 1 8
1 2 4
2 10 8
1 1 3
2 8 4
2 6 8
2 2 10
1 9 9
2 3 7
1 6 6
1 8 8
```

### Output

```text
43
42
1
8
4
```

### Explanation

The first queried array is $[3,8,2]$ . Its six subarray XOR values are $3,8,2,11,10,9$ , summing to $43$ .

## Sample 2

### Input

```text
2 4
65536 65536
1 1 2
2 1 0
1 1 2
1 1 1
```

### Output

```text
131072
131072
0
```

### Explanation

Value $65536$ has bit $16$ set and must be included. The length-two subarray has XOR $0$ before the update and $65536$ afterward.

## Constraints and Guarantees

- $1\le n,q\le100000$ .
- Initial values and assigned values satisfy $0\le a_i,v\le65536$ .
- $1\le l\le r\le n$ and $1\le p\le n$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
