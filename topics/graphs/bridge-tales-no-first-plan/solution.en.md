# Bridge Tales: The First Plan Is Out — Solution

## Comparing solutions

The problem setter’s method builds an MST with Kruskal, then considers each non-tree edge and removes the largest strictly smaller weight on its tree path. Its binary-lifting tables maintain the largest and second-largest distinct weights. Handling equal weights requires the second distinct value. The exchange argument and the sufficiency of these two values are proved below for both implementations.

If no removable edge exists, skip the candidate: simply adding the new edge weight to the MST total leaves a cycle. The implementation by Codex (GPT-6) uses this check, 64-bit totals and explicit traversal. For $n$ vertices and $m$ edges, time is $O(m\log(m+1)+(n+m)\log(n+1))$ and space is $O(m+n\log(n+1))$ .

## Idea

First find a minimum spanning tree $M$ using Kruskal's algorithm, and let its weight be $W_{\min}$ . Adding a non-tree edge $(u,v,w)$ to $M$ creates a cycle. Remove one edge of weight $x$ from the $u$–$v$ path in $M$ to obtain a tree of cost $W_{\min}+w-x$ .

To make the new cost strictly greater than $W_{\min}$ but as small as possible, remove the **largest path-edge weight strictly below $w$** . If the path maximum equals $w$ , removing an edge of that weight gives another minimum spanning tree and does not qualify. We then need the second-largest **distinct** weight. If no smaller weight exists, this non-tree edge yields no candidate.

## Path Queries

Use binary lifting on $M$ . For each vertex and each ancestor $2^j$ levels above it, store the two largest distinct edge weights on that path. Merge two paths by keeping the two largest distinct values among at most four candidates. Each non-tree edge then needs an $O(\log n)$ path query.

Enumerate all non-tree edges, compute every strictly larger candidate, and take the minimum. Traverse the tree iteratively when building parent data so a path-shaped tree cannot overflow the call stack.

## Correctness

Let $T$ be any spanning tree with cost greater than $W_{\min}$ , and let $W(T)$ denote its total edge weight, or total cost. The spanning-tree exchange lemma pairs the edges in $T\setminus M$ with those in $M\setminus T$ so that each pair can be exchanged in $M$ to form a spanning tree. Because $M$ is minimum, every paired exchange has a nonnegative cost increase. Their increases sum to $W(T)-W_{\min}>0$ , so at least one exchange has a positive increase no larger than $W(T)-W_{\min}$ . In particular, the smallest strictly larger tree cost is attained by a single-edge exchange from $M$ .

For a fixed non-tree edge of weight $w$ , Kruskal's optimality ensures that no edge on its path in $M$ is heavier than $w$ . Removing the largest path weight $x<w$ gives the smallest positive increase for that non-tree edge. The two largest distinct path weights suffice to find it. Taking the minimum over all non-tree edges gives the answer.

## Complexity

Sorting and finding the minimum spanning tree take $O(m\log m)$ time; binary-lifting preprocessing takes $O(n\log n)$ ; all path queries take $O(m\log n)$ . Space is $O(n\log n+m)$ .
