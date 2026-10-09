// GPT-6: modular rational expectation, including cancellation of a noninvertible denominator.
#pragma once
#include <iostream>
using FInt = long long;
constexpr FInt Modulus = 1000000007;
inline FInt Power(FInt Base, FInt Exponent)
{
	FInt Answer = 1;
	while (Exponent)
	{
		if (Exponent & 1)
		{
			Answer = Answer * Base % Modulus;
		}
		Base = Base * Base % Modulus;
		Exponent /= 2;
	}
	return Answer;
}
inline void AnswerQueries(FInt Distinct, FInt Unique, int Q)
{
	bool bCancel = Unique % Modulus == 0;
	FInt Denominator = bCancel ? Unique / Modulus : Unique % Modulus;
	FInt Inverse = Power(Denominator, Modulus - 2);
	while (Q--)
	{
		FInt Target;
		std::cin >> Target;
		FInt Numerator;
		if (!bCancel)
		{
			Numerator = (Target % Modulus) * (Distinct % Modulus) % Modulus;
		}
		else if (Target % Modulus == 0)
		{
			Numerator = (Target / Modulus % Modulus) * (Distinct % Modulus) % Modulus;
		}
		else if (Distinct % Modulus == 0)
		{
			Numerator = (Target % Modulus) * (Distinct / Modulus % Modulus) % Modulus;
		}
		else
		{
			std::cout << -1 << '\n';
			continue;
		}
		std::cout << Numerator * Inverse % Modulus << '\n';
	}
}
