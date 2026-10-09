// 本题解法设计与实现：Codex（GPT-6）。基于已有的三状态路径分解方法设计逐格转移。
// Solution design and implementation for this problem: Codex (GPT-6).
// Adapts established three-state frontier DP; O(n * m * 3^w), w = min(n, m).
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::string> Grid(n);
	for (auto& Row : Grid)
	{
		std::cin >> Row;
	}
	if (m > n)
	{
		std::vector<std::string> Transposed(m, std::string(n, 'x'));
		for (int x = 0; x < n; ++x)
		{
			for (int y = 0; y < m; ++y)
			{
				Transposed[y][x] = Grid[x][y];
			}
		}
		Grid.swap(Transposed);
		std::swap(n, m);
	}
	std::vector<int> Power(m + 1, 1);
	for (int i = 1; i <= m; ++i)
	{
		Power[i] = Power[i - 1] * 3;
	}
	const int States = Power[m];
	const int Infinity = n * m + 1;
	std::vector<int> Dp(States, Infinity);
	std::vector<int> Next(States, Infinity);
	Dp[0] = 0;
	auto Adjacent = [&](int x, int y, int a, int b)
	{
		return 0 <= a && a < n && 0 <= b && b < m &&
			((Grid[x][y] == 'l' && Grid[a][b] == 'o') ||
			(Grid[x][y] == 'o' && Grid[a][b] == 'l'));
	};
	for (int x = 0; x < n; ++x)
	{
		for (int y = 0; y < m; ++y)
		{
			const bool bUpEdge = Adjacent(x, y, x - 1, y);
			const bool bLeftEdge = Adjacent(x, y, x, y - 1);
			const bool bFutureEdge = Adjacent(x, y, x + 1, y) || Adjacent(x, y, x, y + 1);
			std::fill(Next.begin(), Next.end(), Infinity);
			for (int Mask = 0; Mask < States; ++Mask)
			{
				const int Cost = Dp[Mask];
				if (Cost == Infinity)
				{
					continue;
				}
				const int Up = Mask / Power[y] % 3;
				const int Left = y == 0 ? 0 : Mask / Power[y - 1] % 3;
				const int Base = Mask - Up * Power[y];
				if (Up != 1)
				{
					if ((!bUpEdge || Up != 0) && (!bLeftEdge || Left != 0))
					{
						Next[Base] = std::min(Next[Base], Cost);
					}
					if (bFutureEdge)
					{
						const int Target = Base + Power[y];
						Next[Target] = std::min(Next[Target], Cost);
					}
					if (bLeftEdge && Left == 1)
					{
						const int Target = Base + 2 * Power[y] + Power[y - 1];
						Next[Target] = std::min(Next[Target], Cost + 1);
					}
				}
				if (bUpEdge && Up == 1)
				{
					const int Target = Base + 2 * Power[y];
					Next[Target] = std::min(Next[Target], Cost + 1);
				}
			}
			Dp.swap(Next);
		}
	}
	int Answer = Infinity;
	for (int Mask = 0; Mask < States; ++Mask)
	{
		int Digits = Mask;
		bool bComplete = true;
		for (int y = 0; y < m; ++y)
		{
			bComplete = bComplete && Digits % 3 != 1;
			Digits /= 3;
		}
		if (bComplete)
		{
			Answer = std::min(Answer, Dp[Mask]);
		}
	}
	std::cout << Answer << '\n';
}
