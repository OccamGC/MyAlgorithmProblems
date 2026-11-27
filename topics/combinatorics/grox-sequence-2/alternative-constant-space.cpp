// Constant-space evaluation. C++17 implementation by Codex (GPT-6).
#include <cstdint>
#include <iostream>

using FInteger = std::int64_t;
constexpr FInteger Mod = 1004535809;

FInteger Power(FInteger Base, FInteger Exponent)
{
	FInteger Result = 1;
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
	int n;
	std::cin >> n;
	FInteger Factorial = 1;
	FInteger PowerOfTwo = 1;
	FInteger Sign = 1;
	FInteger Total = 1;
	FInteger Difference = 1;
	for (int k = 1; k <= n; ++k)
	{
		Factorial = Factorial * k % Mod;
		PowerOfTwo = 2 * PowerOfTwo % Mod;
		Sign = Mod - Sign;
		Total = (k * Total + PowerOfTwo) % Mod;
		Difference = (k * Difference + Sign) % Mod;
	}
	const FInteger Scale = Power(3 * Factorial % Mod, Mod - 2);
	const FInteger Zero = (Total + 2 * Difference) % Mod * Scale % Mod;
	const FInteger Other = (Total - Difference + Mod) % Mod * Scale % Mod;
	std::cout << Zero << ' ' << Other << ' ' << Other << '\n';
}
