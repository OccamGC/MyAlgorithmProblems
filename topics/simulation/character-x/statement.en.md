# Character X

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The deployed limit is twice the largest per-input median runtime of the reference program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [reference measurements](../../../docs/评测环境与性能.md).

## Story

To access a set of practice materials, a student must pass a printing check on a website: draw a fixed-size X using the requested character.

## Formal Problem Statement

For each character $c$ , print a rectangle with $8$ rows and $10$ columns. Rows $i$ run from $1$ through $8$ , and columns $j$ run from $1$ through $10$ . Print $c$ at $(i,j)$ if at least one of the following conditions holds; otherwise print one space:

$$i\le j\le i+2\qquad\text{or}\qquad9-i\le j\le11-i$$

![Eight-by-ten X pattern, with dots marking spaces](assets/pattern.svg)

Dots in the diagram only mark space positions; output actual spaces. Where the two strips overlap, print just one character.

## Input

The first line contains an integer $T$ . Each of the next $T$ lines contains one character $c$ .

## Output

Print $8$ consecutive rows for each character, each containing exactly $10$ characters followed by a newline. Preserve leading and trailing spaces, with no blank lines between groups. There are $8T$ output rows in total; print nothing when $T=0$ .

## Samples

### Sample 1

### Input

```text
3
A
c
9
```

### Output

```text
AAA    AAA
 AAA  AAA 
  AAAAAA  
   AAAA   
   AAAA   
  AAAAAA  
 AAA  AAA 
AAA    AAA
ccc    ccc
 ccc  ccc 
  cccccc  
   cccc   
   cccc   
  cccccc  
 ccc  ccc 
ccc    ccc
999    999
 999  999 
  999999  
   9999   
   9999   
  999999  
 999  999 
999    999
```

### Sample 2

### Input

```text
1
Z
```

### Output

```text
ZZZ    ZZZ
 ZZZ  ZZZ 
  ZZZZZZ  
   ZZZZ   
   ZZZZ   
  ZZZZZZ  
 ZZZ  ZZZ 
ZZZ    ZZZ
```

### Sample 3

### Input

```text
0
```

### Output

```text

```

## Sample explanations

Sample 1 draws the same pattern using an uppercase letter, a lowercase letter and a digit. In Sample 2, rows two and seven each end with one space. Sample 3 has no printing tasks and produces empty output.

## Constraints and guarantees

For all inputs: $0\le T\le20$ ; $c$ is an uppercase English letter, a lowercase English letter or a decimal digit.

| Score | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
