// Problem setter's solution: skip leading zeroes, then compare opposite digits.
// Codex (GPT-6): bounds-safe scan and portable C++17 implementation.
#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	for (int i = 0; i < T; ++i)
	{
		std::string Digits;
		std::cin >> Digits;
		int Left = 0;
		int Right = static_cast<int>(Digits.size()) - 1;
		while (Left < Right && Digits[Left] == '0')
		{
			++Left;
		}
		bool bPalindrome = true;
		while (Left < Right)
		{
			if (Digits[Left] != Digits[Right])
			{
				bPalindrome = false;
				break;
			}
			++Left;
			--Right;
		}
		std::cout << (bPalindrome ? 'Y' : 'N') << '\n';
	}
}
