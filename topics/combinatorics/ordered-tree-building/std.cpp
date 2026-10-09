#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

constexpr long long Modulus = 998244353;

long long Normalize(long long Value)
{
	Value %= Modulus;
	return Value < 0 ? Value + Modulus : Value;
}

long long Power(long long Base, long long Exponent)
{
	Base = Normalize(Base);
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
	int n;
	std::cin >> n;
	if (n <= 2)
	{
		std::cout << 1 << '\n';
		return 0;
	}
	long long Factorial = 1;
	for (int i = 1; i < n; ++i)
	{
		Factorial = Factorial * i % Modulus;
	}
	std::cout << Factorial * Power(n, n - 2) % Modulus << '\n';
}
