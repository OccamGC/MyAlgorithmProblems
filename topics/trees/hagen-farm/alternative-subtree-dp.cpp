// Subtree expectation DP. C++17 implementation by Codex (GPT-6).
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
				Order.push_back(v);
			}
		}
	}
	for (int i = n - 1; i > 0; --i)
	{
		Size[Parent[Order[i]]] += Size[Order[i]];
	}
	// Count weighted subset totals directly; normalization is needed only at the end.
	std::vector<FInteger> Fact(n + 1, 1);
	std::vector<FInteger> InvFact(n + 1, 1);
	std::vector<FInteger> Inv(n + 1, 1);
	for (int i = 1; i <= n; ++i)
	{
		if (i > 1)
		{
			Inv[i] = Mod - Mod / i * Inv[Mod % i] % Mod;
		}
		Fact[i] = Fact[i - 1] * i % Mod;
		InvFact[i] = InvFact[i - 1] * Inv[i] % Mod;
	}
	auto Choose = [&](int s, int k)
	{
		return Fact[s] * InvFact[k] % Mod * InvFact[s - k] % Mod;
	};
	std::vector<std::vector<FInteger>> Forced(n + 1);
	std::vector<std::vector<FInteger>> AtLca(n + 1);
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		int u = *It;
		int s = 1;
		Forced[u] = {0, 0};
		AtLca[u].resize(Size[u] + 1);
		for (auto [v, w] : Graph[u])
		{
			if (Parent[v] != u)
			{
				continue;
			}
			int t = Size[v];
			std::vector<FInteger> Merged(s + t + 1);
			for (int j = 0; j <= t; ++j)
			{
				FInteger Choices = Choose(t, j);
				FInteger Branch = (Forced[v][j] + (j ? w * Choices : 0)) % Mod;
				AtLca[u][j] = (AtLca[u][j] - Branch + Mod) % Mod;
				for (int i = 0; i <= s; ++i)
				{
					Merged[i + j] = (Merged[i + j] + Forced[u][i] * Choices
						+ Choose(s, i) * Branch) % Mod;
				}
			}
			Forced[u].swap(Merged);
			s += t;
		}
		for (int k = 1; k <= s; ++k)
		{
			AtLca[u][k] = (AtLca[u][k] + Forced[u][k]) % Mod;
		}
	}
	// W_parent(k) is available for all k <= size(u).
	std::vector<std::vector<FInteger>> AncestorWeight(n + 1);
	FInteger Total = 0;
	for (int u : Order)
	{
		int s = Size[u];
		AncestorWeight[u].resize(s + 1);
		for (int k = 1; k <= s; ++k)
		{
			FInteger Term = Inv[s] * InvFact[s] % Mod * Fact[k] % Mod * Fact[s - k] % Mod;
			if (Parent[u] != 0)
			{
				Term = (Term + AncestorWeight[Parent[u]][k]) % Mod;
			}
			AncestorWeight[u][k] = Term;
			Total = (Total + Term * AtLca[u][k]) % Mod;
		}
	}
	std::cout << Total * 2 % Mod * Inv[n] % Mod << '\n';
}
