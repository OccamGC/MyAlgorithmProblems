// Rolling Stirling DP. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <cstdint>
#include <vector>

using FInteger = std::int64_t;

inline FInteger Power(FInteger Base, FInteger Exponent, FInteger Modulus)
{
	FInteger Result = 1;
	while (Exponent > 0)
	{
		if (Exponent & 1)
		{
			Result = Result * Base % Modulus;
		}
		Base = Base * Base % Modulus;
		Exponent >>= 1;
	}
	return Result;
}

constexpr FInteger Modulus = 1005060097;

int main()
{
	FInteger n;
	int k;
	std::cin >> n >> k;
	if (k == 0)
	{
		std::cout << (Power(2, n, Modulus) - 1 + Modulus) % Modulus << '\n';
		return 0;
	}
	int Limit = static_cast<int>(std::min<FInteger>(n, k));
	if (Limit == 0)
	{
		std::cout << 0 << '\n';
		return 0;
	}
	std::vector<FInteger> Stirling(Limit + 1);
	Stirling[0] = 1;
	for (int i = 1; i <= k; ++i)
	{
		for (int j = std::min(i, Limit); j >= 1; --j)
		{
			Stirling[j] = (Stirling[j - 1] + j * Stirling[j]) % Modulus;
		}
		Stirling[0] = 0;
	}
	FInteger Falling = 1;
	FInteger Answer = 0;
	FInteger BinaryPower = Power(2, n, Modulus);
	FInteger InverseTwo = (Modulus + 1) / 2;
	for (int j = 1; j <= Limit; ++j)
	{
		Falling = Falling * ((n - j + 1) % Modulus) % Modulus;
		BinaryPower = BinaryPower * InverseTwo % Modulus;
		Answer = (Answer + Stirling[j] * Falling % Modulus * BinaryPower) % Modulus;
	}
	std::cout << Answer << '\n';
}
