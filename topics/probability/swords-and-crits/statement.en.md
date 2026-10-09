# Swords and Critical Hits

Reference time limit: 2 seconds. Memory limit: 256 MiB. On the target judge, multiply the reference solution's largest per-input median time by 2 and round up to a multiple of 0.5 seconds. See the [evaluation notes](tests/README.md).

## Story

While playing *+1 DMG Per Revive*, you obtained a collection of swords. Each sword can independently trigger a critical hit and contribute its own damage multiplier. When several swords trigger, their multipliers are multiplied together.

You are now challenging the Tower of Death, where the peak damage of a single attack matters. Critical-hit multipliers are an important part of that peak. For several floors, you have listed target multipliers and want to know how likely one attack with the same collection of swords is to reach each target.

## Formal Problem Statement

You have $n$ swords. Sword $i$ has two integer parameters $p_i,m_i$ : it triggers with probability $p_i/10^6$ . It contributes multiplier $m_i$ when it triggers and multiplier $1$ otherwise. The triggering events of all swords are mutually independent.

The total critical-hit multiplier of one attack is the product of all contributed multipliers. If no sword triggers, the total multiplier is $1$ . Every sword participates; you do not choose or equip a subset of the swords.

You are given $q$ integer thresholds $K_1,\ldots,K_q$ . For each threshold, find the probability that one attack's total multiplier is **greater than or equal to** that threshold. All queries use the same swords. Each asks for its own probability, not a joint probability, and queries do not modify the swords or their probabilities.

Let $P=998244353$ . Write the required probability as a reduced fraction $A/B$ and output the least nonnegative residue of $AB^{-1}\bmod P$ . Since every triggering probability has denominator $10^6$ , the reduced denominator is always coprime to $P$ and the answer is well-defined.

**Only the probability answer is taken modulo the prime. Multipliers, thresholds, and comparisons retain their ordinary integer meanings.**

## Input Format

The first line contains an integer $T$ , the number of independent test cases.

Each test case contains:

- A line with two integers $n,q$ , the number of swords and queries.
- Then $n$ lines, each containing two integers $p_i,m_i$ .
- Then $q$ lines, each containing an integer $K_j$ written in ordinary decimal notation.

## Output Format

For each query, in input order within and across test cases, output one line containing its probability modulo $P$ .

## Sample 1

### Input

```text
1
3 6
500000 2
250000 3
1000000 5
1
5
10
15
30
31
```

### Output

```text
1
1
374341633
748683265
873463809
0
```

## Sample 2

### Input

```text
1
2 3
500000 999999937
500000 999999929
999999866000004472
999999866000004473
999999866000004474
```

### Output

```text
748683265
748683265
0
```

## Sample 3

### Input

```text
2
2 2
0 1000000000
743921 1
1
2
3 2
1000000 1000000000
1000000 1000000000
1000000 1000000000
1
1000000000000000000
```

### Output

```text
1
0
1
1
```

## Sample Explanation

In Sample 1, the third sword always triggers. The possible total multipliers are $5,10,15,30$ . Reaching $10$ requires at least one of the first two swords to trigger, with probability $5/8$ . Reaching $15$ requires the second sword to trigger, with probability $1/4$ . Reaching $30$ requires both of the first two swords to trigger, with probability $1/8$ .

In Sample 2, both swords together produce multiplier $999999866000004473$ with probability $1/4$ . Both of the first two thresholds require both swords to trigger. The third threshold is impossible to reach.

In Sample 3, the multiplier is always $1$ in the first test case. All three swords in the second test case trigger, giving a mathematical product of $10^{27}$ and answer $1$ to both queries. A solution only needs the information required for threshold comparisons, without storing that full product.

## Constraints and Guarantees

For 100% of the data:

- $1\le T\le8$ , $1\le n\le2000$ , and $1\le q\le5600$ .
- $0\le p_i\le10^6$ , $1\le m_i\le10^9$ , and $1\le K_j\le10^{18}$ .
- Each test case satisfies at least one of: $n\le44$ , or every threshold is at most $2\cdot10^7$ .
- All input values are integers and fit in a signed 64-bit integer. The full product of all sword multipliers need not be evaluated; exact solutions can use only 64-bit integer arithmetic.

For the aggregate bounds in one input file, let $n_t,q_t$ be the numbers of swords and queries in test case $t$ . Let $\mathcal A$ contain the test cases whose thresholds are all at most $2\cdot10^7$ , and let $\mathcal B$ contain the other test cases. The total number of queries in one input file satisfies $\sum_t q_t\le5600$ . The following bounds hold:

$$
\sum_{t\in\mathcal A}n_tq_t\le2000
$$

$$
\sum_{t\in\mathcal B}(q_t+4)\,2^{\lceil n_t/2\rceil}\le7\cdot2^{24}
$$

The multiple-query specification, integer bounds, scoring groups, and performance constraints were designed by Codex (GPT-6).

| Score | Additional conditions |
| --- | --- |
| 20% | Every test case satisfies $n\le18$ |
| 30% | Every threshold is at most $2\cdot10^7$ |
| 20% | Every test case satisfies $n\le34$ |
| 30% | No additional conditions |

There are 10 test files worth 10% each. See the [test recipes and evaluation notes](tests/README.md).
