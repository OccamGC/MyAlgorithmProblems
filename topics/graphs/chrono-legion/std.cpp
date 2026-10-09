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
	std::vector<std::vector<bool>> Linked(K, std::vector<bool>(K, false));
	for (int i = 0; i < K; ++i)
	{
		std::vector<std::pair<int, int>> Ordered;
		for (int j = 0; j < K; ++j)
		{
			int Radius = std::max(std::abs(Buildings[i].x - Buildings[j].x),
				std::abs(Buildings[i].y - Buildings[j].y));
			Ordered.emplace_back(Radius, j);
		}
		std::sort(Ordered.begin(), Ordered.end());
		std::vector<int> Latest(K);
		int Best = i;
		for (int Left = 0; Left < K;)
		{
			int Right = Left;
			while (Right < K && Ordered[Right].first == Ordered[Left].first)
			{
				int j = Ordered[Right].second;
				if (Buildings[j].Time > Buildings[Best].Time)
				{
					Best = j;
				}
				++Right;
			}
			for (int Position = Left; Position < Right; ++Position)
			{
				Latest[Position] = Best;
			}
			Left = Right;
		}
		for (int D : Buildings[i].Thresholds)
		{
			int j = Latest[D - 1];
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
