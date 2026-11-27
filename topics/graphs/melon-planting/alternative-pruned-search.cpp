// Pruned maximal-matching search. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int Type;
	std::cin >> n >> m >> Type;
	std::vector<std::string> Grid(n);
	for (auto& Row : Grid)
	{
		std::cin >> Row;
	}
	std::vector<std::vector<int>> Neighbors;
	const int dx[] = {-1, 1, 0, 0};
	const int dy[] = {0, 0, -1, 1};
	for (int x = 0; x < n; ++x)
	{
		for (int y = 0; y < m; ++y)
		{
			if (Grid[x][y] != 'l')
			{
				continue;
			}
			Neighbors.emplace_back();
			for (int d = 0; d < 4; ++d)
			{
				const int a = x + dx[d];
				const int b = y + dy[d];
				if (0 <= a && a < n && 0 <= b && b < m && Grid[a][b] == 'o')
				{
					Neighbors.back().push_back(a * m + b);
				}
			}
		}
	}
	const int p = static_cast<int>(Neighbors.size());
	std::vector<int> Match(n * m, -1);
	std::vector<int> Seen(n * m);
	int Stamp = 0;
	std::function<bool(int)> Augment = [&](int u)
	{
		for (int v : Neighbors[u])
		{
			if (Seen[v] == Stamp)
			{
				continue;
			}
			Seen[v] = Stamp;
			if (Match[v] == -1 || Augment(Match[v]))
			{
				Match[v] = u;
				return true;
			}
		}
		return false;
	};
	int Maximum = 0;
	for (int u = 0; u < p; ++u)
	{
		++Stamp;
		Maximum += Augment(u);
	}
	if (Type == 0)
	{
		std::cout << Maximum << '\n';
		return 0;
	}
	std::vector<int> Remaining(n * m);
	std::vector<int> Required(n * m);
	std::vector<bool> Occupied(n * m);
	for (const auto& Row : Neighbors)
	{
		for (int v : Row)
		{
			++Remaining[v];
		}
	}
	int Best = Maximum;
	std::function<void(int, int)> Search = [&](int u, int Count)
	{
		if (Count >= Best)
		{
			return;
		}
		if (u == p)
		{
			Best = Count;
			return;
		}
		for (int v : Neighbors[u])
		{
			--Remaining[v];
		}
		auto CanFinish = [&]()
		{
			for (int v : Neighbors[u])
			{
				if (Required[v] && !Occupied[v] && Remaining[v] == 0)
				{
					return false;
				}
			}
			return true;
		};
		for (int v : Neighbors[u])
		{
			++Required[v];
		}
		if (CanFinish())
		{
			Search(u + 1, Count);
		}
		for (int v : Neighbors[u])
		{
			--Required[v];
		}
		for (int v : Neighbors[u])
		{
			if (!Occupied[v])
			{
				Occupied[v] = true;
				if (CanFinish())
				{
					Search(u + 1, Count + 1);
				}
				Occupied[v] = false;
			}
		}
		for (int v : Neighbors[u])
		{
			++Remaining[v];
		}
	};
	Search(0, 0);
	std::cout << Best << '\n';
}
