# Grox's Sequence V B

- Indicative time limit: 0.5 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> What do you believe? And how much are you willing to risk on that belief? Would you risk your existence, and the existence of your species, on a hunch? A whim? The word of a prophet a thousand years dead?
>
> — *Spore*, [Book of Science Pt. 1](https://spore.fandom.com/wiki/Books_of_Science)

Your persistent efforts finally bring an alliance with the Grox. At the same moment, every other civilization in the galaxy declares war on you!

After billions of Spore years, the Grox have finally made a friend, and they treasure that friendship. You discover that they are no longer as cold as they once seemed: they feel joy, anger, sorrow, and delight, and they can laugh. As a gift, they construct a sequence for you.

The whole sequence is far too long, so you decide to calculate its characteristic value and send that value back to your home planet.

## Formal Problem Statement

Given nonnegative integers $n,k$ , let $P=1005060097$ . Define

$$a_i=i^k\binom ni\qquad(0\le i\le n)$$

For this problem, $0^0=0$ ; the zeroth power of any other integer is $1$ . Compute

$$S=\left(\sum_{i=0}^n a_i\right)\bmod P$$

Report the least nonnegative residue.

## Input Format

One line contains $n,k$ .

## Output Format

Output the integer $S$ on one line.

## Samples

### Sample 1

### Input

```text
10 103
```

### Output

```text
14606983
```

### Sample 2

### Input

```text
10 0
```

### Output

```text
1023
```

### Sample 3

### Input

```text
0 0
```

### Output

```text
0
```

## Sample Explanation

The answer in sample 2 is $2^{10}-1=1023$ . In sample 3, the only term is $0^0\binom00=0$ .

## Constraints and Guarantees

For **100% of the data**:

$0\le n\le10^9$ ; $0\le k\le100000$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
