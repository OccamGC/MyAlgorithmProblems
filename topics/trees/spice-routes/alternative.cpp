#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

constexpr long long Mod = 1000000007;

struct FEdge
{
	int u;
	int v;
	int q;
	int p;
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<FEdge> Edges(n - 1);
	std::vector<std::vector<int>> Graph(n + 1);
	int MaximumDenominator = 1;
	for (int i = 0; i < n - 1; ++i)
	{
		auto& Edge = Edges[i];
		std::cin >> Edge.u >> Edge.v >> Edge.q >> Edge.p;
		Graph[Edge.u].push_back(i);
		Graph[Edge.v].push_back(i);
		MaximumDenominator = std::max(MaximumDenominator, Edge.p);
	}
	std::vector<int> Type(n + 1);
	for (int Mark = 1; Mark <= 2; ++Mark)
	{
		int Count;
		std::cin >> Count;
		for (int i = 0; i < Count; ++i)
		{
			int u;
			std::cin >> u;
			Type[u] |= Mark;
		}
	}
	std::vector<long long> Inverse(MaximumDenominator + 1);
	Inverse[1] = 1;
	for (int i = 2; i <= MaximumDenominator; ++i)
	{
		Inverse[i] = Mod - Mod / i * Inverse[Mod % i] % Mod;
	}
	std::vector<int> Parent(n + 1);
	std::vector<int> Order{1};
	for (int i = 0; i < n; ++i)
	{
		const int u = Order[i];
		for (int Index : Graph[u])
		{
			const auto& Edge = Edges[Index];
			const int v = Edge.u ^ Edge.v ^ u;
			if (v != Parent[u])
			{
				Parent[v] = u;
				Order.push_back(v);
			}
		}
	}
	std::vector<std::array<long long, 3>> Dp(n + 1);
	for (int i = n - 1; i >= 0; --i)
	{
		const int u = Order[i];
		if (Type[u] != 3)
		{
			Dp[u][Type[u]] = 1;
		}
		for (int Index : Graph[u])
		{
			const auto& Edge = Edges[Index];
			const int v = Edge.u ^ Edge.v ^ u;
			if (Parent[v] != u)
			{
				continue;
			}
			const long long Closed = Edge.q * Inverse[Edge.p] % Mod;
			const long long Open = (1 - Closed + Mod) % Mod;
			std::array<long long, 3> Next{};
			for (int a = 0; a < 3; ++a)
			{
				for (int b = 0; b < 3; ++b)
				{
					const long long Joint = Dp[u][a] * Dp[v][b] % Mod;
					Next[a] = (Next[a] + Joint * Closed) % Mod;
					if ((a | b) != 3)
					{
						Next[a | b] = (Next[a | b] + Joint * Open) % Mod;
					}
				}
			}
			Dp[u] = Next;
		}
	}
	long long Answer = 1;
	for (long long Value : Dp[1])
	{
		Answer = (Answer - Value + Mod) % Mod;
	}
	std::cout << Answer << '\n';
}
