# Recursive Statistics

## Algorithms and attribution

The preferred algorithm uses differences and a multiples sieve; see [std.cpp](std.cpp). Codex (GPT-6) derives a proper-divisor recurrence from this problem's recurrence and applies the established multiples-sieve technique.

The problem setter's solution uses quotient blocks with incremental memoization. See the [complete explanation](solution-alternative-quotient-blocks.en.md) and [alternative-quotient-blocks.cpp](alternative-quotient-blocks.cpp). It evaluates the recurrence directly and reads queries as a stream. The difference algorithm improves the asymptotic preprocessing time, while its supplied implementation stores the queries.

## Differences of consecutive arguments

All calculations for positive arguments are modulo $P=998244353$ . Set $F(0)=0$ and define

$$D(n)=F(n)-F(n-1)\pmod P\qquad(n\ge1)$$

Compare $F(n)$ with $F(n-1)$ . For $i\ge2$ , the value $\lfloor n/i\rfloor$ increases from $\lfloor(n-1)/i\rfloor$ exactly when $i$ divides $n$ . The newly introduced term $i=n$ follows the same rule because $F(0)=0$ . Thus

$$D(n)=1+\sum_{\substack{i\mid n\\i\ge2}}D(n/i)=1+\sum_{\substack{d\mid n\\d<n}}D(d)\pmod P$$

In particular, $D(1)=1$ . This identity uses only nonnegative arguments. Negative queries are returned directly and do not enter the sieve.

## Updating multiples

Let $N$ be the largest positive query, or $N=0$ if none exists. Initialize every $D(n)$ to $1$ . Process $d=1,\ldots,N$ in increasing order, adding its finalized value to $D(2d),D(3d),\ldots$ . Recover answers with prefix sums:

$$F(n)=\sum_{d=1}^{n}D(d)\pmod P$$

Reduce after each addition. The sum of two residues is smaller than $2P$ and fits in a signed 32-bit integer. Delaying reduction requires a separate bound on intermediate values.

## Correctness

Before processing $d$ , all its proper divisors have already been processed and have contributed exactly once. Its stored value therefore equals the difference recurrence. Induction establishes every difference. Summing the differences telescopes to $F(n)$ . Returning each nonpositive query unchanged handles the remaining cases.

## Complexity and tradeoffs

There are $\sum_{d=1}^{N}(\lfloor N/d\rfloor-1)$ updates. Total time is $O(N\log(N+1)+Q+1)$ , and the supplied implementation uses $O(N+Q+1)$ space. Quotient blocks take $O(N\sqrt{N}+Q+1)$ time and $O(N+1)$ space.

The difference algorithm is the reference because of its lower preprocessing time bound. Quotient blocks remain a parallel option with a different time/space tradeoff that does not store all queries. Measurements and applicability under the current limit appear below.

## Verification and Use

Direct summation of every denominator checks empty queries, negative values, repeated queries and increasing/decreasing arguments. Full-size inputs are also compared against quotient blocks.

The ten input recipes, fixed seeds and purposes are in `tests/plan.json` . After compiling the program, run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs, or use `--case 01` to select one input. Independent checks are in [check_r15.py](../../../tools/check_r15.py). See the [five-round alternating measurements](../../../docs/benchmark-R15.json) and [environment](../../../docs/评测环境与性能.md). Finite tests and timings of these implementations supplement the proofs; they do not establish a time guarantee for every implementation with the same asymptotic bound.

## Measured Results

| Program | Largest per-case median | Peak working set |
| --- | ---: | ---: |
| Reference | 0.044081 s | 6.46 MiB |
| Alternative | 0.322212 s | 6.01 MiB |

The reference limit is 0.5 seconds. Both programs agree on all ten measured formal inputs and finish within this limit. Peak working set includes process overhead; maximum time and memory may come from different inputs.

Although quotient blocks have a higher asymptotic time bound, the current constraints and calibrated limit do not reliably exclude them. These measurements do not establish a separation between the algorithm classes.
