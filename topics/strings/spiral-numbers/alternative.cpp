// Codex (GPT-6): arithmetic digit reversal as an alternative representation.
#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int T;
	std::cin >> T;
	for (int i = 0; i < T; ++i)
	{
		unsigned long long Value;
		std::cin >> Value;
		unsigned long long Remaining = Value;
		unsigned long long Reversed = 0;
		while (Remaining > 0)
		{
			Reversed = Reversed * 10 + Remaining % 10;
			Remaining /= 10;
		}
		std::cout << (Value == Reversed ? 'Y' : 'N') << '\n';
	}
}
