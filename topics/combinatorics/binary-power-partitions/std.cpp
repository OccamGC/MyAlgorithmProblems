// Problem setter's splitting DP; prefix-sum acceleration and portable implementation: GPT-6.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr std::int64_t Mod = 1000000000;
std::int64_t Count[63][63][63]{};

int main()
{
	std::uint64_t n;
	std::cin >> n;
	if (n == 0)
	{
		std::cout << 1 << '\n';
		return 0;
	}
	std::vector<int> Bits;
	for (int i = 0; i < 63; ++i)
	{
		if ((n >> i) & 1)
		{
			Bits.push_back(i);
		}
	}
	int Maximum = Bits.back();
	for (int j = 0; j <= Maximum; ++j)
	{
		Count[j][j][j] = 1;
		for (int k = 0; k < j; ++k)
		{
			std::int64_t Suffix[63]{};
			std::int64_t Sum = 0;
			for (int l = k; l >= 0; --l)
			{
				Sum = (Sum + Count[l][j - 1][k]) % Mod;
				Suffix[l] = Sum;
			}
			for (int i = 0; i <= k; ++i)
			{
				std::int64_t Result = 0;
				for (int l = i; l <= k; ++l)
				{
					Result = (Result + Count[i][j - 1][l] * Suffix[l]) % Mod;
				}
				Count[i][j][k] = Result;
			}
		}
	}
	std::int64_t Next[63];
	std::fill(Next, Next + 63, 1);
	for (int Index = static_cast<int>(Bits.size()) - 1; Index >= 0; --Index)
	{
		int b = Bits[Index];
		std::int64_t Current[63]{};
		for (int i = 0; i <= b; ++i)
		{
			for (int k = i; k <= b; ++k)
			{
				Current[i] = (Current[i] + Count[i][b][k] * Next[k]) % Mod;
			}
		}
		for (int i = b - 1; i >= 0; --i)
		{
			Current[i] = (Current[i] + Current[i + 1]) % Mod;
		}
		std::copy(Current, Current + 63, Next);
	}
	std::cout << Next[0] << '\n';
}

