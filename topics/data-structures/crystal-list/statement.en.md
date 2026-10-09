# Crystal List

- Indicative time limit: **0.5 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual limit: measure the reference solution on the target system, take the largest median time over test files, multiply by 2, and round up to a multiple of 0.5 seconds.
- Memory limit: **128 MB**.

## Story

In a DNF event, players operate on a shared row of crystals. Replacing a range by one crystal type earns a score based on the energy change at every position. The energy of a type may also change during the event, so the same replacement can earn different scores at different times.

## Formal Problem Statement

There are $n$ positions numbered $1,\ldots,n$ and $k$ crystal types numbered $1,\ldots,k$ . Position $i$ currently contains type $c_i$ , and the current energy of type $t$ is $e_t$ .

Process $m$ operations in order:

- `0 l r c` : using the state before the operation, calculate

$$\sum_{i=l}^{r}|e_{c_i}-e_c|$$

  Output this score, then set the type at every position in $[l,r]$ to $c$ .
- `1 c e` : set the energy of type $c$ to $e$ . This changes the energy used by all crystals of that type in future scoring, but changes no position's type and produces no score.

Different types may have equal energy. A replacement still changes types even when its score is zero.

## Input Format

The first line contains $n,k,m$ . The second line contains the initial types $c_1,\ldots,c_n$ . The third line contains the initial energies $e_1,\ldots,e_k$ .

Each of the next $m$ lines describes an operation. The second or third line is empty when its corresponding count is zero.

## Output Format

For each operation 0, output its score on a separate line, in operation order. If there are no such operations, output nothing.

## Sample 1

### Input

```text
5 5 5
1 2 3 4 5
1 2 3 4 5
0 1 2 3
0 1 2 1
1 4 1
0 1 5 5
0 5 5 4
```

### Output

```text
3
4
14
4
```

## Sample 2

### Input

```text
3 2 4
1 1 2
5 5
0 1 3 1
1 1 2
0 1 3 2
0 2 2 2
```

### Output

```text
0
9
0
```

## Sample 3

### Input

```text
0 0 0


```

### Output

```text

```

## Sample Explanation

The first replacement in sample 1 earns $|1-3|+|2-3|=3$ . After type 4's energy changes, subsequent replacements use its updated energy.

In sample 2, the first replacement scores $0$ but changes all three positions to type $1$ . After its energy becomes $2$ , replacing all positions by type $2$ with energy $5$ scores $9$ . Sample 3 is an empty instance and has empty output.

## Constraints and Guarantees

For all test cases: $0\le n,k\le500000$ and $0\le m\le100000$ . Every type identifier lies in $1,\ldots,k$ , and every initial or updated energy satisfies $1\le e\le50000$ .

Every operation 0 has $1\le l\le r\le n$ . All input is valid: for example, $n>0$ implies $k>0$ ; when $n=0$ there are no operations 0, and when $k=0$ there are no operations at all.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
