#include <iostream>
#include <vector>

constexpr long long Mod = 1000000007;

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Mod;
		}
		Base = Base * Base % Mod;
		Exponent >>= 1;
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::vector<std::vector<long long>>> Probability(n,
		std::vector<std::vector<long long>>(n, std::vector<long long>(m + 1)));
	for (int i = 0; i < n; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			long long Sum = 0;
			for (int c = 1; c <= m; ++c)
			{
				std::cin >> Probability[i][j][c];
				Sum += Probability[i][j][c];
			}
			const long long Inverse = Power(Sum, Mod - 2);
			for (int c = 1; c <= m; ++c)
			{
				Probability[i][j][c] = Probability[i][j][c] * Inverse % Mod;
			}
		}
	}
	std::vector<std::vector<long long>> UniformRow(n, std::vector<long long>(m + 1, 1));
	for (int i = 0; i < n; ++i)
	{
		UniformRow[i][0] = 0;
		for (int c = 1; c <= m; ++c)
		{
			for (int j = 0; j < n; ++j)
			{
				UniformRow[i][c] = UniformRow[i][c] * Probability[i][j][c] % Mod;
			}
			UniformRow[i][0] = (UniformRow[i][0] + UniformRow[i][c]) % Mod;
		}
	}
	int StateCount = 1;
	for (int j = 0; j < n; ++j)
	{
		StateCount *= m + 1;
	}
	long long Answer = 0;
	std::vector<int> Color(n);
	for (int State = 0; State < StateCount; ++State)
	{
		int Code = State;
		int Selected = 0;
		int CommonColor = 0;
		bool bMixed = false;
		for (int j = 0; j < n; ++j)
		{
			Color[j] = Code % (m + 1);
			Code /= m + 1;
			if (Color[j] != 0)
			{
				++Selected;
				bMixed = bMixed || (CommonColor != 0 && CommonColor != Color[j]);
				CommonColor = Color[j];
			}
		}
		long long Product = 1;
		for (int i = 0; i < n; ++i)
		{
			long long Row = 1;
			for (int j = 0; j < n; ++j)
			{
				if (Color[j] != 0)
				{
					Row = Row * Probability[i][j][Color[j]] % Mod;
				}
			}
			if (!bMixed)
			{
				Row = (Row - UniformRow[i][CommonColor] + Mod) % Mod;
			}
			Product = Product * Row % Mod;
		}
		Answer = (Answer + ((Selected & 1) ? Mod - Product : Product)) % Mod;
	}
	std::cout << Answer << '\n';
}
