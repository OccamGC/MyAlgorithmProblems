// Codex (GPT-6): constant-space evaluation using the shorter of a falling
// product and its Wilson complement. Correct but slower on full-sized inputs.
#include <cstdio>
#include <algorithm>

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
int main()
{
	int n;
	int k;
	if (std::scanf("%d%d", &n, &k) != 2)
	{
		return 0;
	}
	if (k > n)
	{
		std::puts("0");
		return 0;
	}
	long long Answer = 1;
	if (k <= Mod - 1 - k)
	{
		for (int i = n - k + 1; i <= n; ++i)
		{
			Answer = Answer * i % Mod;
		}
	}
	else
	{
		for (int i = 1; i <= n - k; ++i)
		{
			Answer = Answer * i % Mod;
		}
		for (int i = n + 1; i < Mod; ++i)
		{
			Answer = Answer * i % Mod;
		}
		Answer = Mod - Power(Answer, Mod - 2);
	}
	Answer = Answer * Power(2, n - k) % Mod;
	std::printf("%lld\n", Answer);
}
