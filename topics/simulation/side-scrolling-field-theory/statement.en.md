# Side-Scrolling Field Theory

Estimated time limit: 0.5 seconds. Memory limit: 256 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

There are $N$ students in a side-scrolling field that wraps around horizontally. From our viewpoint, they stand in a row numbered $1,\ldots,N$ from left to right. Each student either faces us or faces away, and interprets “left” and “right” relative to their own facing direction.

The students are playing a game of passing an object, initially held by student one. On each turn, the holder passes it to the student $p$ positions to their own left or right; zero positions means the holder themselves. Since the field wraps around, $p$ may exceed $N$. Crossing the boundary where the ends meet does not change anyone's facing direction.

Each student has exactly one major, represented by an uppercase letter from `A` to `Z`. Different students may have the same major. There will be $M$ transfers. After each transfer, print the major of the student holding the object.

## Formal Problem Statement

From the observer's viewpoint, $N$ students are numbered $1,\ldots,N$ from left to right, with the right end connected to the left end. Student $i$ has facing value $f_i$ : zero means facing away from the observer, and one means facing the observer. Their major is represented by the uppercase letter $C_i$ ; different students may have the same major.

Student one initially holds the object. Each operation gives $d,p$ : zero means the holder's own left and one means their own right. Move $p$ positions in that direction and pass the object to that student. Zero positions means the holder themselves, and a move may go around the row multiple times. Facing directions never change. Print the new holder's major after every operation.

![Facing directions in Sample 1 and its five successive transfers](assets/passing.svg)

An upward arrow means facing away from the observer below; a downward arrow means facing the observer. The chain of indices below shows the holder after each transfer.

## Input Format

The first line contains integers $N,M$ . Each of the next $N$ lines contains an integer $f_i$ and an uppercase letter $C_i$ for student $i$ . Each of the following $M$ lines contains integers $d,p$ describing a transfer.

## Output Format

Print $M$ lines, each containing the uppercase letter representing the holder's major after the corresponding transfer.

## Samples

### Sample 1

### Input

```text
5 5
0 A
1 B
0 C
1 D
1 E
1 0
1 6
1 6
0 6
1 2
```

### Output

```text
A
B
A
E
C
```

### Sample 2

### Input

```text
1 3
1 Z
0 0
1 1000000000
0 1
```

### Output

```text
Z
Z
Z
```

## Sample Explanation

In Sample 1, the successive holders are students one, two, one, five, and three. Left and right are determined by the current holder. Sample 2 has only one student, who keeps the object after every transfer.

## Constraints and Guarantees

For 100% of the data: $1\le N,M\le30000$ , $f_i,d\in\{0,1\}$ , $0\le p\le10^9$ , and every $C_i$ is an uppercase English letter.

“No move crosses an end” means that the index stays between one and $N$ throughout each move before any wrapping. The total step count is the sum of all $p$ values in one input file.

| Score share | Additional conditions |
| --- | --- |
| 50% | Total step count at most $4000000$ ; no move crosses an end |
| 20% | Total step count at most $4000000$ |
| 30% | None |
