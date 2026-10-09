// Problem setter's solution: symmetry count and binary exponentiation.
// Codex (GPT-6): explicit reverse-complement model and standard C++17 implementation.

#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Modulus = 1000000007;

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

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int m;
	std::cin >> m;
	long long Answer = 0;
	while (m-- > 0)
	{
		long long n;
		std::cin >> n;
		long long Count;
		if (n & 1)
		{
			Count = Power(2, 2 * n - 1);
		}
		else
		{
			const long long Half = Power(2, n - 1);
			Count = Half * (2 * Half + 1) % Modulus;
		}
		Answer ^= Count;
	}
	std::cout << Answer << '\n';
}
