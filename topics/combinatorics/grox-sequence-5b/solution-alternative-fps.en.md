# Grox's Sequence V B: an exponential generating function

**Codex (GPT-6): apply the exponential generating function of binomial moments and formal-series log/exp.** Generating functions, Newton iteration and NTT are established methods, not inventions of this problem. The [program](alternative-fps.cpp) uses a substantially different derivation from the [Stirling-convolution reference](solution.en.md). The latter uses fewer operations and can truncate to needed terms, so it remains preferred.

## Extract the moment directly

For $k>0$ , the formal exponential gives

$$\sum_{i=0}^n\binom ni e^{iz}=(1+e^z)^n$$

Thus the answer is

$$S=k!\,[z^k](1+e^z)^n$$

Here $[z^k]$ extracts the coefficient of degree $k$ . The zero-index term contributes zero to a positive power, matching the statement. For $k=0$ , return $2^n-1$ separately rather than using the generating function's constant term.

Normalize the constant term to one:

$$H(z)=\frac{1+e^z}{2},\qquad H(0)=1,\qquad (1+e^z)^n=2^n\exp\big(n\log H(z)\big)$$

Construct the first $k+1$ coefficients of $e^z$ from inverse factorials, calculate $F=n\log H$ , then $G=\exp F$ . The answer is $2^n k!G_k$ . Keep only terms of degree at most $k$ throughout.

## Formal-series implementation

Inverse precision doubles: if $AU=1\pmod{z^m}$ , use

$$U_{\mathrm{next}}=U(2-AU)\pmod{z^{2m}}$$

The new error is the square of the old one. For a series with constant term one, use

$$\log A=\int\frac{A'}A\,dz$$

with integration constant zero. If $G=\exp F\pmod{z^m}$ , use

$$G_{\mathrm{next}}=G(1+F-\log G)\pmod{z^{2m}}$$

The error $F-\log G$ starts at degree $m$ . The linear correction cancels it, while quadratic terms start at degree $2m$ , proving the new precision. Products use NTT or naive multiplication at fixed small sizes.

## Correctness and applicability

The binomial theorem establishes the generating function; its degree-$k$ exponential coefficient is the positive-power moment divided by $k!$ . Normalization and the log/exp identity preserve the formal series. Precision-doubling iterations recover the required coefficient exactly, and multiplication by $2^n k!$ gives the answer.

For the fixed prime $P=1005060097$ , $k<P$ , so inverse factorials, integer integration denominators and the inverse of $2$ exist. Series inversion has a nonzero constant term; log input has constant term one and exp input has constant term zero. The largest NTT length is $2^{18}$ , dividing $P-1$ . This division-based implementation cannot be transferred directly to V A's arbitrary composite modulus.

## Complexity and tradeoffs

The precision-doubling costs sum over geometrically increasing polynomial multiplications. Total time is $O(k\log(k+1)+\log(n+1))$ and space is $O(k+1)$ . These match the untruncated Stirling convolution asymptotically, but repeated inversion, log and exp have larger constants. The preferred method can reduce work further when $m=\min(n,k)$ is small. This option supplies a different complete derivation and program; measurements determine whether it meets the current limit, since matching asymptotic bounds alone do not establish that.

## Same-input measurements

Both programs agree on all 10 formal inputs. Five alternating timing runs and input, source and binary hashes are in the [full record](../../../docs/benchmark-R14-supplements.json); see the [reference environment](../../../docs/评测环境与性能.md). Largest per-input median times are 0.124843 seconds for the reference and 0.637622 seconds for this option. Peak working sets are 9.89 and 14.93 MiB respectively, including process/runtime overhead.
This implementation exceeds the 0.5-second indicative limit on cases 04, 05, 06, 07, 08, 09. It is therefore a **backup option that does not pass the measured full data under the current limit**. Algorithmic correctness and timing applicability are separate; this implementation cannot serve as the current reference.
