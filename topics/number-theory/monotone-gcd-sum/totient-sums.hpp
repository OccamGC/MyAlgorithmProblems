// Codex (GPT-6): standard totient sieve and summatory-convolution recurrences.
#ifndef TOTIENT_SUMS_HPP
#define TOTIENT_SUMS_HPP
#include <algorithm>
#include <utility>
#include <vector>

constexpr long long Mod = 1000000007;
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
long long Triangle(long long x)
{
	return x * (x + 1) % Mod * 500000004 % Mod;
}
class FTotientSums
{
public:
	int n;
	int Bound;
	std::vector<int> Phi;
	std::vector<int> Weighted;
	std::vector<int> MemoPhi;
	std::vector<int> MemoWeighted;
	explicit FTotientSums(int Size) : n(Size), Bound(std::min(Size, 2000000)),
		Phi(Bound + 1), Weighted(Bound + 1), MemoPhi(n / (Bound + 1) + 2, -1),
		MemoWeighted(n / (Bound + 1) + 2)
	{
		std::vector<int> Primes;
		Phi[1] = 1;
		for (int i = 2; i <= Bound; ++i)
		{
			if (Phi[i] == 0)
			{
				Phi[i] = i - 1;
				Primes.push_back(i);
			}
			for (int p : Primes)
			{
				if (p > Bound / i)
				{
					break;
				}
				if (i % p == 0)
				{
					Phi[i * p] = Phi[i] * p;
					break;
				}
				Phi[i * p] = Phi[i] * (p - 1);
			}
		}
		for (int i = 1; i <= Bound; ++i)
		{
			Weighted[i] = (Weighted[i - 1] + 1LL * i * Phi[i]) % Mod;
			Phi[i] = (Phi[i] + Phi[i - 1]) % Mod;
		}
	}
	// x must be zero or floor(n / k); recursive quotients retain this property.
	std::pair<int, int> Sum(int x)
	{
		if (x <= Bound)
		{
			return {Phi[x], Weighted[x]};
		}
		int Index = n / x;
		if (MemoPhi[Index] != -1)
		{
			return {MemoPhi[Index], MemoWeighted[Index]};
		}
		long long a = Triangle(x);
		long long b = 1LL * x * (x + 1) % Mod * (2LL * x + 1) % Mod * 166666668 % Mod;
		for (int l = 2; l <= x; )
		{
			int q = x / l;
			int r = x / q;
			auto Value = Sum(q);
			a = (a - 1LL * (r - l + 1) * Value.first % Mod + Mod) % Mod;
			long long Coefficient = (Triangle(r) - Triangle(l - 1) + Mod) % Mod;
			b = (b - Coefficient * Value.second % Mod + Mod) % Mod;
			l = r + 1;
		}
		MemoPhi[Index] = static_cast<int>(a);
		MemoWeighted[Index] = static_cast<int>(b);
		return {static_cast<int>(a), static_cast<int>(b)};
	}
};
#endif
