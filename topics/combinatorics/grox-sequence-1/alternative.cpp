#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <string>
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

struct FInput
{
	long long a = 0;
	int b;
	int c;
	long long Exponent = 0;
	bool bZero = true;
	void Read()
	{
		std::string Text;
		std::cin >> Text;
		for (char Digit : Text)
		{
			a = (10 * a + Digit - '0') % Modulus;
		}
		std::cin >> b >> c >> Text;
		for (char Digit : Text)
		{
			Exponent = (10 * Exponent + Digit - '0') % (Modulus - 1);
			bZero = bZero && Digit == '0';
		}
	}
	long long Evaluate(int Index) const
	{
		long long Base = Normalize(a - b - c + Index);
		return Base == 0 && !bZero ? 0 : Power(Base, Exponent);
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	FInput Input;
	Input.Read();
	int Degree = 2 * (Input.b + Input.c);
	int Length = 1;
	while (Length <= Degree)
	{
		Length *= 2;
	}
	std::vector<long long> First(Length);
	std::vector<long long> Second(Length);
	std::vector<long long> Inverse(Input.b + 2);
	Inverse[1] = 1;
	for (int i = 2; i <= Input.b; ++i)
	{
		Inverse[i] = Modulus - (Modulus / i) * Inverse[Modulus % i] % Modulus;
	}
	First[0] = 1;
	for (int i = 1; i <= Input.b; ++i)
	{
		First[2 * i] = First[2 * i - 2] * (Input.b - i + 1) % Modulus * Inverse[i] % Modulus;
	}
	Second[0] = 1;
	for (int i = 0; i < Input.c; ++i)
	{
		for (int j = 2 * i + 2; j >= 0; --j)
		{
			long long Value = -Second[j];
			if (j >= 1)
			{
				Value += 2 * Second[j - 1];
			}
			if (j >= 2)
			{
				Value += Second[j - 2];
			}
			Second[j] = Normalize(Value);
		}
	}
	Transform(First, false);
	Transform(Second, false);
	for (int i = 0; i < Length; ++i)
	{
		First[i] = First[i] * Second[i] % Modulus;
	}
	Transform(First, true);
	long long Answer = 0;
	for (int i = 0; i <= Degree; ++i)
	{
		Answer = (Answer + First[i] * Input.Evaluate(i)) % Modulus;
	}
	std::cout << Answer * Power((Modulus + 1) / 2, Input.b + Input.c) % Modulus << '\n';
}
