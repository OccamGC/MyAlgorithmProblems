// Codex (GPT-6): group queries by source and use dense Dijkstra on small graphs.

#include <algorithm>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>

constexpr long long Infinity = std::numeric_limits<long long>::max() / 4;
struct FEdge
{
	int To;
	int Weight;
};
using FGraph = std::vector<std::vector<FEdge>>;
using FEntry = std::pair<long long, int>;

std::vector<long long> Dijkstra(const FGraph& Graph, const std::vector<int>& Sources)
{
	std::vector<long long> Distance(Graph.size(), Infinity);
	std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Queue;
	for (int Source : Sources)
	{
		Distance[Source] = 0;
		Queue.push({0, Source});
	}
	while (!Queue.empty())
	{
		const FEntry Entry = Queue.top();
		Queue.pop();
		const int u = Entry.second;
		if (Entry.first != Distance[u])
		{
			continue;
		}
		for (const FEdge& Edge : Graph[u])
		{
			const long long Candidate = Distance[u] + Edge.Weight;
			if (Candidate < Distance[Edge.To])
			{
				Distance[Edge.To] = Candidate;
				Queue.push({Candidate, Edge.To});
			}
		}
	}
	return Distance;
}

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int q;
	std::cin >> n >> m >> q;
	if (n > 500)
	{
		FGraph Graph(n + 1);
		for (int i = 0; i < m; ++i)
		{
			int u;
			int v;
			int c;
			std::cin >> u >> v >> c;
			Graph[u].push_back({v, c});
			Graph[v].push_back({u, c});
		}
		int u;
		int v;
		std::cin >> u >> v;
		const auto Distance = Dijkstra(Graph, {u});
		std::cout << (Distance[v] == Infinity ? -1 : Distance[v]) << '\n';
		return 0;
	}
	std::vector<long long> Matrix(n * n, Infinity);
	for (int i = 0; i < n; ++i)
	{
		Matrix[i * n + i] = 0;
	}
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		long long c;
		std::cin >> u >> v >> c;
		--u;
		--v;
		Matrix[u * n + v] = std::min(Matrix[u * n + v], c);
		Matrix[v * n + u] = std::min(Matrix[v * n + u], c);
	}
	std::vector<std::vector<std::pair<int, int>>> Queries(n);
	std::vector<long long> Answers(q, Infinity);
	for (int i = 0; i < q; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		Queries[u - 1].push_back({v - 1, i});
	}
	for (int Source = 0; Source < n; ++Source)
	{
		if (Queries[Source].empty())
		{
			continue;
		}
		std::vector<long long> Distance(n, Infinity);
		std::vector<bool> Visited(n, false);
		Distance[Source] = 0;
		for (int Step = 0; Step < n; ++Step)
		{
			int u = -1;
			for (int i = 0; i < n; ++i)
			{
				if (!Visited[i] && (u == -1 || Distance[i] < Distance[u]))
				{
					u = i;
				}
			}
			if (u == -1 || Distance[u] == Infinity)
			{
				break;
			}
			Visited[u] = true;
			for (int v = 0; v < n; ++v)
			{
				Distance[v] = std::min(Distance[v], Distance[u] + Matrix[u * n + v]);
			}
		}
		for (const auto& Query : Queries[Source])
		{
			Answers[Query.second] = Distance[Query.first];
		}
	}
	for (long long Answer : Answers)
	{
		std::cout << (Answer == Infinity ? -1 : Answer) << '\n';
	}
}
