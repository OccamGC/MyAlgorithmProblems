# 数据生成与检验 / Test recipes

仅需 C++17 与 Python 3 标准库。在本题目录执行：
Only C++17 and the Python 3 standard library are needed. Run in this problem directory:

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --out-dir ../../../build/data/digging-the-subway --std ./std.exe
python tests/validate.py ../../../build/data/digging-the-subway/01.in
```

[plan.json](plan.json) 列出固定种子、用途和10份各10%的正式文件。`--plan` 指定其他计划；可重复 `--case 01 --case 02` 选择编号；省略 `--std` 只生成输入。文本使用LF换行。生成器核验参考程序结果；构造题允许任意合法最优输出。复现环境为 Python 3.12.14。

[plan.json](plan.json) lists seeds, purposes, and ten formal files worth 10% each. Use `--plan` for another plan, repeat `--case` to select files, and omit `--std` for input generation only. Text uses LF line endings. The generator checks reference results; constructive answers may use any optimal valid output. The reference environment uses Python 3.12.14.

## 覆盖 / Coverage

直接路径并集枚举；原贪心反例、最优集合不嵌套、千点链/星形/平衡/随机树；星形两类叶子枚举与单源边际收益独立核验。 / Literal path unions; greedy and non-nesting regressions; 1000-vertex chains, stars, balanced and random trees; independent star leaf counts and single-source marginal gains.

## 仓库检验 / Repository checks

[独立小模型工具](../../../../tools/check_r38.py)核验五题，包含输入拒绝检查；[测量工具](../../../../tools/benchmark_r38.py)重复生成数据、验证答案、记录五次耗时，并另测整进程峰值内存。先将程序编译至仓库 `build/R38/<slug>-std.exe` ；传送门的补充程序编译为 `nether-portal-alternative-deadline.exe` . 在仓库根目录执行：

The [independent-model tool](../../../../tools/check_r38.py) checks all five problems and rejects invalid inputs. The [benchmark tool](../../../../tools/benchmark_r38.py) regenerates inputs, checks answers, records five timings, and separately measures whole-process peak memory. Compile programs into the repository's `build/R38/<slug>-std.exe` , plus `nether-portal-alternative-deadline.exe` for the portal alternative. Run from the repository root:

```text
python tools/check_r38.py
python tools/benchmark_r38.py --only digging-the-subway
```

[逐次耗时、输入输出和源码哈希 / Timings and hashes](../../../../docs/benchmark-R38.json)。时限取标准程序最慢中位数的两倍、向上取整至0.5秒；更换环境需重新校准。

The limit is twice the slowest reference median, rounded up to 0.5 seconds; recalibrate in another environment.
