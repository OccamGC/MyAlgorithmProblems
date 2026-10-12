# 复杂度研究资料 / Complexity research

首次阅读可从两项成果的摘要开始：[网格森林平移匹配的三次方上界](results/cubic-bound.zh.md)与[诱导网格森林不能总靠补点扩充成树](results/tree-extension.zh.md)。摘要分别给出模型、结论、证明入口和复核命令。

Start with the summaries of [the cubic bound for grid forest translation matching](results/cubic-bound.en.md) and [obstructions to extending induced grid forests to trees](results/tree-extension.en.md). Each identifies the model, result, proof, and verification commands.

[结论状态索引 / Result status index](../../../../research-index.json) · [Agent 导航 / Agent guide](../../../../llms.txt) · [固定版本引用 / Versioned citations](../../../../CITATION.md)

一般的 $O(n^3+m)$ 上界已由有限第二轴引理与完整历史收费证明得到；当 $m\ge n-1$ 时有匹配下界。以下材料区分当前证明、辅助计费方法的反例与历史探索。

A finite second-axis lemma and complete-history charge now prove the general $O(n^3+m)$ bound, matching the lower bound when $m\ge n-1$. These materials distinguish the current proof, counterexamples to auxiliary charges, and research history.

2026-10-12 续研更新：方向 A 的连通资源不交性被左右早横枝反例否定；替代证明按标签轴长分组，非参考部分每点至多支付两次，全部标记每标签至多支付四次。主题解已同步，新证明对所有幂次成立，不依赖无限物理轴延长。

Continuation update, 2026-10-12: opposite early arms refute direction A's connected-union disjointness. The replacement proof groups by label-axis length, using each vertex at most twice for nonreference markers and at most four times overall per label. The editorial is updated; the proof covers all powers without infinite physical-axis extension.

## 阅读顺序 / Reading order

| 内容 / Topic | 中文 | English |
| --- | --- | --- |
| 算法 / Algorithm | [题解](../solution.zh.md) | [Editorial](../solution.en.md) |
| 有限第二轴引理与一般三次方证明 / Finite second-axis lemma and general cubic proof | [证明、符号速查与收费算例](proofs/cubic-bound.zh.md) | [Proof, notation guide, and worked charge](proofs/cubic-bound.en.md) |
| 较早的带对数上界 / Earlier logarithmic bound | [详细证明与图示](../complexity.zh.md) | [Illustrated proof](../complexity.en.md) |
| 去掉对数的进展 / Removing the logarithm | [研究综述](../complexity-research.zh.md) | [Overview](../complexity-research.en.md) |
| 路径与方向字符串 / Paths and direction strings | [证明](proofs/complexity-paths.zh.md) | [Proof](proofs/complexity-paths.en.md) |
| 根叶链、对偶及短分枝 / Chains, duality, short branches | [证明](proofs/complexity-chains.zh.md) | [Proof](proofs/complexity-chains.en.md) |
| 分叉、挂枝与高度记录 / Branches, attachments, height records | [证明](proofs/complexity-branches.zh.md) | [Proof](proofs/complexity-branches.en.md) |
| 跨前缀重叠与前沿 / Overlap across prefixes and frontiers | [证明](proofs/complexity-overlaps.zh.md) | [Proof](proofs/complexity-overlaps.en.md) |
| 完整早资源、标签与树轴 / Complete early resources, labels, axes | [证明](proofs/complexity-labels.zh.md) | [Proof](proofs/complexity-labels.en.md) |
| 参考类方向的十轮研究：失效边反例、列带证明、轴跨度归约 / Ten-round follow-up: failure edges, column bands, axis spans | [结论与逐轮记录](proofs/reference-followup.zh.md) | [Results and round log](proofs/reference-followup.en.md) |
| 左右早横枝反例与容量二证明稿 / Opposite early arms and a capacity-two draft | [构造、推导与审计状态](proofs/reference-capacity.zh.md) | [Construction, derivation, audit status](proofs/reference-capacity.en.md) |

## 构造与反例 / Constructions and counterexamples

这些反例用于排除过强的中间命题，均不构成算法三次方复杂度的反例。专题证明保留原有章节号和余项符号，以便准确对照。提供中英双语的说明已在下表标出，其余补充说明为中文；对应的主要结论也在上面的英文专题证明中说明。

These constructions refute stronger intermediate claims, not the cubic algorithm bound. Section numbers and remainder notation are retained for cross-reference. Bilingual notes are marked below; the remaining supporting notes are in Chinese, with their main results also covered by the English proofs above.

| 主题 / Topic | 说明 / Notes |
| --- | --- |
| 多尺度梳形与混合层高 / Comb scales and mixed heights | [中文](examples/comb-scales.zh.md) · [English](examples/comb-scales.en.md) |
| 梳形树问答：线性筛选、平方候选与三次方费用 / Comb-tree questions: scans, candidates, and cubic work | [中文及图示](examples/comb-candidates.zh.md) · [English with illustration](examples/comb-candidates.en.md) |
| 森林补成树的障碍与线性数量的大分量 / Obstructions to tree extension and linearly many large components | [中文及图示](examples/tree-extension.zh.md) · [English with illustrations](examples/tree-extension.en.md) |
| 包围盒、并集与方向分组的局限 / Limits of local geometric charges | [中文](examples/local-obstructions.zh.md) · [English](examples/local-obstructions.en.md) |
| 局部完整路径容量 / Local path capacity | [构造证明](examples/local-path-capacity.zh.md) |
| 正交双梳与粗势能预算 / Orthogonal combs | [构造证明](examples/orthogonal-combs.zh.md) |
| 同一道路交集中的多类型和重复早端 / Mixed types in one road intersection | [构造证明](examples/mixed-types.zh.md) |
| 连通完整资源中的多类型和重复早端 / Mixed types with connected resources | [构造证明](examples/connected-resources.zh.md) |
| 无界的逐点轴带参与数 / Unbounded band participation | [构造证明](examples/overlapping-bands.zh.md) |
| 重复轴类与连通资源 / Repeated axis classes | [参数证明](examples/repeated-axis-classes.zh.md) |
| 跨参考轴像的资源重复计数 / Resource reuse across reference-axis images | [嵌套梳参数证明](examples/nested-combs.zh.md) |
| 去对数路线合并后的参考类验证 / Reference-class investigation after merging research directions | [中文](examples/reference-components.zh.md) · [English](examples/reference-components.en.md) |

## 复核 / Verification

[输入清单](examples/inputs/manifest.json)保存八个代表性正式输入及其 SHA-256。[验证脚本](verify_examples.py)检查道路森林，使用位集计算全部答案和候选检查次数，并对小例从完整前缀定义直接枚举复核。可以传入已编译的标准程序逐项比较答案。

The [manifest](examples/inputs/manifest.json) records eight representative inputs and their SHA-256 digests. The [verifier](verify_examples.py) checks the road forest, computes every answer and scan count with bitsets, and independently enumerates complete-prefix matches on small cases. Pass a compiled solution to compare every output.

[补树构造验证脚本](verify_tree_extension.py)另行核对不可补成诱导树的小反例、两条长路径和多层嵌套族，包括全部四邻接边、分量大小和禁止格点。它检查静态图性质，不计算查询费用。

The separate [tree-extension verifier](verify_tree_extension.py) checks the small nonextendable forest, two long paths, and nested families, including all induced grid edges, component sizes, and forbidden cells. It checks static graph properties rather than query costs.

[参考类验证脚本](verify_reference_components.py)重新计算真实星心与共同切口，检查删除参考轴类后的资源连通分量。它覆盖公开输入、变化访问顺序的嵌套梳和周期弯折实例；[结果记录](reference-components-results.json)保存逐例指纹、实际费用、移动数与非空检查数量。该次有限验证没有发现反例；后续的左右早横枝已经否定其一般不交猜想，见[反例记录](proofs/reference-capacity.zh.md)。

The [reference-class verifier](verify_reference_components.py) rebuilds genuine earliest stars and common cuts, then checks resource components after reference deletion. It covers public fixtures, nested combs with varied discovery orders, and periodically bent instances. The [results](reference-components-results.json) retain fingerprints, actual costs, move counts, and nonempty-check counts. That finite investigation found no counterexample; subsequent opposite early arms refute its general disjointness conjecture, as recorded in the [obstruction note](proofs/reference-capacity.en.md).

[十轮研究脚本](explore_reference_rounds.py)进一步改变源相位、层间距、查询根、访问顺序和宿主叶子，并检查不同共同切口。它还核对失效边无界复用的参数族、原顺序列带证明及轴投影等价引理。逐轮数据与实验的非空范围见上表中的十轮记录；保留参考类的正对照不属于一般猜想的反例。

The [ten-round script](explore_reference_rounds.py) varies source phases, layer gaps, query roots, discovery orders, host leaves, and common cuts. It also checks the unbounded failure-edge family, the original-order column-band argument, and the axis-projection equivalence. See the round log above for evidence and nonempty coverage; positive controls retaining reference classes do not refute the general conjecture.

[完整收费验证器](verify_cubic_bound.py)独立重建全部实际成功事件，在事后按目标和查询行取星心；对所有真实标签计算共同切口、每个道路交域分量的参考类与逐笔资源分配。轴投影由抽象方向词树上的距离计算，不沿用旧验证器的投影实现。它包括幂次一的弯曲轴及同早端重复副本、低幂实例、嵌套梳、改变根和访问顺序、三阶网格的全部诱导森林以及固定种子的随机图和真实行走。[结果文件](cubic-bound-results.json)保存指纹与逐例统计，并为左右早横枝和幂次一实例保存完整收费证书；只有状态为 `passed` 才表示整批完成。

The [complete-charge verifier](verify_cubic_bound.py) independently reconstructs all actual successful events, then obtains stars by grouping target vertices and query rows. It checks every actual label, common cut, component-local reference, and per-marker assignment. Projection coordinates come from distances in the abstract direction-word tree, independently of the earlier projection code. Coverage includes curved power-one axes with repeated early endpoints, low powers, nested combs, changed roots and orders, every induced forest on a three-by-three board, and fixed-seed random boards and actual walks. The [report](cubic-bound-results.json) stores fingerprints and per-case statistics, retaining full certificates for opposite early arms and the power-one case; only status `passed` denotes a completed batch.

### 环境与当前结论的复现 / Requirements and current-proof checks

从仓库根目录运行。验证脚本只依赖 Python 3.10+ 标准库；C++ 答案对照另需 C++17 编译器。下面把新结果写入已忽略的临时目录，保留随仓库发布的结果记录。

Run from the repository root. Verification uses only the Python 3.10+ standard library; comparing C++ answers additionally needs a C++17 compiler. Fresh reports below go into an ignored temporary directory, preserving the published evidence.

```text
python -c "from pathlib import Path; Path('tmp/grid-forest-matching').mkdir(parents=True, exist_ok=True)"
python topics/simulation/grid-forest-matching/research/check_documents.py
python topics/simulation/grid-forest-matching/research/verify_tree_extension.py
python topics/simulation/grid-forest-matching/research/verify_examples.py
python topics/simulation/grid-forest-matching/research/verify_cubic_bound.py --output tmp/grid-forest-matching/cubic-bound-results.json
```

需要与标准程序比较时，编译后选择下面的完整复核命令。它包含全部 1,886 个实例的 Python 复核，并对其中 17 个实例运行标准程序。结果中的 `program_compared` 字段取决于是否传入该选项。

For comparison with the standard program, compile it and use the complete command below. It includes Python verification of all 1,886 cases and runs the standard program on 17 of them. The `program_compared` field depends on whether that option is supplied.

```text
python -c "from pathlib import Path; Path('build').mkdir(exist_ok=True); Path('tmp/grid-forest-matching').mkdir(parents=True, exist_ok=True)"
g++ -std=c++17 -O2 topics/simulation/grid-forest-matching/std.cpp -o build/grid-forest-matching.exe
python topics/simulation/grid-forest-matching/research/verify_cubic_bound.py --output tmp/grid-forest-matching/cubic-bound-results.json --program build/grid-forest-matching.exe
```

### 历史实验与图示 / Historical experiments and figures

下面的命令复核早期不交性探索和替代容量证明稿。它们保留各自的限定范围，不替代上面的全标签验证。轮次参数取一到十，可分别重建十轮报告；全幂次容量报告补充了幂次二和三，但其中没有非空幂次一场景，幂次一由新的完整验证器覆盖。

The following commands reproduce the earlier disjointness investigation and replacement capacity draft within their original scopes. They do not replace the all-label verifier above. Round values one through ten reproduce the ten reports separately. The all-powers capacity report adds powers two and three but contains no nonempty power-one case; the new complete verifier covers power one.

```text
python topics/simulation/grid-forest-matching/research/verify_reference_components.py --output tmp/grid-forest-matching/reference-components-results.json
python topics/simulation/grid-forest-matching/research/explore_reference_rounds.py --round 2 --output tmp/grid-forest-matching/reference-round-02.json
python topics/simulation/grid-forest-matching/research/verify_reference_capacity.py --output tmp/grid-forest-matching/reference-capacity-results.json
python topics/simulation/grid-forest-matching/research/verify_reference_capacity.py --min-power 1 --output tmp/grid-forest-matching/reference-capacity-all-powers-results.json
```

发布的[全幂次报告](reference-capacity-all-powers-results.json)与[早期容量报告](reference-capacity-results.json)一并保留，便于核对后来扩大了哪些验证范围。[左右早横枝输入](examples/inputs/opposite-arms.in)是原八例之外的独立补充，输入指纹保存在早期容量报告中。

The published [all-powers report](reference-capacity-all-powers-results.json) and [earlier capacity report](reference-capacity-results.json) document how coverage expanded. The [opposite-arms input](examples/inputs/opposite-arms.in) supplements the original eight fixtures; its input fingerprint is stored in the earlier capacity report.

仓库已经包含可直接阅读的图示。只有重画容量二 PNG 才需要可选依赖 Pillow；[绘图脚本](plot_cubic_bins.py)自动尝试常见字体，也可用 `--font` 指定本机的 TrueType/OpenType 字体文件。不同字体的像素布局可能略有差异。

Figures are already included. Only regenerating the capacity-two PNG needs the optional Pillow package. The [drawing script](plot_cubic_bins.py) tries common fonts and accepts a local TrueType/OpenType file through `--font`. Pixel layout may vary slightly with the chosen font.

```text
python -m pip install Pillow
python topics/simulation/grid-forest-matching/research/plot_cubic_bins.py --output tmp/grid-forest-matching/cubic-axis-bins.png
```

这些有限输入用于复核构造和计数，不替代参数族证明或一般复杂度证明。允许参数无界增长的数学构造也应与题面中的正式数据范围区分。

Finite fixtures check constructions and counts; they do not prove an asymptotic bound. Parameter families beyond the official input limits are mathematical constructions, not additional official test cases.
