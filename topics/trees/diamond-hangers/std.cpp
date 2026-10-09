// Problem setter: down-before-right traversal grouped by level.
// Codex (GPT-6): explicit stack avoids recursion overflow.

#include <iostream>
#include <utility>
#include <vector>
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Down(n + 1);
	std::vector<int> Right(n + 1);
	std::vector<bool> HasParent(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Down[i] >> Right[i];
		HasParent[Down[i]] = true;
		HasParent[Right[i]] = true;
	}
	int Root = 1;
	while (HasParent[Root])
	{
		++Root;
	}

	std::vector<std::vector<int>> Rows(n);
	std::vector<std::pair<int, int>> Stack{{Root, 0}};
	int LastLevel = 0;
	while (!Stack.empty())
	{
		auto [u, Level] = Stack.back();
		Stack.pop_back();
		Rows[Level].push_back(u);
		if (Level > LastLevel)
		{
			LastLevel = Level;
		}
		if (Right[u] != 0)
		{
			Stack.emplace_back(Right[u], Level);
		}
		if (Down[u] != 0)
		{
			Stack.emplace_back(Down[u], Level + 1);
		}
	}
	for (int Level = 0; Level <= LastLevel; ++Level)
	{
		for (std::size_t i = 0; i < Rows[Level].size(); ++i)
		{
			if (i != 0)
			{
				std::cout << ' ';
			}
			std::cout << Rows[Level][i];
		}
		std::cout << '\n';
	}

}
