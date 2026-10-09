# Counting Paired DNA Strands over a Length Range

**Codex (GPT-6) contributions:** count fixed reverse-complement representations, derive length-prefix sums, and implement division-free geometric block merging. The counting uses the classical orbit partition of an involution, not a newly invented method.

## A fixed length

Let $q=2K$ . Reverse complementation applied twice returns the original string, so each class has one or two representations. An odd-length string cannot be fixed, because its middle letter would have to complement itself. At even length $t=2h$ , the first half is arbitrary and determines the second half, giving $q^h$ fixed representations.

Each fixed representation forms one class; all others form pairs. Thus

$$F(t,K)=\frac{q^t+[2\mid t]q^{t/2}}{2}$$

Brackets denote one when the condition holds and zero otherwise. The modulus $P=1000000007$ is an odd prime, so division by two is multiplication by $500000004$ .

## Prefixes of lengths

Define $G(h)=\sum_{i=1}^{h}q^i$ and $G(0)=0$ . Summing the fixed-length formula gives

$$H(n)=\sum_{t=1}^{n}F(t,K)=\frac{G(n)+G(\lfloor n/2\rfloor)}{2}$$

Set $h=\lfloor n/2\rfloor$ , $p=q^h$ , and $s=G(h)$ . We have $G(2h)=s(1+p)$ ; for odd size, add $q^{2h+1}=p^2q$ . Therefore

$$H(n)=\frac{s(p+2)+[2\nmid n]p^2q}{2}$$

The interval answer is $H(R)-H(L-1)$ , normalized modulo the modulus. This also gives $H(0)=0$ .

## Division-free geometric blocks

A block of length $h$ stores $(p,s)=(q^h,G(h))$ . Appending a length-$b$ block to a length-$a$ block gives

$$p_{a+b}=p_ap_b,\qquad s_{a+b}=s_a+p_as_b$$

Starting with empty block $(1,0)$ and unit block $(q,q)$ , merge and double according to the binary digits of the length. This computes any $(q^h,G(h))$ . Every identity holds modulo $P$ , even when $q\equiv1\pmod P$ , without a special case.

Fixed-representation counting proves the single-length formula. The block invariant proves each merge correct, and subtracting prefixes gives the required interval count. Each query takes $O(\log(R+1))$ time and $O(1)$ auxiliary space. Streaming all queries takes total time $O(\sum\log(R+1))$ . Use 64-bit modular products; a product of two reduced values is below approximately $10^{18}$ .

[Closed-form geometric sums](solution-alternative.en.md) give another method of the same asymptotic order; see the [program](alternative.cpp). It uses fewer block variables but needs a modular inverse per query or a special-ratio case. Both programs pass the complete data.

## Implementation and validation

[Standard program](std.cpp), [generator](tests/generate.py), and [test recipes](tests/plan.json).

The slowest standard-program median in the reference environment is 0.076774 seconds, with peak working set 5.32 MiB, and calibrated limit 0.5 seconds. Each case has five independent timing runs.

See the [evaluation environment](../../../docs/评测环境与性能.md) and [individual timings and hashes](../../../docs/benchmark-R31.json). Measurements apply to that environment; recalibrate on another judge.
