#include "mst.hpp"

#include <iostream>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	if (!(std::cin >> n))
	{
		return 0;
	}
	std::vector<FPoint> Points(n);
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Points[i].x >> Points[i].y;
		Points[i].Id = i;
	}
	const FTree Tree = BuildMinimumSpanningTree(Points);
	struct FArc
	{
		int To;
		int Next;
	};
	std::vector<int> Head(n, -1);
	std::vector<FArc> Arcs;
	Arcs.reserve(2 * (n - 1));
	auto AddArc = [&](int u, int v)
	{
		Arcs.push_back({v, Head[u]});
		Head[u] = static_cast<int>(Arcs.size()) - 1;
	};
	for (auto [u, v] : Tree.Edges)
	{
		AddArc(u, v);
		AddArc(v, u);
	}
	// Preorder is the first-visit order of the doubled-tree Euler walk.
	// An explicit stack also handles a path of 400000 farms safely.
	std::vector<std::pair<int, int>> Stack;
	Stack.emplace_back(0, -1);
	while (!Stack.empty())
	{
		const auto [u, Parent] = Stack.back();
		Stack.pop_back();
		std::cout << u + 1 << ' ';
		for (int e = Head[u]; e != -1; e = Arcs[e].Next)
		{
			if (Arcs[e].To != Parent)
			{
				Stack.emplace_back(Arcs[e].To, u);
			}
		}
	}
	std::cout << "1\n";
	return 0;
}
