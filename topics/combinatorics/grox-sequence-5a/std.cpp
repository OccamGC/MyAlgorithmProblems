// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Rolling Stirling row; exact/safely lifted exponents for arbitrary composite moduli.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using FInteger = std::int64_t;

FInteger Power(FInteger Base, FInteger Exponent, FInteger Modulus)
{
	FInteger Result = 1 % Modulus;
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

int main()
{
	std::string n;
	int k;
	FInteger p;
	std::cin >> n >> k >> p;
	if (p == 1)
	{
		std::cout << 0 << '\n';
		return 0;
	}
	FInteger Phi = p;
	FInteger Remaining = p;
	for (FInteger Factor = 2; Factor * Factor <= Remaining; ++Factor)
	{
		if (Remaining % Factor == 0)
		{
			Phi -= Phi / Factor;
			while (Remaining % Factor == 0)
			{
				Remaining /= Factor;
			}
		}
	}
	if (Remaining > 1)
	{
		Phi -= Phi / Remaining;
	}
	FInteger Remainder = 0;
	FInteger PhiRemainder = 0;
	FInteger Capped = 0;
	FInteger BinaryPower = 1;
	for (char Digit : n)
	{
		int Value = Digit - '0';
		Remainder = (10 * Remainder + Value) % p;
		PhiRemainder = (10 * PhiRemainder + Value) % Phi;
		Capped = std::min(Phi + k, Capped * 10 + Value);
		BinaryPower = Power(BinaryPower, 10, p) * Power(2, Value, p) % p;
	}
	if (k == 0)
	{
		std::cout << (BinaryPower - 1 + p) % p << '\n';
		return 0;
	}
	std::vector<FInteger> Stirling(k + 1);
	Stirling[0] = 1;
	for (int i = 1; i <= k; ++i)
	{
		for (int j = i; j >= 1; --j)
		{
			Stirling[j] = (j * Stirling[j] + Stirling[j - 1]) % p;
		}
		Stirling[0] = 0;
	}
	FInteger Falling = 1;
	FInteger Answer = 0;
	int Limit = static_cast<int>(std::min<FInteger>(k, Capped));
	for (int j = 1; j <= Limit; ++j)
	{
		Falling = Falling * ((Remainder - j + 1 + p) % p + p) % p;
		FInteger Exponent = (PhiRemainder - j) % Phi;
		Exponent = (Exponent + Phi) % Phi;
		if (Capped >= Phi + j)
		{
			Exponent += Phi;
		}
		Answer = (Answer + Stirling[j] * Falling % p * Power(2, Exponent, p)) % p;
	}
	std::cout << Answer << '\n';
}
