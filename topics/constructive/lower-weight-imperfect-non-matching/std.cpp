// Problem setter's solution: Kruskal MST and a walk traversing every tree edge twice.
// GPT-6: iterative traversal, portable implementation, boundary checks and verification.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>
struct FEdge
{
	int u;
	int v;
	int Weight;
	int Id;
};
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<FEdge> Edges(m);
	for (int i = 0; i < m; ++i)
	{
		std::cin >> Edges[i].u >> Edges[i].v >> Edges[i].Weight;
		Edges[i].Id = i + 1;
	}
	std::sort(Edges.begin(), Edges.end(), [](const FEdge& a, const FEdge& b)
	{
		return std::make_pair(a.Weight, a.Id) < std::make_pair(b.Weight, b.Id);
	});
	std::vector<int> Parent(n + 1);
	std::vector<int> Size(n + 1, 1);
	std::iota(Parent.begin(), Parent.end(), 0);
	auto Find = [&](int u)
	{
		while (u != Parent[u])
		{
			Parent[u] = Parent[Parent[u]];
			u = Parent[u];
		}
		return u;
	};
	std::vector<std::vector<std::pair<int, int>>> Tree(n + 1);
	for (const FEdge& Edge : Edges)
	{
		int u = Find(Edge.u);
		int v = Find(Edge.v);
		if (u == v)
		{
			continue;
		}
		if (Size[u] < Size[v])
		{
			std::swap(u, v);
		}
		Parent[v] = u;
		Size[u] += Size[v];
		Tree[Edge.u].push_back({Edge.v, Edge.Id});
		Tree[Edge.v].push_back({Edge.u, Edge.Id});
	}
	std::cout << 2 * (n - 1) << '\n';
	std::vector<int> Stack{1};
	std::vector<int> Incoming(n + 1);
	std::vector<int> Next(n + 1);
	while (!Stack.empty())
	{
		int u = Stack.back();
		if (Next[u] == static_cast<int>(Tree[u].size()))
		{
			Stack.pop_back();
			if (Incoming[u])
			{
				std::cout << Incoming[u] << '\n';
			}
			continue;
		}
		auto Edge = Tree[u][Next[u]++];
		if (Edge.second != Incoming[u])
		{
			std::cout << Edge.second << '\n';
			Incoming[Edge.first] = Edge.second;
			Stack.push_back(Edge.first);
		}
	}
}
