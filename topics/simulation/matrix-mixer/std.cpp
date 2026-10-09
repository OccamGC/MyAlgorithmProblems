// Problem setter's solution: physically swap rows/columns and rotate the grid.
// Codex (GPT-6): standard C++17 containers and explicit invalid-operation handling.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int K;
	std::cin >> n >> m >> K;
	std::vector<std::vector<int>> Grid(n, std::vector<int>(m));
	for (auto& Row : Grid)
	{
		for (int& Value : Row)
		{
			std::cin >> Value;
		}
	}
	while (K-- > 0)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 3)
		{
			std::vector<std::vector<int>> Rotated(m, std::vector<int>(n));
			for (int i = 0; i < n; ++i)
			{
				for (int j = 0; j < m; ++j)
				{
					Rotated[j][n - 1 - i] = Grid[i][j];
				}
			}
			Grid.swap(Rotated);
			std::swap(n, m);
		}
		else
		{
			int a;
			int b;
			std::cin >> a >> b;
			int Limit = Operation == 1 ? n : m;
			if (a < 1 || b < 1 || a > Limit || b > Limit)
			{
				std::cout << "Invalid arguments!\n";
				continue;
			}
			--a;
			--b;
			if (Operation == 1)
			{
				Grid[a].swap(Grid[b]);
			}
			else
			{
				for (auto& Row : Grid)
				{
					std::swap(Row[a], Row[b]);
				}
			}
		}
		for (const auto& Row : Grid)
		{
			for (int j = 0; j < m; ++j)
			{
				std::cout << (j == 0 ? "" : " ") << Row[j];
			}
			std::cout << '\n';
		}
	}
}
