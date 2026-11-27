# 告示牌识别 · 整数排名后缀 Treap

Codex（GPT-6）编写的 [C++17 实现](alternative-suffix-treap.cpp)保留从右向左插入后缀的构造。先比较首字符；相等时，由子树大小及父指针求出两条尾后缀的当前中序排名，因此旋转不会造成浮点标签碰撞。一次查找至多比较 $h$ 次，每次求排名为 $O(h)$，构造上界为 $O(Sh^2)$，其中 $h$ 是过程中最大树高。实现采用固定种子的优先级；构造后沿用主解的 LCP 与各来源扫描。

在正式输入 `long-prefixes` 上，三次运行的中位耗时为 0.2783 秒，标程为 0.1197 秒；单独测得的进程峰值工作集分别为 14.11 和 12.90 MiB。[测量条件和原始数据](../../../docs/benchmark-editorial-alternatives.json)

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
