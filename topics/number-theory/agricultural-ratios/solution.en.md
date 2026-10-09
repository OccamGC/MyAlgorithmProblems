# Harvest Office — Solution

## Comparing solutions

The problem setter’s solution converts finite and repeating decimals exactly into fractions. Finite digits use powers of ten; a repeating part uses denominator $10^f(10^r-1)$ , where $f,r$ are the nonrepeating and repeating lengths. It adds the parts, reduces each fraction, and takes the LCM of reduced denominators. An integer multiplier works exactly when each reduced denominator divides it, so the proof below also covers the problem setter’s method.

The problem setter’s program provides base-$10^9$ big integers and trial-quotient division. The implementation used by Codex (GPT-6) uses more direct decimal big-integer operations and clarifies parsing of zeros, leading zeros and repeats. Both use schoolbook multiplication/division and Euclidean GCD. For maximum intermediate decimal length $D$ , a conservative bound is $O(nD^3)$ time and $O(D)$ arithmetic workspace. Changing the base changes constants and does not establish a speed gain. The benefits are portable exact arithmetic and explicit boundaries; the mathematical model is unchanged.

## Convert the decimal exactly

Do not parse a ratio with floating point. Let $f$ be the number of fractional digits in the finite prefix and $r$ the repeating-part length. Remove the decimal point from the prefix to obtain integer $A$ , then append the repeating digits to obtain integer $B$ . The value is

$$x=\frac{B-A}{10^f(10^r-1)}$$

Indeed, $10^f x$ and $10^{f+r}x$ have the same infinite fractional tail, so subtracting gives $B-A$ . This works for zero periods, leading zeros, and repeating $9$s. For example, `0.7 142857` gives $(7142857-7)/(10(10^6-1))=5/7$ .

Reduce the fraction using its greatest common divisor to obtain $x=u/v$ . A zero numerator needs no special mathematical rule: $\gcd(0,v)=v$ , so its reduced denominator is $1$ .

## Take the least common multiple of denominators

Since $u,v$ are coprime, $Hx$ is integral exactly when $v\mid H$ . Thus the answer is the least common multiple of all reduced denominators. Update it with

$$H\leftarrow\frac{H}{\gcd(H,v)}\,v$$

These divisibility conditions are sufficient as well. The listed crop quantities are integers whose sum is at most $H$ . The remainder $H-\sum_i Hr_i$ is also a nonnegative integer and can be assigned to unlisted crops. Starting from $H=1$ yields the smallest feasible positive total.

## Arbitrary-precision implementation

The answer can exceed 64 bits. The reference uses standard C++17 only, implementing nonnegative decimal big integers with comparison, subtraction, multiplication, quotient, and remainder.

Long division reads the dividend from its most significant digit. For each digit, multiply the remainder by ten, add the digit, and repeatedly subtract the divisor to find the next quotient digit. The previous remainder was smaller than the divisor, so at most nine subtractions are needed. This loop does not grow linearly with the represented value. Divisors are nonzero; Euclid's algorithm checks its second argument before dividing.

Let $D$ be the maximum decimal digit count of an intermediate integer and $L$ the maximum input length of one ratio. Then $D=O(nL)$ . Schoolbook multiplication and one long division take $O(D^2)$ time. Every two Euclidean iterations at least halve the larger argument, giving at most $O(D)$ iterations. A conservative overall bound is $O(nD^3)$ time and $O(D)$ space. Digit counts remain symbolic rather than being replaced by the numeric input limit.

## Verification

An independent Python exact-fraction implementation adds the finite prefix and repeating geometric series separately, then takes the LCM of the denominators. It also checks every official output, covering zero shares, repeating nines, repeated periods, long finite prefixes, and long repeating parts.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
