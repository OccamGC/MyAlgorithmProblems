# Grox's Sequence VII

- Indicative time limit: 1.0 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> Some of our theoreticians suggest that the motivation for the Grox's actions may lie in the difference between machines and organic life, though there seems to be no way to test this hypothesis.
>
> — *Spore*, [Book of Science Pt. 10](https://spore.fandom.com/wiki/Books_of_Science)

The Grox's minds are fascinating. After a long history of cybernetic modification, their thinking has become very different from that of other creatures. It even involves matrix determinants.

You recall a romantic matrix made of Chinese characters:

$$\det\begin{pmatrix}\text{我}&0&\text{生}\\0&\text{有}&0\\\text{你}&0&\text{幸}\end{pmatrix}=\text{我有幸}-\text{生有你}$$

Reading the minus sign as the Chinese character 一 turns the result into “我有幸，一生有你”: “I am lucky to have you in my life.” The matrix the Grox give you, however, contains neither words nor ordinary numbers. Its entries are polynomials, and the determinant follows the same rules as usual.

The Grox want the coefficient sequence of this determinant. Since both the number of terms and their coefficients may be large, you must group the coefficients as specified and report the results modulo the given number.

## Formal Problem Statement

Given an integer $k$ , let $N=2^k$ . The input provides $N$ polynomials indexed from $1$ to $N$ :

$$A_i(x)=\sum_{j=0}^{N-1}a_{i,j}x^j$$

Construct an $N\times N$ polynomial matrix $M$ with

$$M_{r,i}=A_i(x)^{r-1}\qquad(1\le r,i\le N)$$

Every entry in the first row is the constant polynomial $1$ , including when $A_i(x)=0$ . Let

$$B(x)=\det M=\sum_{t\ge0}b_t x^t$$

For $0\le r<N$ , compute

$$V_r=\left(\sum_{\substack{t\ge0\\t\equiv r\pmod N}}b_t\right)\bmod P\qquad(P=1004535809)$$

Thus coefficients are added together after reducing exponents modulo $N$ . Report the least nonnegative residue of every coefficient.

## Input Format

The first line contains $k$ . Each of the next $N$ lines describes one polynomial. Line $i$ contains $N$ integers $a_{i,0},\ldots,a_{i,N-1}$ in increasing order of degree.

## Output Format

Output $N$ space-separated integers $V_0,\ldots,V_{N-1}$ on one line.

## Samples

### Sample 1

### Input

```text
1
1 2
3 4
```

### Output

```text
2 2
```

### Sample 2

### Input

```text
0
999
```

### Output

```text
1
```

### Sample 3

### Input

```text
2
1 2 3 4
7 8 9 10
1 2 3 4
5 6 7 8
```

### Output

```text
0 0 0 0
```

## Sample Explanation

The determinant in sample 1 is $(3+4x)-(1+2x)=2+2x$ . Sample 2 has a one-by-one matrix with determinant $1$ . Sample 3 has two identical columns, so its determinant is the zero polynomial.

## Constraints and Guarantees

For **100% of the data**:

$0\le k\le9$ ; $0\le a_{i,j}\le999$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
