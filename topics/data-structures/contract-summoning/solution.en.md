# Contract Summoning — Solution

Credits: reachability closure and three-dimensional dominance queries come from the problem setter’s solution. Codex (GPT-6) uses static range trees sized to their buckets and supplies the space bound and correctness argument.

## Comparing solutions

### Problem setter’s solution: a Fenwick tree of dynamic segment trees

The problem setter’s program processes available characters with a queue to compute the closure of summonable NPCs. Each lookup is a three-dimensional dominance query for one character. After compressing the requirement coordinates, a Fenwick tree handles the first dimension. Each NPC is inserted into several Fenwick buckets, and a first-coordinate prefix query visits disjoint buckets.

Each bucket dynamically builds a segment tree over the global range of second-coordinate ranks. A leaf corresponds to one such rank and stores NPCs sorted by their third requirement, together with a cursor for unprocessed entries. Internal nodes store the smallest remaining third requirement. A second-coordinate prefix query skips subtrees whose minimum exceeds the character's third attribute. It consumes eligible prefixes of leaf lists, advances their cursors and updates minima. Each copy is consumed once, while a global visited flag prevents repeated queue insertion of an NPC.

The first-coordinate buckets and second-coordinate prefix retain exactly the candidates satisfying the first two conditions. Minima and sorted lists check the third. Consuming an NPC's first copy immediately enqueues it, so delayed consumption of other copies cannot hide an undiscovered NPC. The closure proof below applies to the problem setter’s method as well.

Each NPC has $O(\log(n+1))$ copies, and queries and updates follow paths in the inner segment trees, giving $O(n\log^2(n+1))$ total time. However, each copy can create $O(\log(n+1))$ dynamic nodes over the global second-coordinate range. The space bound is $O(n\log^2(n+1))$ , and the problem setter’s implementation reserves a node pool according to that bound.

### Static range trees used by Codex

The Codex implementation uses a static segment tree for the first coordinate. Within each bucket, it sorts copies by their second requirement and builds a compact minimum segment tree over **only the copies actually in that bucket**. A bucket of size $s$ needs $O(s)$ space, and all buckets together need $O(n\log(n+1))$ . This removes the extra logarithmic space factor from opening inner-tree paths over the global coordinate range. Total time remains $O(n\log^2(n+1))$ .

The closure model, dominance queries and visited flags for duplicate suppression are inherited from the problem setter’s method. The benefit is the proven space bound and allocation based on actual bucket sizes. The Codex implementation still stores multiple copies and maintains inner trees; no comparison of speed or measured peak memory between the programs was performed.

## Summoning is a reachability closure

Initially the queue contains only the summoner. For each available character, find NPCs whose requirement triples are componentwise no larger than its attribute triple, and enqueue every newly discovered type once.

Characters are not consumed and attributes never change, so every feasible call stays feasible. Every queued NPC has a valid summoning step. Conversely, the direct caller of any reachable NPC will eventually be processed, so the NPC will be discovered.

Taking separate maxima of the available characters' attributes is invalid: it can assemble the abilities of different characters into a summoner that does not exist.

## Decompose the first-coordinate prefix

Sort NPCs by their first requirement and build a static segment tree over their positions. Store one copy of each NPC in every node on its leaf-to-root path, giving $O(\log(n+1))$ copies per type.

For attributes $(F,I,S)$ , all positions with first requirement at most $F$ form a prefix. Decompose it into $O(\log(n+1))$ disjoint complete tree nodes, and query only their buckets.

## Search the remaining two coordinates

Within each bucket, sort NPCs by their second requirement. Build another segment tree whose leaves store third requirements and whose internal nodes store minima.

Binary-search the prefix whose second requirement is at most $I$ . Search that prefix for a leaf with third requirement at most $S$ : skip intervals outside the prefix or with minimum greater than $S$ , and otherwise descend to a qualifying leaf.

After finding a leaf, set **this copy in the current bucket** to infinity and update its ancestor minima. If the NPC is unseen, mark and enqueue it; otherwise do not enqueue it again. Repeat until the bucket has no eligible copy.

There is no need to delete all its other copies immediately. Delete those lazily when encountered; the visited flag prevents repeated summons. Each copy is removed at most once.

## Correctness and complexity

The first-coordinate decomposition selects exactly the strength-eligible positions. The bucket prefix filters intelligence, and the minimum search filters spirit. Every reported NPC therefore meets all three requirements.

An undiscovered NPC cannot have any deleted copy: the first deletion of any copy would have enqueued it. Thus lazy removal of other copies cannot hide an undiscovered NPC. Together with the closure argument, this proves the final count.

For preprocessing, globally sort by the second requirement, then append each NPC along its first-coordinate ancestor path. Every bucket is then already sorted. All bucket segment trees together occupy $O(n\log(n+1))$ space.

Each available character visits $O(\log(n+1))$ buckets. A prefix search or deletion within a bucket costs $O(\log(n+1))$ , and only $O(n\log(n+1))$ copies can ever be deleted. There are at most $n+1$ processed characters, giving $O(n\log^2(n+1))$ total time and $O(n\log(n+1))$ space. The bound uses neither random balancing nor heuristic pruning.

The infinity sentinel must exceed every legal attribute. Identical requirement triples remain separate leaves because distinct NPC types count separately.

## Validation

An independent model scans every NPC for each processed character and computes the closure directly. Tests cover the invalid attribute-aggregation shortcut, equality, zero attributes, duplicates, no reachable NPC and reversed long chains. Formal cases also include reporting every NPC in one query.

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.
