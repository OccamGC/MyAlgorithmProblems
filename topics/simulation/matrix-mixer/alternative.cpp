// Codex (GPT-6): row/column permutations plus a transposition flag.
// This avoids moving cell values; printing every valid state is still required.
#include <algorithm>
#include <iostream>
#include <numeric>
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
	std::vector<int> Rows(n);
	std::vector<int> Columns(m);
	std::iota(Rows.begin(), Rows.end(), 0);
	std::iota(Columns.begin(), Columns.end(), 0);
	bool bTransposed = false;
	while (K-- > 0)
	{
		int Operation;
		std::cin >> Operation;
		if (Operation == 3)
		{
			Rows.swap(Columns);
			std::reverse(Columns.begin(), Columns.end());
			bTransposed = !bTransposed;
		}
		else
		{
			int a;
			int b;
			std::cin >> a >> b;
			auto& Indices = Operation == 1 ? Rows : Columns;
			if (a < 1 || b < 1 || a > static_cast<int>(Indices.size()) || b > static_cast<int>(Indices.size()))
			{
				std::cout << "Invalid arguments!\n";
				continue;
			}
			std::swap(Indices[a - 1], Indices[b - 1]);
		}
		for (int Row : Rows)
		{
			for (std::size_t j = 0; j < Columns.size(); ++j)
			{
				int Column = Columns[j];
				int Value = bTransposed ? Grid[Column][Row] : Grid[Row][Column];
				std::cout << (j == 0 ? "" : " ") << Value;
			}
			std::cout << '\n';
		}
	}
}
