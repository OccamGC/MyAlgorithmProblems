// Problem setter's character-state scan, also present in the teaching notes.
// Codex (GPT-6): stream input directly and accumulate exact hundredths.
#include <iomanip>
#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	long long IntegerSum = 0;
	long long DecimalSum = 0;
	long long Value = 0;
	int Digits = 0;
	bool bDot = false;
	std::string Lower;
	std::string Upper;
	auto Flush = [&]()
	{
		if (bDot)
		{
			while (Digits < 2)
			{
				Value *= 10;
				++Digits;
			}
			DecimalSum += Value;
		}
		else
		{
			IntegerSum += Value;
		}
		Value = 0;
		Digits = 0;
		bDot = false;
	};
	char c;
	while (std::cin.get(c))
	{
		if ('0' <= c && c <= '9')
		{
			Value = Value * 10 + c - '0';
			Digits += bDot;
		}
		else if (c == '.')
		{
			bDot = true;
		}
		else
		{
			Flush();
			if ('A' <= c && c <= 'Z')
			{
				Lower.push_back(static_cast<char>(c - 'A' + 'a'));
			}
			else if ('a' <= c && c <= 'z')
			{
				Upper.push_back(static_cast<char>(c - 'a' + 'A'));
			}
		}
	}
	Flush();
	std::cout << IntegerSum << '\n' << DecimalSum / 100 << '.'
		<< std::setw(2) << std::setfill('0') << DecimalSum % 100 << '\n'
		<< Lower << '\n' << Upper << '\n';
}
