// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Vandermonde determinant, evaluated at roots of unity.
#include <iostream>
#include "ntt.hpp"

constexpr FInteger Modulus = 1004535809;
constexpr FInteger Root = 3;

int main()
{
	int k;
	std::cin >> k;
	int n = 1 << k;
	std::vector<std::vector<FInteger>> a(n, std::vector<FInteger>(n));
	for (auto& Polynomial : a)
	{
		for (FInteger& Coefficient : Polynomial)
		{
			std::cin >> Coefficient;
		}
		Transform(Polynomial, false, Modulus, Root);
	}
	std::vector<FInteger> Result(n, 1);
	for (int i = 0; i < n; ++i)
	{
		for (int j = i + 1; j < n; ++j)
		{
			for (int t = 0; t < n; ++t)
			{
				Result[t] = Result[t] * ((a[j][t] - a[i][t] + Modulus) % Modulus) % Modulus;
			}
		}
	}
	Transform(Result, true, Modulus, Root);
	for (int i = 0; i < n; ++i)
	{
		std::cout << Result[i] << (i + 1 == n ? '\n' : ' ');
	}
}
