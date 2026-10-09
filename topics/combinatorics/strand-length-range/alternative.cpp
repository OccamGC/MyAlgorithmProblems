// Codex (GPT-6): closed geometric sums, with the singular ratio q = 1 handled explicitly.

#include <iostream>
constexpr long long Mod = 1000000007;
constexpr long long InverseTwo = 500000004;

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

long long Prefix(long long n, long long q, long long Inverse)
{
	long long h = n / 2;
	long long p = Power(q, h);
	long long s = q == 1 ? h % Mod : q * ((p + Mod - 1) % Mod) % Mod * Inverse % Mod;
	long long Numerator = s * (p + 2) % Mod;
	if (n % 2)
	{
		Numerator = (Numerator + p * p % Mod * q) % Mod;
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
		long long Inverse = q == 1 ? 0 : Power((q + Mod - 1) % Mod, Mod - 2);
		std::cout << (Prefix(R, q, Inverse) - Prefix(L - 1, q, Inverse) + Mod) % Mod << '\n';
	}
}
