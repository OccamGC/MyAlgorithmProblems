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
| 01 | 1 | 10% | zero |
| 02 | 1 | 10% | random |
| 03 | 2 | 10% | zero |
| 04 | 2 | 10% | chain |
| 05 | 2 | 10% | random |
| 06 | 3 | 10% | chain |
| 07 | 3 | 10% | random |
| 08 | 3 | 10% | zero |
| 09 | 3 | 10% | max |
| 10 | 3 | 10% | star |

## 独立验证 / Independent Validation

Prim 计算独立MST基准，完整检查路线并要求标准程序得100分；非唯一构造不与固定路线逐字比较。

Independent Prim baseline plus complete route validation; the standard route must score 100. Valid constructions are not compared literally with a fixed route.

独立小输入共 250 组，10份正式配方均重复生成并核对输入限制及分组；另检查6类非法输入。每份程序每个正式输入测时5次，并单独测峰值。

There are 250 independent small inputs. All 10 formal recipes were regenerated and checked against input and group constraints; six invalid-input classes were rejected. Each program has five timing runs per formal input and a separate peak-memory run.

## 构造评分 / Constructive Scoring

```text
python checker.py data/01.in data/01.out
```

输出整数得分0至100。退出状态0仅表示路线合法，部分分也返回0；非法路线返回1。评分器独立计算基准，无需标准输出文件。已验证12类非法输出、8个评分边界、普通及 `python -O` 模式。不要用输出文本相等来替代此检查。

The checker prints an integer score from 0 to 100. Exit status zero means a valid route, including partial-credit routes; invalid routes return 1. It computes the baseline independently and needs no reference output file. Twelve invalid-output classes, eight scoring boundaries, and normal and `python -O` modes were checked. Do not replace this with literal output comparison.

## 工具和证据 / Tools and Evidence

仓库根目录的 [check_r35.py](../../../../tools/check_r35.py) 包含独立小模型和输入校验；[benchmark_r35.py](../../../../tools/benchmark_r35.py) 重新生成正式数据、交叉检查并测量。先将编译产物放在 `build/R35/<slug>-std.exe`（有补充程序时也放 `<slug>-alternative.exe`）。基准支持 `--only <slug>` ，当前峰值测量依赖 Windows。校验工具的开发断言需正常 Python 模式运行；独立公开评分器不依赖断言。

From the repository root, [check_r35.py](../../../../tools/check_r35.py) supplies independent small models and input validation. [benchmark_r35.py](../../../../tools/benchmark_r35.py) regenerates, verifies, and measures formal inputs. First place compiled programs at `build/R35/<slug>-std.exe` and, if applicable, `<slug>-alternative.exe` . The benchmark accepts `--only <slug>` ; peak-memory measurement currently requires Windows. Run development validators with normal Python assertions enabled; the standalone public checker does not rely on assertions.

[逐次测量与哈希 / Timings and hashes](../../../../docs/benchmark-R35.json) · [环境与时限校准 / Environment and calibration](../../../../docs/评测环境与性能.md)
