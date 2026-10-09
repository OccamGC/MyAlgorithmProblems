// Problem setter's solution: partitions and Euler's pentagonal recurrence.
// Codex (GPT-6): sparse recurrence, modular arithmetic and C++17 implementation.
#include <iostream>
#include <vector>

int main()
{
	int X;
	std::cin >> X;
	constexpr long long Mod = 998244353;
	std::vector<long long> Count(X + 1);
	Count[0] = 1;
	for (int s = 1; s <= X; ++s)
	{
		for (int k = 1; k * (3 * k - 1) / 2 <= s; ++k)
		{
			int First = k * (3 * k - 1) / 2;
			int Second = k * (3 * k + 1) / 2;
			long long Sign = k % 2 == 1 ? 1 : -1;
			Count[s] = (Count[s] + Sign * Count[s - First] + Mod) % Mod;
			if (Second <= s)
			{
				Count[s] = (Count[s] + Sign * Count[s - Second] + Mod) % Mod;
			}
		}
	}
	long long Answer = 0;
	for (int s = 0; s <= X; ++s)
	{
		Answer = (Answer + (X - s) * Count[s]) % Mod;
	}
	std::cout << Answer << '\n';
}
