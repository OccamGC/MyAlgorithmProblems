# Block Tower

## Algorithms and attribution

The preferred method is the problem setter's Hanoi recursion, using the accompanying editorial's direct block-index parameter. See [std.cpp](std.cpp). Codex (GPT-6) organizes complete-line input and output formatting. No arrays simulating the platform stacks are required.

[Generating moves by step number](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), is a backup with the same asymptotic cost and a different construction. It applies established Hanoi move patterns to compute the block and platforms; those patterns are not attributed as a model invention.

## Initial positions define the ordering

Index blocks $0,1,\ldots,n-1$ from bottom to top. A larger index may only be placed above a smaller one. Names are output labels and must not be sorted.

Define $\operatorname{Move}(i,a,b,c)$ to transfer blocks $i$ through $n-1$ from platform $a$ to $b$ , using $c$ . If $i=n$ , do nothing. Otherwise:

1. Call $\operatorname{Move}(i+1,a,c,b)$ .
2. Move block $i$ from $a$ to $b$ and print the instruction.
3. Call $\operatorname{Move}(i+1,c,b,a)$ .

Start with $\operatorname{Move}(0,0,1,2)$ , where platform indices follow input order.

## Legality and optimality

Induct on tower height. First transfer the upper tower legally. The bottom block can then move to the target, followed by the upper tower, yielding the required state.

Let $F(k)$ be the minimum moves for $k$ blocks. Before the bottom block first moves, all other $k-1$ blocks must be transferred to the one remaining platform. After its last move into the target, the upper tower must still reach that target. Thus at least $2F(k-1)+1$ moves are required. The recursive construction attains this bound.

$$F(0)=0,\qquad F(k)=2F(k-1)+1=2^k-1$$

Equality requires the bottom block to move once and both subproblems to be optimal. Induction also proves uniqueness of the shortest sequence of block identities on three platforms. Repeated names still give a determined output text.

## Strings and complexity

After reading $n$ , discard the remainder of that line, then read each name with `getline` . Do not tokenize names or trim leading or trailing spaces. Insert complete names into the output template, preserving both their spaces and the template's spaces.

Let $H$ count input name characters and $Z$ count output characters. Time is $O(H+Z+n)$ , with $2^n-1$ emitted moves. Names and the recursion stack use $O(H+n)$ space. The current upper bound produces $1023$ moves.

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
| [Hanoi recursion](std.cpp) | 0.029726 | 5.31 | Measured inputs pass |
| [Step-number construction](alternative.cpp) | 0.031369 | 5.30 | Measured inputs pass |

The limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R16.json) for all runs and input/source/binary hashes. Recalibrate on other judges. These measurements describe the supplied implementations and measured inputs.
