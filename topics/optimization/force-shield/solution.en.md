# Force Shield — Solution

## Comparing solutions

The problem setter’s method uses two-dimensional differences in time and position to recover damage, counts buildings eligible at activation, and uses spatial prefix sums with a monotone queue to find the best protection at each time. Its forward DP either skips a time and pays that time's loss, or activates and jumps past the active and cooldown periods, paying interval loss minus protection. These alternatives cover every next activation, and their intervals do not overlap, yielding minimum total loss.

Codex (GPT-6) uses backward DP to maximize saved loss relative to the fixed no-shield baseline. This is equivalent to forward loss DP and uses the same differences and monotone queue. Implementation must distinguish per-time and cumulative loss and count closed spatial intervals correctly. For $W$ positions, time range $T$ and $I$ input records, both have $O(I+WT)$ time and storage bounds.

## Loss without shields

Let $W$ be the span of fortification coordinates plus one, and $T$ the last event end time. With no events, print $0$ immediately.

Apply events to a two-dimensional difference grid indexed by position and time. Bombardments contribute $+H$ and repairs contribute $-H$ . Two-dimensional prefix sums recover the net loss $d_{x,t}$ at each position and time.

Let $c_{x,t}$ be the number of fortifications at position $x$ completed by the start of time $t$ , obtained by prefixing construction counts. Total loss without shields is

$$B=\sum_x\sum_{t=1}^{T}c_{x,t}d_{x,t}$$

Also prefix each position's net loss over time, writing the result as $P_{x,t}$ .

## Benefit of one activation

An activation at time $t$ ends at $e=\min(T,t+R_s-1)$ within the relevant horizon. Its benefit at position $x$ is

$$g_{x,t}=c_{x,t}(P_{x,e}-P_{x,t-1})$$

The count is fixed at activation time, so this formula never protects a fortification completed later. Repairs may make this benefit negative.

A closed interval whose endpoints are at distance at most $M$ contains at most $M+1$ consecutive integer coordinates. Prefix the values $g_{x,t}$ over position and use a monotone deque to maintain the smallest allowed left prefix. This finds the best activation benefit $G_t$ in $O(W)$ time. Permit benefit $0$ , representing no activation.

## Dynamic programming over time

Let $F_t$ be the maximum benefit obtainable when the device is available at time $t$ . Set $F_{T+1}=0$ and compute backward:

$$F_t=\max\left(F_{t+1},\ G_t+F_{\min(T+1,t+R_s+S)}\right)$$

The first option waits. The second activates now and resumes when the device becomes available again. Shield durations do not overlap, so their benefits add. The answer is $B-F_1$ .

## Correctness and boundary cases

Difference sums recover the combined event effects exactly. Construction counts include precisely the completed fortifications, making $B$ the unshielded loss. Each $g_{x,t}$ is exactly the bombardment and repair contribution blocked by one activation, and the deque considers all legal spatial intervals. An optimal schedule either waits when the device is available or activates immediately; the recurrence considers both choices. Hence $F_1$ is the maximum avoidable loss and the reported total is minimal.

Remember that $M=0$ still covers one coordinate, loss may be negative, construction at the activation time is protected, and an event may begin before a fortification exists.

Time complexity is $O(n+A+B+WT)$ and space complexity is $O(n+A+B+WT)$ , with $W,T\le3000$ . Use 64-bit integers for losses, benefits, and DP values. Input arrays are released after their contents have been incorporated into the grids.
