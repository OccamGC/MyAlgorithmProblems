# 四邻接网格森林平移匹配的三次方复杂度上界

[English](cubic-bound.en.md) · [完整证明](../proofs/cubic-bound.zh.md) · [引用](../../../../../CITATION.md) · [研究目录](../README.md)

在道路格诱导出森林的方形网格上，逐步给定上下左右移动，并统计能完整执行当前移动前缀的所有起点。只在首次到达一个相对位移时扫描候选列表的算法，其总候选检查次数有三次方上界。证明适用于任意森林，无需限制为单棵树、路径或梳形树。

检索词：网格森林匹配、平移匹配、移动前缀匹配、候选筛选、摊还分析、去除对数因子；grid forest matching, translation matching, walk prefix matching, candidate filtering, amortized analysis, cubic time bound。

## 模型与准确结论

网格边长为 $n$，道路顶点数为 $N\le n^2$，实际移动次数为 $m$。道路之间保留全部四邻接边，诱导图必须是森林；道路集合可以为空。匹配只允许平移，不允许旋转、反射或重新嵌入。

候选起点一旦在移动前缀中走出道路就永久失效。已经检查过的相对位移无需再次扫描；首次出现的位移才遍历当前候选。令 $W$ 为这些扫描中的候选检查总次数，则

$$
W\le(5n-3)N,\qquad T=O(n^2+m+nN)\subseteq O(n^3+m).
$$

空间复杂度为 $O(n^2)$。当 $m\ge n-1$ 时，存在匹配的最坏情况总时间下界 $\Omega(n^3+m)$；该下界指这里分析的候选列表算法，不声称所有可能算法都需要三次方时间。对于较短的移动序列，还有 $O(n^2+m+N\min(m,n))$ 的上界。

拓展：[只允许四个对角方向时](diagonal-only.zh.md)，奇偶类的坐标同构保留上述检查次数与复杂度界；该推论有独立的模型说明和完整归约证明。

## 证明思路

证明一次性统计整段历史中的成功检查。按“实际落到的道路顶点”和“查询行”分组，每组保留最早成功，其余成功与之配对，得到水平平移标签和一个完整早前缀资源。

固定标签后，证明把资源分成共同切口类、各道路交域分量中的参考类以及剩余类。有限第二轴引理保证同早端的剩余副本充分分离；按标签轴长给资源投影的左端点分组，同一组内可以单射分配道路顶点，而每个道路顶点最多参与两组。

共同切口、参考类、剩余类的容量分别为一、一、二。因此每个标签最多使用四份道路交域预算。最后对水平标签求和，只是在计数同一行内的有序道路点对，总量受网格边长乘道路数控制。详细定义、有限第二轴引理、收费算例和下界见[完整证明](../proofs/cubic-bound.zh.md)；算法实现见[题解](../../solution.zh.md)和[标准程序](../../std.cpp)。

## 结论与历史探索的关系

这里的状态是“仓库已给出一般证明”。有限程序验证是辅助证据，不替代任意规模下的证明；本页不作外部同行评审声明。

较早的 $O(n^3\log(n+1)+m)$ 上界仍然有效，但较弱。旧方向 A 中“删除参考类后，每个连通资源并集都与其标签平移不交”的猜想已被左右早横枝反例否定。当前证明控制逐点容量，不需要这一不交性。各文档的状态见[结论索引](../../../../../research-index.json)。

## 复核与引用

在仓库根目录使用 Python 3.10 或更高版本运行：

```text
python -c "from pathlib import Path; Path('tmp/grid-forest-matching').mkdir(parents=True, exist_ok=True)"
python topics/simulation/grid-forest-matching/research/verify_cubic_bound.py --output tmp/grid-forest-matching/cubic-bound-results.json
```

[已发布报告](../cubic-bound-results.json)记录 1,886 个实例，包括三阶网格的全部诱导森林在指定遍历下的检查、构造例和固定种子随机例。它不穷举任意网格大小或所有移动序列。C++ 对照及文档检查命令见[复核说明](../README.md)。

证明版本：2026-10-12 发布的[提交 640ae4a](https://github.com/OccamGC/MyAlgorithmProblems/commit/640ae4ac52a1ce5a3082022162611839f97591fe)。引用条目 `OccamGC2026GridForestCubic` 及该版本的固定证明链接见[引用说明](../../../../../CITATION.md)。
