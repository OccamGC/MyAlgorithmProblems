// Linear counting sort. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <iostream>
#include <array>
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
	std::vector<std::array<int, 2>> Counts(n + 1);
	int GainCount = 0;
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
					++Counts[Height[v]][0];
					++GainCount;
				}
			}
			Height[u] = Height[Longest] + 1;
		}
		++Counts[Height[Root]][1];
		++GainCount;
	}
	std::cout << GainCount << '\n';
	int Cut = 0;
	int Trees = 0;
	for (int Gain = n; Gain >= 1; --Gain)
	{
		for (int First = 0; First <= 1; ++First)
		{
			for (int i = 0; i < Counts[Gain][First]; ++i)
			{
				Cut += Gain;
				Trees += First;
				std::cout << Cut << ' ' << Trees << '\n';
			}
		}
	}
}
