// Contribution: Codex (GPT-6): explicit traversals and a zero-safe prefix/suffix implementation of the original cases.
// Original two-endpoint path classification; iterative branch failure DP.
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
	std::vector<int> High;
	for (int u = 1; u <= n; ++u)
	{
		if (Type[u] & 2)
		{
			High.push_back(u);
		}
	}
	if (High.empty())
	{
		std::cout << 0 << '\n';
		return 0;
	}
	std::vector<int> Parent(n + 1);
	std::vector<int> ParentEdge(n + 1, -1);
	std::vector<int> Order{High[0]};
	for (int i = 0; i < n; ++i)
	{
		const int u = Order[i];
		for (int Index : Graph[u])
		{
			const FEdge& Edge = Edges[Index];
			const int v = Edge.u ^ Edge.v ^ u;
			if (v != Parent[u])
			{
				Parent[v] = u;
				ParentEdge[v] = Index;
				Order.push_back(v);
			}
		}
	}
	std::vector<int> Path;
	std::vector<char> OnPath(n + 1, false);
	for (int u = High.back(); u != 0; u = Parent[u])
	{
		Path.push_back(u);
		OnPath[u] = true;
	}
	std::reverse(Path.begin(), Path.end());
	std::vector<long long> Failure(n + 1, 1);
	for (auto It = Order.rbegin(); It != Order.rend(); ++It)
	{
		const int u = *It;
		if (Type[u] & 1)
		{
			Failure[u] = 0;
		}
		for (int Index : Graph[u])
		{
			const FEdge& Edge = Edges[Index];
			const int v = Edge.u ^ Edge.v ^ u;
			if (Parent[v] == u && !OnPath[v])
			{
				const long long Closed = Edge.q * Inverse[Edge.p] % Mod;
				Failure[u] = Failure[u] * (Closed + (1 - Closed + Mod) * Failure[v] % Mod) % Mod;
			}
		}
	}
	const int Length = static_cast<int>(Path.size());
	std::vector<long long> Closed(std::max(0, Length - 1));
	std::vector<long long> Suffix(Length);
	Suffix.back() = Failure[Path.back()];
	for (int i = Length - 2; i >= 0; --i)
	{
		const FEdge& Edge = Edges[ParentEdge[Path[i + 1]]];
		Closed[i] = Edge.q * Inverse[Edge.p] % Mod;
		Suffix[i] = Failure[Path[i]] * (1 - Closed[i] + Mod) % Mod * Suffix[i + 1] % Mod;
	}
	long long NoConnection = Suffix[0];
	long long LaterCuts = 0;
	for (int i = 0; i + 1 < Length; ++i)
	{
		LaterCuts = (LaterCuts + Closed[i] * Suffix[i + 1]) % Mod;
	}
	long long Prefix = Failure[Path[0]];
	for (int i = 0; i + 1 < Length; ++i)
	{
		LaterCuts = (LaterCuts - Closed[i] * Suffix[i + 1] % Mod + Mod) % Mod;
		NoConnection = (NoConnection + Prefix * Closed[i] % Mod * ((Suffix[i + 1] + LaterCuts) % Mod)) % Mod;
		Prefix = Prefix * (1 - Closed[i] + Mod) % Mod * Failure[Path[i + 1]] % Mod;
	}
	std::cout << (1 - NoConnection + Mod) % Mod << '\n';
}
