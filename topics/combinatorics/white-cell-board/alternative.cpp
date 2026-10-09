// Codex (GPT-6): application, proof and implementation of inclusion-exclusion,
// grouping selected rows by mirror pairs. This calculates the fixed table.
#include <cstdio>

constexpr long long Mod = 1000000007;
long long Choose[21][21];
long long Two[21];

long long Power(long long a, int e)
{
	long long Result = 1;
	while (e > 0)
	{
		if (e & 1)
		{
			Result = Result * a % Mod;
		}
		a = a * a % Mod;
		e >>= 1;
	}
	return Result;
}

long long Factor(int Free, int Columns)
{
	if (Columns == 0)
	{
		return 1;
	}
	return Power(Two[Free] - 1, Columns);
}

long long Count(int n, int Diagonals)
{
	long long Result = 0;
	if (Diagonals < 2)
	{
		for (int r = 0; r <= n; ++r)
		{
			long long Term = Choose[n][r];
			if (Diagonals == 0)
			{
				Term = Term * Factor(n - r, n) % Mod;
			}
			else
			{
				Term = Term * Factor(n - r, r) % Mod;
				Term = Term * Factor(n - r - 1, n - r) % Mod;
			}
			Result = (Result + ((r & 1) ? Mod - Term : Term)) % Mod;
		}
		return Result;
	}
	int Pairs = n / 2;
	for (int t = 0; t <= Pairs; ++t)
	{
		for (int u = 0; u + t <= Pairs; ++u)
		{
			int v = Pairs - t - u;
			for (int c = 0; c <= n % 2; ++c)
			{
				int r = u + 2 * v + c;
				long long Term = Choose[Pairs][t] * Choose[Pairs - t][u] % Mod * Two[u] % Mod;
				Term = Term * Factor(n - r - 2, 2 * t) % Mod;
				Term = Term * Factor(n - r - 1, 2 * u + n % 2 - c) % Mod;
				Term = Term * Factor(n - r, 2 * v + c) % Mod;
				Result = (Result + ((r & 1) ? Mod - Term : Term)) % Mod;
			}
		}
	}
	return Result;
}

int main()
{
	Two[0] = 1;
	for (int i = 0; i <= 20; ++i)
	{
		Choose[i][0] = 1;
		Choose[i][i] = 1;
		if (i > 0)
		{
			Two[i] = Two[i - 1] * 2;
		}
		for (int j = 1; j < i; ++j)
		{
			Choose[i][j] = Choose[i - 1][j - 1] + Choose[i - 1][j];
		}
	}
	std::puts("1");
	for (int n = 1; n <= 20; ++n)
	{
		long long Answer = (Count(n, 0) - 2 * Count(n, 1) + Count(n, 2) + 2 * Mod) % Mod;
		std::printf("%lld\n", Answer);
	}
}
