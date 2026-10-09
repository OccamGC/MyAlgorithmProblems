// Problem setter's solution: differentiate a finite geometric series.
// Codex (GPT-6): handle every modular ratio of one and organize standard C++17.

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

long long Calculate(long long l, long long r, long long a, long long b, long long c, long long d)
{
	const long long q = Power(c, b);
	const long long Length = r - l + 1;
	long long Sum;
	if (q == 1)
	{
		constexpr long long InverseTwo = (Modulus + 1) / 2;
		const long long Indices = (l + r) % Modulus * Length % Modulus * InverseTwo % Modulus;
		Sum = (a * Length + b * Indices) % Modulus;
	}
	else
	{
		const long long Inverse = Power(q - 1, Modulus - 2);
		const long long InverseSquared = Inverse * Inverse % Modulus;
		auto Prefix = [&](long long n)
		{
			const long long NextPower = Power(q, n + 1);
			const long long Plain = (NextPower - q + Modulus) % Modulus * Inverse % Modulus;
			long long Weighted = (n % Modulus * q - (n + 1)) % Modulus;
			Weighted = (Weighted * NextPower + q) % Modulus;
			Weighted = (Weighted + Modulus) % Modulus * InverseSquared % Modulus;
			return (a * Plain + b * Weighted) % Modulus;
		};
		Sum = (Prefix(r) - Prefix(l - 1) + Modulus) % Modulus;
	}
	return Power(c, d) * Sum % Modulus;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int m;
	std::cin >> m;
	while (m-- > 0)
	{
		long long l;
		long long r;
		long long a;
		long long b;
		long long c;
		long long d;
		std::cin >> l >> r >> a >> b >> c >> d;
		std::cout << Calculate(l, r, a, b, c, d) << '\n';
	}
}
