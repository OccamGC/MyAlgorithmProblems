// Row blocks and column segment trees. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

// A column tree for range addition and range sum. A node's Sum includes its own tag.
class FLine
{
	int Width;
	std::vector<long long> Sum;
	std::vector<long long> Tag;

	long long Visit(int Node, int l, int r, int a, int b, long long Delta, bool bQuery)
	{
		if (a <= l && r <= b)
		{
			if (!bQuery)
			{
				Sum[Node] += Delta * (r - l + 1);
				Tag[Node] += Delta;
			}
			return Sum[Node];
		}
		int Mid = (l + r) / 2;
		int Overlap = std::min(b, r) - std::max(a, l) + 1;
		long long Result = Overlap * Tag[Node];
		if (a <= Mid)
		{
			Result += Visit(2 * Node, l, Mid, a, b, Delta, bQuery);
		}
		if (b > Mid)
		{
			Result += Visit(2 * Node + 1, Mid + 1, r, a, b, Delta, bQuery);
		}
		if (!bQuery)
		{
			Sum[Node] += Delta * Overlap;
		}
		return Result;
	}
public:
	explicit FLine(int w) : Width(w), Sum(4 * w), Tag(4 * w)
	{
	}
	long long Range(int a, int b, long long Delta, bool bQuery)
	{
		return Visit(1, 1, Width, a, b, Delta, bQuery);
	}
};

class FRowBlocks
{
	int Height;
	int Size;
	std::vector<FLine> Rows;
	std::vector<FLine> BaseSum;
	std::vector<FLine> Shared;
	long long Range(int x1, int y1, int x2, int y2, long long Value, bool bQuery)
	{
		long long Result = 0;
		for (int x = x1; x <= x2; )
		{
			int Block = (x - 1) / Size;
			int End = std::min(Height, (Block + 1) * Size);
			int Last = std::min(x2, End);
			int Count = Last - x + 1;
			if (x == Block * Size + 1 && Last == End)
			{
				Result += Count * Shared[Block].Range(y1, y2, Value, bQuery);
				if (bQuery)
				{
					Result += BaseSum[Block].Range(y1, y2, 0, true);
				}
			}
			else
			{
				for (int i = x; i <= Last; ++i)
				{
					Result += Rows[i - 1].Range(y1, y2, Value, bQuery);
				}
				if (bQuery)
				{
					Result += Count * Shared[Block].Range(y1, y2, 0, true);
				}
				else
				{
					BaseSum[Block].Range(y1, y2, Count * Value, false);
				}
			}
			x = Last + 1;
		}
		return Result;
	}
public:
	FRowBlocks(int h, int w) : Height(h), Size(std::max(1, static_cast<int>(std::sqrt(h)))),
		Rows(h, FLine(w)), BaseSum((h + Size - 1) / Size, FLine(w)), Shared(BaseSum)
	{
	}
	void Add(int x1, int y1, int x2, int y2, long long Value)
	{
		Range(x1, y1, x2, y2, Value, false);
	}
	long long Query(int x1, int y1, int x2, int y2)
	{
		return Range(x1, y1, x2, y2, 0, true);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int m;
	int XMin;
	int YMin;
	int XMax;
	int YMax;
	std::cin >> m >> XMin >> YMin >> XMax >> YMax;
	FRowBlocks Tree(XMax - XMin + 1, YMax - YMin + 1);
	auto Apply = [&](int x1, int y1, int x2, int y2, long long Value, bool bQuery)
	{
		x1 = std::max(x1, XMin);
		y1 = std::max(y1, YMin);
		x2 = std::min(x2, XMax);
		y2 = std::min(y2, YMax);
		if (x1 > x2 || y1 > y2)
		{
			return 0LL;
		}
		x1 += 1 - XMin;
		x2 += 1 - XMin;
		y1 += 1 - YMin;
		y2 += 1 - YMin;
		if (bQuery)
		{
			return Tree.Query(x1, y1, x2, y2);
		}
		Tree.Add(x1, y1, x2, y2, Value);
		return 0LL;
	};
	while (m--)
	{
		int Op;
		int x1;
		int y1;
		int x2;
		int y2;
		std::cin >> Op >> x1 >> y1 >> x2 >> y2;
		if (Op == 0)
		{
			std::cout << Apply(x1, y1, x2, y2, 0, true) << '\n';
		}
		else if (Op == 2)
		{
			int Value;
			std::cin >> Value;
			Apply(x1, y1, x2, y2, -Value, false);
		}
		else
		{
			int r = x2;
			int p = y2;
			if (r == 1)
			{
				Apply(x1, y1, x1, y1, p, false);
			}
			else
			{
				Apply(x1 - r + 1, y1 - r + 1, x1 + r - 1, y1 + r - 1, p, false);
				Apply(x1 - r, y1 - r + 2, x1 - r, y1 + r - 2, (p + 3) / 4, false);
				Apply(x1 + r, y1 - r + 2, x1 + r, y1 + r - 2, (p + 3) / 4, false);
				Apply(x1 - r + 2, y1 - r, x1 + r - 2, y1 - r, (p + 3) / 4, false);
				Apply(x1 - r + 2, y1 + r, x1 + r - 2, y1 + r, (p + 3) / 4, false);
			}
		}
	}
}
