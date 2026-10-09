# Grox's Sequence III

- Indicative time limit: 1.0 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 512 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> That is why we proceed only from what we know, and why we constantly test what we believe to be true. We are rigorous with the truth, and ruthless.
>
> — *Spore*, [Book of Science Pt. 6](https://spore.fandom.com/wiki/Books_of_Science)

After you solve the second sequence problem, the Grox grow even fonder of you. They are still investigating how to solve the first sequence problem over a larger range, and discover yet another interesting sequence along the way.

This time, the Grox will give you several sets of parameters and ask you to calculate the corresponding results.

## Formal Problem Statement

Given a nonnegative integer $n$ and $q$ queries, each query provides nonnegative integers $a,b$ . Compute

$$G(a,b)=\sum_{i=a}^{\min(n,n+a-b)}(i+b-a)!\prod_{k=a}^{i}k\pmod{921260340}$$

An empty sum is $0$ when its upper bound is smaller than its lower bound. Define $0!=1$ . Both product endpoints are included; in particular, when $a=0$ , every product that occurs contains a factor of $0$ .

Print the representative between $0$ and $921260339$ .

## Input

The first line contains $n,q$ . Each of the following $q$ lines contains $a,b$ .

## Output

Print one answer per query on its own line.

## Sample 1

### Input

```text
5 5
1 2
3 4
1 1
3 1
5 5
```

### Output

```text
3038
1512
15017
387
600
```

## Sample 2

### Input

```text
0 3
0 0
1 0
0 1
```

### Output

```text
0
0
0
```

## Sample 3

### Input

```text
3 4
1 0
0 1
4 1
2 2
```

### Output

```text
15
0
0
40
```

## Sample Explanation

The last query of sample 1 has one term: $G(5,5)=5!\cdot5=600$ . In sample 2, the first query has a zero product and the other two have empty sums.

## Constraints and Guarantees

$0\le n,a,b\le5000$ ; $1\le q\le200000$ . The query indices $a,b$ may exceed $n$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
