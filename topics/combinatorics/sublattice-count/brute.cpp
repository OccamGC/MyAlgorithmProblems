// Problem setter's enumeration: check all pairs of every nonempty subset.
// Codex (GPT-6): standard C++17 small-case verification implementation.

#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int MaximumSize = 22;
int n;
std::array<std::array<int, MaximumSize>, MaximumSize> Operation{};


int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cin >> n;
	for (int i = 0; i < n; ++i)
	{
		for (int j = 0; j < n; ++j)
		{
			std::cin >> Operation[i][j];
			--Operation[i][j];
		}
	}
	int Answer = 0;
	for (std::uint32_t Mask = 1; Mask < (std::uint32_t{1} << n); ++Mask)
	{
		bool bClosed = true;
		for (int i = 0; i < n && bClosed; ++i)
		{
			if ((Mask & (std::uint32_t{1} << i)) == 0)
			{
				continue;
			}
			for (int j = i + 1; j < n; ++j)
			{
				if ((Mask & (std::uint32_t{1} << j)) != 0 &&
					((Mask & (std::uint32_t{1} << Operation[i][j])) == 0 ||
					(Mask & (std::uint32_t{1} << Operation[j][i])) == 0))
				{
					bClosed = false;
					break;
				}
			}
		}
		Answer += bClosed;
	}
	std::cout << Answer << '\n';
}
