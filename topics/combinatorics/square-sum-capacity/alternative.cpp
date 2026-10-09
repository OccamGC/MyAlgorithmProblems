#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

std::vector<long long> ReadIncremented(const std::string& Text)
{
	std::vector<long long> Digits;
	for (int End = static_cast<int>(Text.size()); End > 0; End -= 4)
	{
		int Start = std::max(0, End - 4);
		Digits.push_back(std::stoi(Text.substr(Start, End - Start)));
	}
	long long Carry = 1;
	for (long long& Digit : Digits)
	{
		Digit += Carry;
		Carry = Digit / 10000;
		Digit %= 10000;
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
		Carry = Digit / 10000;
		Digit %= 10000;
	}
	while (Carry > 0)
	{
		Digits.push_back(Carry % 10000);
		Carry /= 10000;
	}
	long long Remainder = 0;
	for (int i = static_cast<int>(Digits.size()) - 1; i >= 0; --i)
	{
		long long Value = Remainder * 10000 + Digits[i];
		Digits[i] = Value / 2;
		Remainder = Value % 2;
	}
	int Index = 0;
	while (Digits[Index] == 0)
	{
		Digits[Index++] = 9999;
	}
	--Digits[Index];
	while (Digits.size() > 1 && Digits.back() == 0)
	{
		Digits.pop_back();
	}
	std::cout << Digits.back();
	for (int i = static_cast<int>(Digits.size()) - 2; i >= 0; --i)
	{
		std::cout << std::setw(4) << std::setfill('0') << Digits[i];
	}
	std::cout << '\n';
}

std::vector<long long> Multiply(const std::vector<long long>& Values)
{
	int Length = static_cast<int>(Values.size());
	std::vector<long long> Result(2 * Length);
	if (Length <= 32)
	{
		for (int i = 0; i < Length; ++i)
		{
			Result[2 * i] += Values[i] * Values[i];
			for (int j = i + 1; j < Length; ++j)
			{
				Result[i + j] += 2 * Values[i] * Values[j];
			}
		}
		return Result;
	}
	int Half = Length / 2;
	std::vector<long long> LowValues(Values.begin(), Values.begin() + Half);
	std::vector<long long> HighValues(Values.begin() + Half, Values.end());
	std::vector<long long> Low = Multiply(LowValues);
	std::vector<long long> High = Multiply(HighValues);
	for (int i = 0; i < Half; ++i)
	{
		LowValues[i] += HighValues[i];
	}
	std::vector<long long> Middle = Multiply(LowValues);
	for (int i = 0; i < Length; ++i)
	{
		Middle[i] -= Low[i] + High[i];
		Result[i] += Low[i];
		Result[i + Half] += Middle[i];
		Result[i + Length] += High[i];
	}
	return Result;
}

std::vector<long long> Square(std::vector<long long> Digits)
{
	int Length = 1;
	while (Length < static_cast<int>(Digits.size()))
	{
		Length *= 2;
	}
	Digits.resize(Length);
	return Multiply(Digits);
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
