// Codex (GPT-6): falling-factorial identity and fixed-modulus checkpoints.
// Offline table generation is O(P); online evaluation is O(B + log P).
#include <cstdio>
#include "factorial-table.hpp"

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
long long Factorial(int x)
{
	int Block = x / CheckpointStep;
	long long Result = FactorialCheckpoint[Block];
	for (int i = Block * CheckpointStep + 1; i <= x; ++i)
	{
		Result = Result * i % Mod;
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
	long long Answer = Factorial(n) * Power(Factorial(n - k), Mod - 2) % Mod;
	Answer = Answer * Power(2, n - k) % Mod;
	std::printf("%lld\n", Answer);
}
