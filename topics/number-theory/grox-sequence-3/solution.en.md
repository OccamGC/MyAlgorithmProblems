# Grox's Sequence III Editorial

**Problem setter’s solution: blocks of factorial indices with precomputed product-weighted sums.** Codex (GPT-6) organizes the C++17 implementation and handles zero indices, empty sums, and the final block. The modulus is composite; the method uses only addition and multiplication, without factorial inverses.

## 1. Move two indices together

Set $j=i+b-a$ . During a query, $i$ starts at $a$ and $j$ at $b$ . Both increase by one until either exceeds $n$ .

Maintain the product $R$ of factors processed so far, initially one. To process one term directly:

$$R\gets Ri,\qquad \mathrm{Ans}\gets\mathrm{Ans}+R\,j!$$

This computes the definition but takes $O(n+1)$ time per query.

## 2. Precompute whole blocks

Choose $B=\lfloor\sqrt{n+1}\rfloor+1$ and split the factorial index $j$ into blocks. For a block beginning at $s$ and a product beginning at $x$ , precompute

$$H(s,x)=\sum_{k=0}^{B-1}(s+k)!\prod_{t=0}^{k}(x+t)$$

Keep only terms with $s+k\le n$ and $x+k\le n$ . Also store the product of a full block:

$$M(x)=\prod_{t=0}^{B-1}(x+t)$$

Compute factorials by recurrence. Enumerate each block start and $x$ , multiplying the next factor as the local index advances. No modular division is involved.

## 3. Answer a query

Process individual terms until $j$ is aligned to a block start. Whenever both current indices have room for a full block, apply

$$\mathrm{Ans}\gets\mathrm{Ans}+R\,H(j,i),\qquad R\gets R\,M(i)$$

Advance both indices by $B$ . Process any incomplete suffix term by term. Reduce all arithmetic modulo the given modulus.

Before a block, $R$ contains exactly the preceding factors. Each term in $H$ contains only the newly introduced factors within that block. Therefore $R H$ is precisely the block’s contribution to the definition, and $R M$ is the prefix product needed by the next block. Induction proves the query result.

If $a>n$ or $b>n$ , the sum is empty from the start. If $a=0$ , all products naturally become zero. For $n=0$ , a valid one-entry factorial array is still created.

## Complexity and implementation

Write $N=n+1$ . Preprocessing takes $O(N^2)$ time. Each query processes at most two partial blocks and $O(N/B)$ full blocks, taking $O(B+N/B)$ time. Total time is $O(N^2+q\sqrt N)$ ; space is $O(N^2/B+N)=O(N\sqrt N)$ .

This stores less than a complete two-dimensional answer table while retaining the information needed for queries. The problem setter’s blocking strategy is preserved. Check index bounds before array access. Signed 64-bit arithmetic is sufficient because the product of two residues is less than $921260340^2$ .

## Data and validation

`tests/generate.py` covers maximum-size long ranges, random queries, zero factors, partial blocks, and starting indices beyond $n$ . The small-instance oracle evaluates exact integer factorials and products from the definition, then reduces the result. Use `--std` to generate answers with a compiled reference program. See [environment and measurements](../../../docs/评测环境与性能.md).
