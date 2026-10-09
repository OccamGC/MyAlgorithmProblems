// Codex (GPT-6): binomial moments through an exponential generating function.
// Standard formal-series logarithm/exponential, implemented with Newton iteration.
#include <iostream>
#include "polynomial.hpp"

constexpr FInteger Modulus = 1005060097;
constexpr FInteger Root = 5;
using FArithmetic = FPolynomialArithmetic<Modulus, Root>;

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
	std::vector<FInteger> InverseFactorial(k + 1, 1);
	FInteger Factorial = 1;
	for (int i = 1; i <= k; ++i)
	{
		Factorial = Factorial * i % Modulus;
	}
	InverseFactorial[k] = Power(Factorial, Modulus - 2, Modulus);
	for (int i = k; i > 0; --i)
	{
		InverseFactorial[i - 1] = InverseFactorial[i] * i % Modulus;
	}
	FInteger InverseTwo = (Modulus + 1) / 2;
	std::vector<FInteger> Normalized(k + 1);
	Normalized[0] = 1;
	for (int i = 1; i <= k; ++i)
	{
		Normalized[i] = InverseFactorial[i] * InverseTwo % Modulus;
	}
	std::vector<FInteger> Logarithm = FArithmetic::Logarithm(Normalized, k + 1);
	for (FInteger& Value : Logarithm)
	{
		Value = Value * n % Modulus;
	}
	std::vector<FInteger> Result = FArithmetic::Exponential(Logarithm, k + 1);
	std::cout << Result[k] * Factorial % Modulus * Power(2, n, Modulus) % Modulus << '\n';
}
