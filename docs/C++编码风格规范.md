# C++ 编码风格规范（草案 v0.1）

本规范适用于翻新题目的 `std.cpp`、`brute.cpp`、`generator.cpp`、`checker.cpp` 等 C++ 源码。以 [Epic C++ Coding Standard](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine) 的命名和排版习惯为基础；本页明确的题库约定优先。代码仍是可独立编译的标准 C++17，不包含 Unreal Engine 头文件，也不依赖引擎类型、宏、构建系统或运行时。

## 命名

- 自定义类型、函数、方法、普通变量和常量使用大驼峰（`PascalCase`），例如 `FEdge`、`FindAnswer`、`PathMaximum`、`MaxWeight`。普通结构体和类沿用 UE 风格的 `F` 前缀；布尔变量使用 `b` 前缀，例如 `bInTree`。前缀只是命名习惯，不意味着引入 UE 类型。
- 名称应表达作用，尽量避免无解释的缩写。一个变量单独占一条声明语句。
- 当变量直接对应题面的数学符号或输入字段时，允许保留题面的大小写，例如 `n`、`m`、`u`、`v`、`w`、`i`、`j`。这种例外用于保持题面、题解与程序的对应关系，不作为任意采用小驼峰或下划线命名的理由。
- 题面可以按[变量命名与公式释义](题面格式草案.md#变量命名与公式释义)调整符号。代码中的对应标识符与注释应同步核对；也可使用更清楚的大驼峰全称，并在必要处说明对应关系，例如题面的 `H` 对应代码中的 `Health`。
- C++ 规定的入口 `main`、标准库成员名、第三方接口名和必须匹配的外部格式保持原名。文件和主题目录仍按[单题文件结构](单题文件结构草案.md)使用小写 ASCII 名称，不受 C++ 标识符规则影响。

## 大括号与缩进

- 类型、函数、方法、lambda 以及 `if`、`else`、`for`、`while`、`switch` 等代码块的左大括号另起一行；右大括号独占一行。`else` 与前一块的右大括号分行。
- 即使控制语句的主体只有一条语句，也写完整大括号；不使用 `if (...) return;` 或 `while (...) {}` 这类单行块。
- 每层代码块缩进一个制表符，按 4 列显示；对齐表达式时可使用必要的空格。聚合初始化或初始化列表中的 `{...}` 不属于代码块，可按可读性放在同一行。
- 仓库根目录的 `.editorconfig` 为 C++ 文件声明制表符缩进和 LF 换行；编辑器若支持 EditorConfig，可直接采用。

```cpp
struct FEdge
{
	int u;
	int v;
	int Weight;
	bool bInTree = false;
};

int main()
{
	int n;
	int m;
	std::cin >> n >> m;

	for (int i = 0; i < m; ++i)
	{
		if (i == 0)
		{
			// Handle the first edge.
		}
	}
}
```

整理旧程序时先保持算法和输入输出不变，再检查命名、括号、缩进与单行声明。若同时修复算法，须在单题记录中单独说明，不把行为变化混入纯风格整理。
