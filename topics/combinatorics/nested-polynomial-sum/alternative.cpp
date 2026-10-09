// Problem setter's solution: expand each monomial by triangular elimination.
// Codex (GPT-6): implement the supplied method in C++17 and batch binomial inverses.

#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Modulus = 2147483647;

long long Power(long long Base, long long Exponent)
{
	long long Result = 1;
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

long long Evaluate(long long n, int m, const std::vector<long long>& Weights)
{
	const int k = static_cast<int>(Weights.size()) - 1;
	long long Numerator = 1;
	long long Denominator = 1;
	for (int i = 1; i <= m; ++i)
	{
		Numerator = Numerator * (n + i - 1) % Modulus;
		Denominator = Denominator * i % Modulus;
	}
	long long Combination = Numerator * Power(Denominator, Modulus - 2) % Modulus;
	std::vector<long long> Prefix(k + 1, 1);
	std::vector<long long> Inverses(k + 1, 1);
	for (int j = 1; j <= k; ++j)
	{
		Prefix[j] = Prefix[j - 1] * (m + j) % Modulus;
	}
	long long Inverse = Power(Prefix[k], Modulus - 2);
	for (int j = k; j >= 1; --j)
	{
		Inverses[j] = Inverse * Prefix[j - 1] % Modulus;
		Inverse = Inverse * (m + j) % Modulus;
	}
	long long Answer = Weights[0] * Combination % Modulus;
	for (int j = 1; j <= k; ++j)
	{
		Combination = Combination * (n + m + j - 1) % Modulus * Inverses[j] % Modulus;
		Answer = (Answer + Weights[j] * Combination) % Modulus;
	}
	return Answer;
}

std::vector<long long> Convert(const std::vector<long long>& Coefficients)
{
	const int k = static_cast<int>(Coefficients.size()) - 1;
	std::vector<std::vector<long long>> Basis(k + 1, std::vector<long long>(k + 1, 0));
	std::vector<long long> Factorial(k + 1, 1);
	Basis[0][0] = 1;
	for (int j = 1; j <= k; ++j)
	{
		const long long Inverse = Power(j, Modulus - 2);
		Factorial[j] = Factorial[j - 1] * j % Modulus;
		for (int t = 0; t <= j; ++t)
		{
			const long long Previous = t == 0 ? 0 : Basis[j - 1][t - 1];
			Basis[j][t] = (Previous + (j - 1) * Basis[j - 1][t]) % Modulus * Inverse % Modulus;
		}
	}
	std::vector<long long> Weights(k + 1, 0);
	for (int i = 0; i <= k; ++i)
	{
		std::vector<long long> Remainder(k + 1, 0);
		Remainder[i] = 1;
		for (int j = i; j >= 0; --j)
		{
			const long long Coefficient = Remainder[j] * Factorial[j] % Modulus;
			Weights[j] = (Weights[j] + Coefficients[i] * Coefficient) % Modulus;
			for (int t = 0; t <= j; ++t)
			{
				Remainder[t] = (Remainder[t] - Coefficient * Basis[j][t] % Modulus + Modulus) % Modulus;
			}
		}
	}
	return Weights;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	long long n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<long long> Coefficients(k + 1);
	for (long long& Coefficient : Coefficients)
	{
		std::cin >> Coefficient;
	}
	std::cout << Evaluate(n, m, Convert(Coefficients)) << '\n';
}
