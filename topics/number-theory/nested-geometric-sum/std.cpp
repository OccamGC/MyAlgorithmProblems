#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

constexpr long long Modulus = 2147483647;

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
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	long long n;
	int m;
	long long a;
	std::cin >> n >> m >> a;
	int Count = static_cast<int>(std::min(n, static_cast<long long>(m))) + 1;
	std::vector<long long> Inverse(Count + 1);
	Inverse[1] = 1;
	for (int i = 2; i <= Count; ++i)
	{
		Inverse[i] = Modulus - (Modulus / i) * Inverse[Modulus % i] % Modulus;
	}
	long long Answer = 0;
	if (n <= m)
	{
		long long Weight = 1;
		long long LowPower = Power(a, n);
		long long HighPower = Power(a, 2 * n + 1);
		long long InverseA = Power(a, Modulus - 2);
		long long InverseSquare = InverseA * InverseA % Modulus;
		long long InverseDifference = Power(a - 1, Modulus - 2);
		for (int Offset = 0; Offset < n; ++Offset)
		{
			long long Value = a == 1 ? n - Offset + 1 : Normalize(HighPower - LowPower) * InverseDifference % Modulus;
			Answer = (Answer + Weight * Value) % Modulus;
			Weight = Weight * (m + static_cast<long long>(Offset)) % Modulus * Inverse[Offset + 1] % Modulus;
			LowPower = LowPower * InverseA % Modulus;
			HighPower = HighPower * InverseSquare % Modulus;
		}
	}
	else if (a == 1)
	{
		long long Binomial = 1;
		for (int i = 1; i <= m; ++i)
		{
			Binomial = Binomial * (n + i - 1) % Modulus * Inverse[i] % Modulus;
		}
		Answer = (Binomial + Binomial * ((n + m) % Modulus) % Modulus * Inverse[m + 1]) % Modulus;
	}
	else
	{
		long long Square = a * a % Modulus;
		long long First = Power(a, n);
		long long Second = Power(Square, n);
		long long FirstRatio = a * Power(a - 1, Modulus - 2) % Modulus;
		long long SecondRatio = Square * Power(Square - 1, Modulus - 2) % Modulus;
		long long Binomial = 1;
		for (int i = 1; i <= m; ++i)
		{
			First = FirstRatio * Normalize(First - Binomial) % Modulus;
			Second = SecondRatio * Normalize(Second - Binomial) % Modulus;
			Binomial = Binomial * (n + i - 1) % Modulus * Inverse[i] % Modulus;
		}
		Answer = Normalize(a * Second % Modulus - First) * Power(a - 1, Modulus - 2) % Modulus;
	}
	std::cout << Answer << '\n';
}
