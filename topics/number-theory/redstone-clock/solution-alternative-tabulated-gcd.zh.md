# 红石钟 · 查表 GCD

Codex（GPT-6）编写的 [C++17 实现](alternative-tabulated-gcd.cpp)只分解第一个参数 $i\le n$。在线性筛中把最小质因子 $p$ 乘入当前最小因子 $x$，再将三个因子排序。若 $x>1$，其余两项都至少为 $x\ge p$，故新合数因子 $px$ 的平方不超过三个因子的积；大于 $\sqrt n$ 的因子只能是单个质数。小因子查表，大质数用整除判断，每次除掉已匹配的公因子。预处理与总查询均为 $O(n)$，空间 $O(n)$。

在正式输入 `maximum-bound` 上，三次运行的中位耗时为 0.5296 秒，标程为 1.4982 秒；单独测得的进程峰值工作集分别为 141.54 和 4.76 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
