# Grox's Sequence VI

- Indicative time limit: 0.5 seconds.
- Actual limit: twice the slowest per-case median of the reference program on the target judge, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> Was it prophets and mystics who gave us electricity, antibiotics, modern signatation, aerospace science, and digital timepieces? No. It was those who proceeded rationally, building on the work of others to create new wonders.
>
> — *Spore*, [Book of Science Pt. 5](https://spore.fandom.com/wiki/Books_of_Science)

Although the Grox are a mechanical species, they were not always as they are today. They reached their present form through a long history of evolution and self-modification.

To commemorate that epic history, you decide to give them a recurrence sequence. It has infinitely many terms, so the Grox ask only about terms that interest them. They may also change some parameters while keeping the key parameters that determine the recurrence's structure fixed. Since nobody enjoys copying enormous numbers, all answers must be reported modulo the specified number.

## Formal Problem Statement

Fix an integer $\beta$ and a nonnegative integer $k$ . Integer parameters $\alpha,a_0,\ldots,a_k$ define a sequence by

$$f(0)=\alpha$$

$$f(n)=\beta f(n-1)+\sum_{i=0}^k a_i n^i\qquad(n\ge1)$$

Perform $Q$ operations:

- `0 n` : report the least nonnegative residue of $f(n)$ modulo $P=1000000007$ under the current parameters.
- `1 alpha a0 ... ak` : replace $\alpha,a_0,\ldots,a_k$ together. The values of $\beta$ and $k$ remain fixed.

After replacement, every term is defined again by the new parameters and the recurrence above. Parameters may be negative.

## Input Format

The first line contains $Q,\beta,k$ . The second contains $k+2$ integers $\alpha,a_0,\ldots,a_k$ . Each of the next $Q$ lines gives one operation in the format above.

## Output Format

Output one integer per query. Replacement operations produce no output.

## Samples

### Sample 1

### Input

```text
5 2 1
1 0 1
0 1
0 2
0 3
0 4
0 5
```

### Output

```text
3
8
19
42
89
```

### Sample 2

### Input

```text
5 1 0
-2 3
0 0
0 2
1 5 -1
0 0
0 3
```

### Output

```text
1000000005
4
5
2
```

### Sample 3

### Input

```text
3 0 1
7 3 -2
0 0
0 1
0 3
```

### Output

```text
7
1
1000000004
```

## Sample Explanation

Sample 1 has $f(n)=2f(n-1)+n$ . In sample 2, $f(n)=-2+3n$ before replacement and $f(n)=5-n$ afterward. In sample 3, $\beta=0$ , so positive-index terms equal $3-2n$ , while the zeroth term remains $7$ .

## Constraints and Guarantees

For **100% of the data**:

$1\le Q\le500$ ; $0\le k\le200$ ; $0\le n\le10^9$ ; $|\alpha|,|\beta|,|a_i|\le10^9$ ; operation codes are $0$ or $1$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
