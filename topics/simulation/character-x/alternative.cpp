// Problem setter's solution: substitute characters into a fixed template.
// Codex (GPT-6): C++17 formatting and whitespace validation.
#include <array>
#include <iostream>
#include <string>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	const std::array<std::string, 8> Pattern = {
		"###    ###", " ###  ### ", "  ######  ", "   ####   ",
		"   ####   ", "  ######  ", " ###  ### ", "###    ###"
	};
	int T;
	std::cin >> T;
	while (T--)
	{
		char c;
		std::cin >> c;
		for (const std::string& Row : Pattern)
		{
			for (char Cell : Row)
			{
				std::cout << (Cell == '#' ? c : ' ');
			}
			std::cout << '\n';
		}
	}
}
