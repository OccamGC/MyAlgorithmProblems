# Counting Pairs under Dynamic Binary Bounds

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A counting terminal stores five binary upper bounds. Each time an operator flips a bit, it reports how many extra conditions each eligible pair satisfies.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Five binary strings of length $n$ represent nonnegative integers $A,B,C,D,E$ from most significant to least significant bit. Leading zeros are allowed.

Consider all ordered pairs of nonnegative integers $(a,b)$ satisfying $a\le A$ and $b\le B$ . There are three extra conditions:
$$
a\mathbin{\&}b\le C,\qquad a\mathbin{\oplus}b\le D,\qquad a\mathbin{|}b\le E.
$$
The operators $\&$ , $\oplus$ and $|$ mean bitwise AND, XOR and OR.

Each operation flips one specified bit in one string. Initially and after every operation, report the numbers of eligible ordered pairs satisfying exactly zero, one, two and three extra conditions, respectively, modulo $998244353$ .

## Input Format

The first line contains $n,m$ . The next five lines contain the binary representations of $A,B,C,D,E$ in that order. Each of the next $m$ lines contains $x,y$ : flip bit $y$ of string $x$ , counting bits from right to left starting at one. Strings are numbered one through five.

## Output Format

Print $m+1$ lines, each with four integers: the counts satisfying exactly zero, one, two and three extra conditions modulo $998244353$ . The first line describes the initial state; later lines describe the state after each update.

## Samples

### Sample 1

### Input

```text
2 3
11
10
00
01
10
3 1
1 2
5 2
```

### Output

```text
1 4 4 3
0 5 3 4
0 1 1 4
0 2 3 1
```

### Sample 2

### Input

```text
1 0
0
0
0
0
0
```

### Output

```text
0 0 0 1
```

### Sample 3

### Input

```text
3 2
111
111
111
111
111
4 3
4 3
```

### Output

```text
0 0 0 64
0 0 32 32
0 0 0 64
```

## Sample Explanation

Sample one initially has $(3+1)(2+1)=12$ eligible pairs, so the four counts sum to twelve. Sample two has only $(0,0)$ , satisfying all three conditions. In sample three all sixty-four pairs initially satisfy three conditions; changing $D$ from seven to three gives thirty-two satisfying two and thirty-two satisfying three. The second flip restores the initial state.

## Constraints and Guarantees

$1\le n\le10000$ , $0\le m\le10000$ , $1\le x\le5$ , $1\le y\le n$ . Every string contains only zeros and ones.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
