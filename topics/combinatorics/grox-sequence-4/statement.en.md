# Grox's Sequence IV

- Indicative time limit: 1.0 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 1024 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> Knowledge can be obtained through a process of investigation, observation, the gathering of empirical data, reason, hypothesis, and the testing of the hypothesis.
>
> — *Spore*, [Book of Science Pt. 3](https://spore.fandom.com/wiki/Books_of_Science)

After the second sequence problem is solved, the Grox discover a remarkable algorithm that generates a remarkable sequence. This time, the construction uses bitwise XOR, OR, and AND together.

The Grox want to know the sequence's values, but ask you to calculate just three summary values to keep the output manageable.

## Formal Problem Statement

Given a nonnegative integer $n$ and integer lists $a_0,\ldots,a_n$ and $b_0,\ldots,b_n$ , let $P=1004535809$ .

For $0\le t\le n$ , define

$$C_t=\sum_{\substack{0\le i,j\le n\\i+j\le n\\i\mathbin{\mathrm{XOR}}j=t}}a_i b_j+\sum_{\substack{0\le i,j\le n\\i+j\le n\\i\mathbin{\mathrm{OR}}j=t}}a_i b_j+\sum_{\substack{0\le i,j\le n\\i+j\le n\\i\mathbin{\mathrm{AND}}j=t}}a_i b_j$$

$\mathrm{XOR}$ , $\mathrm{OR}$ , and $\mathrm{AND}$ denote bitwise exclusive OR, OR, and AND. The three sums count separately; an ordered pair may contribute to more than one sum.

For $r=0,1,2$ , compute

$$V_r=\left(\sum_{\substack{0\le t\le n\\t\equiv r\pmod3}}C_t\right)\bmod P$$

An empty sum is $0$ . Report the least nonnegative residue of each result.

## Input Format

The first line contains $n$ . The second line contains $n+1$ integers $a_0,\ldots,a_n$ , and the third contains $n+1$ integers $b_0,\ldots,b_n$ .

## Output Format

Output $V_0,V_1,V_2$ , one per line.

## Samples

### Sample 1

### Input

```text
2
1 2 3
3 2 1
```

### Output

```text
31
24
20
```

### Sample 2

### Input

```text
0
2
3
```

### Output

```text
18
0
0
```

### Sample 3

### Input

```text
3
1 0 2 3
0 4 1 0
```

### Output

```text
29
8
2
```

## Sample Explanation

In sample 1, $C_0=31,C_1=24,C_2=20$ . In sample 2, the only ordered pair contributes $6$ in each of the three sums, giving $V_0=18$ .

## Constraints and Guarantees

For **100% of the data**:

$0\le n\le2^{20}-1$ ; $0\le a_i,b_i\le10^9$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
