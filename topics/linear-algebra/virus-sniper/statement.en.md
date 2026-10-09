# Virus Sniper

- Indicative time limit: 1.0 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: twice the reference program's benchmark time on the slowest official input in the target environment, rounded up to a multiple of 0.5 seconds. Round up again if the platform requires a coarser unit.
- Memory limit: 128 MB

## Story

Yuri is testing a new warhead for the game's Virus sniper. Technicians first increase the initial intensity in several rectangles of a test field, then isolate a smaller rectangle to observe how the intensity spreads.

Every experiment starts from the same initial record. Yuri wants results far into the future, and the region chosen for the next experiment depends on the previous output.

## Formal Problem Statement

The field has $A$ rows and $B$ columns, initially with zero intensity everywhere. First perform $Q$ rectangle additions. An operation adds the integer $C$ to every cell of the closed rectangle with upper-left corner $(x_1,y_1)$ and lower-right corner $(x_2,y_2)$ . No spreading takes place during these operations.

Each experiment isolates an $N$ by $M$ rectangle. Number its cells from $1$ to $d=NM$ in row order, top to bottom and left to right within each row. Probabilities depend on these relative cell indices and are reused in every experiment.

For each source cell $i$ , five probabilities $p_{ij}=a_{ij}/b_{ij}$ correspond to itself, up, down, left, and right. At each integer time step, a transmission occurs with the given probability for each direction whose target remains inside the isolated rectangle. A transmission adds the source's entire current intensity to the target at the next time step. All transmissions are simultaneous, and existing intensity is retained. Newly added intensity can only spread starting with the following step. Directions leaving the rectangle are ignored, but their input pairs must still be read. All transmission trials are independent; the five probabilities need not sum to $1$ .

There are $K$ queries, each specifying a nonnegative integer time $T$ . Find the expected intensity in every isolated cell at time $T$ . Each experiment restarts from the field after the rectangle additions, without inheriting any state from the previous experiment.

Let $P=1000000009$ . Each expectation is a rational number whose denominator is not divisible by $P$ . For an expectation $r/s$ , output the unique integer $z$ satisfying $zs\equiv r\pmod P$ and $0\le z<P$ .

The first experiment has upper-left corner $(1,1)$ . Let $S$ be the ordinary integer sum of the $d$ output values of the current experiment; do not reduce this sum modulo $P$ . The next upper-left corner is

$$x=1+(S\bmod(A-N+1)),\qquad y=1+((7S)\bmod(B-M+1))$$

Thus, convert each expectation to its output residue first, then use the integer sum of those residues to choose the next region.

## Input Format

The first line contains six integers $A,B,N,M,Q,K$ .

Each of the next $Q$ lines contains five integers $x_1,y_1,x_2,y_2,C$ .

The next $d$ lines describe the probabilities. Line $i$ contains $a_{i0},b_{i0},a_{i1},b_{i1},\ldots,a_{i4},b_{i4}$ in the order self, up, down, left, right.

Each of the next $K$ lines contains a nonnegative decimal integer $T$ with no unnecessary leading zeroes.

## Output Format

Output $K$ lines, each containing $d$ integers in relative cell order for that query.

## Sample 1

### Input

```text
1 2 1 2 2 3
1 1 1 1 5
1 2 1 2 2
0 1 0 1 0 1 0 1 1 1
0 1 0 1 0 1 1 1 0 1
0
1
2
```

### Output

```text
5 2
7 7
14 14
```

### Explanation

Both cells transmit to each other at every step while retaining their existing intensities, giving $(5,2)$ , then $(7,7)$ , then $(14,14)$ . Every query restarts from $(5,2)$ .

## Sample 2

### Input

```text
1 2 1 2 1 1
1 1 1 1 1
0 1 0 1 0 1 0 1 1 1
0 1 0 1 0 1 0 1 0 1
1000000008
```

### Output

```text
1 1000000008
```

### Explanation

The first cell always has intensity $1$ , while the second gains $1$ each step. At time $T$ , the result is $(1,T\bmod P)$ .

## Sample 3

### Input

```text
3 3 1 2 3 2
1 1 1 2 1000000000
2 1 2 2 7
3 1 3 2 11
0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1
0
0
```

### Output

```text
1000000000 1000000000
11 11
```

### Explanation

The first output sum is $2000000000$ , so the next upper-left corner is $(3,1)$ and both outputs are $11$ . Reducing the sum modulo $P$ again would select the wrong rectangle.


## Constraints and Guarantees

- $1\le N\le A\le1000$ , $1\le M\le B\le1000$ , and $1\le d=NM\le50$ .
- $1\le Q\le10^6$ , $1\le K\le5$ , and $0\le C\le10^9$ .
- $1\le x_1\le x_2\le A$ and $1\le y_1\le y_2\le B$ .
- $0\le a_{ij}\le b_{ij}\le10^9$ and $b_{ij}\ge1$ .
- $0\le T\le10^{1000}$ . All input values are integers.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $A=N$ , $B=M$ , $T\le1000$ , $Q\le1000$ |
| 10% | $A=N$ , $B=M$ , $T=0$ |
| 20% | $A=N$ , $B=M$ , $T\le10^{18}$ |
| 30% | $T\le10^{18}$ |
| 10% | No additional conditions |
