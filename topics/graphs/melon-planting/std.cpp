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
	std::vector<std::vector<int>> Reverse(n * m);
	for (int u = 0; u < p; ++u)
	{
		for (int v : Neighbors[u])
		{
			Reverse[v].push_back(u);
		}
	}
	int Answer = Maximum;
	for (int Mask = 0; Mask < (1 << p); ++Mask)
	{
		int Count = 0;
		std::vector<bool> Required(n * m);
		for (int u = 0; u < p; ++u)
		{
			if (Mask >> u & 1)
			{
				++Count;
			}
			else
			{
				for (int v : Neighbors[u])
				{
					Required[v] = true;
				}
			}
		}
		if (Count >= Answer || std::count(Required.begin(), Required.end(), true) > Count)
		{
			continue;
		}
		std::vector<int> VineMatch(p, -1);
		std::vector<bool> Visited(p);
		std::function<bool(int)> Cover = [&](int v)
		{
			for (int u : Reverse[v])
			{
				if (!(Mask >> u & 1) || Visited[u])
				{
					continue;
				}
				Visited[u] = true;
				if (VineMatch[u] == -1 || Cover(VineMatch[u]))
				{
					VineMatch[u] = v;
					return true;
				}
			}
			return false;
		};
		bool bPossible = true;
		for (int v = 0; v < n * m && bPossible; ++v)
		{
			if (Required[v])
			{
				std::fill(Visited.begin(), Visited.end(), false);
				bPossible = Cover(v);
			}
		}
		if (!bPossible)
		{
			continue;
		}
		std::fill(Match.begin(), Match.end(), -1);
		for (int u = 0; u < p; ++u)
		{
			if (VineMatch[u] != -1)
			{
				Match[VineMatch[u]] = u;
			}
		}
		for (int u = 0; u < p && bPossible; ++u)
		{
			if ((Mask >> u & 1) && VineMatch[u] == -1)
			{
				++Stamp;
				bPossible = Augment(u);
			}
		}
		if (bPossible)
		{
			Answer = Count;
		}
	}
	std::cout << Answer << '\n';
}
