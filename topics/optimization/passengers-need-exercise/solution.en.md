# Passengers Need More Exercise: Solution

## Comparing solutions

The problem setter’s method enumerates interval endpoints and positions aligning a passenger with the midpoint of two adjacent doors. Between consecutive candidates, each passenger keeps the same nearest door, giving an absolute-value distance function. Their sum is convex, so its maximum and leftmost optimal position can be attained at a candidate. For each candidate, a two-pointer scan of ordered passengers and doors computes the sum of nearest-door distances. The convexity proof below preserves this reasoning.

Every candidate coordinate is an integer or half-integer. The implementation by Codex (GPT-6) doubles coordinates and compares total distances and leftmost positions exactly as integers, avoiding tolerance-dependent ties. With $M$ passengers and $N$ doors, candidate evaluation takes $O(MN(M+N))$ time and $O(M+N)$ space.

## Candidate positions

For one passenger, the nearest door can switch only when two adjacent doors are equally distant:

$$S=P_i-\frac{D_j+D_{j+1}}{2}$$

Between these switch points, the passenger's nearest-door distance is an absolute-value segment. Aligning a door with the passenger makes an upward corner (a local minimum); equal distances to adjacent doors may make a downward corner (a local maximum). The sum is linear on all other intervals. Thus the maximum, including its leftmost location in case of a tie, occurs at $0$ , $L-D_N$ , or one of the switch points.

Double every coordinate. All candidate positions, individual distances, and totals are then integers, so 64-bit integer arithmetic compares values and breaks ties exactly.

In the implementation, `PassengerPositions` and `DoorOffsets` store the passenger positions $P_i$ and door offsets $D_j$ at their original input scale. They are doubled when computing distances; `TwiceStart` stores twice the first door's stopping coordinate, $2S$ .

## Evaluating a candidate

Passenger positions are sorted. Scan them in order while maintaining the index of a nearest door. As passenger position increases, that index never decreases, so evaluating one candidate takes $O(M+N)$ time. Either door may be chosen on an equal-distance tie.

Enumerate at most $M(N-1)+2$ candidates, evaluate the total distance, then prefer a smaller $S$ when totals are equal.

## Correctness

Keep only candidates in the allowed interval and use them to partition it. Between consecutive candidates, each passenger keeps the same nearest door, so its distance is an absolute-value function. The total is therefore convex: no interior value exceeds the larger endpoint value. If an interior point attains the global maximum, at least one endpoint does too. If the left endpoint were smaller, convexity would put that interior value strictly below the right endpoint, a contradiction. Thus the leftmost optimum is a candidate. Exact evaluation and the specified tie rule select the correct answer.

## Complexity

There are $O(MN)$ candidates, each evaluated in $O(M+N)$ time, for $O(MN(M+N))$ total time and $O(M+N)$ space. The doubled total distance is at most $2ML$ and fits in signed 64-bit arithmetic.
