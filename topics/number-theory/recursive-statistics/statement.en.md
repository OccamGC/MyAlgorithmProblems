# Recursive Statistics

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See [environment and measurements](../../../docs/评测环境与性能.md).

## Story

An archivist keeps a recursive counting rule. Evaluate it for a batch of query arguments.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Let $P=998244353$ . Define $F(x)$ for every integer $x$ as follows:

- If $x\le0$ , return the integer $F(x)=x$ directly.
- If $x>0$ , let

$$F(x)=\left(x+\sum_{i=2}^{x}F\!\left(\left\lfloor\frac{x}{i}\right\rfloor\right)\right)\bmod P$$

An empty sum is zero. For positive arguments, use the representative from $0$ to $P-1$ . Evaluate every query. Values returned for nonpositive arguments are not reduced modulo $P$ .

## Input Format

The first line contains the query count $Q$ . Each of the next $Q$ lines contains one integer $x$ .

## Output Format

Print $Q$ lines containing the query results in input order. If $Q=0$ , produce no output.

## Examples

### Example 1

### Input

```text
7
-3
0
1
2
3
4
6
```

### Output

```text
-3
0
1
3
5
9
17
```

### Example 2

### Input

```text
5
-1000000000
1
10
10
0
```

### Output

```text
-1000000000
1
37
37
0
```

### Example 3

### Input

```text
7
226
513
1026
1212
1123
1026
1123
```

### Output

```text
7571
31299
103391
137241
118947
103391
118947
```

## Example Explanation

In the first example, $F(1)=1$ , $F(2)=2+F(1)=3$ , and $F(4)=4+F(2)+2F(1)=9$ . A negative argument is returned directly, without conversion to a nonnegative residue.

## Constraints and Guarantees

All inputs satisfy: $0\le Q\le10^5$ and $-10^9\le x\le10^5$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
