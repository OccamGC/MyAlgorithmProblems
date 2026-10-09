// Problem setter's solution: significant binary length plus set-bit count minus one.
// Codex (GPT-6): specify the exponent-reduction boundary and verify leading zeros.
#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int Q;
	std::cin >> Q;
	while (Q-- > 0)
	{
		std::string Bits;
		std::cin >> Bits;
		int Length = 0;
		int Ones = 0;
		bool bStarted = false;
		for (char Bit : Bits)
		{
			bStarted = bStarted || Bit == '1';
			if (bStarted)
			{
				++Length;
				Ones += Bit == '1';
			}
		}
		std::cout << (bStarted ? Length + Ones - 1 : 0) << '\n';
	}
}
