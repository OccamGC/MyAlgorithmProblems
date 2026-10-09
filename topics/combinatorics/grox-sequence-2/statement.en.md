# Grox's Sequence II

- Indicative time limit: 0.5 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 512 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> The universe is no place for amateurs. Learn all you can, abolish your prejudices, and then act.
>
> — *Spore*, [Book of Science Pt. 7](https://spore.fandom.com/wiki/Books_of_Science)

After you solve the first sequence problem, the Grox are delighted with your expertise. Still, the previous task placed too strict a limit on the number of substances allowed to occur zero or an odd number of times. Do not worry: the Grox do not know how to handle the larger range either.

While searching for a method for the larger case, they discover another interesting sequence. To keep the output manageable, the Grox ask for only three summary values.

## Formal Problem Statement

Let $P=1004535809$ . Given a nonnegative integer $n$ , define the following Laurent polynomial (a finite polynomial that allows negative integer exponents), with coefficients modulo $P$ :

$$F_n(x)=\sum_{i=0}^{n}(i!)^{-1}x^i\sum_{j=0}^{n-i}(j!)^{-1}x^{-j}$$

Here $(i!)^{-1}$ is the multiplicative inverse of $i!$ modulo $P$ , and $0!=1$ . After collecting equal powers, let $[x^e]F_n(x)$ denote the coefficient of exponent $e$ .

Print $A_0,A_1,A_2$ in this order, where

$$A_r=\sum_{\substack{-n\le e\le n\\e\equiv r\pmod3}}[x^e]F_n(x)\pmod P$$

Use remainders $0,1,2$ ; for example, exponent $-1$ belongs to remainder $2$ . Print representatives between $0$ and $P-1$ .

## Input

One line containing $n$ .

## Output

One line containing $A_0,A_1,A_2$ , separated by spaces.

## Sample 1

### Input

```text
1
```

### Output

```text
1 1 1
```

## Sample 2

### Input

```text
3
```

### Output

```text
334845272 2 2
```

## Sample 3

### Input

```text
0
```

### Output

```text
1 0 0
```

## Sample Explanation

For $n=1$ , $F_1(x)=1+x+x^{-1}$ , so every residue class has coefficient sum $1$ . For $n=0$ , only the constant term $1$ remains.

## Constraints and Guarantees

$0\le n\le100000$ . The modulus $P$ is prime, $P=479\cdot2^{21}+1$ , and $3$ is a primitive root modulo $P$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
