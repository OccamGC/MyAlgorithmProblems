// Problem setter: binomial formula. Codex (GPT-6): symmetric product evaluation.

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
std::int64_t Choose(std::int64_t Total, std::int64_t Selected)
{
	if (Selected < 0 || Selected > Total)
	{
		return 0;
	}
	Selected = std::min(Selected, Total - Selected);
	std::int64_t Numerator = 1;
	std::int64_t Denominator = 1;
	for (std::int64_t i = 1; i <= Selected; ++i)
	{
		Numerator = Numerator * ((Total - Selected + i) % Mod) % Mod;
		Denominator = Denominator * i % Mod;
	}
	return Numerator * Power(Denominator, Mod - 2) % Mod;
}

int main()
{
	std::int64_t n;
	std::int64_t m;
	std::int64_t k;
	std::int64_t c;
	std::cin >> n >> m >> k >> c;
	if (m == 0)
	{
		std::cout << 0 << '\n';
		return 0;
	}
	std::cout << (k * Choose(n + m, n + 1) + c * Choose(n + m - 1, n)) % Mod << '\n';
}
