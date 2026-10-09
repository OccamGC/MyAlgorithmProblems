// Contribution: Codex (GPT-6): exact rolling bit windows and repeated-block
// recurrences; O(nK) time and O(n + K) space, with no hashing collisions.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int K;
	std::string s;
	std::cin >> n >> K >> s;
	std::vector<int> Ending(n);
	std::vector<int> Answer(n, 0);
	for (int j = 1; j <= std::min(n, K); ++j)
	{
		const std::uint32_t Mask = (1U << j) - 1;
		const int Limit = n / j * j;
		for (int Direction = 0; Direction < 2; ++Direction)
		{
			std::vector<std::uint32_t> Previous(j, 0);
			std::vector<int> Run(j, 0);
			std::uint32_t Forward = 0;
			std::uint32_t Backward = 0;
			for (int i = 0; i < 2 * n - 1; ++i)
			{
				int Position = i % n;
				if (Direction == 1)
				{
					Position = n - 1 - Position;
				}
				std::uint32_t Bit = static_cast<std::uint32_t>(s[Position] - '0');
				Forward = ((Forward << 1) | Bit) & Mask;
				Backward = (Backward >> 1) | (Bit << (j - 1));
				int Slot = i % j;
				int Length = 0;
				if (i + 1 >= j && Forward == Backward)
				{
					Length = j;
					if (Previous[Slot] == Forward)
					{
						Length += Run[Slot];
					}
				}
				Previous[Slot] = Forward;
				Run[Slot] = Length;
				if (i >= n - 1)
				{
					Length = std::min(Length, Limit);
					if (Direction == 0)
					{
						Ending[Position] = Length;
					}
					else
					{
						Answer[Position] ^= j * std::max(Ending[Position], Length);
					}
				}
			}
		}
	}
	for (int Result : Answer)
	{
		std::cout << Result << '\n';
	}
}
