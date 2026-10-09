# 积木塔

预估时间限制：0.5 秒。内存限制：128 MB。

实际时限以标准程序在目标评测环境的最慢用例中位时间乘以 $2$ ，按 $0.5$ 秒向上取整。参考环境见[评测说明](../../../docs/评测环境与性能.md)。

## 背景故事

三个平台上要进行一次积木塔搬运。积木都有自己的名字，搬运员需要按顺序读出每一步移动指令。

## 形式化问题描述

有三个平台，依次称为平台 $A,B,C$ ；它们各自的显示名字由输入给出。初始时，$n$ 个积木全部在平台 $A$ ，从底到顶的次序由输入给出，另外两个平台为空。

一次移动只能取走某个平台最顶端的一个积木，放到另一个平台顶部。任意时刻，如果积木 $Y$ 直接位于积木 $X$ 上方，那么 $Y$ 在初始塔中也必须位于 $X$ 上方，允许初始时二者之间有其他积木。

把全部积木搬到平台 $B$ ，并输出移动次数最少的一组操作。名字只是标签；积木的先后关系由初始位置决定，名字不要求互不相同。

## 输入格式

第一行一个整数 $n$ .

接下来三行，分别是平台 $A,B,C$ 的显示名字。再接下来 $n$ 行，是初始塔从底到顶的积木名字。

每个名字占完整一行，包含 $1$ 到 $20$ 个英文字母、数字、半角空格或下划线。开头、内部和结尾的空格都是名字的一部分，必须保留；换行符不属于名字。

## 输出格式

每次移动输出一行，严格使用以下格式：

```text
Move <block> from <source> to <target>.
```

将 `<block>`、`<source>`、`<target>` 分别替换为积木、来源平台和目标平台的完整名字；尖括号不输出。其余字母、空格和末尾英文句号按模板输出。不另外输出移动次数。

## 样例

### 样例 1

### 输入

```text
2
226 A AA ____ 1026
CC
BB
1
2_
```

### 输出

```text
Move 2_ from 226 A AA ____ 1026 to BB.
Move 1 from 226 A AA ____ 1026 to CC.
Move 2_ from BB to CC.
```

### 样例 2

### 输入

```text
1
A
B
C
Only
```

### 输出

```text
Move Only from A to B.
```

### 样例 3

### 输入

```text
3
Left
Middle
Right
Large block
Mid_block
Small
```

### 输出

```text
Move Small from Left to Middle.
Move Mid_block from Left to Right.
Move Small from Middle to Right.
Move Large block from Left to Middle.
Move Small from Right to Left.
Move Mid_block from Right to Middle.
Move Small from Left to Middle.
```

## 样例解释

第一组中，输入的三个平台名字依次对应 $A,B,C$ .先把上方积木移到平台 $C$ ，再把下方积木移到平台 $B$ ，最后把上方积木移到平台 $B$ ，共三步。

![两块积木从平台 A 移到平台 B 的三步过程](assets/moves.svg)

图中用 $A,B,C$ 表示平台身份，用 $1,2$ 表示从底到顶的初始积木编号。实际输出使用输入提供的名字。

## 数据范围与保证

$1\le n\le10$ .每个名字长度满足 $1\le |S|\le20$ ，字符范围及空格规则见输入格式。

| 分值比例 | 额外条件 |
| --- | --- |
| 100% | 无额外条件 |
