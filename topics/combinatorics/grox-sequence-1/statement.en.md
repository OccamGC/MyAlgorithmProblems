# Grox's Sequence I

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

> The Grox are an experiment that has not yet run its course.
>
> — *Spore*, [Book of Science Pt. 8](https://spore.fandom.com/wiki/Books_of_Science)

In pursuit of truth, you set out to explore the galactic center. Yet the vast Grox Empire occupies the surrounding star systems. Strong gravity and densely packed stars restrict your warp drive to nearby destinations. Forcing your way through the Grox's attacks may be a feat only someone with the “Joker” badge could manage.

To form an alliance with the Grox, you accept a task from their homeworld: calculate a Grox sequence.

The Grox's partly mechanical, partly organic bodies survive in extremely hostile environments, but adapting to those conditions has irreversibly changed their organic structures. Their bodies contain a chainlike polymer called GNA. There are $a$ substances that may occur any number of times, $b$ that may occur only an even number of times, and $c$ that may occur either zero times or an odd number of times. The Grox want to count the directed GNA sequences of length $N$ .

## Formal Problem Statement

There are three disjoint groups of distinct symbols:

- Each of the $a$ symbols in the first group may occur any nonnegative number of times.
- Each of the $b$ symbols in the second group must occur an even number of times, including zero.
- Each of the $c$ symbols in the third group must occur either zero times or a positive odd number of times.

Count valid directed sequences of length $N$ , modulo $p=1004535809$ . Two sequences differ exactly when their symbols differ at some position. Apply each restriction separately to each symbol. The unique empty sequence is valid when $N=0$ .

## Input Format

Four lines contain the nonnegative decimal integers $a,b,c,N$ , respectively. The values of $a,N$ can greatly exceed built-in integer ranges.

## Output Format

Print the least nonnegative residue of the answer.

## Samples

### Sample 1

### Input

```text
6
9
7
5
```

### Output

```text
446518
```

### Sample 2

### Input

```text
0
0
2
1
```

### Output

```text
2
```

### Sample 3

### Input

```text
0
0
0
0
```

### Output

```text
1
```

## Sample Explanation

Checking the occurrence restrictions of each individual symbol gives $446518$ sequences in the first case. In the second, either of the two symbols forms a valid length-one sequence. The third case has just the empty sequence.

## Constraints and Guarantees

$0\le a,N\le10^{1000}$ , $0\le b\le10^5$ , $0\le c\le1000$ . The modulus $1004535809=479\times2^{21}+1$ is prime, with primitive root three.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
