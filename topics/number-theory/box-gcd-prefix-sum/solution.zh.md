# 题解：某不科学的立方盒中的最大公约数累计

Codex（GPT-6）：应用欧拉函数展开、整除分块、数论函数前缀递推和拉格朗日插值，完成本题推导、证明与实现。这些基础方法不归为模型原创。

## 消去元组枚举

欧拉函数满足 $g=\sum_{d\mid g}\varphi(d)$ .在边长 $t$ 的盒子中，所有坐标都被 $d$ 整除的元组恰有 $\lfloor t/d\rfloor^m$ 个。交换求和顺序，得到

$$A=\sum_{d=1}^{n}\varphi(d)\sum_{t=d}^{n}\lfloor t/d\rfloor^m$$

设 $q=\lfloor n/d\rfloor$ ，$S_m(x)=\sum_{j=1}^{x}j^m$ ，且 $S_m(0)=0$ .商为 $1,\ldots,q-1$ 的每段长 $d$ ，最后一段长 $n-dq+1$ ，所以

$$A=\sum_{d=1}^{n}\varphi(d)\left[dS_m(q-1)+(n-dq+1)q^m\right]$$

将商相同的 $d\in[l,r]$ 合并，贡献为

$$
\left(\sum_{d=l}^{r}d\varphi(d)\right)\left[S_m(q-1)-q^{m+1}\right]
+(n+1)q^m\sum_{d=l}^{r}\varphi(d)
$$

每段右端点为 $r=\lfloor n/q\rfloor$ ，一共有 $O(\sqrt n)$ 段。上述步骤只改变有限求和的次序与分组，故保持答案。

## 两种欧拉函数前缀

记 $\Phi(x)=\sum_{d\le x}\varphi(d)$ ，$\Psi(x)=\sum_{d\le x}d\varphi(d)$ .由

$$\sum_{d\mid u}\varphi(d)=u,\qquad \sum_{d\mid u}d\varphi(d)\frac ud=u^2$$

先对 $u\le x$ 求和，再分离商参数为一的部分，得到

$$\Phi(x)=\frac{x(x+1)}2-\sum_{k=2}^{x}\Phi(\lfloor x/k\rfloor)$$

$$\Psi(x)=\frac{x(x+1)(2x+1)}6-\sum_{k=2}^{x}k\Psi(\lfloor x/k\rfloor)$$

两式右侧的和也按相同商分块，第二式一段的系数是该段整数之和。线性筛预处理到阈值 $B$ ；更大的参数递归求值并记忆化。递归参数严格减小，故从已知小前缀归纳，两种递推均正确。

所有大参数都是 $\lfloor n/i\rfloor$ ，因为嵌套整除仍具有这种形式。大参数可用 $\lfloor n/x\rfloor$ 作缓存下标，数量为 $O(n/B)$ .右端点及上一段右端点都满足这个条件，不能把这种下标方案直接用于任意整数查询。

## 幂和插值

先计算 $1^m,\ldots,B^m$ 及前缀，处理所有不超过 $B$ 的幂和查询。幂和 $S_m(x)$ 是次数至多 $m+1$ 的多项式：离散差分 $S_m(x)-S_m(x-1)=x^m$ 使次数降低一，且 $S_m(0)=0$ 确定常数。

令 $D=m+1$ ，取连续插值点 $0,1,\ldots,D$ .对于更大的 $x$ ，使用

$$
S_m(x)=\sum_{i=0}^{D}S_m(i)
\frac{\prod_{0\le j\le D,\ j\ne i}(x-j)}{i!(-1)^{D-i}(D-i)!}
$$

前后缀乘积得到每个分子，逆阶乘得到分母的逆元，单次插值耗时 $O(m)$ .$D<P$ 保证所有分母非零；$n<P$ 保证查询覆盖的整数位于同一模域内。实现取 $B=\min(n,2000000)$ ；需要插值时必有 $B\ge D$ ，所有插值点都已预处理。

## 正确性与复杂度

欧拉函数展开准确计数每个元组的公约数贡献；分块公式准确累计每个上界；两个前缀递推与幂和插值返回所需的精确模值。因此所有段之和就是题目答案。

记阈值为 $B$ .幂表耗时 $O(B\log(m+1))$ .每个大前缀参数求值需要 $O(\sqrt x)$ 分块，总计

$$O\left(\sum_{i\le n/B}\sqrt{n/i}\right)=O(n/\sqrt B)$$

大于 $B$ 的商至多 $n/B$ 个，插值总耗时 $O(nm/B)$ .总时间为 $O(B\log(m+1)+n/\sqrt B+nm/B)$ ，空间为 $O(B+n/B+m)$ ，递归深度 $O(\log n)$ .用 64 位中间乘积，分步取模并归一化减法。

[标准程序](std.cpp)与[前缀组件](totient-sums.hpp)可在本目录独立编译。直接筛出全部欧拉函数并枚举 $d$ 适合小规模核验，但在 $n=10^9$ 时不适合作为本题标程。见[测试说明](tests/README.md)和[性能记录](../../../docs/benchmark-R36.json)。
