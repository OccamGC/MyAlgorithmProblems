# Garden Click Coefficient

Reference time limit: 0.5 s; memory limit: 128 MiB. Use twice the slowest formal-file median on the target platform, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A cookie factory has unlocked a small garden. Its gardener may change the plants and soil to maximize the cookie coefficient obtained from each click when the garden is unfrozen.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Each cell of an $n\times m$ rectangle has exactly one type from the table. All cells use the same soil coefficient $S\in\{1,1.25\}$ . The achievement count is $A$ .

| Type | Meaning | Effect |
| --- | --- | --- |
| E | Empty | None |
| B | Wheat | Production bonus |
| T | Corn | Click bonus |
| W | Bloom | Milk bonus |
| N | Nurse tulip | Amplifies neighboring plants |
| D | Fern | Production bonus and click penalty |
| G | Glove mushroom | Click and cursor bonuses, production penalty |

Two distinct cells are neighbors when both coordinate differences are at most one. If cell $i$ has $a_i$ neighboring N cells, its effect coefficient, when it is not N, is

$$F_i=S(1+0.2a_iS).$$

N cells do not amplify other N cells and have no direct production effect. A type letter below denotes the set of cells of that type. Empty sums are zero and empty products are one.

$$\begin{aligned}
C_{\rm cursor}&=1+0.01\sum_{i\in G}F_i,\\
C_{\rm production}&=1+0.01\sum_{i\in B}F_i+0.03\sum_{i\in D}F_i,\\
D_{\rm production}&=\prod_{i\in G}(1-0.01F_i),\\
C_{\rm click}&=0.02\sum_{i\in T}F_i+0.04\sum_{i\in G}F_i,\\
D_{\rm click}&=\prod_{i\in D}(1-0.05F_i),\\
f_W&=0.002\sum_{i\in W}F_i,\\
M&=0.04A\cdot1.05^2\cdot1.1\cdot f_W.
\end{aligned}$$

$$K=(1+0.05M)(1+0.1M)^2(1+0.115M)(1+0.125M)^2
(1+0.15M)^2(1+0.175M)^2(1+0.2M)^5.$$

Maximize

$$C=(0.956+0.044C_{\rm cursor})K C_{\rm production}D_{\rm production}C_{\rm click}D_{\rm click}.$$

These formulas fully define the problem. Neither $C_{\rm click}$ nor $f_W$ has an additional constant one. Ignore golden-cookie effects.

![Neighbors in a two-row garden](assets/example.svg)

The N cell affects every neighboring non-N cell, including diagonal neighbors.

## Input Format

One line contains `n m A` .

## Output Format

Print the maximum coefficient. The absolute or relative error may be at most $10^{-9}$ : an output $x$ and optimum $y$ must satisfy $|x-y|\le10^{-9}\max(1,|y|)$ .


## Example 1

### Input

```text
1 1 0
```

### Output

```text
4.940215625000000000e-02
```

## Example 2

### Input

```text
2 2 1000
```

### Output

```text
1.906043514560546875e-01
```

## Example 3

### Input

```text
2 4 1000
```

### Output

```text
5.854567874453084032e-01
```


## Constraints and Guarantees

$n,m\ge1$ , $nm\le8$ , and $0\le A\le1000$ .

Redesign by Codex (GPT-6): the source omitted bounds, output rules, and examples. This edition supplies them and resolves the conflicting neighbor formula in favor of the stated 20% amplification, using $0.2a_iS$ . All other factors and exponents are retained.

| Score | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, worth 10% each. [Generation guide](tests/README.md).
