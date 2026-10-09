# Time Management and Team Sports

Estimated time limit: 4.5 seconds. Memory limit: 512 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

As everyone knows, CCPC and ICPC are team sports.

After retiring from competition, you become the captain of an ACM team at a liberal arts college. You need to schedule training slots for a series of contests. Thanks to your uncanny foresight, you know how much the team would gain from entering each contest in each slot. Each slot must contain exactly one contest, and each contest must be entered exactly once, so there are equally many slots and contests.

The benefits cannot simply be added together, so you classify them into 71 grades, from 0 through 70. You want as many rewards of the highest grade as possible, then as many of the next grade as possible, and so on. Find the count of each reward grade in an optimal schedule.

## Formal Problem Statement

There are $n$ time slots and $n$ contests. Assign exactly one contest to each slot and use each contest exactly once. Assigning contest $j$ to slot $i$ gives reward grade $a_{ij}$ , an integer from zero through seventy.

Let $c_g$ count the rewards of grade $g$ . Choose an assignment that makes
$$
(c_{70},c_{69},\ldots,c_0)
$$
lexicographically largest, and output this sequence. First maximize grade-seventy rewards, then grade sixty-nine without sacrificing the previous count, and so on. If $n=0$ , every count is zero.

## Input Format

The first line contains $n$ . Each of the next $n$ lines contains $n$ integers; entry $j$ on line $i$ is $a_{ij}$ .

## Output Format

Print seventy-one integers: the optimal $c_{70},c_{69},\ldots,c_0$ , separated by single spaces.

## Samples

### Sample 1

### Input

```text
5
5 5 5 5 5
5 3 2 1 1
2 2 2 2 2
2 5 2 5 2
4 4 1 1 1
```

### Output

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 1 0 1 0 0
```

### Sample 2

### Input

```text
0
```

### Output

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Sample 3

### Input

```text
3
70 69 0
70 0 69
0 70 68
```

### Output

```text
2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Sample Explanation

Sample one attains three grade-five rewards, one grade-four reward and one grade-two reward. Sample two has no contests but still prints seventy-one zeros. Sample three attains two grade-seventy rewards and one grade-sixty-nine reward.

## Constraints and Guarantees

$0\le n\le500$ , $0\le a_{ij}\le70$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
