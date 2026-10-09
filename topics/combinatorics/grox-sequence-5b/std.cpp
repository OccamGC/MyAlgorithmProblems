// Problem setter's solution. Codex (GPT-6): boundary handling and C++17 implementation.
// Stirling row by convolution, using the fixed prime modulus.
// Codex (GPT-6): truncate the convolution to the only relevant j <= min(n, k).
#include <algorithm>
#include <iostream>
#include "ntt.hpp"

constexpr FInteger Modulus = 1005060097;
constexpr FInteger Root = 5;

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
	int Length = 1;
	while (Length <= 2 * Limit)
	{
		Length <<= 1;
	}
	std::vector<FInteger> InverseFactorial(Limit + 1, 1);
	FInteger Factorial = 1;
	for (int i = 1; i <= Limit; ++i)
	{
		Factorial = Factorial * i % Modulus;
	}
	InverseFactorial[Limit] = Power(Factorial, Modulus - 2, Modulus);
	for (int i = Limit; i > 0; --i)
	{
		InverseFactorial[i - 1] = InverseFactorial[i] * i % Modulus;
	}
	std::vector<FInteger> Left(Length);
	std::vector<FInteger> Right(Length);
	for (int i = 0; i <= Limit; ++i)
	{
		Left[i] = Power(i, k, Modulus) * InverseFactorial[i] % Modulus;
		Right[i] = (i & 1) ? Modulus - InverseFactorial[i] : InverseFactorial[i];
	}
	Transform(Left, false, Modulus, Root);
	Transform(Right, false, Modulus, Root);
	for (int i = 0; i < Length; ++i)
	{
		Left[i] = Left[i] * Right[i] % Modulus;
	}
	Transform(Left, true, Modulus, Root);
	FInteger Falling = 1;
	FInteger Answer = 0;
	FInteger BinaryPower = Power(2, n, Modulus);
	FInteger InverseTwo = (Modulus + 1) / 2;
	for (int j = 1; j <= Limit; ++j)
	{
		Falling = Falling * ((n - j + 1) % Modulus) % Modulus;
		BinaryPower = BinaryPower * InverseTwo % Modulus;
		Answer = (Answer + Left[j] * Falling % Modulus * BinaryPower) % Modulus;
	}
	std::cout << Answer << '\n';
}
