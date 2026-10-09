#include <algorithm>
#include <iostream>
#include <iterator>
#include <memory>
#include <set>
#include <vector>

struct FBag
{
	std::set<int> Order;
	long long CycleSum = 0;
	long long ControlledWeight = 0;
};

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
	auto PathDistance = [&](int u, int v)
	{
		return Distance[u] + Distance[v] - 2 * Distance[Lca(u, v)];
	};
	auto Insert = [&](FBag& Bag, int Vertex)
	{
		const int Key = Entry[Vertex];
		if (!Bag.Order.empty())
		{
			auto Next = Bag.Order.lower_bound(Key);
			if (Next == Bag.Order.end())
			{
				Next = Bag.Order.begin();
			}
			auto Previous = Next == Bag.Order.begin() ? std::prev(Bag.Order.end()) : std::prev(Next);
			const int u = Order[*Previous];
			const int v = Order[*Next];
			Bag.CycleSum += PathDistance(u, Vertex) + PathDistance(Vertex, v) - PathDistance(u, v);
		}
		Bag.Order.insert(Key);
		Bag.ControlledWeight += Value[Vertex];
	};
	std::vector<std::unique_ptr<FBag>> Bags(n + 1);
	std::vector<long long> Answer(n + 1);
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		const int u = *It;
		int Largest = 0;
		for (int v : Edges[u])
		{
			if (Ancestor[0][v] == u && (Largest == 0 || Bags[v]->Order.size() > Bags[Largest]->Order.size()))
			{
				Largest = v;
			}
		}
		Bags[u] = Largest == 0 ? std::make_unique<FBag>() : std::move(Bags[Largest]);
		for (int v : Edges[u])
		{
			if (Ancestor[0][v] == u && v != Largest)
			{
				for (int Key : Bags[v]->Order)
				{
					Insert(*Bags[u], Order[Key]);
				}
				Bags[v].reset();
			}
		}
		Insert(*Bags[u], Control[u]);
		const FBag& Bag = *Bags[u];
		const int Top = Lca(Order[*Bag.Order.begin()], Order[*Bag.Order.rbegin()]);
		Answer[u] = Bag.CycleSum / 2 + Value[Top] - Bag.ControlledWeight;
	}
	for (int u = 1; u <= n; ++u)
	{
		std::cout << Answer[u] << '\n';
	}
}
