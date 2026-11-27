// Row-state DP. C++17 implementation by Codex (GPT-6).
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
	// Digit zero means that the column is already mixed.
	std::vector<int> Place(n + 1, 1);
	for (int j = 0; j < n; ++j)
	{
		Place[j + 1] = Place[j] * (m + 1);
	}
	std::vector<long long> Ways(Place[n]);
	for (int State = 0; State < Place[n]; ++State)
	{
		int First = State % (m + 1);
		bool bUniform = true;
		long long Product = 1;
		for (int j = 0; j < n; ++j)
		{
			int c = State / Place[j] % (m + 1);
			Product = Product * Probability[0][j][c] % Mod;
			bUniform = bUniform && c == First;
		}
		Ways[State] = bUniform ? 0 : Product;
	}
	for (int Row = 1; Row < n; ++Row)
	{
		// Apply independent keep/mix transitions one column at a time.
		std::vector<long long> Next = Ways;
		for (int j = 0; j < n; ++j)
		{
			for (int State = 0; State < Place[n]; ++State)
			{
				int c = State / Place[j] % (m + 1);
				if (c != 0)
				{
					long long Keep = Next[State] * Probability[Row][j][c] % Mod;
					int Mixed = State - c * Place[j];
					Next[Mixed] = (Next[Mixed] + Next[State] - Keep + Mod) % Mod;
					Next[State] = Keep;
				}
			}
		}
		// Subtract each monochromatic row, whose resulting state is deterministic.
		for (int c = 1; c <= m; ++c)
		{
			long long Mono = 1;
			for (int j = 0; j < n; ++j)
			{
				Mono = Mono * Probability[Row][j][c] % Mod;
			}
			std::vector<int> Target(Place[n]);
			for (int State = 0; State < Place[n]; ++State)
			{
				Target[State] = Target[State / (m + 1)] * (m + 1)
					+ (State % (m + 1) == c ? c : 0);
				int To = Target[State];
				Next[To] = (Next[To] - Ways[State] * Mono % Mod + Mod) % Mod;
			}
		}
		Ways.swap(Next);
	}
	std::cout << Ways[0] << '\n';
}
