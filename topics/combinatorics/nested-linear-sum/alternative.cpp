// Problem setter: shared numerator product. Codex (GPT-6): C++17 implementation.

#include <algorithm>
#include <cstdint>
#include <iostream>
const std::int64_t Mod = 998244353;
std::int64_t Power(std::int64_t Base, std::int64_t Exponent)
{
	std::int64_t Result = 1;
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

int main()
{
	std::int64_t n;
	std::int64_t m;
	std::int64_t k;
	std::int64_t c;
	std::cin >> n >> m >> k >> c;
	std::int64_t Product = 1;
	std::int64_t Factorial = 1;
	for (std::int64_t i = 0; i < n; ++i)
	{
		Product = Product * ((m + i) % Mod) % Mod;
		Factorial = Factorial * (i + 1) % Mod;
	}
	Factorial = Factorial * (n + 1) % Mod;
	std::int64_t Coefficient = (k * ((n + m) % Mod) + c * (n + 1)) % Mod;
	std::cout << Product * Power(Factorial, Mod - 2) % Mod * Coefficient % Mod << '\n';
}
