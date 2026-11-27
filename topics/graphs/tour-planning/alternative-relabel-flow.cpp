// Zero-cost augmentation and relabeling. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <tuple>
#include <utility>
#include <vector>

using FInt = long long;
constexpr FInt Infinity = 4000000000000000000LL;

struct FEdge
{
	int To;
	int Reverse;
	FInt Capacity;
	FInt Cost;
};

class FCostFlow
{
private:
	std::vector<std::vector<FEdge>> Graph;
public:
	explicit FCostFlow(int Size) : Graph(Size)
	{
	}
	void Add(int u, int v, FInt Capacity, FInt Cost)
	{
		FEdge Forward{v, static_cast<int>(Graph[v].size()), Capacity, Cost};
		FEdge Backward{u, static_cast<int>(Graph[u].size()), 0, -Cost};
		Graph[u].push_back(Forward);
		Graph[v].push_back(Backward);
	}
	FInt Run(int Source, int Sink)
	{
		int Size = static_cast<int>(Graph.size());
		std::vector<FInt> Potential(Size, 0);
		FInt Answer = 0;
		while (true)
		{
			std::vector<int> Parent(Size, -1);
			std::vector<int> Via(Size);
			std::vector<int> Queue{Source};
			Parent[Source] = Source;
			for (std::size_t i = 0; i < Queue.size() && Parent[Sink] < 0; ++i)
			{
				int u = Queue[i];
				for (int j = 0; j < static_cast<int>(Graph[u].size()); ++j)
				{
					const auto& Edge = Graph[u][j];
					if (Edge.Capacity > 0 && Parent[Edge.To] < 0
						&& Edge.Cost + Potential[u] == Potential[Edge.To])
					{
						Parent[Edge.To] = u;
						Via[Edge.To] = j;
						Queue.push_back(Edge.To);
					}
				}
			}
			if (Parent[Sink] >= 0)
			{
				FInt Amount = Infinity;
				for (int v = Sink; v != Source; v = Parent[v])
				{
					Amount = std::min(Amount, Graph[Parent[v]][Via[v]].Capacity);
				}
				for (int v = Sink; v != Source; v = Parent[v])
				{
					auto& Edge = Graph[Parent[v]][Via[v]];
					Edge.Capacity -= Amount;
					Graph[v][Edge.Reverse].Capacity += Amount;
					Answer += Amount * Edge.Cost;
				}
				continue;
			}
			FInt Delta = Infinity;
			for (int u : Queue)
			{
				for (const auto& Edge : Graph[u])
				{
					if (Edge.Capacity > 0 && Parent[Edge.To] < 0)
					{
						Delta = std::min(Delta, Edge.Cost + Potential[u] - Potential[Edge.To]);
					}
				}
			}
			if (Delta == Infinity)
			{
				break;
			}
			for (int u : Queue)
			{
				Potential[u] -= Delta;
			}
		}
		return Answer;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::tuple<int, int, FInt>> Edges;
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		FInt w;
		std::cin >> u >> v >> w;
		Edges.emplace_back(u - 1, v - 1, w);
	}
	std::vector<int> k(n);
	std::vector<FInt> V(n);
	std::vector<FInt> C(n);
	std::vector<FInt> H(n);
	std::vector<FInt> P(n);
	for (int i = 0; i < n; ++i)
	{
		std::cin >> k[i] >> V[i] >> C[i] >> H[i] >> P[i];
	}
	// A virtual source reaches every vertex at zero cost.
	std::vector<FInt> Potential(n, 0);
	for (int Round = 0; Round < n; ++Round)
	{
		bool bChanged = false;
		for (auto [u, v, w] : Edges)
		{
			if (Potential[v] > Potential[u] + w)
			{
				Potential[v] = Potential[u] + w;
				bChanged = true;
			}
		}
		if (!bChanged)
		{
			break;
		}
		if (Round == n - 1)
		{
			std::cout << "Negative loop found.\n";
			return 0;
		}
	}
	std::vector<std::vector<std::pair<int, FInt>>> Graph(n);
	for (auto [u, v, w] : Edges)
	{
		Graph[u].push_back({v, w + Potential[u] - Potential[v]});
	}
	int Source = 2 * n;
	int Sink = Source + 1;
	FCostFlow Flow(2 * n + 2);
	for (int i = 0; i < n; ++i)
	{
		Flow.Add(Source, i, V[i], 0);
		Flow.Add(n + i, Sink, H[i], 0);
	}
	for (int i = 0; i < n; ++i)
	{
		if (k[i] == 0 || V[i] == 0)
		{
			continue;
		}
		std::vector<FInt> Distance(n, Infinity);
		using FEntry = std::pair<FInt, int>;
		std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Heap;
		Distance[i] = 0;
		Heap.push({0, i});
		while (!Heap.empty())
		{
			auto [Current, u] = Heap.top();
			Heap.pop();
			if (Current != Distance[u])
			{
				continue;
			}
			for (auto [v, w] : Graph[u])
			{
				if (Distance[v] > Current + w)
				{
					Distance[v] = Current + w;
					Heap.push({Distance[v], v});
				}
			}
		}
		std::vector<std::tuple<FInt, int, int>> Choices;
		for (int j = 0; j < n; ++j)
		{
			if (j != i && Distance[j] != Infinity)
			{
				Choices.emplace_back(Distance[j] + Potential[j] - Potential[i], std::abs(j - i), j);
			}
		}
		std::sort(Choices.begin(), Choices.end());
		int Count = std::min(k[i], static_cast<int>(Choices.size()));
		while (Count > 0 && Count < static_cast<int>(Choices.size()) &&
			std::get<0>(Choices[Count]) == std::get<0>(Choices[Count - 1]) &&
			std::get<1>(Choices[Count]) == std::get<1>(Choices[Count - 1]))
		{
			++Count;
		}
		for (int t = 0; t < Count; ++t)
		{
			int j = std::get<2>(Choices[t]);
			Flow.Add(i, n + j, V[i], C[i] * P[j]);
		}
	}
	std::cout << Flow.Run(Source, Sink) << '\n';
}
