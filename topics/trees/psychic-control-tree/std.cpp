// Contribution: Codex (GPT-6): explicit DSU scheduling and 64-bit path sums.
// Original DSU-on-tree and predecessor/successor path-union increments.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <memory>
#include <set>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<int> Value(n + 1);
	std::vector<int> Control(n + 1);
	std::vector<std::vector<int>> Edges(n + 1);
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Value[i] >> Control[i];
	}
	for (int i = 1; i < n; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Edges[u].push_back(v);
		Edges[v].push_back(u);
	}
	int Levels = 1;
	while ((1 << Levels) <= n)
	{
		++Levels;
	}
	std::vector<std::vector<int>> Ancestor(Levels, std::vector<int>(n + 1));
	std::vector<int> Depth(n + 1);
	std::vector<int> Entry(n + 1);
	std::vector<int> Order;
	std::vector<long long> Distance(n + 1);
	std::vector<int> Stack = {1};
	while (!Stack.empty())
	{
		const int u = Stack.back();
		Stack.pop_back();
		Entry[u] = static_cast<int>(Order.size());
		Order.push_back(u);
		for (int v : Edges[u])
		{
			if (v == Ancestor[0][u])
			{
				continue;
			}
			Ancestor[0][v] = u;
			Depth[v] = Depth[u] + 1;
			Distance[v] = Distance[u] + Value[v];
			Stack.push_back(v);
		}
	}
	for (int j = 1; j < Levels; ++j)
	{
		for (int u = 1; u <= n; ++u)
		{
			Ancestor[j][u] = Ancestor[j - 1][Ancestor[j - 1][u]];
		}
	}
	auto Lca = [&](int u, int v)
	{
		if (Depth[u] < Depth[v])
		{
			std::swap(u, v);
		}
		for (int j = 0; j < Levels; ++j)
		{
			if (((Depth[u] - Depth[v]) >> j) & 1)
			{
				u = Ancestor[j][u];
			}
		}
		if (u == v)
		{
			return u;
		}
		for (int j = Levels - 1; j >= 0; --j)
		{
			if (Ancestor[j][u] != Ancestor[j][v])
			{
				u = Ancestor[j][u];
				v = Ancestor[j][v];
			}
		}
		return Ancestor[0][u];
	};
	std::vector<int> Size(n + 1, 1);
	std::vector<int> Heavy(n + 1, 0);
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		const int u = *It;
		const int Parent = Ancestor[0][u];
		if (Parent != 0)
		{
			Size[Parent] += Size[u];
			if (Heavy[Parent] == 0 || Size[u] > Size[Heavy[Parent]])
			{
				Heavy[Parent] = u;
			}
		}
	}
	std::set<int> Bag;
	long long UnionCost = 0;
	int Top = 0;
	auto Insert = [&](int Vertex)
	{
		if (Bag.empty())
		{
			Bag.insert(Entry[Vertex]);
			UnionCost = Distance[Vertex] + Value[1] - Value[Vertex];
			Top = Vertex;
			return;
		}
		auto Next = Bag.lower_bound(Entry[Vertex]);
		if (Next == Bag.end())
		{
			Next = Bag.begin();
		}
		auto Previous = Next == Bag.begin() ? std::prev(Bag.end()) : std::prev(Next);
		const int a = Lca(Vertex, Order[*Previous]);
		const int b = Lca(Vertex, Order[*Next]);
		const int Meet = Depth[a] > Depth[b] ? a : b;
		UnionCost += Distance[Vertex] - Distance[Meet] - Value[Vertex];
		Top = Lca(Top, Vertex);
		Bag.insert(Entry[Vertex]);
	};
	struct FTask
	{
		int Vertex;
		int Phase;
		bool bKeep;
	};
	std::vector<FTask> Tasks{{1, 0, true}};
	std::vector<long long> Answer(n + 1);
	while (!Tasks.empty())
	{
		const FTask Task = Tasks.back();
		Tasks.pop_back();
		const int u = Task.Vertex;
		if (Task.Phase == 0)
		{
			Tasks.push_back({u, 1, Task.bKeep});
			if (Heavy[u] != 0)
			{
				Tasks.push_back({Heavy[u], 0, true});
			}
			for (int v : Edges[u])
			{
				if (Ancestor[0][v] == u && v != Heavy[u])
				{
					Tasks.push_back({v, 0, false});
				}
			}
		}
		else
		{
			Insert(Control[u]);
			for (int v : Edges[u])
			{
				if (Ancestor[0][v] == u && v != Heavy[u])
				{
					for (int i = Entry[v]; i < Entry[v] + Size[v]; ++i)
					{
						Insert(Control[Order[i]]);
					}
				}
			}
			Answer[u] = UnionCost - Distance[Top] - Value[1] + Value[Top];
			if (!Task.bKeep)
			{
				Bag.clear();
			}
		}
	}
	for (int u = 1; u <= n; ++u)
	{
		std::cout << Answer[u] << '\n';
	}
}
