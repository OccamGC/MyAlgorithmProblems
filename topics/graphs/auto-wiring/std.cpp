// Contribution: Codex (GPT-6): iterative Hopcroft-Karp implementation and
// minimum vertex cover extraction from alternating reachability.
#include <algorithm>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Side(n);
	std::vector<std::vector<int>> Graph(n);
	for (int& a : Side)
	{
		std::cin >> a;
	}
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		--u;
		--v;
		if (Side[u] == 1)
		{
			std::swap(u, v);
		}
		Graph[u].push_back(v);
	}
	std::vector<int> Mate(n, -1);
	std::vector<int> Distance(n);
	std::vector<std::size_t> Current(n);
	while (true)
	{
		std::fill(Distance.begin(), Distance.end(), -1);
		std::fill(Current.begin(), Current.end(), 0);
		std::queue<int> Queue;
		for (int u = 0; u < n; ++u)
		{
			if (Side[u] == 0 && Mate[u] == -1)
			{
				Distance[u] = 0;
				Queue.push(u);
			}
		}
		int Shortest = std::numeric_limits<int>::max();
		while (!Queue.empty())
		{
			int u = Queue.front();
			Queue.pop();
			if (Distance[u] >= Shortest)
			{
				continue;
			}
			for (int v : Graph[u])
			{
				if (Mate[v] == -1)
				{
					Shortest = Distance[u] + 1;
				}
				else if (Distance[Mate[v]] == -1)
				{
					Distance[Mate[v]] = Distance[u] + 1;
					Queue.push(Mate[v]);
				}
			}
		}
		if (Shortest == std::numeric_limits<int>::max())
		{
			break;
		}
		for (int Start = 0; Start < n; ++Start)
		{
			if (Side[Start] != 0 || Mate[Start] != -1)
			{
				continue;
			}
			std::vector<int> Stack{Start};
			bool bAugmented = false;
			while (!Stack.empty() && !bAugmented)
			{
				int u = Stack.back();
				bool bAdvanced = false;
				while (Current[u] < Graph[u].size())
				{
					int v = Graph[u][Current[u]++];
					if (Mate[v] == -1 && Distance[u] + 1 == Shortest)
					{
						for (auto It = Stack.rbegin(); It != Stack.rend(); ++It)
						{
							int Old = Mate[*It];
							Mate[*It] = v;
							Mate[v] = *It;
							v = Old;
						}
						bAugmented = true;
						break;
					}
					if (Mate[v] != -1 && Distance[Mate[v]] == Distance[u] + 1)
					{
						Stack.push_back(Mate[v]);
						bAdvanced = true;
						break;
					}
				}
				if (!bAdvanced && !bAugmented)
				{
					Distance[u] = -1;
					Stack.pop_back();
				}
			}
		}
	}
	std::vector<char> Reached(n, false);
	std::queue<int> Queue;
	for (int u = 0; u < n; ++u)
	{
		if (Side[u] == 0 && Mate[u] == -1)
		{
			Reached[u] = true;
			Queue.push(u);
		}
	}
	while (!Queue.empty())
	{
		int u = Queue.front();
		Queue.pop();
		for (int v : Graph[u])
		{
			if (v != Mate[u] && !Reached[v])
			{
				Reached[v] = true;
				if (Mate[v] != -1 && !Reached[Mate[v]])
				{
					Reached[Mate[v]] = true;
					Queue.push(Mate[v]);
				}
			}
		}
	}
	std::vector<int> Cover;
	for (int u = 0; u < n; ++u)
	{
		if ((Side[u] == 0 && !Reached[u]) || (Side[u] == 1 && Reached[u]))
		{
			Cover.push_back(u + 1);
		}
	}
	std::cout << Cover.size() << '\n';
	for (int u : Cover)
	{
		std::cout << u << ' ';
	}
	std::cout << '\n';
}
