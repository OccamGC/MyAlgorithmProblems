// Divide-and-conquer NTT. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Modulus = 1004535809;

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

void Transform(std::vector<long long>& Values, bool bInverse)
{
	int Length = static_cast<int>(Values.size());
	int Reversed = 0;
	for (int i = 1; i < Length; ++i)
	{
		int Bit = Length / 2;
		while (Reversed & Bit)
		{
			Reversed ^= Bit;
			Bit >>= 1;
		}
		Reversed ^= Bit;
		if (i < Reversed)
		{
			std::swap(Values[i], Values[Reversed]);
		}
	}
	for (int Width = 2; Width <= Length; Width *= 2)
	{
		long long Root = Power(3, (Modulus - 1) / Width);
		if (bInverse)
		{
			Root = Power(Root, Modulus - 2);
		}
		for (int Start = 0; Start < Length; Start += Width)
		{
			long long Factor = 1;
			for (int j = 0; j < Width / 2; ++j)
			{
				long long Left = Values[Start + j];
				long long Right = Values[Start + j + Width / 2] * Factor % Modulus;
				Values[Start + j] = (Left + Right) % Modulus;
				Values[Start + j + Width / 2] = Normalize(Left - Right);
				Factor = Factor * Root % Modulus;
			}
		}
	}
	if (bInverse)
	{
		long long InverseLength = Power(Length, Modulus - 2);
		for (long long& Value : Values)
		{
			Value = Value * InverseLength % Modulus;
		}
	}
}

// Coefficient index is exponent + n, which equals i + t.
void Accumulate(int l, int r, const std::vector<long long>& Inverse, std::vector<long long>& Coefficient)
{
	const int n = static_cast<int>(Inverse.size()) - 1;
	if (r - l < 32)
	{
		for (int i = l; i <= r; ++i)
		{
			for (int t = i; t <= r; ++t)
			{
				Coefficient[i + t] = (Coefficient[i + t] + Inverse[i] * Inverse[n - t]) % Modulus;
			}
		}
		return;
	}
	int Mid = (l + r) / 2;
	Accumulate(l, Mid, Inverse, Coefficient);
	Accumulate(Mid + 1, r, Inverse, Coefficient);
	int Length = 1;
	while (Length < r - l)
	{
		Length *= 2;
	}
	std::vector<long long> Left(Length);
	std::vector<long long> Right(Length);
	for (int i = l; i <= Mid; ++i)
	{
		Left[i - l] = Inverse[i];
	}
	for (int t = Mid + 1; t <= r; ++t)
	{
		Right[t - Mid - 1] = Inverse[n - t];
	}
	Transform(Left, false);
	Transform(Right, false);
	for (int i = 0; i < Length; ++i)
	{
		Left[i] = Left[i] * Right[i] % Modulus;
	}
	Transform(Left, true);
	for (int i = 0; i < r - l; ++i)
	{
		int Index = l + Mid + 1 + i;
		Coefficient[Index] = (Coefficient[Index] + Left[i]) % Modulus;
	}
}

int main()
{
	int n;
	std::cin >> n;
	std::vector<long long> Inverse(n + 1, 1);
	long long Factorial = 1;
	for (int i = 1; i <= n; ++i)
	{
		Factorial = Factorial * i % Modulus;
	}
	Inverse[n] = Power(Factorial, Modulus - 2);
	for (int i = n; i > 0; --i)
	{
		Inverse[i - 1] = Inverse[i] * i % Modulus;
	}
	std::vector<long long> Coefficient(2 * n + 1);
	Accumulate(0, n, Inverse, Coefficient);
	std::array<long long, 3> Answer{};
	for (int i = 0; i <= 2 * n; ++i)
	{
		int Residue = ((i - n) % 3 + 3) % 3;
		Answer[Residue] = (Answer[Residue] + Coefficient[i]) % Modulus;
	}
	std::cout << Answer[0] << ' ' << Answer[1] << ' ' << Answer[2] << '\n';
}
