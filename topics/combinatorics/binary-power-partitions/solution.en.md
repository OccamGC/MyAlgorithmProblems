# Partitions into Powers of Two: Solution

**Problem setter’s solution: a three-dimensional DP for power-of-two blocks. GPT-6 adds the unique-splitting proof and suffix-sum acceleration.**

## 1. States for one block

Let $C_{i,j,k}$ count nondecreasing partitions of $2^j$ with smallest exponent exactly $i$ and largest exponent exactly $k$ . Necessarily $0\le i\le k\le j$ .

The unsplit block gives $C_{j,j,j}=1$ . Every other partition uses terms at most $2^{j-1}$ and can be cut uniquely into two consecutive halves of sum $2^{j-1}$ each.

To see why a cut cannot be skipped, let the next term be $v$ . All following terms are multiples of $v$ , and the total is also a multiple of $v$ , so the preceding prefix sum is a multiple of $v$ . The target $2^{j-1}$ is likewise a multiple of $v$ . Adding one $v$ cannot jump over it. Positive terms make the cut unique.

If the left half’s largest exponent is $l$ and the right half’s smallest exponent is $r$ , sorted order requires $l\le r$ . Thus, for $k<j$ ,
$$
C_{i,j,k}=\sum_{l=i}^{k}\sum_{r=l}^{k}
C_{i,j-1,l}C_{r,j-1,k}.
$$
Endpoint exponents identify the states, and the unique cut prevents both omissions and duplicate counts.

The direct setter recurrence takes $O(L^5)$ time and $O(L^3)$ space, where $L$ is the bit length.

## 2. Suffix-sum acceleration

For fixed $j,k$ , compute
$$
B_{l,k}=\sum_{r=l}^{k}C_{r,j-1,k}
$$
by scanning $l$ downwards. Then use
$$
C_{i,j,k}=\sum_{l=i}^{k}C_{i,j-1,l}B_{l,k}.
$$
Eliminating the innermost loop reduces time to $O(L^4)$ while preserving $O(L^3)$ space. This is the same state model and counting recurrence; the reference program uses the accelerated form.

## 3. Assemble a general integer

Write the set-bit positions of $N$ as $b_0<\cdots<b_{t-1}$ . Every valid nondecreasing partition has a unique division into consecutive blocks with sums $2^{b_0},\ldots,2^{b_{t-1}}$ .

First consider $T=2^{b_0}$ . If a prefix is still below $T$ and the next term $v$ exceeds $T$ , all remaining terms are multiples of $v$ . The prefix must equal $N\bmod v$ , which is at least $T$ because $T$ is the lowest set bit: a contradiction. Hence the next term cannot exceed $T$ before the cut. The divisibility argument above then prevents jumping over $T$ . Remove the first block and repeat.

Let $G_p(x)$ count assemblies starting at block $p$ whose exponents are all at least $x$ . The empty suffix satisfies $G_t(x)=1$ . For $b=b_p$ ,
$$
G_p(x)=\sum_{i=x}^{b}\sum_{k=i}^{b}C_{i,b,k}G_{p+1}(k).
$$
Requiring subsequent exponents to be at least the current maximum $k$ exactly enforces global nondecreasing order. Compute the inner sum for each exact minimum $i$ , then take suffix sums over $i$ . All assembly steps take $O(L^3)$ time. The answer is $G_0(0)$ .

## 4. Boundaries and complexity

For $N=0$ , return one. Other inputs have at most $63$ bits, so indices are only $0,\ldots,62$ and no shift reaches the type width.

Only addition, multiplication, and reduction are used; the modulus need not be prime. A product of two reduced values plus a reduced accumulator is below $10^{18}$ , so signed 64-bit arithmetic suffices.

Total time is $O(L^4)$ and space is $O(L^3)$ . Ordinary coin-change DP needs a number of states proportional to $N$ and is useful only for small-instance verification.

[Reference program](std.cpp).

## Illustration

The six rows show every nondecreasing partition of $N=7$ . Each rectangle’s value and width represent one power of two; the numbers on the left are just row indices.

![Algorithm illustration](assets/example.svg)

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables stay outside the published package. See the [reference measurements](../../../docs/benchmark-R29.json) for runtime and memory.
