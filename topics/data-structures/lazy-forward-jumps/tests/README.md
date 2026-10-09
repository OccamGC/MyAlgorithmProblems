# 数据生成与检验 / Test recipes

本题只依赖 C++17 与 Python 3 标准库。在本题目录执行：
Only C++17 and the Python 3 standard library are needed. Run in this problem directory:

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --out-dir ../../../build/data/lazy-forward-jumps --std ./std.exe
python tests/validate.py ../../../build/data/lazy-forward-jumps/01.in
```

计划、固定种子、分值和用途见 [plan.json](plan.json)。`--plan` 指定其他计划；`--case 01 --case 02` 可重复选择编号。省略 `--std` 只生成输入。生成器也计算结构化用例的预期结果，运行参考程序时会核对输出。全部文本使用 LF 换行。本轮使用 Python 3.12.14；复现实测数据请使用相同配方和种子。

See [plan.json](plan.json) for seeds, scoring, and purposes. Use `--plan` for another plan and repeat `--case` to select cases. Omit `--std` to produce only inputs. The generator also derives expected results for its recipes and checks the supplied executable. Text uses LF line endings. The reference run uses Python 3.12.14; reproduce with the same recipes and seeds.

## 覆盖 / Coverage

四组各两份，最大600万操作、64位总和、100个纯批次、局部跨度500、零次操作和越界起点。 / Two cases per group, six million operations, 64-bit totals, 100 pure batches, span 500, zero operations, and outside starts.

## 仓库检验工具 / Repository checks

[小模型工具](../../../../tools/check_r37.py)使用独立模型核验；[测量工具](../../../../tools/benchmark_r37.py)重复生成每份正式数据、验证输入和预期输出，计时五次并另测整进程峰值。先把相应程序编译到仓库的 `build/R37/<slug>-std.exe`；有补充程序时另编译为 `<slug>-alternative.exe`。

The [small-model tool](../../../../tools/check_r37.py) uses independent models. The [benchmark tool](../../../../tools/benchmark_r37.py) reproduces every formal input, checks validity and expected results, records five timings, and separately measures whole-process peak memory. It expects executables in the repository's `build/R37/<slug>-std.exe`, and `<slug>-alternative.exe` when supplied.

```text
python tools/check_r37.py
python tools/check_r37.py --packing-exhaustive
python tools/check_r37.py --validation-only
python tools/benchmark_r37.py --only lazy-forward-jumps
```

这些仓库命令在仓库根目录执行。完整字符串枚举比较Python森林模型与直接打包；默认命令另行核验编译后的C++程序，二者的验证对象分别记录。正式大数据的闭式结构与共享胜负公式不能替代小规模的直接博弈或打包枚举。

Run these repository commands from its root. Exhaustive strings compare the Python forest model with direct packing; the default command separately checks the compiled C++ programs. Large structural formulas and shared game criteria supplement, rather than replace, direct small game and packing enumeration.

[逐次耗时、输入输出及源码哈希 / Timings and hashes](../../../../docs/benchmark-R37.json)。

`alternative.cpp` 是不依赖批次形状的动态树方案；完整正式答案一致，但超过当前参考时限，取舍见双语题解。
`alternative.cpp` supports general operation shapes with a link-cut tree. All formal answers agree, but it exceeds the current reference limit; see the bilingual comparison.
