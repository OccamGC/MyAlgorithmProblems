# Partitioning Tiles with Distinct Runs

Estimated time limit: 1.5 seconds. Memory limit: 128 MB.

The limit is 2 times the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A workshop receives batches of tiles marked with a type and a number. Its organizer wants to pack every tile into prescribed groups, using each distinct run at most once.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $m$ tile types. Each type may have numbers $1,\ldots,n$ . Starting with no tiles, you receive $k$ batches. Batch $i$ contains $a_i$ tiles of type $b_i$ and number $c_i$ . Identical tiles are accumulated regardless of which batch supplied them.

Decide whether **every tile can be used exactly once** in a partition into the following groups:

- A run consists of three or five consecutive numbers of one type, with exactly one tile of each number. Runs must be pairwise distinct: a fixed combination of type, starting number and length may occur at most once.
- An identical-tile group consists of three or four tiles with the same type and number. Any number of identical copies of such a group is allowed.

Either category may contain zero groups. Runs of different types or lengths are distinct. Determine whether a valid partition exists.

## Input Format

The first line contains $n,m,k$ . Each of the next $k$ lines contains $a_i,b_i,c_i$ .

## Output Format

Print `1` if a valid partition exists, or `0` otherwise.

## Samples

### Sample 1

### Input

```text
5 1 5
1 1 1
1 1 2
1 1 3
1 1 4
1 1 5
```

### Output

```text
1
```

### Sample 2

### Input

```text
3 1 3
2 1 1
2 1 2
2 1 3
```

### Output

```text
0
```

### Sample 3

### Input

```text
1 2 3
1 1 1
2 1 1
4 2 1
```

### Output

```text
1
```

## Sample Explanation

The first sample uses one run of length five. In the second, the only possible run starts at one and has length three; it may be used only once, leaving three tiles that cannot form a valid group. In the third, the first two batches combine into an identical triple, and the four tiles of the other type form their own group.

## Constraints and Guarantees

$1\le n,m,k\le5\times10^6$ , $1\le a_i\le10^9$ , $1\le b_i\le m$ , $1\le c_i\le n$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
