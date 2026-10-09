# Simple Analysis

## Algorithm and attribution

Problem setter's solution: count significant binary digits and set bits. Codex (GPT-6) specifies the exponent-reduction boundary and organizes the implementation and checks, retaining the counting algorithm. Program: [std.cpp](std.cpp).

## Reduction preserves the exponent

The guarantee $0\le e<\text{modulus}-1$ means that reducing the initial exponent leaves it equal to $e$ . The auxiliary parameter values cannot affect the loop count. Count calls to `multiply` , rather than arithmetic instructions inside the multiplication module.

## Count the two call sites

An all-zero string represents zero. The loop never executes, so the answer is zero.

Otherwise, discard leading zeros. Let $L$ be the remaining number of digits and $w$ their number of set bits. The loop examines digits from least to most significant. Each set bit triggers one multiplication into the result, giving $w$ calls.

The exponent shifts right once per iteration. It remains positive after the first $L-1$ shifts, each of which triggers a squaring call. The final shift makes it zero and triggers no squaring. Hence the answer is

$$L+w-1$$

These counts cover both call sites in the pseudocode, without overlap.

## Implementation and complexity

Read and scan one string at a time. Start counting significant digits at the first $1$ , while also counting set bits. No conversion to a machine integer, modular reduction or actual multiplication is needed.

Let $S$ be total string length and $B$ the maximum string length. Time is $O(S+Q+1)$ and the supplied implementation uses $O(B+1)$ space. A positive exponent has at most $2L-1$ calls; the maximum here is $4199999$ , which fits in a signed 32-bit integer.

The rule “one per significant zero, two per one, then subtract one” expresses the same identity and is not a separate algorithm. Literal loop execution provides a small-case oracle; repeatedly shifting large integers is unnecessary for long strings.

## Verification and Use

Fixed-seed input recipes are in `tests/plan.json` . Compile a program, then run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs; `--case 01` selects one case. See [independent verification](../../../tools/check_r15_followup.py), [five-round timings, memory and hashes](../../../docs/benchmark-R15-followup.json), and the [environment](../../../docs/评测环境与性能.md).

Independent checks simulate each conditional multiplication and squaring for every nonempty binary string of length at most ten and additional random strings. Stress inputs cover maximum total length, all zeros, all ones, a single set bit and many short queries.

## Measured Results

Each program ran five times on the same ten formal inputs, using an Intel Core Ultra 9 275HX, Windows 11, GCC 16.2.0 and C++17 `-O2` . Time is the largest per-input median, including process startup and input/output. Memory is the separately measured peak working set, including runtime overhead.

| Program and algorithm | Largest median (seconds) | Peak (MiB) | 0.5-second reference limit |
| --- | ---: | ---: | --- |
| [Significant-digit and set-bit counting](std.cpp) | 0.108609 | 9.95 | Measured inputs pass |

The reference limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R15-followup.json) for all runs and input/source hashes. Recalibrate on other judge machines.
