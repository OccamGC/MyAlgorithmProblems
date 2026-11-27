// Single-modulus reconstruction. C++17 implementation by Codex (GPT-6).
#include <cstdint>
#include <iostream>
#include <string>

using FInt = std::int64_t;

constexpr FInt Mod = 31525197391593473LL;

FInt Multiply(FInt a, FInt b)
{
	FInt Result = 0;
	while (b > 0)
	{
		if (b & 1)
		{
			Result = (Result + a) % Mod;
		}
		a = (a + a) % Mod;
		b >>= 1;
	}
	return Result;
}

FInt Power(FInt a, FInt b)
{
	FInt Result = 1;
	while (b > 0)
	{
		if (b & 1)
		{
			Result = Multiply(Result, a);
		}
		a = Multiply(a, a);
		b >>= 1;
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int k;
	std::cin >> n >> k;
	std::string Suffix;
	if (k > 0)
	{
		std::cin >> Suffix;
	}
	FInt Factorial = 1;
	for (int i = 2; i <= n; ++i)
	{
		Factorial = Multiply(Factorial, i);
	}
	FInt Low = 0;
	for (char Digit : Suffix)
	{
		Low = (Low * 10 + Digit - '0') % Mod;
	}
	const FInt Inverse = Power(Power(10, k), Mod - 2);
	const FInt Prefix = Multiply((Factorial - Low + Mod) % Mod, Inverse);
	if (Prefix != 0)
	{
		std::cout << Prefix;
	}
	std::cout << Suffix << '\n';
}
