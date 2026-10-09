// Codex (GPT-6): totient expansion and multiset counting with quotient grouping.
#include <cstdio>
#include "totient-sums.hpp"

int main()
{
	int n;
	int m;
	if (std::scanf("%d%d", &n, &m) != 2)
	{
		return 0;
	}
	FTotientSums Totients(n);
	int Bound = Totients.Bound;
	std::vector<int> Inverse(Bound + 1);
	std::vector<int> Binomial(Bound + 1);
	Inverse[1] = 1;
	Binomial[1] = 1;
	for (int i = 2; i <= Bound; ++i)
	{
		Inverse[i] = static_cast<int>(Mod - Mod / i * Inverse[Mod % i] % Mod);
		Binomial[i] = 1LL * Binomial[i - 1] * (i + m - 1) % Mod * Inverse[i - 1] % Mod;
	}
	long long Factorial = 1;
	for (int i = 1; i <= m; ++i)
	{
		Factorial = Factorial * i % Mod;
	}
	long long InverseFactorial = Power(Factorial, Mod - 2);
	long long Answer = 0;
	int Before = 0;
	for (int l = 1; l <= n; )
	{
		int q = n / l;
		int r = n / q;
		int Through = Totients.Sum(r).first;
		long long Ways;
		if (q <= Bound)
		{
			Ways = Binomial[q];
		}
		else
		{
			Ways = InverseFactorial;
			for (int i = 0; i < m; ++i)
			{
				Ways = Ways * (q + i) % Mod;
			}
		}
		Answer = (Answer + (Through - Before + Mod) * Ways) % Mod;
		Before = Through;
		l = r + 1;
	}
	std::printf("%lld\n", Answer);
}
