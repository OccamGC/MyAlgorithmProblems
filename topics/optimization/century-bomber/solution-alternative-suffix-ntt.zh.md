# 世纪轰炸机 · 后缀卷积

Codex（GPT-6）编写的 [C++17 实现](alternative-suffix-ntt.cpp)把每次投放登记为从 $l$ 开始的正后缀、从 $r+1$ 开始且平移 $r-l+1$ 位的负后缀。所有起飞点共用同一个位置多项式，可在频域总和上只乘一次。单次投放截断后的次数小于 $n$，最终次数小于 $n+m$，补零到相应长度 $H$ 即可。时间 $O(q+k+nH\log H)$，空间 $O(q+n+H)$。

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
