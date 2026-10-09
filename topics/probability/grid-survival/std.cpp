// Problem setter's solution: rolling path-count DP.
// Codex (GPT-6): flat storage and portable overflow-safe normalization.
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
	const int Cells = n * m;
	std::string Grid;
	Grid.reserve(Cells);
	for (int i = 0; i < n; ++i)
	{
		std::string Row;
		std::cin >> Row;
		Grid += Row;
	}
	std::vector<long long> Current(Cells);
	std::vector<long long> Next(Cells, 0);
	for (int i = 0; i < Cells; ++i)
	{
		Current[i] = Grid[i] == '1';
	}
	for (int Step = 0; Step < k; ++Step)
	{
		for (int i = 0; i < n; ++i)
		{
			for (int j = 0; j < m; ++j)
			{
				const int Index = i * m + j;
				if (Grid[Index] == '0')
				{
					continue;
				}
				long long Ways = 0;
				if (i > 0)
				{
					Ways += Current[Index - m];
				}
				if (i + 1 < n)
				{
					Ways += Current[Index + m];
				}
				if (j > 0)
				{
					Ways += Current[Index - 1];
				}
				if (j + 1 < m)
				{
					Ways += Current[Index + 1];
				}
				Next[Index] = Ways;
			}
		}
		Current.swap(Next);
	}
	long long Count = 0;
	for (long long Ways : Current)
	{
		Count = (Count + Ways) % Modulus;
	}
	std::cout << Normalize(Count, Cells, k) << '\n';
}
