# Paper Tiger Sequence

## Algorithms and attribution

The preferred algorithm is the problem setter's shared-suffix storage; see [std.cpp](std.cpp). Codex (GPT-6) sizes the length table from the input, allocates the exact final character range, and specifies the cyclic-copy boundaries.

[Interval backtracking with a bounded cache](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), is a parallel option with less character storage. Shared suffixes give linear construction time; backtracking trades interval decomposition for a small cache.

## Every version shares one suffix

An operation only adds a prefix. Thus $S_i$ is a suffix of $S_{i+1}$ and of the final string $S_N$ . Write $L_i=|S_i|$ and precompute

$$L_i=L_{i-1}+\left\lceil\frac{L_{i-1}}5\right\rceil$$

Allocate $L_N$ characters and place the initial string in $[L_N-L_0,L_N)$ . Version $i$ will always occupy $[L_N-L_i,L_N)$ , so no historical copies are needed.

## Copying an added prefix

Suppose the current version starts at $b$ and has length $L$ , and the new prefix has length $D$ . Write

$$\mathrm{Text}[b-D+k]=\mathrm{Text}[b+(p_i+k)\bmod L],\qquad 0\le k<D$$

Every destination is left of $b$ , while every source is inside the current version. The ranges do not overlap, so copying cannot read newly added characters. The new start is $b-D$ .

## Correctness

The initial suffix is correct. Assuming the current suffix is correct, the formula writes the complete new prefix in the required cyclic order and preserves the existing suffix. The resulting suffix is therefore the next version. Induction proves every version. For query $q$ , output exactly $L_q$ characters starting at $L_N-L_q$ .

## Complexity and boundaries

Let $Z$ count all output characters, including newlines. Initial characters plus all additions total exactly $L_N$ . Time is $O(N+L_N+Z+1)$ and space is $O(N+L_N)$ . Existing characters never need to be shifted.

The length table needs $N+1$ entries, including version $0$ . Starting with the maximum length $10$ and applying the recurrence $70$ times gives maximum final length $4055267$ . This follows from the length recurrence and avoids an oversized fixed allocation. Distinct queries produce at most $24331433$ string characters, plus newlines.

For $N=0$ , queries refer to the initial version. For $M=0$ , there is no output. Reduce $p_i$ modulo the pre-growth length, and wrap within that same version.

## Verification and Use

Ten fixed-seed formal recipes are in `tests/plan.json` . Compile the program, then run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate inputs only; `--case 01` selects one case. See [independent small checks](../../../tools/check_r16.py), [input validation](../../../tools/validate_r16.py), the [five-round timing, memory and hash record](../../../docs/benchmark-R16.json), and the [environment and calibration method](../../../docs/评测环境与性能.md).

## Measured Results

Intel Core Ultra 9 275HX, Windows 11, GCC 16.2.0 and C++17 -O2. Both programs ran for five alternating rounds on the same ten formal inputs. Time is the largest per-input median, including startup and I/O. Peak working sets were measured separately and include runtime overhead.

| Program and algorithm | Largest median (seconds) | Peak (MiB) | 0.5-second reference limit |
| --- | ---: | ---: | --- |
| [Shared suffixes](std.cpp) | 0.070396 | 9.04 | Measured inputs pass |
| [Interval backtracking with bounded cache](alternative.cpp) | 0.069889 | 5.36 | Measured inputs pass |

The limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R16.json) for all runs and input/source/binary hashes. Recalibrate on other judges. These measurements describe the supplied implementations and measured inputs.
