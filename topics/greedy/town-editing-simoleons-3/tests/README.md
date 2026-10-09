# 数据生成与检验 / Data generation and validation

使用 Python 3.10+ 标准库，以及自行编译的 C++17 程序。输入包含最多100000份独立存档。10个正式文件各占10%，分组与[题面](../statement.zh.md)一致。

Use Python 3.10+ and a locally compiled C++17 program. An input has at most 100000 independent towns. Each of the 10 formal files is worth 10%, as in the [statement](../statement.en.md).

```sh
g++ -std=c++17 -O2 std.cpp -o std
g++ -std=c++17 -O2 alternative-affine.cpp -o alternative-affine
python tests/generate.py --out-dir ../../../build/data/town-editing-simoleons-3 --std ./std
python tests/validate.py ../../../build/data/town-editing-simoleons-3/01.in
```

在题目目录中运行；Windows 可传入 `.exe` 路径。省略 `--std` 只生成输入。`--plan` 可以指定计划；可重复传入 `--case 01 --case 02` 选择文件，未知编号会报错。文件统一使用UTF-8和LF换行。

Run from the problem directory; Windows users may pass an `.exe` path. Omit `--std` for input-only generation. Use `--plan` for another plan, or repeat `--case 01 --case 02` to select files. Unknown IDs are rejected. Files use UTF-8 and LF.

## 覆盖 / Coverage

| 文件 / File | 检查重点 / Focus |
| --- | --- |
| 01 | 样例分支与恢复成员组成 / Sample branches and regrouping identities |
| 02 | 小人数、小财富穷举 / Exhaustive small populations and money |
| 03 | 空户、零财富、人数及财富上界 / Empty, zero-money and maximum boundaries |
| 04 | 目标初始不穷于对方 / Target initially at least as rich |
| 05 | 偶数总人数 / Even total population |
| 06 | 奇数总人数 / Odd total population |
| 07 | 两户人数高度不对称 / Highly unbalanced populations |
| 08 | 大人数与较穷的目标 / Large populations with a poorer target |
| 09 | 人均财富相近、相等、微小交叉差 / Near-equal means and exact comparisons |
| 10 | 4096种随机人数配合随机财富 / Random wealth across 4096 population pairs |

## 答案核验 / Answer verification

`oracle.py` 对两户人数均不超过30的实例使用精确分数全状态搜索。状态是B中的目标人数和A中的外部人数，枚举四类搬家，包括搬回原位置；用最大乘积Dijkstra求财富差的最优保留比例。经过空户后的均分情形单独处理。

For populations up to 30 each, `oracle.py` uses exact rational full-state search. Its state records targets in B and outsiders in A. All four move types, including returns, are allowed. Maximum-product Dijkstra finds the best retained wealth gap; global equal wealth after an empty slot is handled separately.

大实例使用已证明最优的搬家路线，对实际家庭财富建立2×2转移矩阵并进行通用矩阵快速幂。它不调用闭式答案；最优性依赖题解证明，不能把矩阵计算称为大规模穷举。按人数缓存转移系数只用于加快生成器，不是对输入的额外限制。

Large cases use the proven optimal moving route, generic 2×2 transfer matrices on actual household money, and matrix exponentiation. This does not call the closed answer formula; optimality comes from the proof, not exhaustive large-case search. Caching by population only speeds up generation and adds no input restriction.

生成器验证参考输出的数量、范围和每个答案。检查器显式抛出异常，因此 `python -O` 不会关闭输入检查。样例与两种语言的题面逐项核对。

The generator checks the count, range, and value of every reference answer. Input checks raise exceptions explicitly and remain enabled with `python -O` . Samples are checked against both language versions.

[全状态对拍与边界检查 / State-search and boundary checks](../../../../tools/check_r41.py)；[正式数据测量 / Formal-data measurements](../../../../tools/benchmark_r41.py)；[逐次耗时及哈希 / Timings and hashes](../../../../docs/benchmark-R41.json)。
