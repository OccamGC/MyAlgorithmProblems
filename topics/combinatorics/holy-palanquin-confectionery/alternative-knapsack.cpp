// Codex (GPT-6): complete-knapsack formulation and proof for the budget sum.
#include <iostream>
#include <vector>

int main()
{
	int X;
	std::cin >> X;
	constexpr long long Mod = 998244353;
	std::vector<long long> Count(X + 1);
	Count[0] = 1;
	for (int Price = 1; Price <= X; ++Price)
	{
		for (int s = Price; s <= X; ++s)
		{
			Count[s] = (Count[s] + Count[s - Price]) % Mod;
		}
	}
	long long Answer = 0;
	for (int s = 0; s <= X; ++s)
	{
		Answer = (Answer + (X - s) * Count[s]) % Mod;
	}
	std::cout << Answer << '\n';
}
