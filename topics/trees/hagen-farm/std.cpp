// Codex (GPT-6): sum edge-inclusion probabilities; O(n^2) time and O(n) space.
// The problem setter's subtree DP is described alongside this method in the editorial.
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using FInteger = std::int64_t;
constexpr FInteger Mod = 1000000007;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<std::vector<std::pair<int, int>>> Graph(n + 1);
	for (int i = 1; i < n; ++i)
	{
		int u;
		int v;
		int w;
		std::cin >> u >> v >> w;
		Graph[u].push_back({v, w});
		Graph[v].push_back({u, w});
	}
	std::vector<int> Parent(n + 1);
	std::vector<int> Weight(n + 1);
	std::vector<int> Size(n + 1, 1);
	std::vector<int> Order{1};
	for (std::size_t i = 0; i < Order.size(); ++i)
	{
		int u = Order[i];
		for (auto [v, w] : Graph[u])
		{
			if (v != Parent[u])
			{
				Parent[v] = u;
				Weight[v] = w;
				Order.push_back(v);
			}
		}
	}
	for (int i = n - 1; i > 0; --i)
	{
		Size[Parent[Order[i]]] += Size[Order[i]];
	}
	std::vector<FInteger> Inverse(n + 2, 1);
	for (int i = 2; i <= n + 1; ++i)
	{
		Inverse[i] = Mod - (Mod / i) * Inverse[Mod % i] % Mod;
	}
	FInteger Answer = 0;
	for (int v = 2; v <= n; ++v)
	{
		int t = Size[v];
		FInteger ProbabilitySum = 0;
		for (int u = Parent[v]; u != 0; u = Parent[u])
		{
			int s = Size[u];
			FInteger Excluded = (t * Inverse[s - t + 1] + (s - t) * Inverse[t + 1]) % Mod;
			FInteger Included = (1 - Excluded * Inverse[s] % Mod + Mod) % Mod;
			ProbabilitySum = (ProbabilitySum + Included) % Mod;
		}
		Answer = (Answer + 2 * Weight[v] * ProbabilitySum) % Mod;
	}
	std::cout << Answer * Inverse[n] % Mod << '\n';
}
