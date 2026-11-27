# 告示牌识别 · 按长度预处理

Codex（GPT-6）编写的 [C++17 实现](alternative-length-prefix.cpp)用两趟稳定计数排序构建每一轮倍增排名。后缀数组中，一个后缀与左侧其他来源的最长公共前缀，只需比较最近的不同来源。相邻来源变更时取当前 LCP，否则把前一个结果与当前 LCP 取最小值；往右同理。两遍扫描同时处理所有来源。每个起点贡献的长度恰好是 $[\mathrm{Shared}+1,\mathrm{Remaining}]$，在差分数组上加一。两次前缀和依次得到各长度的出现数、长度区间的答案。总长含分隔符为 $S$ 时，时间 $O(S\log(S+1)+q)$，空间 $O(S)$。

在正式输入 `long-prefixes` 上，三次运行的中位耗时为 0.0566 秒，标程为 0.1197 秒；单独测得的进程峰值工作集分别为 14.35 和 12.90 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
