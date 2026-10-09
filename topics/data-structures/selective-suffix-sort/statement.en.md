# Sorting Selected Suffix Elements

Estimated time limit: 0.5 seconds. Memory limit: 256 MB.

The deployed limit is the standard program’s largest input median in the target environment multiplied by $2$ and rounded up to a multiple of $0.5$ seconds. See the [benchmark notes](../../../docs/评测环境与性能.md).

## Story

A sorting station has a row of numbered crates. Each instruction sorts one crate and the smaller crates after it within their selected positions. The manager tracks the remaining inversions.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

An integer array $a$ has length $n$ . An inversion is a pair $(i,j)$ with $1\le i<j\le n$ and $a_i>a_j$ .

An operation chooses position $k$ . Using the array at the start of the operation, form
$$
S=\{k\}\cup\{j:k<j\le n,\ a_j<a_k\}.
$$
Sort the selected values into nondecreasing order and put them back into the same positions, with smaller values at smaller indices. Other positions stay unchanged. Position $k$ itself is included; later positions equal to $a_k$ are excluded.

There are $m$ operations, each specified by integer $q$ . If $q>0$ , use $k=q$ ; otherwise use
$$
k=((\mathrm{ans}+q)\bmod n)+1,
$$
where $\mathrm{ans}$ is the previous output and the remainder lies in $0,\ldots,n-1$ . The first operation uses the initial inversion count as $\mathrm{ans}$ .

## Input

The first line contains $n,m$ . The second contains $a_1,\ldots,a_n$ . Each of the next $m$ lines contains one integer $q$ .

## Output

Print $m+1$ lines: the initial inversion count followed by the count after every operation.

## Samples

### Sample 1

### Input

```text
3 2
2 3 1
1
1
```

### Output

```text
2
1
1
```

### Sample 2

### Input

```text
4 2
2 2 1 0
1
1
```

### Output

```text
5
1
1
```

### Sample 3

### Input

```text
4 3
3 -1 3 0
-4
-8
2
```

### Output

```text
3
3
3
3
```

## Sample explanations

In sample one, sorting positions $1,3$ produces $(1,3,2)$ with one inversion. Selecting position $1$ again changes nothing. In sample two, sorting positions $1,3,4$ gives $(0,2,1,2)$ ; the next operation changes nothing. Sample three illustrates mathematical remainders for negative instructions.

## Constraints and guarantees

$1\le n,m\le100000$ , $|a_i|\le10^9$ , and $q\in[-10^9,-1]\cup[1,n]$ . All input values are integers.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
