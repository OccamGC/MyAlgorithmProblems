# 砍树 · DFS 序与线段树

Codex（GPT-6）编写的 [C++17 实现](alternative-subtree-updates.cpp)反复选择根路径未覆盖点数最多的端点，对新覆盖的每个点将整棵子树减一，再按两级并列规则输出收益。

DFS 序把子树变为连续区间。尚未覆盖的新结点只被扣减一次，所有父链行走共 $O(n)$ 步，区间更新与最终排序共 $O(n\log(n+1))$ 时间，空间 $O(n)$。

在正式输入 `maximum-balanced` 上，三次运行的中位耗时为 0.2525 秒，标程为 0.1518 秒；单独测得的进程峰值工作集分别为 54.73 和 36.95 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
