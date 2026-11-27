# 再来一小段 · 完整构造

Codex（GPT-6）编写的 [C++17 实现](alternative-materialize.cpp)只构造到实际询问的最大版本，每次询问直接写出相应长度的前缀。

第 $v+1$ 版只在第 $v$ 版末尾追加前缀，所以所有被询问的版本都是最长版本的前缀。$V$ 个版本、$Q$ 次询问、最长串长 $L$、共输出 $C$ 个字符时，时间 $O(V+Q+L+C)$，空间 $O(L+V+Q)$。

在正式输入 `maximum-output` 上，三次运行的中位耗时为 0.0658 秒，标程为 0.1841 秒；单独测得的进程峰值工作集分别为 7.94 和 5.27 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

这个输入上 7.94 MiB 的进程峰值已接近题面的 8 MB 限制。评测环境内存紧张时可选按需输出的标程。

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
