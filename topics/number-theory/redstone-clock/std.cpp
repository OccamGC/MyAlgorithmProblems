#include <cstdio>
#include <numeric>

int main()
{
	constexpr long long ValueBound = 10000000;
	long long n;
	long long a;
	std::scanf("%lld%lld", &n, &a);
	long long OddXor = 0;
	long long EvenXor = 0;
	for (long long i = 1; i <= n; ++i)
	{
		OddXor ^= i / std::gcd(i, a) * a;
		a = (a + 10007) % ValueBound + 1;
		EvenXor ^= i / std::gcd(i, a) * a;
		a = (a * a + 1) % ValueBound + 1;
	}
	std::printf("%lld\n%lld\n", OddXor, EvenXor);
	return 0;
}
