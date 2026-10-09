// Contribution: Codex (GPT-6): explicit traversal while preserving the original counting buckets.
// Original longest-chain gains with counting buckets; iterative traversal repairs stack depth.
#include <iostream>
#include <string>
#include <vector>

struct FEdge
{
	int To;
	int Next;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	if (!(std::cin >> n))
	{
		return 0;
	}
	std::vector<int> Head(n + 1, -1);
	std::vector<FEdge> Edges;
	Edges.reserve(2 * (n - 1));
	auto AddEdge = [&](int u, int v)
	{
		Edges.push_back({v, Head[u]});
		Head[u] = static_cast<int>(Edges.size()) - 1;
	};
	for (int i = 1; i < n; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		AddEdge(u, v);
		AddEdge(v, u);
	}

	std::vector<int> Parent(n + 1, 0);
	std::vector<int> Order;
	Order.reserve(n);
	Order.push_back(1);
	for (std::size_t i = 0; i < Order.size(); ++i)
	{
		const int u = Order[i];
		for (int e = Head[u]; e != -1; e = Edges[e].Next)
		{
			const int v = Edges[e].To;
			if (v == Parent[u])
			{
				continue;
			}
			Parent[v] = u;
			Order.push_back(v);
		}
	}

	std::vector<int> PathVertices(n + 1, 1);
	std::vector<int> Heavy(n + 1, 0);
	for (int i = n - 1; i >= 0; --i)
	{
		const int u = Order[i];
		for (int e = Head[u]; e != -1; e = Edges[e].Next)
		{
			const int v = Edges[e].To;
			if (v != Parent[u] && PathVertices[v] + 1 > PathVertices[u])
			{
				PathVertices[u] = PathVertices[v] + 1;
				Heavy[u] = v;
			}
		}
	}

	std::vector<int> Count(n, 0);
	++Count[PathVertices[1] - 1];
	int Days = 1;
	for (int v = 2; v <= n; ++v)
	{
		if (Heavy[Parent[v]] != v)
		{
			++Count[PathVertices[v]];
			++Days;
		}
	}
	std::string Output = std::to_string(Days) + '\n';
	int Served = 0;
	for (int Gain = n - 1; Gain >= 1; --Gain)
	{
		for (int i = 0; i < Count[Gain]; ++i)
		{
			Served += Gain;
			Output += std::to_string(Served) + '\n';
		}
	}
	std::cout << Output;
}
