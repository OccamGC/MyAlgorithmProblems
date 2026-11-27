// Offline column-coverage DP. C++17 implementation by Codex (GPT-6).
#include <iostream>
#include <vector>

constexpr int Mod = 1000000007;

// Masks mark columns already containing a white cell.
int Count(int n, int Diagonals)
{
	const int States = 1 << n;
	std::vector<int> Ways(States);
	Ways[0] = 1;
	for (int Row = 0; Row < n; ++Row)
	{
		auto Next = Ways;
		for (int j = 0; j < n; ++j)
		{
			if ((Diagonals >= 1 && Row == j) || (Diagonals == 2 && Row + j == n - 1))
			{
				continue;
			}
			int Bit = 1 << j;
			for (int Base = 0; Base < States; Base += 2 * Bit)
			{
				for (int Offset = 0; Offset < Bit; ++Offset)
				{
					int Empty = Base + Offset;
					int Filled = Empty + Bit;
					Next[Filled] = (2LL * Next[Filled] + Next[Empty]) % Mod;
				}
			}
		}
		for (int Mask = 0; Mask < States; ++Mask)
		{
			Next[Mask] -= Ways[Mask];
			if (Next[Mask] < 0)
			{
				Next[Mask] += Mod;
			}
		}
		Ways.swap(Next);
	}
	return Ways.back();
}

int main()
{
	std::cout << 1 << '\n';
	for (int n = 1; n <= 20; ++n)
	{
		long long Answer = Count(n, 0) - 2LL * Count(n, 1) + Count(n, 2);
		std::cout << (Answer + 2LL * Mod) % Mod << '\n';
	}
}
