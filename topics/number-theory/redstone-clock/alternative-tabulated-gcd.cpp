// Tabulated GCD. C++17 implementation by Codex (GPT-6).
#include <cstdio>
#include <algorithm>
#include <array>
#include <cmath>
#include <vector>

int main()
{
	constexpr long long ValueBound = 10000000;
	long long n;
	long long a;
	std::scanf("%lld%lld", &n, &a);
	// Split only i (1 <= i <= n); the generated second argument may be larger.
	const int Small = static_cast<int>(std::sqrt(n));
	std::vector<std::array<int, 3>> Factors(n + 1);
	std::vector<int> Primes;
	Factors[1] = {1, 1, 1};
	for (int i = 2; i <= n; ++i)
	{
		if (Factors[i][2] == 0)
		{
			Primes.push_back(i);
			Factors[i] = {1, 1, i};
		}
		for (int p : Primes)
		{
			if (p > n / i)
			{
				break;
			}
			auto Parts = Factors[i];
			Parts[0] *= p;
			std::sort(Parts.begin(), Parts.end());
			Factors[i * p] = Parts;
			if (i % p == 0)
			{
				break;
			}
		}
	}
	const int Stride = Small + 1;
	std::vector<unsigned short> Table(Stride * Stride);
	for (int x = 1; x <= Small; ++x)
	{
		Table[x * Stride] = static_cast<unsigned short>(x);
		for (int y = 1; y < x; ++y)
		{
			Table[x * Stride + y] = Table[y * Stride + x % y];
		}
	}
	auto Gcd = [&](int i, int b)
	{
		int Result = 1;
		for (int x : Factors[i])
		{
			int Common = x <= Small ? Table[x * Stride + b % x] : (b % x == 0 ? x : 1);
			Result *= Common;
			b /= Common;
		}
		return Result;
	};
	long long OddXor = 0;
	long long EvenXor = 0;
	for (long long i = 1; i <= n; ++i)
	{
		OddXor ^= i / Gcd(i, static_cast<int>(a)) * a;
		a = (a + 10007) % ValueBound + 1;
		EvenXor ^= i / Gcd(i, static_cast<int>(a)) * a;
		a = (a * a + 1) % ValueBound + 1;
	}
	std::printf("%lld\n%lld\n", OddXor, EvenXor);
	return 0;
}
