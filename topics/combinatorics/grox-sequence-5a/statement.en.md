# Grox's Sequence V A

- Indicative time limit: 0.5 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 512 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> What do you believe? And how much are you willing to risk on that belief? Would you risk your existence, and the existence of your species, on a hunch? A whim? The word of a prophet a thousand years dead?
>
> — *Spore*, [Book of Science Pt. 1](https://spore.fandom.com/wiki/Books_of_Science)

Your persistent efforts finally bring an alliance with the Grox. At the same moment, every other civilization in the galaxy declares war on you!

After billions of Spore years, the Grox have finally made a friend, and they treasure that friendship. You discover that they are no longer as cold as they once seemed: they feel joy, anger, sorrow, and delight, and they can laugh. As a gift, they construct a sequence for you.

The whole sequence is far too long, so you decide to calculate its characteristic value and send that value back to your home planet.

## Formal Problem Statement

Given nonnegative integers $n,k$ and a positive integer $p$ , define a sequence of length $n+1$ by

$$a_i=i^k\binom ni\qquad(0\le i\le n)$$

For this problem, $0^0=0$ ; the zeroth power of any other integer is $1$ . Compute the characteristic value

$$S=\left(\sum_{i=0}^n a_i\right)\bmod p$$

Report its least nonnegative residue. The decimal integer $n$ may not fit in ordinary integer types. The modulus $p$ need not be prime.

## Input Format

One line contains the decimal integers $n,k,p$ .

## Output Format

Output the integer $S$ on one line.

## Samples

### Sample 1

### Input

```text
10 103 10007
```

### Output

```text
5367
```

### Sample 2

### Input

```text
10 0 10007
```

### Output

```text
1023
```

### Sample 3

### Input

```text
3 1 8
```

### Output

```text
4
```

## Sample Explanation

In sample 2, only $i=0$ contributes nothing, so the result is $2^{10}-1=1023$ . In sample 3, the sum is $3+6+3=12$ , whose residue modulo $8$ is $4$ .

## Constraints and Guarantees

For **100% of the data**:

$0\le n\le10^{1000}$ ; $0\le k\le3000$ ; $1\le p\le2\times10^9$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
