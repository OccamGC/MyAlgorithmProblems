// GPT-6: update-run batching, 2D differences and compact static 2D segment tree.
// The 32-bit cell bound follows from |initial|,|increment| <= 20000 and Q <= 100000.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>
class FGrid
{
	int Rows;
	int Columns;
	int Width;
	std::vector<std::int32_t> Tree;
	std::vector<std::int64_t> Difference;
	void Corner(int x, int y, std::int64_t Value)
	{
		if (x < Rows && y < Columns)
		{
			Difference[x * Columns + y] += Value;
		}
	}
	std::int32_t QueryColumns(int Row, int Left, int Right) const
	{
		std::int32_t Answer = std::numeric_limits<std::int32_t>::lowest();
		for (Left += Columns, Right += Columns; Left < Right; Left /= 2, Right /= 2)
		{
			if (Left & 1)
			{
				Answer = std::max(Answer, Tree[Row * Width + Left++]);
			}
			if (Right & 1)
			{
				Answer = std::max(Answer, Tree[Row * Width + --Right]);
			}
		}
		return Answer;
	}
public:
	explicit FGrid(int n, int m) : Rows(n), Columns(m), Width(2 * m), Tree(4 * n * m), Difference(n * m)
	{
	}
	void Read()
	{
		for (int i = 0; i < Rows; ++i)
		{
			for (int j = 0; j < Columns; ++j)
			{
				std::cin >> Tree[(i + Rows) * Width + j + Columns];
			}
		}
	}
	void Add(int x1, int y1, int x2, int y2, int Value)
	{
		Corner(x1, y1, Value);
		Corner(x1, y2, -Value);
		Corner(x2, y1, -Value);
		Corner(x2, y2, Value);
	}
	void Rebuild()
	{
		for (int i = 0; i < Rows; ++i)
		{
			std::int64_t Running = 0;
			for (int j = 0; j < Columns; ++j)
			{
				Running += Difference[i * Columns + j];
				std::int64_t Delta = Running + (i ? Difference[(i - 1) * Columns + j] : 0);
				Difference[i * Columns + j] = Delta;
				Tree[(i + Rows) * Width + j + Columns] += Delta;
			}
		}
		std::fill(Difference.begin(), Difference.end(), 0);
		for (int i = Rows; i < 2 * Rows; ++i)
		{
			for (int j = Columns - 1; j > 0; --j)
			{
				Tree[i * Width + j] = std::max(Tree[i * Width + 2 * j], Tree[i * Width + 2 * j + 1]);
			}
		}
		for (int i = Rows - 1; i > 0; --i)
		{
			for (int j = 1; j < Width; ++j)
			{
				Tree[i * Width + j] = std::max(Tree[2 * i * Width + j], Tree[(2 * i + 1) * Width + j]);
			}
		}
	}
	std::int32_t Query(int x1, int y1, int x2, int y2) const
	{
		std::int32_t Answer = std::numeric_limits<std::int32_t>::lowest();
		for (x1 += Rows, x2 += Rows; x1 < x2; x1 /= 2, x2 /= 2)
		{
			if (x1 & 1)
			{
				Answer = std::max(Answer, QueryColumns(x1++, y1, y2));
			}
			if (x2 & 1)
			{
				Answer = std::max(Answer, QueryColumns(--x2, y1, y2));
			}
		}
		return Answer;
	}
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int Q;
	std::cin >> n >> m >> Q;
	FGrid Grid(n, m);
	Grid.Read();
	bool bDirty = true;
	while (Q--)
	{
		int Type;
		int x1;
		int y1;
		int x2;
		int y2;
		std::cin >> Type >> x1 >> y1 >> x2 >> y2;
		if (Type == 1)
		{
			int Value;
			std::cin >> Value;
			Grid.Add(x1 - 1, y1 - 1, x2, y2, Value);
			bDirty = true;
		}
		else
		{
			if (bDirty)
			{
				Grid.Rebuild();
				bDirty = false;
			}
			std::cout << Grid.Query(x1 - 1, y1 - 1, x2, y2) << '\n';
		}
	}
}
