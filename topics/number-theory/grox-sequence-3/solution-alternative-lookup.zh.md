# Grox的序列三 · 整表查询

Codex（GPT-6）编写的 [C++17 实现](alternative-lookup.cpp)从 $a=n$ 向上填表，使用递推 $F(a,b)=a(b!+F(a+1,b+1))\bmod P$。当任一坐标超过 $n$ 时，定义中的求和为空，边界值为零。递推的推导见[离线对角线解法](solution-alternative-diagonal-dp.zh.md)。每次在线查询只访问一个整数。预处理时间和空间均为 $O((n+1)^2)$；在 $n=5000$ 时表约占 95.5 MiB，低于题面的 512 MB 限制。适合内存充足且希望边读边答的场合。

在正式输入 `05` 上，三次运行的中位耗时为 0.1312 秒，标程为 0.2560 秒；单独测得的进程峰值工作集分别为 100.21 和 7.97 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
