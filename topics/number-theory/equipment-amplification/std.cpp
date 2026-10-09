// Problem setter's solution: fixed-width prefix table followed by a partial-block scan.
// Codex (GPT-6): C++17 organization, final-block bounds, and reproducible table generation.
#include <cstdint>
#include <iostream>
#include <string>
#include "prefix-table.hpp"

constexpr std::uint32_t BlockSize = 160000;

std::uint32_t EncodeBound(const std::string& Text)
{
	std::uint32_t Result = 0;
	bool bFill = false;
	for (char Digit : Text)
	{
		bFill = bFill || Digit > '1';
		Result = Result * 2 + (bFill ? 1 : Digit - '0');
	}
	return Result;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::uint32_t Powers[30];
	Powers[0] = 1;
	for (int i = 1; i < 30; ++i)
	{
		Powers[i] = Powers[i - 1] * 10u;
	}
	int q;
	std::cin >> q;
	while (q--)
	{
		std::string Bound;
		std::cin >> Bound;
		std::uint32_t End = EncodeBound(Bound);
		std::uint32_t Block = End / BlockSize;
		std::uint32_t Answer = PrefixCount[Block];
		if (Block + 1 >= PrefixCount.size() || PrefixCount[Block + 1] != Answer)
		{
			for (std::uint32_t Mask = Block * BlockSize + 1; Mask <= End; ++Mask)
			{
				std::uint32_t Decimal = 0;
				std::uint32_t Bits = Mask;
				for (int i = 0; Bits != 0; ++i, Bits >>= 1)
				{
					if (Bits & 1u)
					{
						Decimal += Powers[i];
					}
				}
				if ((Decimal & Mask) == Mask)
				{
					++Answer;
				}
			}
		}
		std::cout << Answer << '\n';
	}
}
