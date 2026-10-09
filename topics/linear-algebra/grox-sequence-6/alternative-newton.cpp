// Codex (GPT-6): Newton basis and a bidiagonal particular-solution equation.
// Standard finite differences; O(k) space without a precomputed coefficient matrix.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

using FInteger = std::int64_t;
constexpr FInteger Modulus = 1000000007;

FInteger Normalize(FInteger Value)
{
	return (Value % Modulus + Modulus) % Modulus;
}

FInteger Power(FInteger Base, FInteger Exponent)
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

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int Q;
	FInteger Beta;
	int k;
	std::cin >> Q >> Beta >> k;
	Beta = Normalize(Beta);
	int Degree = k + (Beta == 1);
	std::vector<FInteger> Inverse(Degree + 2, 1);
	for (int j = 2; j <= Degree + 1; ++j)
	{
		Inverse[j] = Modulus - (Modulus / j) * Inverse[Modulus % j] % Modulus;
	}
	FInteger InverseDifference = Beta == 1 ? 0 : Power(Normalize(1 - Beta), Modulus - 2);
	std::vector<FInteger> Coefficients(Degree + 1);
	FInteger Exponential = 0;
	for (int OperationIndex = 0; OperationIndex <= Q; ++OperationIndex)
	{
		int Operation = 1;
		if (OperationIndex > 0)
		{
			std::cin >> Operation;
		}
		if (Operation == 1)
		{
			FInteger Alpha;
			std::cin >> Alpha;
			std::vector<FInteger> a(k + 1);
			for (FInteger& Value : a)
			{
				std::cin >> Value;
				Value = Normalize(Value);
			}
			std::vector<FInteger> Differences(k + 1);
			for (int t = 0; t <= k; ++t)
			{
				for (int j = k; j >= 0; --j)
				{
					Differences[t] = (Differences[t] * (t + 1) + a[j]) % Modulus;
				}
			}
			std::fill(Coefficients.begin(), Coefficients.end(), 0);
			for (int j = 0; j <= k; ++j)
			{
				Coefficients[j + (Beta == 1)] = Differences[0];
				for (int t = 0; t < k - j; ++t)
				{
					Differences[t] = Normalize(Differences[t + 1] - Differences[t]);
				}
			}
			if (Beta != 1)
			{
				FInteger Next = 0;
				for (int j = k; j >= 0; --j)
				{
					Coefficients[j] = Normalize(Coefficients[j] - Next) * InverseDifference % Modulus;
					Next = Coefficients[j];
				}
			}
			Exponential = Normalize(Alpha - Coefficients[0]);
		}
		else
		{
			FInteger n;
			std::cin >> n;
			FInteger Binomial = 1;
			FInteger Answer = 0;
			for (int j = 0; j <= Degree; ++j)
			{
				Answer = (Answer + Coefficients[j] * Binomial) % Modulus;
				Binomial = Binomial * Normalize(n - j) % Modulus * Inverse[j + 1] % Modulus;
			}
			Answer = (Answer + Exponential * Power(Beta, n)) % Modulus;
			std::cout << Answer << '\n';
		}
	}
}
