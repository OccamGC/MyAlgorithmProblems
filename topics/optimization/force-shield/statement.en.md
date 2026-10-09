# Force Shield

- Indicative time limit: 1.0 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge only supports coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

The Allies are building fortifications along a long defensive line. Bombardments cause damage while engineers carry out repairs. A Force Shield protects a section of the line, but also prevents repairs there. Given the construction and event schedules, choose when and where to activate the shield to minimize total loss.

## Formal Problem Statement

There are $n$ fortifications on a number line. Fortification $i$ is at integer coordinate $X_i$ and is completed at the start of integer time $T_i$ , with initial loss $0$ . Multiple fortifications may share a coordinate. They accumulate loss separately and never disappear because of damage.

A bombardment or repair event is described by $(L,R,T,K,H)$ . At each integer time $T,T+1,\ldots,T+K-1$ , it affects every completed, unshielded fortification in the closed interval $[L,R]$ : a bombardment adds $H$ to its loss, and a repair subtracts $H$ . Effects add, and loss may be negative. A fortification is unaffected by times before its completion, but ongoing events affect it from its completion time onward.

There is one shield device. You may use it any number of times, including zero. To activate it at integer time $C$ , choose a closed interval $[l,r]$ with integer endpoints and $r-l\le M$ . It protects the fortifications in that interval that have been completed by the start of time $C$ :

- Those fortifications are immune to both bombardments and repairs at times $C$ through $C+R_s-1$ , inclusive.
- Fortifications completed after activation are not protected by this activation.
- The next activation is allowed at time $C+R_s+S$ or later, and may choose a different interval.

At a given time, construction finishes first, a shield may then be activated, and event effects are applied last. When $M=0$ , the shield can still protect fortifications at one coordinate. Activations may occur at any positive integer time.

![A shield activated at time 1 lasts through time 3, cools down at time 4, and becomes available at time 5; a fortification completed at time 2 is not protected by that activation](assets/shield-timeline.svg)

Figure 1: The selected spatial interval is $[0,1]$ , with $M=1$ , $R_s=3$ , and $S=1$ . A is completed at coordinate $0$ at time $1$ ; B is completed at coordinate $1$ at time $2$ . Checks mark protection by this activation. Crosses mark completed but unprotected fortifications. Time $5$ marks availability only; no further activation is shown.

Minimize total loss after all known bombardments and repairs end. With no events, the answer is $0$ .

## Input Format

The first line contains $n,M,R_s,S,A,B$ , where $A$ is the number of bombardments and $B$ the number of repair events.

The next $n$ lines each contain $X_i,T_i$ . The next $A$ lines describe bombardments, followed by $B$ lines describing repairs. Each event line contains $L,R,T,K,H$ in that order.

## Output Format

Print one integer: the minimum total loss.

## Sample 1

### Input

```text
5 5 1 0 2 3
1 1
2 1
3 1
4 5
5 5
1 1 1 5 10
3 4 1 5 10
1 1 2 4 5
1 2 2 4 7
3 5 5 1 1
```

### Output

```text
-37
```

### Explanation

Shield coordinates $1$ through $3$ at time $1$ , only coordinate $3$ at times $2,3,4$ , and coordinates $3$ through $4$ at time $5$ . The repairs that remain unblocked give total loss $-37$ .

## Sample 2

### Input

```text
1 0 1 0 1 0
0 1
0 0 1 1 5
```

### Output

```text
0
```

### Explanation

$M=0$ still permits the closed interval $[0,0]$ , blocking the entire bombardment.

## Sample 3

### Input

```text
2 0 3 1 1 0
0 1
0 2
0 0 1 3 5
```

### Output

```text
5
```

### Explanation

Activate at time $2$ to protect both fortifications. Only the first fortification takes damage at time $1$ , giving loss $5$ .

## Constraints and Guarantees

- $1\le n\le500000$ and $0\le A,B\le200000$ .
- $-1499\le X_i\le1500$ and $-1499\le L\le R\le1500$ .
- $1\le T_i,T\le3000$ , $K\ge1$ , and $T+K-1\le3000$ .
- $0\le M<3000$ , $1\le R_s\le3000$ , $0\le S\le3000$ , and $0\le H\le1000$ .
- All input values are integers.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $n\le2000$ , $A,B\le1000$ ; coordinates lie in $[-14,15]$ ; construction times, event end times, $R_s,S\le30$ , and $M\le30$ |
| 70% | No additional conditions |
