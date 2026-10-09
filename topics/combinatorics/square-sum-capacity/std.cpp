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

std::vector<long long> ReadIncremented(const std::string& Text)
{
	std::vector<long long> Digits;
	for (int End = static_cast<int>(Text.size()); End > 0; End -= 2)
	{
		int Start = std::max(0, End - 2);
		Digits.push_back(std::stoi(Text.substr(Start, End - Start)));
	}
	long long Carry = 1;
	for (long long& Digit : Digits)
	{
		Digit += Carry;
		Carry = Digit / 100;
		Digit %= 100;
	}
	if (Carry > 0)
	{
		Digits.push_back(Carry);
	}
	return Digits;
}

void PrintAnswer(std::vector<long long> Digits)
{
	long long Carry = 0;
	for (long long& Digit : Digits)
	{
		Digit += Carry;
		Carry = Digit / 100;
		Digit %= 100;
	}
	while (Carry > 0)
	{
		Digits.push_back(Carry % 100);
		Carry /= 100;
	}
	long long Remainder = 0;
	for (int i = static_cast<int>(Digits.size()) - 1; i >= 0; --i)
	{
		long long Value = Remainder * 100 + Digits[i];
		Digits[i] = Value / 2;
		Remainder = Value % 2;
	}
	int Index = 0;
	while (Digits[Index] == 0)
	{
		Digits[Index++] = 99;
	}
	--Digits[Index];
	while (Digits.size() > 1 && Digits.back() == 0)
	{
		Digits.pop_back();
	}
	std::cout << Digits.back();
	for (int i = static_cast<int>(Digits.size()) - 2; i >= 0; --i)
	{
		std::cout << std::setw(2) << std::setfill('0') << Digits[i];
	}
	std::cout << '\n';
}

std::vector<long long> Square(std::vector<long long> Digits)
{
	int Length = 1;
	while (Length < 2 * static_cast<int>(Digits.size()))
	{
		Length *= 2;
	}
	Digits.resize(Length);
	Transform(Digits, false);
	for (long long& Digit : Digits)
	{
		Digit = Digit * Digit % Modulus;
	}
	Transform(Digits, true);
	return Digits;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T--)
	{
		std::string Text;
		std::cin >> Text;
		Text.erase(0, Text.find_first_not_of('0'));
		std::vector<long long> Digits = ReadIncremented(Text);
		PrintAnswer(Square(Digits));
	}
}
