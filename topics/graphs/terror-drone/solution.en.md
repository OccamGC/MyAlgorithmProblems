# Terror Drone: Solution

## Comparing solutions

The problem setter’s method first labels four-connected obstacle groups, then runs BFS on $(x,y,a,c)$ , where $a$ is the previous movement axis and $c$ is the removed group, including no removal. Every move changes axis, and only the chosen group becomes passable. A separate reachability check distinguishes the two specified failure outcomes. For fixed $c$ , these are exactly the BFS transitions below; unit edge lengths make first arrival optimal.

The problem setter’s program stores distances for all choices of $c$ simultaneously. For $V$ cells and $C$ obstacle groups, both time and space are bounded by $O((C+1)V)$ . The implementation used by Codex (GPT-6) processes choices separately and reuses position-and-axis buffers. Time is unchanged and working space falls to $O(V)$ . The improvement concerns simultaneously stored states; component enumeration and alternating-axis BFS are inherited.

## Expressing the chase as a path

Fix the bombing choice. Let the fortress path be $v_0,v_1,\ldots,v_t$ , where $v_0$ is the start and $v_t$ is the first trap reached. Drop the drone at $v_1$ . Before the fortress reaches $v_i$ , the drone moves from $v_i$ to $v_{i+1}$ . Finally, it stays at $v_t$ until the fortress enters.

One drone suffices exactly when every two consecutive moves $v_{i-1}\to v_i$ and $v_i\to v_{i+1}$ lie on different straight lines. Group the eight directions into four undirected axes: vertical, horizontal, and the two diagonals. Consecutive steps must use different axes. No turn is required after the final move, because capture has already ended the attempt.

## Reverse search from all traps

A state $(u,a)$ records a cell $u$ and the axis $a$ of the preceding step. Reversing a path preserves the condition that consecutive axes differ.

Initialize all four states of every trap with distance $0$ . This allows the first reverse step to use any axis. From $(u,a)$ , visit a traversable neighbor $v$ if the connecting axis $b$ differs from $a$ , entering state $(v,b)$ at one greater distance. A multisource BFS gives shortest distances. The minimum over the four states of a starting cell is the minimum number of fortress moves using one drone for this bombing choice.

Initializing all axes at a trap does not represent an actual move. It expresses that the first step is unrestricted: any nonempty reverse path can choose an initial axis different from its first step.

## Several drones or no route

With replacement drones, any traversable eight-neighbor path is possible. Drop a drone at the next cell and let it stay; repeat if needed. Conversely, every fortress move must follow an edge of this traversable grid.

Run an ordinary eight-neighbor search from all traps as well. If no direction-state route exists but ordinary reachability holds, this bombing choice requires several drones.

Label obstacle components using four-neighbor connectivity. Enumerate removing no component and removing each individual component, rerunning both searches. If any choice admits one drone, take the smallest distance. Otherwise output `-2` if any choice is ordinarily reachable, and `-1` if none is.

## Correctness

The chase rules are equivalent, step by step, to consecutive path edges having different axes, with a final sacrifice permitted. Thus direction-state paths and one-drone strategies correspond and preserve length. BFS finds the shortest one for each bombing choice. Ordinary connectivity is equivalent to feasibility with replacement drones. All permitted bombing choices are enumerated, and one-drone strategies take priority as required, proving correctness.

## Complexity and implementation

Let $V=nm$ and let $c$ be the number of obstacle components. Each search has $O(V)$ states, each checking at most eight neighbors. Total time is $O((c+1)V)$ and auxiliary space is $O(V)$ . Search arrays are reused between bombing choices.

Diagonal movement checks only the destination. Obstacles use four-neighbor components, while both searches use eight-neighbor movement. With no traps, both initial queues are empty, so every start correctly receives `-1` .
