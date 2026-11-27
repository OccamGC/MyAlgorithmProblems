# 砍树 · 线性计数排序

Codex（GPT-6）编写的 [C++17 实现](alternative-counting.cpp)按收益值和是否首次用树分别计数。每项收益是 $1$ 至 $n$ 的链长，按值递减、同值先非首次再首次输出即可复现上文的并列规则。扫描 $n$ 个桶，输出至多 $n$ 项，总时间和空间均为 $O(n)$。

在正式输入 `maximum-balanced` 上，三次运行的中位耗时为 0.1557 秒，标程为 0.1518 秒；单独测得的进程峰值工作集分别为 37.43 和 36.95 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
