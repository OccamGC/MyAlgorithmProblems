# 数据生成与检验 / Data generation and validation

使用 Python 3.10+ 标准库和 C++17 编译器，在题目目录执行下列命令。每个输入只有一个城镇，10个正式文件各占10%。

Use the Python 3.10+ standard library and a C++17 compiler. Run these commands from the problem directory. Each input contains one town; each of the 10 formal files is worth 10%.

```sh
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std
python tests/generate.py --out-dir ../../../build/data/town-editing-simoleons-4 --std ./std
python tests/validate.py ../../../build/data/town-editing-simoleons-4/01.in
```

Windows 可传入 `.exe` 路径。省略 `--std` 只写入输入文件；生成器仍计算期望答案用于自检准备。`--plan` 指定计划，重复 `--case 01 --case 02` 选择文件，未知编号会报错。输出统一为UTF-8和LF换行。

Windows users can supply an `.exe` path. Without `--std`, only input files are written, though expected answers are still computed. Use `--plan` for another plan and repeat `--case 01 --case 02` to select cases. Unknown IDs are rejected. Files use UTF-8 and LF.

## 覆盖 / Coverage

| 文件 / File | 检查重点 / Focus |
| --- | --- |
| 01 | 两名目标与一个收集空位 / Two targets and one empty collection position |
| 02 | 分数目标均值 / Fractional target mean |
| 03 | 百万位置但没有更富居民 / One million positions, no richer outsider |
| 04 | 百万目标，仅三个较富居民 / One million targets, three richer outsiders |
| 05 | 目标与外部人数均接近百万，同一财富 / Both populations near one million; equal outsider wealth |
| 06 | 百万输入，两种财富，打乱顺序 / One million records, two shuffled wealth levels |
| 07 | 三种较富财富及较穷居民 / Three richer wealth levels and poor outsiders |
| 08 | 单个目标，近百万任意财富 / One target, nearly one million arbitrary outsider values |
| 09 | 20个目标，近百万不同财富 / 20 targets, nearly one million distinct values |
| 10 | 百万目标及一般外部财富 / One million targets and general outsider values |

03至10均为百万家庭位置输入。 / Files 03–10 all contain one million household positions.

## 答案核验 / Answer verification

`generate.py` 自带全部核验算法：01–02使用精确 Fraction 网格，03使用初始财富上界，04使用外部维度的通用矩阵快速幂，05–07使用按列推导的分组尾和，08–09逐格执行模平均。10用同一已证明系数恒等式的阶乘计算核对标准递推；这份检查不属于独立状态穷举。

All oracles are included in `generate.py`: exact Fraction grids for 01–02, the initial-wealth bound for 03, generic matrix exponentiation across outsiders for 04, column-wise grouped tails for 05–07, and literal modular grids for 08–09. Case 10 evaluates the same proven coefficient identity through factorials; it is not independent state enumeration.

额外完成350组精确网格对拍、100组大目标人数矩阵对拍，以及2000组合法搬家模拟。模拟检查固定位置、财富守恒、空户财富为零、目标身份与最终纯目标家庭，均达到上界。

Additional checks include 350 exact grids, 100 matrix cases with large target counts, and 2000 legal-move simulations. Simulations verify fixed positions, conservation, zero money in empty households, target identity, a pure final target household, and equality to the upper bound.

输入校验使用显式异常，正常模式和 `python -O` 均能拒绝越界、不满足位置保证、空户有财富及多余字段。输出校验要求恰好一个范围内整数，并比较期望值。每题6组样例与双语题面逐项核对。

Input validation uses explicit exceptions and rejects invalid bounds, insufficient positions, money in empty households, and extra fields in both normal and `python -O` modes. Output validation requires exactly one in-range integer matching the expected value. Each problem's six samples are matched against both language versions.

## 仓库级复现 / Repository-level reproduction

先将程序编译到 `build/R42/`，命名为 `town-editing-simoleons-4-std.exe`、`town-editing-simoleons-5-std.exe`、`town-editing-simoleons-5-alternative-forward.exe`，再从仓库根目录运行：

Compile programs into `build/R42/` with the names above, then run from the repository root:

```sh
python tools/check_r42.py
python tools/check_r42_constructions.py
python tools/benchmark_r42.py
python tools/draw_r42_figures.py
python tools/check_statements.py
```

不要对包含 `assert` 的复现检查脚本启用 `-O`；输入校验器单独支持该模式。正式性能测量使用Windows工作集统计，每份输入计时五次、另测一次内存峰值，并记录输入、输出、程序和生成器哈希。其他平台须重新校准时限。

Do not use `-O` for reproduction scripts containing assertions; the input validator separately supports that mode. Performance measurements use Windows working-set statistics, five timings per file, and a separate peak-memory run. Input, output, program, and generator hashes are recorded. Recalibrate time limits on other platforms.

[程序对拍 / Program comparisons](../../../../tools/check_r42.py) · [合法搬家模拟 / Legal-move simulations](../../../../tools/check_r42_constructions.py) · [正式测量 / Formal measurements](../../../../tools/benchmark_r42.py) · [逐次耗时及哈希 / Timings and hashes](../../../../docs/benchmark-R42.json)。
