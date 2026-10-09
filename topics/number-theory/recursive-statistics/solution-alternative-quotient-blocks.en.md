# Recursive Statistics: Quotient Blocks

Problem setter's solution; Codex (GPT-6) organizes the implementation, boundary handling and explanation. Program: [alternative-quotient-blocks.cpp](alternative-quotient-blocks.cpp). See the [main editorial](solution.en.md) for the preferred algorithm and comparison.

## Method and correctness

Initialize $F(0)=0,F(1)=1$ . On receiving a positive query $x$ , fill missing values in increasing order. Every argument $\lfloor n/i\rfloor$ used to compute $F(n)$ is smaller than $n$ , so its value is already available.

For a denominator starting at $l\ge2$ , define

$$q=\lfloor n/l\rfloor,\qquad r=\lfloor n/q\rfloor$$

Every denominator in $[l,r]$ has quotient $q$ , so this block contributes $(r-l+1)F(q)$ . Accumulate it and continue at $l=r+1$ . These blocks cover exactly the summation range, without overlap. Induction on the argument proves the computed values equal the definition.

## Complexity and implementation

There are $O(\sqrt n)$ distinct quotients: at most $\sqrt n$ small denominators, and at most $\sqrt n$ possible quotients from larger denominators. If the largest positive query is $N$ , total time is $O(N\sqrt N+Q+1)$ and space is $O(N+1)$ . With no positive queries, only input and output are needed.

Use 64-bit products and reduce after each block. Return nonpositive arguments unchanged. Repeated and decreasing queries are table lookups. This is useful for streaming queries, at the cost of more preprocessing work. See the [main editorial's measurements](solution.en.md#verification-and-use) for applicability under the current limit.
