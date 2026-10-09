// Codex (GPT-6): compress road cells into a sparse graph for rolling DP.
#include <array>
#include <iostream>
#include <string>
#include <vector>

constexpr long long Modulus = 7881299347898369LL;

long long Multiply(long long a, long long b)
{
	long long Result = 0;
	while (b > 0)
	{
		if (b & 1)
		{
			Result = (Result + a) % Modulus;
		}
		a = (a + a) % Modulus;
		b >>= 1;
	}
	return Result;
}

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Multiply(Result, Base);
		}
		Base = Multiply(Base, Base);
		Exponent >>= 1;
	}
	return Result;
}

long long Normalize(long long Count, int Cells, int k)
{
	const long long Choices = 1LL << (2 * k);
	const long long Denominator = Multiply(Cells, Choices);
	return Multiply(Count, Power(Denominator, Modulus - 2));
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<std::array<int, 4>> Neighbors;
	std::vector<int> PreviousRow(m, -1);
	for (int i = 0; i < n; ++i)
	{
		std::string Row;
		std::cin >> Row;
		int Left = -1;
		for (int j = 0; j < m; ++j)
		{
			const int Up = PreviousRow[j];
			int Index = -1;
			if (Row[j] == '1')
			{
				Index = static_cast<int>(Neighbors.size());
				Neighbors.push_back({Left, Up, -1, -1});
				if (Left >= 0)
				{
					Neighbors[Left][2] = Index;
				}
				if (Up >= 0)
				{
					Neighbors[Up][3] = Index;
				}
			}
			PreviousRow[j] = Index;
			Left = Index;
		}
	}
	std::vector<long long> Current(Neighbors.size(), 1);
	std::vector<long long> Next(Neighbors.size(), 0);
	for (int Step = 0; Step < k; ++Step)
	{
		for (std::size_t i = 0; i < Neighbors.size(); ++i)
		{
			long long Ways = 0;
			for (int Neighbor : Neighbors[i])
			{
				if (Neighbor >= 0)
				{
					Ways += Current[Neighbor];
				}
			}
			Next[i] = Ways;
		}
		Current.swap(Next);
	}
	long long Count = 0;
	for (long long Ways : Current)
	{
		Count = (Count + Ways) % Modulus;
	}
	std::cout << Normalize(Count, n * m, k) << '\n';
}
