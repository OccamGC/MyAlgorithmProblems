#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

class FRectangleFenwick
{
public:
	FRectangleFenwick(int InWidth, int InHeight)
		: Width(InWidth), Height(InHeight), Tree((Width + 1) * (Height + 1))
	{
	}

	void Add(int x1, int y1, int x2, int y2, long long Value)
	{
		Corner(x1, y1, Value);
		Corner(x1, y2 + 1, -Value);
		Corner(x2 + 1, y1, -Value);
		Corner(x2 + 1, y2 + 1, Value);
	}

	long long Query(int x1, int y1, int x2, int y2) const
	{
		return Prefix(x2, y2) - Prefix(x1 - 1, y2)
			- Prefix(x2, y1 - 1) + Prefix(x1 - 1, y1 - 1);
	}

private:
	int Width;
	int Height;
	std::vector<std::array<long long, 4>> Tree;

	void Corner(int x, int y, long long Value)
	{
		std::array<long long, 4> Change = {Value, Value * (x - 1),
			Value * (y - 1), Value * (x - 1) * (y - 1)};
		for (int i = x; i <= Width; i += i & -i)
		{
			for (int j = y; j <= Height; j += j & -j)
			{
				auto& Node = Tree[i * (Height + 1) + j];
				for (int k = 0; k < 4; ++k)
				{
					Node[k] += Change[k];
				}
			}
		}
	}

	long long Prefix(int x, int y) const
	{
		std::array<long long, 4> Sum = {};
		for (int i = x; i > 0; i -= i & -i)
		{
			for (int j = y; j > 0; j -= j & -j)
			{
				const auto& Node = Tree[i * (Height + 1) + j];
				for (int k = 0; k < 4; ++k)
				{
					Sum[k] += Node[k];
				}
			}
		}
		return Sum[0] * x * y - Sum[1] * y - Sum[2] * x + Sum[3];
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
	FRectangleFenwick Tree(XMax - XMin + 1, YMax - YMin + 1);
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
