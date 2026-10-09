#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::vector<int>> Graph(n + 1);
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	std::vector<int> Parent(n + 1, -1);
	std::vector<int> Order;
	std::vector<int> Height(n + 1, 1);
	Height[0] = 0;
	std::vector<std::pair<int, bool>> Gains;
	for (int Root = 1; Root <= n; ++Root)
	{
		if (Parent[Root] != -1)
		{
			continue;
		}
		Parent[Root] = 0;
		const int Begin = static_cast<int>(Order.size());
		Order.push_back(Root);
		for (int i = Begin; i < static_cast<int>(Order.size()); ++i)
		{
			const int u = Order[i];
			for (int v : Graph[u])
			{
				if (v != Parent[u])
				{
					Parent[v] = u;
					Order.push_back(v);
				}
			}
		}
		for (int i = static_cast<int>(Order.size()) - 1; i >= Begin; --i)
		{
			const int u = Order[i];
			int Longest = 0;
			for (int v : Graph[u])
			{
				if (Parent[v] == u && Height[v] > Height[Longest])
				{
					Longest = v;
				}
			}
			// Height[0] is zero, so a leaf has no continuing child.
			for (int v : Graph[u])
			{
				if (Parent[v] == u && v != Longest)
				{
					Gains.emplace_back(Height[v], false);
				}
			}
			Height[u] = Height[Longest] + 1;
		}
		Gains.emplace_back(Height[Root], true);
	}
	std::sort(Gains.begin(), Gains.end(), [](const auto& Left, const auto& Right)
	{
		if (Left.first != Right.first)
		{
			return Left.first > Right.first;
		}
		return Left.second < Right.second;
	});
	std::cout << Gains.size() << '\n';
	int Cut = 0;
	int Trees = 0;
	for (const auto& Gain : Gains)
	{
		Cut += Gain.first;
		Trees += Gain.second;
		std::cout << Cut << ' ' << Trees << '\n';
	}
}
