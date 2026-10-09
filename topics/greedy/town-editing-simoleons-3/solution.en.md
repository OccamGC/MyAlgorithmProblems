# Edit Town and Simoleons 3: Per-Person Wealth Gaps

Codex (GPT-6) provides the optimality proof, closed formula, and implementation for two fixed household slots. The derivation uses only the stated moving rules.

## 1. Result

Write $k=p_1$ and $l=p_2$ . If $l=0$ , the answer is $m_1$ . Otherwise define

$$
a=\frac{m_1}{k},\quad b=\frac{m_2}{l},\quad N=k+l,\quad r=\min(k,l),\quad t=\max(k,l).
$$

If $a\ge b$ , doing nothing is optimal. Otherwise set

$$
D=\left\lfloor\frac{(N+1)^2}{4}\right\rfloor,\qquad \rho=1-\frac ND.
$$

The answer is

$$
W=\frac{k(m_1+m_2)}N+\frac{r^2}N(b-a)\rho^r.
$$

For $k=l=2,m_1=2,m_2=18$ , we have $\rho=1/3$ and answer $10+8/9=98/9$ .

## 2. The richer slot cannot become the poorer slot

Suppose fixed slots A and B currently have $s,N-s$ residents and per-person wealth $u,v$ . After one resident moves from A to B, A still has per-person wealth $u$ if it remains nonempty, while B has

$$
v'=\frac{(N-s)v+u}{N-s+1}.
$$

Thus the gap $v-u$ is multiplied by $(N-s)/(N-s+1)$ . A move from B to A multiplies it by $s/(s+1)$ . Both factors lie strictly between zero and one when both households remain nonempty.

If a household becomes empty, all residents have merged into the other one and have equal per-person wealth. Every later move preserves this common value.

Consequently the wealth order of the two slots cannot reverse, and the gap can only shrink. This is the key simplification specific to two households.

## 3. Choosing the final slot

If $a\ge b$ , A is initially at least as rich per person. With the targets back in A and its size restored to $k$ , the final gap cannot exceed the initial gap. With the targets in B, they occupy the poorer side. Neither case improves on $m_1$ .

Now assume $a<b$ . Targets ending in A can receive at most their share of global equal wealth, $k(m_1+m_2)/N$ . Merging everyone and then separating by identity attains this share.

If the targets end in B, all residents must exchange slots. Let $F$ be the fraction of the initial per-person gap that remains. A finally has $l$ residents and B has $k$ , so conservation of money gives

$$
W=\frac{k(m_1+m_2)}N+\frac{kl}N(b-a)F.
$$

It remains to maximize $F$ .

## 4. Bounding every possible schedule

First suppose $N\ge3$ and both households remain nonempty throughout. Let $s$ be the population of A. Each move changes it by one; it starts at $k$ and ends at $l$ .

A round trip across the population edge $h\leftrightarrow h+1$ multiplies the gap by

$$
\rho_h=\frac h{h+1}\frac{N-h-1}{N-h}
=1-\frac N{(h+1)(N-h)},\qquad 1\le h\le N-2.
$$

For each edge, pair its upward and downward traversals. Unpaired traversals form exactly a monotone route from $k$ to $l$ . Their factors telescope to $r/t$ : this is $k/l$ for upward travel and $l/k$ for downward travel.

If there are $L$ moves, every resident must change slots, so $L\ge N$ . The number of paired traversals is

$$
q=\frac{L-|k-l|}{2}\ge r.
$$

The two factors of $(h+1)(N-h)$ sum to $N+1$ . Their product is largest when they are as close as possible, giving maximum $D$ . Every round-trip factor is therefore at most $\rho$ , where $0<\rho<1$ , and

$$
F\le\frac rt\rho^q\le\frac rt\rho^r.
$$

A schedule passing through an empty household produces global equal wealth and cannot beat the wealth represented by this bound.

## 5. Attaining the bound

Choose $h=\lfloor N/2\rfloor$ . Its edge satisfies $(h+1)(N-h)=D$ .

Use the following population route: move monotonically from $k$ to $h$ , repeat $h\to h+1\to h$ exactly $r$ times, and move monotonically from $h$ to $l$ . Since $h$ lies between $k$ and $l$ , the route has exactly $N$ steps.

Whenever A loses a resident, move a target who has not yet moved from A to B. Whenever A gains a resident, move an outsider who has not yet moved from B to A. The route has exactly $k$ decreases and $l$ increases, so every step has an eligible resident. Everyone moves exactly once, and the households exchange all members.

The retained gap is exactly $(r/t)\rho^r$ . Substitution using $kl(r/t)=r^2$ proves the formula.

For $N=2$ , both households initially contain one resident. Merge and split them to obtain equal wealth. Here $\rho=0$ , so the same formula applies. In every branch the maximum is attained after finitely many moves.

## 6. Modular implementation

First compare $m_1l$ and $m_2k$ using 64-bit integers. Neither floating-point comparisons nor comparisons of residues are needed.

For $N=2q$ , use $D=q(q+1)$ ; for $N=2q+1$ , use $D=(q+1)^2$ . Compute these products and the initial cross-products in 64-bit integers.

The denominator factors are $k,l,N$ and the two integers forming $D$ . All are nonzero and strictly less than $P$ , so all are invertible modulo $P$ . Although $D$ may exceed $P$ , it is not divisible by $P$ . The reduced optimal wealth also has a denominator coprime to $P$ .

Use Fermat inverses and binary exponentiation for $\rho^r$ . Use 64-bit modular products and reduce between successive multiplications. Initial cross-products are at most $10^{15}$ and also fit in 64 bits.

Let $M$ be the maximum initial household size. One town takes $O(\log P+\log M)$ time and $O(1)$ extra space; $T$ towns take $O(T(\log P+\log M))$ time.

## 7. Two ways to evaluate the optimum

The [reference program](std.cpp) evaluates the closed formula. The [affine moving-schedule method](solution-alternative-affine.en.md) and its [program](alternative-affine.cpp) instead build the proven optimal population route and evaluate each segment in batches. They share the schedule proof but calculate wealth differently. Both use constant space and logarithmic time, and both pass all formal data.

The affine method directly follows the moves; the closed formula gives a direct expression for the result and is selected as the reference. Exact rational full-state search provides additional small-case verification; see the [testing guide](tests/README.md).
