// Unit-capacity Dinic. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

struct FArc
{
	int To;
	bool bOpen;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Side(n);
	const int Source = n;
	const int Sink = n + 1;
	std::vector<std::vector<int>> Graph(n + 2);
	std::vector<FArc> Arcs;
	auto Add = [&](int u, int v)
	{
		Graph[u].push_back(static_cast<int>(Arcs.size()));
		Arcs.push_back({v, true});
		Graph[v].push_back(static_cast<int>(Arcs.size()));
		Arcs.push_back({u, false});
	};
	for (int& a : Side)
	{
		std::cin >> a;
	}
	for (int u = 0; u < n; ++u)
	{
		if (Side[u] == 0)
		{
			Add(Source, u);
		}
		else
		{
			Add(u, Sink);
		}
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
		Add(u, v);
	}
	std::vector<int> Level(n + 2);
	while (true)
	{
		std::fill(Level.begin(), Level.end(), -1);
		std::queue<int> Queue;
		Level[Source] = 0;
		Queue.push(Source);
		while (!Queue.empty())
		{
			int u = Queue.front();
			Queue.pop();
			for (int Id : Graph[u])
			{
				const FArc& Edge = Arcs[Id];
				if (Edge.bOpen && Level[Edge.To] < 0)
				{
					Level[Edge.To] = Level[u] + 1;
					Queue.push(Edge.To);
				}
			}
		}
		if (Level[Sink] < 0)
		{
			break;
		}
		std::vector<std::size_t> Next(n + 2);
		std::vector<int> Path;
		int u = Source;
		while (true)
		{
			if (u == Sink)
			{
				for (int Id : Path)
				{
					Arcs[Id].bOpen = false;
					Arcs[Id ^ 1].bOpen = true;
				}
				Path.clear();
				u = Source;
			}
			while (Next[u] < Graph[u].size())
			{
				const FArc& Edge = Arcs[Graph[u][Next[u]]];
				if (Edge.bOpen && Level[Edge.To] == Level[u] + 1)
				{
					break;
				}
				++Next[u];
			}
			if (Next[u] < Graph[u].size())
			{
				int Id = Graph[u][Next[u]++];
				Path.push_back(Id);
				u = Arcs[Id].To;
			}
			else if (Path.empty())
			{
				break;
			}
			else
			{
				u = Arcs[Path.back() ^ 1].To;
				Path.pop_back();
			}
		}
	}
	std::vector<int> Cover;
	for (int u = 0; u < n; ++u)
	{
		if ((Side[u] == 0 && Level[u] < 0) || (Side[u] == 1 && Level[u] >= 0))
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
