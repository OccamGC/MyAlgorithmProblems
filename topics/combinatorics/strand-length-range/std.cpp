// Codex (GPT-6): reverse-complement orbit counting and geometric block sums.

#include <iostream>
constexpr long long Mod = 1000000007;
constexpr long long InverseTwo = 500000004;

struct FBlock
{
	long long Power;
	long long Sum;
};

FBlock Geometric(long long q, long long Length)
{
	FBlock Result{1, 0};
	FBlock Block{q, q};
	while (Length > 0)
	{
		if (Length & 1)
		{
			Result.Sum = (Result.Sum + Result.Power * Block.Sum) % Mod;
			Result.Power = Result.Power * Block.Power % Mod;
		}
		Block.Sum = Block.Sum * (1 + Block.Power) % Mod;
		Block.Power = Block.Power * Block.Power % Mod;
		Length >>= 1;
	}
	return Result;
}

long long Prefix(long long n, long long q)
{
	FBlock Half = Geometric(q, n / 2);
	long long Numerator = Half.Sum * (Half.Power + 2) % Mod;
	if (n % 2)
	{
		Numerator = (Numerator + Half.Power * Half.Power % Mod * q) % Mod;
	}
	return Numerator * InverseTwo % Mod;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int M;
	std::cin >> M;
	while (M--)
	{
		long long L;
		long long R;
		long long K;
		std::cin >> L >> R >> K;
		long long q = 2 * K % Mod;

		std::cout << (Prefix(R, q) - Prefix(L - 1, q) + Mod) % Mod << '\n';
	}
}
