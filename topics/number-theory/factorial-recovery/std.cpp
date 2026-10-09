// Codex (GPT-6): exact two-modulus reconstruction of the missing prefix.
// Uses the classical Chinese remainder theorem; no floating-point arithmetic.
#include <cstdint>
#include <iostream>
#include <string>

using FInt = std::int64_t;

FInt Power(FInt Base, FInt Exponent, FInt Modulus)
{
	FInt Result = 1;
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

FInt PrefixResidue(int n, int k, const std::string& Suffix, FInt Modulus)
{
	FInt Factorial = 1;
	for (int i = 2; i <= n; ++i)
	{
		Factorial = Factorial * i % Modulus;
	}
	FInt Remainder = 0;
	for (char Digit : Suffix)
	{
		Remainder = (Remainder * 10 + Digit - '0') % Modulus;
	}
	FInt Inverse = Power(Power(10, k, Modulus), Modulus - 2, Modulus);
	return (Factorial - Remainder + Modulus) % Modulus * Inverse % Modulus;
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
	constexpr FInt FirstPrime = 1000000007;
	constexpr FInt SecondPrime = 1000000009;
	FInt First = PrefixResidue(n, k, Suffix, FirstPrime);
	FInt Second = PrefixResidue(n, k, Suffix, SecondPrime);
	FInt Multiplier = (Second - First + SecondPrime) % SecondPrime;
	Multiplier = Multiplier * Power(FirstPrime, SecondPrime - 2, SecondPrime) % SecondPrime;
	FInt Prefix = First + FirstPrime * Multiplier;
	if (Prefix != 0)
	{
		std::cout << Prefix;
	}
	std::cout << Suffix << '\n';
}
