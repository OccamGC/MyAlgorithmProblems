// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Codex (GPT-6): beta=1 summation branch and coefficient composition at updates.
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
	std::vector<std::vector<FInteger>> Choose(Degree + 1, std::vector<FInteger>(Degree + 1));
	for (int i = 0; i <= Degree; ++i)
	{
		Choose[i][0] = 1;
		Choose[i][i] = 1;
		for (int j = 1; j < i; ++j)
		{
			Choose[i][j] = (Choose[i - 1][j - 1] + Choose[i - 1][j]) % Modulus;
		}
	}
	std::vector<std::vector<FInteger>> Basis(k + 1, std::vector<FInteger>(Degree + 1));
	FInteger Inverse = Beta == 1 ? 0 : Power(Normalize(1 - Beta), Modulus - 2);
	for (int i = 0; i <= k; ++i)
	{
		for (int d = i; d >= 0; --d)
		{
			FInteger Value = (d == i);
			if (Beta == 1)
			{
				for (int j = d + 2; j <= i + 1; ++j)
				{
					FInteger Term = Basis[i][j] * Choose[j][d] % Modulus;
					Value = Normalize(Value + (((j - d) & 1) ? -Term : Term));
				}
				Basis[i][d + 1] = Value * Power(d + 1, Modulus - 2) % Modulus;
			}
			else
			{
				for (int j = d + 1; j <= i; ++j)
				{
					FInteger Term = Basis[i][j] * Choose[j][d] % Modulus * Beta % Modulus;
					Value = Normalize(Value + (((j - d) & 1) ? -Term : Term));
				}
				Basis[i][d] = Value * Inverse % Modulus;
			}
		}
	}
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
			std::fill(Coefficients.begin(), Coefficients.end(), 0);
			for (int i = 0; i <= k; ++i)
			{
				FInteger a;
				std::cin >> a;
				a = Normalize(a);
				for (int j = 0; j <= Degree; ++j)
				{
					Coefficients[j] = (Coefficients[j] + a * Basis[i][j]) % Modulus;
				}
			}
			Exponential = Normalize(Alpha - Coefficients[0]);
		}
		else
		{
			FInteger n;
			std::cin >> n;
			FInteger Answer = 0;
			for (int j = Degree; j >= 0; --j)
			{
				Answer = (Answer * n + Coefficients[j]) % Modulus;
			}
			Answer = (Answer + Exponential * Power(Beta, n)) % Modulus;
			std::cout << Answer << '\n';
		}
	}
}
