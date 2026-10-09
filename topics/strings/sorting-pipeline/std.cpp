// Problem setter's solution: scan maximal numeric segments and collect letters.
// Codex (GPT-6): exact fixed-point arithmetic and amortized-linear appending.
#include <iomanip>
#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::string S;
	std::getline(std::cin, S);
	long long IntegerSum = 0;
	long long DecimalSum = 0;
	std::string Lower;
	std::string Upper;
	for (std::size_t i = 0; i < S.size();)
	{
		char c = S[i];
		if ('A' <= c && c <= 'Z')
		{
			Lower.push_back(static_cast<char>(c - 'A' + 'a'));
			++i;
		}
		else if ('a' <= c && c <= 'z')
		{
			Upper.push_back(static_cast<char>(c - 'a' + 'A'));
			++i;
		}
		else if (('0' <= c && c <= '9') || c == '.')
		{
			long long Whole = 0;
			int Fraction = 0;
			int Digits = 0;
			bool bDot = false;
			while (i < S.size() && (('0' <= S[i] && S[i] <= '9') || S[i] == '.'))
			{
				c = S[i++];
				if (c == '.')
				{
					bDot = true;
				}
				else if (bDot)
				{
					Fraction = Fraction * 10 + c - '0';
					++Digits;
				}
				else
				{
					Whole = Whole * 10 + c - '0';
				}
			}
			if (bDot)
			{
				DecimalSum += Whole * 100 + Fraction * (Digits == 1 ? 10 : 1);
			}
			else
			{
				IntegerSum += Whole;
			}
		}
		else
		{
			++i; // Accept the carriage return of a CRLF line.
		}
	}
	std::cout << IntegerSum << '\n' << DecimalSum / 100 << '.'
		<< std::setw(2) << std::setfill('0') << DecimalSum % 100 << '\n'
		<< Lower << '\n' << Upper << '\n';
}
