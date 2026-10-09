// Codex (GPT-6): subset DP for the union of required pair-operation results.

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
	const std::uint32_t Limit = std::uint32_t{1} << n;
	std::vector<std::uint32_t> Need(Limit, 0);
	std::vector<std::uint8_t> Lowest(Limit, 0);
	for (int i = 0; i < n; ++i)
	{
		Lowest[std::uint32_t{1} << i] = i;
	}
	int Answer = 0;
	for (std::uint32_t Mask = 1; Mask < Limit; ++Mask)
	{
		const std::uint32_t Bit = Mask & (~Mask + 1);
		const int i = Lowest[Bit];
		const std::uint32_t Rest = Mask ^ Bit;
		std::uint32_t Required = Need[Rest] | Bit;
		for (std::uint32_t Remaining = Rest; Remaining != 0; Remaining &= Remaining - 1)
		{
			const int j = Lowest[Remaining & (~Remaining + 1)];
			Required |= std::uint32_t{1} << Operation[i][j];
			Required |= std::uint32_t{1} << Operation[j][i];
		}
		Need[Mask] = Required;
		if ((Required & Mask) == Required)
		{
			++Answer;
		}
	}
	std::cout << Answer << '\n';
}
