# 复杂度研究资料 / Complexity research

一般的 $O(n^3+m)$ 上界仍未证明。以下材料区分已证结论、辅助计费方法的反例和未证猜想。

The general $O(n^3+m)$ upper bound remains open. These materials distinguish proved results, counterexamples to auxiliary accounting methods, and conjectures.

## 阅读顺序 / Reading order

| 内容 / Topic | 中文 | English |
| --- | --- | --- |
| 算法 / Algorithm | [题解](../solution.zh.md) | [Editorial](../solution.en.md) |
| 带对数的上界 / Logarithmic upper bound | [详细证明](../complexity.zh.md) | [Detailed proof](../complexity.en.md) |
| 去掉对数的进展 / Removing the logarithm | [研究综述](../complexity-research.zh.md) | [Overview](../complexity-research.en.md) |
| 路径与方向字符串 / Paths and direction strings | [证明](proofs/complexity-paths.zh.md) | [Proof](proofs/complexity-paths.en.md) |
| 根叶链、对偶及短分枝 / Chains, duality, short branches | [证明](proofs/complexity-chains.zh.md) | [Proof](proofs/complexity-chains.en.md) |
| 分叉、挂枝与高度记录 / Branches, attachments, height records | [证明](proofs/complexity-branches.zh.md) | [Proof](proofs/complexity-branches.en.md) |
| 跨前缀重叠与前沿 / Overlap across prefixes and frontiers | [证明](proofs/complexity-overlaps.zh.md) | [Proof](proofs/complexity-overlaps.en.md) |
| 完整早资源、标签与树轴 / Complete early resources, labels, axes | [证明](proofs/complexity-labels.zh.md) | [Proof](proofs/complexity-labels.en.md) |

## 构造与反例 / Constructions and counterexamples

这些反例用于排除过强的中间命题，均不构成算法三次方复杂度的反例。专题证明保留原有章节号和余项符号，以便准确对照。下列补充说明除前两项外为中文；对应的主要结论也在上面的英文专题证明中说明。

These constructions refute stronger intermediate claims, not the cubic algorithm bound. Section numbers and remainder notation are retained for cross-reference. Except for the first two items, the supporting notes below are in Chinese; the main results also appear in the English proofs above.

| 主题 / Topic | 说明 / Notes |
| --- | --- |
| 多尺度梳形与混合层高 / Comb scales and mixed heights | [中文](examples/comb-scales.zh.md) · [English](examples/comb-scales.en.md) |
| 包围盒、并集与方向分组的局限 / Limits of local geometric charges | [中文](examples/local-obstructions.zh.md) · [English](examples/local-obstructions.en.md) |
| 局部完整路径容量 / Local path capacity | [构造证明](examples/local-path-capacity.zh.md) |
| 正交双梳与粗势能预算 / Orthogonal combs | [构造证明](examples/orthogonal-combs.zh.md) |
| 同一道路交集中的多类型和重复早端 / Mixed types in one road intersection | [构造证明](examples/mixed-types.zh.md) |
| 连通完整资源中的多类型和重复早端 / Mixed types with connected resources | [构造证明](examples/connected-resources.zh.md) |
| 无界的逐点轴带参与数 / Unbounded band participation | [构造证明](examples/overlapping-bands.zh.md) |
| 重复轴类与连通资源 / Repeated axis classes | [参数证明](examples/repeated-axis-classes.zh.md) |
| 跨参考轴像的资源重复计数 / Resource reuse across reference-axis images | [嵌套梳参数证明](examples/nested-combs.zh.md) |

## 复核 / Verification

[输入清单](examples/inputs/manifest.json)保存八个代表性正式输入及其 SHA-256。[验证脚本](verify_examples.py)检查道路森林，使用位集计算全部答案和候选检查次数，并对小例从完整前缀定义直接枚举复核。可以传入已编译的标准程序逐项比较答案。

The [manifest](examples/inputs/manifest.json) records eight representative inputs and their SHA-256 digests. The [verifier](verify_examples.py) checks the road forest, computes every answer and scan count with bitsets, and independently enumerates complete-prefix matches on small cases. Pass a compiled solution to compare every output.

从仓库根目录运行 / Run from the repository root:

```text
python topics/simulation/grid-forest-matching/research/check_documents.py
python topics/simulation/grid-forest-matching/research/verify_examples.py
python topics/simulation/grid-forest-matching/research/verify_examples.py --program build/grid-forest-matching.exe
```

这些有限输入用于复核构造和计数，不替代参数族证明或一般复杂度证明。允许参数无界增长的数学构造也应与题面中的正式数据范围区分。

Finite fixtures check constructions and counts; they do not prove an asymptotic bound. Parameter families beyond the official input limits are mathematical constructions, not additional official test cases.
