// Codex (GPT-6): totient expansion, quotient grouping and Lagrange power sums.
// Uses standard number-theoretic identities, not a claim of inventing them.
#include <cstdio>
#include "totient-sums.hpp"

class FPowerSums
{
public:
	int Degree;
	std::vector<int> Powers;
	std::vector<int> Prefix;
	std::vector<int> InverseFactorial;
	std::vector<int> Left;
	std::vector<int> Right;
	FPowerSums(int Bound, int m) : Degree(m + 1), Powers(Bound + 1), Prefix(Bound + 1)
	{
		for (int i = 1; i <= Bound; ++i)
		{
			Powers[i] = static_cast<int>(Power(i, m));
			Prefix[i] = (Prefix[i - 1] + Powers[i]) % Mod;
		}
		if (Bound >= Degree)
		{
			InverseFactorial.resize(Degree + 1);
			Left.resize(Degree + 2);
			Right.resize(Degree + 2);
			long long Factorial = 1;
			for (int i = 1; i <= Degree; ++i)
			{
				Factorial = Factorial * i % Mod;
			}
			InverseFactorial[Degree] = static_cast<int>(Power(Factorial, Mod - 2));
			for (int i = Degree; i > 0; --i)
			{
				InverseFactorial[i - 1] = 1LL * InverseFactorial[i] * i % Mod;
			}
		}
	}
	long long Sum(int x)
	{
		if (x < static_cast<int>(Prefix.size()))
		{
			return Prefix[x];
		}
		Left[0] = 1;
		Right[Degree + 1] = 1;
		for (int i = 0; i <= Degree; ++i)
		{
			Left[i + 1] = 1LL * Left[i] * (x - i) % Mod;
		}
		for (int i = Degree; i >= 0; --i)
		{
			Right[i] = 1LL * Right[i + 1] * (x - i) % Mod;
		}
		long long Result = 0;
		for (int i = 0; i <= Degree; ++i)
		{
			long long Term = 1LL * Prefix[i] * Left[i] % Mod * Right[i + 1] % Mod;
			Term = Term * InverseFactorial[i] % Mod * InverseFactorial[Degree - i] % Mod;
			Result = (Result + (((Degree - i) & 1) ? Mod - Term : Term)) % Mod;
		}
		return Result;
	}
};

int main()
{
	int n;
	int m;
	if (std::scanf("%d%d", &n, &m) != 2)
	{
		return 0;
	}
	FTotientSums Totients(n);
	FPowerSums Powers(Totients.Bound, m);
	long long Answer = 0;
	std::pair<int, int> Before = {0, 0};
	for (int l = 1; l <= n; )
	{
		int q = n / l;
		int r = n / q;
		auto Through = Totients.Sum(r);
		long long Phi = (Through.first - Before.first + Mod) % Mod;
		long long Weighted = (Through.second - Before.second + Mod) % Mod;
		long long Value = q <= Totients.Bound ? Powers.Powers[q] : Power(q, m);
		long long Coefficient = (Powers.Sum(q - 1) - q * Value % Mod + Mod) % Mod;
		Answer = (Answer + Weighted * Coefficient + (n + 1LL) * Phi % Mod * Value) % Mod;
		Before = Through;
		l = r + 1;
	}
	std::printf("%lld\n", Answer);
}
