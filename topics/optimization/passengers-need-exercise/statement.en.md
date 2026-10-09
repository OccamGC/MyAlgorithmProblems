# Passengers Need More Exercise

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments.
- Memory limit: 512 MB

## Story

After careful deliberation, the railway company's board concludes that passengers, tired from their journeys, need more exercise. It therefore orders trains to stop where passengers will have to walk as far as possible.

Once the train stops, each passenger walks to the nearest door. The driver must maximize their total walking distance while keeping every door within the platform. If several positions are equally good, choose the one with the first door farthest to the left.

## Formal Problem Statement

The platform is the coordinate interval $[0,L]$ . There are $M$ passengers at positions $P_1\le\cdots\le P_M$ . A train has $N$ doors with offsets $0=D_1<D_2<\cdots<D_N$ relative to the first door.

Let the first door stop at a real coordinate $S$ , where $0\le S\le L-D_N$ . Door $j$ then has actual coordinate $S+D_j$ , so passenger $i$ walks $\min_{1\le j\le N}|P_i-(S+D_j)|$ to the nearest door. Maximize the sum of these distances. If several positions achieve the maximum, choose the smallest $S$ .

The required position and maximum sum are guaranteed to be integers or half-integers. Print their exact values to one decimal place.

## Input Format

The first line contains $L$ , and the second line contains $M$ .

The third line contains $M$ integers $P_1,\ldots,P_M$ .

The fourth line contains $N$ . If $N>1$ , the fifth line contains $N-1$ integers $D_2,\ldots,D_N$ ; if $N=1$ , input ends after the fourth line.

## Output Format

Print two numbers with exactly one digit after the decimal point: the smallest optimal position $S$ , then the maximum total distance.

## Sample 1

### Input

```text
4
5
0 1 2 3 4
4
1 2 3
```

### Output

```text
0.5 2.5
```

### Explanation

At $S=0.5$ , each of the five passengers is $0.5$ units from the nearest door, giving a total of $2.5$ .

## Sample 2

### Input

```text
10
1
5
1
```

### Output

```text
0.0 5.0
```

### Explanation

With a single door, both $S=0$ and $S=10$ attain the maximum distance of $5$ . The tie rule chooses $S=0$ .

## Constraints and Guarantees

- $1\le L\le 1\,000\,000\,000$ .
- $1\le M,N\le 300$ , and $N\le L+1$ .
- $0\le P_1\le\cdots\le P_M\le L$ .
- $D_1=0<D_2<\cdots<D_N\le L$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $L\le 100$ and $M,N\le 50$ |
| 70% | No additional conditions |
