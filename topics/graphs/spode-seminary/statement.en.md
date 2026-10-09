# Spode Seminary

- Indicative time limit: 0.5 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> Only Spode has the answers. Follow the Law of Spode, and all shall be clear.
>
> — *Spore*, [Scroll of Faith, Book 2](https://spore.fandom.com/wiki/Scrolls_of_Faith)

It is time once again for Spode Seminary's entrance examination, held every Spore year. Many students apply to study under its theology mentors, each of whom has a limited number of places. Students rank mentors in preference tiers, listing at most three in a tier or leaving it empty, and each student sets an acceptable admission tier.

No two students have the same exam score. Admission gives priority to higher-ranking students. While preserving the admission tiers already secured by earlier students, it gives the current student the best possible tier. Students who cannot enter any listed mentor's class consume no places.

The rankings have not yet been finalized. The seminary asks you to evaluate admission tiers under several possible rankings and tell each student how many places they must move up to become satisfied.

## Formal Problem Statement

There are $n$ students and $m$ mentors, numbered $1,\ldots,n$ and $1,\ldots,m$ . Mentor $j$ can admit at most $b_j$ students. Student $i$ assigns mentor $j$ a tier $c_{i,j}$ : $-1$ means unlisted; otherwise it is an integer from $1$ to $m$ , with smaller tiers preferred. Each student lists at most three mentors in any tier and can be assigned to at most one listed mentor.

A ranking lists all students from highest to lowest exam priority. Determine their admission tiers in this order. Keeping every higher-ranked student’s already determined tier fixed, give the current student the smallest tier for which an assignment is possible. If none of the listed mentors can admit the student, the student remains unassigned. Assignments among mentors in the same tier may be rearranged to satisfy these tiers. Unassigned students consume no capacity.

Student $i$ is satisfied if admitted at a tier at most $a_i$ . For each ranking, find:

1. Each student’s admission tier, or $-1$ if unassigned.
2. The minimum number of positions that student must move forward, preserving the relative order of all other students, to become satisfied when admission is recomputed. Output $0$ if already satisfied, or $-1$ if even first place cannot help.

Rankings and individual promotion queries are evaluated independently.

## Input

The first line contains $n,m,q$ .

The second line contains $a_1,\ldots,a_n$ . The third contains $b_1,\ldots,b_m$ .

The next $n$ lines contain $m$ integers each; row $i$ is $c_{i,1},\ldots,c_{i,m}$ .

Each of the last $q$ lines is a permutation of $1,\ldots,n$ , listing student IDs from highest to lowest priority.

## Output

For each ranking, print two lines of $n$ integers in **student ID order**. The first gives admission tiers; the second gives minimum promotions. Print $2q$ lines in total.

## Sample 1

### Input

```text
2 2 1
1 1
1 1
2 2
1 2
1 2
```

### Output

```text
2 1
-1 0
```

## Sample 2

### Input

```text
2 2 1
2 1
1 1
1 2
1 2
1 2
```

### Output

```text
1 2
0 1
```

## Sample 3

### Input

```text
2 2 1
2 2
1 1
-1 1
-1 1
1 2
```

### Output

```text
1 -1
0 1
```

## Sample Explanation

In sample 1, student $1$ can be assigned to either second-tier mentor, allowing student $2$ to obtain a first-tier mentor. Student $1$ has no first-tier choice, so promotion cannot help. In sample 2, student $2$ needs to move up one place. In sample 3, both students list only the same mentor, who can admit only the earlier student.

![Same-tier choices and a feasible assignment in sample 1](assets/same-tier.svg)

Here $S_i$ denotes a student and $M_j$ a mentor. Solid lines show an assignment satisfying both admission tiers.

## Constraints and Guarantees

$1\le n,m\le1000$ ; $1\le q\le10$ ; $0\le a_i\le m$ ; $0\le b_j\le1000$ ; $c_{i,j}\in\{-1,1,\ldots,m\}$ . Each student lists at most three mentors per tier. Every ranking is a permutation.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
