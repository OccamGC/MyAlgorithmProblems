# Factorio: Circuit Board Test

## Algorithms and attribution

The preferred method is the problem setter's exact interval simplification; see [std.cpp](std.cpp). Codex (GPT-6) organizes the C++17 implementation and large-input boundary checks. The interval is already given in the setter's assertion and editorial.

[Safe direct predicate evaluation](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), is retained as a backup. It follows the conditions individually after restricting the range enough to make integer products safe.

## Simplify the conditions

Predicate $p(x)$ first gives $x>0$ . Squares and cubes are strictly increasing on positive integers.

Since $3^2=9<10\le4^2=16$ , the condition $x^2\ge10$ is equivalent to $x\ge4$ .

Since $14^3=2744<3000<3375=15^3$ , the condition $x^3<3000$ is equivalent to $x\le14$ .

Together these give $4\le x\le14$ . Throughout this interval, $16\le x^2\le196<700$ , so $h(x)$ is always true.

Therefore

$$P(x)\iff4\le x\le14$$

## Correctness and implementation

The first two predicates force every accepted value into this interval, and every value inside it satisfies all three predicates. Both necessity and sufficiency hold, so two endpoint comparisons suffice.

Read $x$ as a signed 64-bit integer. The test needs no square, cube or absolute value, making it safe over the full $|x|\le10^{18}$ range without floating-point tolerances.

Each test takes $O(1)$ time. Including input and empty-test handling, total time is $O(T+1)$ and auxiliary space is $O(1)$ .

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
| [Interval simplification](std.cpp) | 0.027496 | 5.32 | Measured inputs pass |
| [Safe direct evaluation](alternative.cpp) | 0.028904 | 5.32 | Measured inputs pass |

The limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R16.json) for all runs and input/source/binary hashes. Recalibrate on other judges. These measurements describe the supplied implementations and measured inputs.
