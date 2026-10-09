// Problem setter's solution: test both diagonal strips.
// Codex (GPT-6): portable C++17 and exact output dimensions.
#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	while (T--)
	{
		char c;
		std::cin >> c;
		for (int i = 1; i <= 8; ++i)
		{
			for (int j = 1; j <= 10; ++j)
			{
				const bool bFilled = (i <= j && j <= i + 2) || (9 - i <= j && j <= 11 - i);
				std::cout << (bFilled ? c : ' ');
			}
			std::cout << '\n';
		}
	}
}
