// Problem setter's Stirling expansion.
// Codex (GPT-6): one decimal modular power followed by ascending powers; no factorization.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using FInteger = std::int64_t;

FInteger Power(FInteger Base, int Exponent, FInteger Modulus)
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

std::string Subtract(std::string Digits, int Amount)
{
	for (int i = static_cast<int>(Digits.size()) - 1; Amount > 0; --i)
	{
		int Value = Digits[i] - '0' - Amount % 10;
		Amount /= 10;
		if (Value < 0)
		{
			Value += 10;
			++Amount;
		}
		Digits[i] = static_cast<char>('0' + Value);
	}
	return Digits;
}

FInteger DecimalPower(const std::string& Exponent, FInteger Modulus)
{
	FInteger Result = 1 % Modulus;
	for (char Digit : Exponent)
	{
		Result = Power(Result, 10, Modulus) * Power(2, Digit - '0', Modulus) % Modulus;
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
	if (k == 0)
	{
		std::cout << (DecimalPower(n, p) - 1 + p) % p << '\n';
		return 0;
	}
	int Capped = 0;
	FInteger Remainder = 0;
	for (char Digit : n)
	{
		Capped = std::min(k, Capped * 10 + Digit - '0');
		Remainder = (10 * Remainder + Digit - '0') % p;
	}
	int Limit = Capped;
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
			Stirling[j] = (j * Stirling[j] + Stirling[j - 1]) % p;
		}
		Stirling[0] = 0;
	}
	std::vector<FInteger> Weights(Limit + 1);
	FInteger Falling = 1;
	for (int j = 1; j <= Limit; ++j)
	{
		FInteger Factor = (Remainder - j + 1) % p;
		Factor = (Factor + p) % p;
		Falling = Falling * Factor % p;
		Weights[j] = Stirling[j] * Falling % p;
	}
	FInteger BinaryPower = DecimalPower(Subtract(n, Limit), p);
	FInteger Answer = 0;
	for (int j = Limit; j >= 1; --j)
	{
		Answer = (Answer + Weights[j] * BinaryPower) % p;
		BinaryPower = BinaryPower * 2 % p;
	}
	std::cout << Answer << '\n';
}
