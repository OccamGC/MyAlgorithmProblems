// Codex (GPT-6): residue-class prefix sums; O(n) evaluation of the three requested sums.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

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
	std::vector<FInteger> InverseFactorial(n + 1, 1);
	FInteger Factorial = 1;
	for (int i = 1; i <= n; ++i)
	{
		Factorial = Factorial * i % Mod;
	}
	InverseFactorial[n] = Power(Factorial, Mod - 2);
	for (int i = n; i > 0; --i)
	{
		InverseFactorial[i - 1] = InverseFactorial[i] * i % Mod;
	}
	std::array<FInteger, 3> Prefix{};
	std::array<FInteger, 3> Answer{};
	for (int i = n; i >= 0; --i)
	{
		int j = n - i;
		Prefix[j % 3] = (Prefix[j % 3] + InverseFactorial[j]) % Mod;
		for (int r = 0; r < 3; ++r)
		{
			int Residue = (i % 3 - r + 3) % 3;
			Answer[r] = (Answer[r] + InverseFactorial[i] * Prefix[Residue]) % Mod;
		}
	}
	std::cout << Answer[0] << ' ' << Answer[1] << ' ' << Answer[2] << '\n';
}
