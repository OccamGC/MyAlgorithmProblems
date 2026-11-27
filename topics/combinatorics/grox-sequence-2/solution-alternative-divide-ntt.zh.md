# Grox的序列二 · 分治 NTT

Codex（GPT-6）编写的 [C++17 实现](alternative-divide-ntt.cpp)按主解第三节先求出全部 $2n+1$ 个系数，最后才按余数合并。

换元 $t=n-j$ 后有 $i\le t$。在二分区间中，两项第一次分属左右两侧时做卷积，同叶的数对直接累加。每对恰好落在一个子问题中。时间 $O(n\log^2(n+2))$，空间 $O(n)$。适合需要全部系数的扩展。

在正式输入 `10` 上，三次运行的中位耗时为 0.1922 秒，标程为 0.0245 秒；单独测得的进程峰值工作集分别为 8.96 和 5.98 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
