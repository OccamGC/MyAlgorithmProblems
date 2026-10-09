// Codex (GPT-6): traverse horizontal chains row by row; stream each completed row.

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

	std::vector<int> Current{Root};
	while (!Current.empty())
	{
		std::vector<int> Next;
		bool bFirst = true;
		for (int Start : Current)
		{
			for (int u = Start; u != 0; u = Right[u])
			{
				if (!bFirst)
				{
					std::cout << ' ';
				}
				bFirst = false;
				std::cout << u;
				if (Down[u] != 0)
				{
					Next.push_back(Down[u]);
				}
			}
		}
		std::cout << '\n';
		Current = std::move(Next);
	}

}
