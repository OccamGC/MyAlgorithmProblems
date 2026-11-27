// Grid segment tree. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>

using FValue = std::int64_t;

struct FBuilding
{
	int x;
	int y;
	FValue Time;
	std::vector<int> Thresholds;
};

FValue Determinant(std::vector<std::vector<FValue>> Matrix, FValue Mod)
{
	int Size = static_cast<int>(Matrix.size());
	FValue Result = 1;
	for (int i = 0; i < Size; ++i)
	{
		for (int j = i + 1; j < Size; ++j)
		{
			// Euclidean elimination uses no modular inverses.
			while (Matrix[j][i] != 0)
			{
				FValue Quotient = Matrix[i][i] / Matrix[j][i];
				for (int k = i; k < Size; ++k)
				{
					Matrix[i][k] = (Matrix[i][k] - Quotient * Matrix[j][k] % Mod + Mod) % Mod;
				}
				std::swap(Matrix[i], Matrix[j]);
				Result = (Mod - Result) % Mod;
			}
		}
		if (Matrix[i][i] == 0)
		{
			return 0;
		}
		Result = Result * Matrix[i][i] % Mod;
	}
	return Result;
}

struct FSummary
{
	int Count = 0;
	int Newest = -1;
};

class FGrid
{
	int Rows = 1;
	int Columns = 1;
	const std::vector<FBuilding>& Buildings;
	std::vector<FSummary> Tree;
	FSummary& At(int x, int y)
	{
		return Tree[x * (2 * Columns) + y];
	}
	FSummary Merge(FSummary a, FSummary b) const
	{
		if (b.Newest != -1 && (a.Newest == -1 || Buildings[b.Newest].Time > Buildings[a.Newest].Time))
		{
			a.Newest = b.Newest;
		}
		a.Count += b.Count;
		return a;
	}
public:
	FGrid(int n, int m, const std::vector<FBuilding>& Points) : Buildings(Points)
	{
		Rows = n;
		Columns = m;
		Tree.resize(4 * n * m);
		for (int i = 0; i < static_cast<int>(Points.size()); ++i)
		{
			auto& Cell = At(n + Points[i].x - 1, m + Points[i].y - 1);
			Cell = Merge(Cell, {1, i});
		}
		for (int x = 2 * n - 1; x > 0; --x)
		{
			if (x < n)
			{
				for (int y = m; y < 2 * m; ++y)
				{
					At(x, y) = Merge(At(2 * x, y), At(2 * x + 1, y));
				}
			}
			for (int y = m - 1; y > 0; --y)
			{
				At(x, y) = Merge(At(x, 2 * y), At(x, 2 * y + 1));
			}
		}
	}
	FSummary Square(int x, int y, int Radius)
	{
		FSummary Result;
		auto QueryRow = [&](int Node)
		{
			int a = Columns + std::max(1, y - Radius) - 1;
			int b = Columns + std::min(Columns, y + Radius);
			while (a < b)
			{
				if (a & 1)
				{
					Result = Merge(Result, At(Node, a++));
				}
				if (b & 1)
				{
					Result = Merge(Result, At(Node, --b));
				}
				a /= 2;
				b /= 2;
			}
		};
		int l = Rows + std::max(1, x - Radius) - 1;
		int r = Rows + std::min(Rows, x + Radius);
		while (l < r)
		{
			if (l & 1)
			{
				QueryRow(l++);
			}
			if (r & 1)
			{
				QueryRow(--r);
			}
			l /= 2;
			r /= 2;
		}
		return Result;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	int K;
	FValue Mod;
	std::cin >> N >> M >> K >> Mod;
	std::vector<FBuilding> Buildings(K);
	for (FBuilding& Building : Buildings)
	{
		int Count;
		std::cin >> Building.x >> Building.y >> Building.Time >> Count;
		Building.Thresholds.resize(Count);
		for (int& D : Building.Thresholds)
		{
			std::cin >> D;
		}
	}
	FGrid Grid(N, M, Buildings);
	std::vector<std::vector<bool>> Linked(K, std::vector<bool>(K, false));
	for (int i = 0; i < K; ++i)
	{
		for (int D : Buildings[i].Thresholds)
		{
			int l = 0;
			int r = std::max(N, M);
			while (l < r)
			{
				int Mid = (l + r) / 2;
				if (Grid.Square(Buildings[i].x, Buildings[i].y, Mid).Count >= D)
				{
					r = Mid;
				}
				else
				{
					l = Mid + 1;
				}
			}
			int j = Grid.Square(Buildings[i].x, Buildings[i].y, l).Newest;
			if (i != j)
			{
				Linked[i][j] = true;
				Linked[j][i] = true;
			}
		}
	}
	std::vector<std::vector<FValue>> Cofactor(K - 1, std::vector<FValue>(K - 1, 0));
	int EdgeCount = 0;
	for (int i = 0; i < K; ++i)
	{
		for (int j = i + 1; j < K; ++j)
		{
			if (!Linked[i][j])
			{
				continue;
			}
			++EdgeCount;
			if (i < K - 1)
			{
				Cofactor[i][i] = (Cofactor[i][i] + 1) % Mod;
			}
			if (j < K - 1)
			{
				Cofactor[j][j] = (Cofactor[j][j] + 1) % Mod;
				Cofactor[i][j] = Mod - 1;
				Cofactor[j][i] = Mod - 1;
			}
		}
	}
	FValue Answer = Determinant(Cofactor, Mod);
	for (int i = 1; i <= EdgeCount - K + 1; ++i)
	{
		Answer = Answer * i % Mod;
	}
	std::cout << Answer << '\n';
}
