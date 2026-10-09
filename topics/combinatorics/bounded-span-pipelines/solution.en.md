# Bounded-Span Pipelines: Solution

## Algorithm and Attribution

Codex (GPT-6) completed the geometric conventions, proved the laminar-matching reduction, and implemented the short-interval DP in [std.cpp](std.cpp).

## Geometry Becomes Noninterleaving Intervals

Every pipe uses two towers, so its endpoints form a matching. Suppose two pipes have endpoints $u<a<v<b$ . Pipe $(u,v)$ must be strictly above tower $a$ , whereas pipe $(a,b)$ must be strictly above tower $v$ . Their vertical order reverses inside $[a,v]$ , forcing an intersection. Valid intervals are disjoint or nested.

Conversely, any such matching of span at most $K$ is realizable with either direction for each pipe. Give an outermost pipe depth 1. At depth $d$ , set its higher endpoint to $K-d+1$ and its lower endpoint to $K-d$ , choosing sides according to its direction. A nested pipe's highest endpoint is no higher than the outer pipe's lowest endpoint. The outer segment is strictly above that minimum in its interior, preventing intersections and tower contact. Set unused towers to height 1.

A depth-$d$ chain uses at least $2d$ distinct endpoints within a span of at most $K$ , hence $d\le\lfloor(K+1)/2\rfloor$ . A valid mandatory pipe implies $K\ge2$ , so all assigned heights lie in $[1,K]$ .

![Two nested pipes](assets/example.svg)

We count directed matchings; height assignments are not counted.

## Interval Recurrence

Let $W(j,r)$ be the number of permitted directions for a pair: 1 or 2 for the endpoints of one mandatory pipe, 2 for two free endpoints, and 0 otherwise.

Let $D(l,r)$ count complete matchings within an interval. A mandatory endpoint whose partner lies outside makes completion impossible. An empty interval has value 1. Classify the rightmost endpoint:

$$
D(l,r)=[r\text{ is free}]D(l,r-1)
+\sum_{j=l}^{r-1}W(j,r)D(l,j-1)D(j+1,r-1).
$$

Compute this only for intervals shorter than $K$ . For the prefix answer $F(r)$ ,

$$
F(r)=[r\text{ is free}]F(r-1)
+\sum_{j=\max(1,r-K)}^{r-1}W(j,r)F(j-1)D(j+1,r-1).
$$

Every required inner interval has length at most $K-1$ .

## Correctness

The geometric argument identifies exactly the realizable matchings. The rightmost endpoint is either unused and free or paired with a unique $j$ . The part before $j$ and the part inside the pair are independent; interleaving pipes are forbidden. These cases are disjoint and exhaustive, and the direction multiplier counts precisely the permitted orientations. Induction on interval and prefix lengths proves that $F(n)$ is the answer.

## Implementation and Complexity

Process right endpoints in increasing order. Only the last $K+1$ rows of short intervals are needed; the code uses a circular table of 20 rows. Time is $O(nK^2)$ and space is $O(n+K^2)$ . Arithmetic is modulo 998244353. Products use 64-bit integers, safe because $2(998244353-1)^2<2^{63}$ .

Tests include literal small matchings, fully paired endpoints, long free suffixes, and independent enclosed intervals. See [generation and validation](tests/README.md).
