// Codex (GPT-6): direct multi-source initialization of classical Dijkstra.

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
	std::cin >> n >> m;
	FGraph Graph(n + 2);
	std::vector<int> Labels(n + 1);
	std::vector<int> Sources;
	for (int i = 1; i <= n; ++i)
	{
		std::cin >> Labels[i];
		if (Labels[i] == 0)
		{
			Sources.push_back(i);
		}
	}
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		int c;
		std::cin >> u >> v >> c;
		Graph[u].push_back({v, c});
		Graph[v].push_back({u, c});
	}
	const auto Distance = Dijkstra(Graph, Sources);
	long long Answer = Infinity;
	for (int i = 1; i <= n; ++i)
	{
		if (Labels[i] == 1)
		{
			Answer = std::min(Answer, Distance[i]);
		}
	}
	std::cout << (Answer == Infinity ? -1 : Answer) << '\n';
}
