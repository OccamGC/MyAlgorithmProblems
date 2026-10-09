# Factorio: Simple Rail Network

## Algorithms and attribution

The preferred method is the problem setter's nonpositive-edge contraction followed by Kruskal; see [std.cpp](std.cpp). Codex (GPT-6) uses union by size and iterative path compression, and handles loops, parallel edges, empty edge sets and 64-bit cost accumulation.

The supplementary [alternative.cpp](alternative.cpp) applies the established Borůvka algorithm to the contracted components. See [minimum outgoing edges by component](solution-alternative.en.md). It is a backup with a different merging strategy: the reference sorts edges, while the alternative scans them in rounds.

## Select nonpositive edges first

Every negative edge must be selected: adding an omitted negative edge preserves connectivity and strictly lowers cost, even if it is a self-loop or creates a cycle.

Selecting every zero-cost edge also does not increase cost. Accumulate the cost of all $w_i\le0$ edges and unite their endpoints. Treat each resulting component as one contracted vertex.

All remaining edges have positive cost. Any cycle in a connected choice between contracted vertices can lose an edge while staying connected and lowering cost. Therefore the optimal additional edges form a minimum spanning tree of the contracted graph.

## Kruskal and correctness

Sort positive edges by increasing cost. Select an edge precisely when its endpoints are in different disjoint-set components, then add its cost and unite them. Skip other edges.

Each selected edge is a minimum available edge across the cut of a current component. If an optimal spanning tree omits it, adding it creates a cycle containing another edge across that cut, of no smaller cost. Exchanging those edges does not increase cost. Every choice can therefore be extended to an optimal spanning tree.

If one component remains, the nonpositive total plus the tree cost is optimal. If several remain, no candidate edge can connect them, so print `bad idea` .

## Complexity and numeric safety

Let $\alpha(n)$ denote the inverse Ackermann function from disjoint-set analysis. Time is $O(n+m\log(m+1)+m\alpha(n))$ and space is $O(n+m)$ , including initialization and empty-edge cases.

The sum of absolute edge costs is at most $2\times10^{15}$ , so use signed 64-bit accumulation. A single vertex can still have negative loops worth selecting. With no edges, only $n=1$ is feasible. Positive loops never connect different components and are skipped. Disjoint-set lookup is iterative, and roots are joined by size.

## Verification and Use

Ten fixed-seed formal recipes are in `tests/plan.json` . Compile the program, then run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate inputs only; `--case 01` selects one case. See [independent small checks](../../../tools/check_r16.py), [input validation](../../../tools/validate_r16.py), the [five-round timing, memory and hash record](../../../docs/benchmark-R16.json), and the [environment and calibration method](../../../docs/评测环境与性能.md).

## Measured Results

Intel Core Ultra 9 275HX, Windows 11, GCC 16.2.0 and C++17 -O2. Both programs ran for five alternating rounds on the same ten formal inputs. Time is the largest per-input median, including startup and I/O. Peak working sets were measured separately and include runtime overhead.

| Program and algorithm | Largest median (seconds) | Peak (MiB) | 1.5-second reference limit |
| --- | ---: | ---: | --- |
| [Nonpositive contraction and Kruskal](std.cpp) | 0.710041 | 35.69 | Measured inputs pass |
| [Nonpositive contraction and Borůvka](alternative.cpp) | 0.747512 | 39.52 | Measured inputs pass |

The limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R16.json) for all runs and input/source/binary hashes. Recalibrate on other judges. These measurements describe the supplied implementations and measured inputs.
