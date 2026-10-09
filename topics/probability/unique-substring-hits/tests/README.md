# 测试与复现 / Tests and Reproduction

在本题目录编译，示例使用 Windows 可执行文件名。GCC 16.2.0，实际测量选项为 `-std=c++17 -O2 -Wall -Wextra` .Python 生成器仅依赖标准库。

Compile from this problem directory; the examples use Windows executable names. Measurements use GCC 16.2.0 with `-std=c++17 -O2 -Wall -Wextra` . The Python generator uses only the standard library.

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --plan tests/plan.json --out-dir data --std std.exe
python tests/generate.py --out-dir selected --case 01 --case 02 --std std.exe
```

`--case` 可重复指定；未指定则生成全部配方。未知编号会报错。省略 `--std` 只生成输入，提供它则运行指定程序生成 ` .out` .同一配方和种子生成相同输入。正式大数据和平台二进制不随包提交；样例已包含。

Repeat `--case` to select several recipes, or omit it for all recipes. Unknown IDs are rejected. Omit `--std` for inputs only, or supply it to generate ` .out` files by running the named executable. A fixed recipe and seed reproduce the same input. Large generated data and platform binaries are not distributed; samples are included.

## 配方 / Recipes

| ID | 分组 / Group | 分值 / Score | 目的 / Purpose |
| --- | --- | --- | --- |
| 01 | 1 | 10% | same |
| 02 | 1 | 10% | binary |
| 03 | 2 | 10% | same |
| 04 | 2 | 10% | alternating |
| 05 | 2 | 10% | ascii |
| 06 | 3 | 10% | same |
| 07 | 3 | 10% | ascii |
| 08 | 3 | 10% | alternating |
| 09 | 3 | 10% | singular |
| 10 | 3 | 10% | binary |

## 独立验证 / Independent Validation

小串枚举所有子串并计出现次数，期望用整数最大公约数约分。正式同字符、交替字符和不可逆分母构造有独立闭式计数；两个十万长随机串用后缀数组和自动机交叉验证，没有声称对它们做逐子串枚举。

Small strings enumerate all substrings and occurrences; exact fractions are reduced with integer gcd. Formal constant, alternating, and singular-denominator strings have separate closed counts. Two random strings of length 100000 are cross-checked by suffix arrays and automata; they are not exhaustively enumerated.

独立小输入共 661 组，10份正式配方均重复生成并核对输入限制及分组；另检查6类非法输入。每份程序每个正式输入测时5次，并单独测峰值。

There are 661 independent small inputs. All 10 formal recipes were regenerated and checked against input and group constraints; six invalid-input classes were rejected. Each program has five timing runs per formal input and a separate peak-memory run.

## 另一程序 / Alternative Program

```text
g++ -std=c++17 -O2 -Wall -Wextra alternative.cpp -o alternative.exe
python tests/generate.py --out-dir alternative-data --std alternative.exe
```

两份程序依赖同目录的 `expectation.hpp` .自动机通过当前完整数据，但稠密94路转移比后缀数组耗费更多内存。

Both programs require `expectation.hpp` in the same directory. The automaton passes the complete data, with higher memory use from dense 94-way transitions.

## 工具和证据 / Tools and Evidence

仓库根目录的 [check_r35.py](../../../../tools/check_r35.py) 包含独立小模型和输入校验；[benchmark_r35.py](../../../../tools/benchmark_r35.py) 重新生成正式数据、交叉检查并测量。先将编译产物放在 `build/R35/<slug>-std.exe`（有补充程序时也放 `<slug>-alternative.exe`）。基准支持 `--only <slug>` ，当前峰值测量依赖 Windows。校验工具的开发断言需正常 Python 模式运行；独立公开评分器不依赖断言。

From the repository root, [check_r35.py](../../../../tools/check_r35.py) supplies independent small models and input validation. [benchmark_r35.py](../../../../tools/benchmark_r35.py) regenerates, verifies, and measures formal inputs. First place compiled programs at `build/R35/<slug>-std.exe` and, if applicable, `<slug>-alternative.exe` . The benchmark accepts `--only <slug>` ; peak-memory measurement currently requires Windows. Run development validators with normal Python assertions enabled; the standalone public checker does not rely on assertions.

[逐次测量与哈希 / Timings and hashes](../../../../docs/benchmark-R35.json) · [环境与时限校准 / Environment and calibration](../../../../docs/评测环境与性能.md)
