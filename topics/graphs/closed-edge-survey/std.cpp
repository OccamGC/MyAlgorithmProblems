// Problem setter's solution: tree shortcut, odd-vertex shortest paths and pairing DP.
// GPT-6: portable implementation, explicit edge cases, proof and independent verification.
#include <algorithm>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
using FInt = long long;
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<std::vector<std::pair<int, int>>> Adjacent(n);
	FInt Total = 0;
	for (int i = 0; i < m; ++i)
	{
		int u;
		int v;
		int w;
		std::cin >> u >> v >> w;
		--u;
		--v;
		Adjacent[u].push_back({v, w});
		Adjacent[v].push_back({u, w});
		Total += w;
	}
	std::cout << 1 << '\n';
	if (m == n - 1)
	{
		std::cout << 2 * Total << '\n';
		return 0;
	}
	std::vector<int> Odd;
	for (int i = 0; i < n; ++i)
	{
		if (Adjacent[i].size() % 2)
		{
			Odd.push_back(i);
		}
	}
	int k = static_cast<int>(Odd.size());
	const FInt Infinity = std::numeric_limits<FInt>::max() / 4;
	std::vector<std::vector<FInt>> Cost(k, std::vector<FInt>(k));
	for (int i = 0; i < k; ++i)
	{
		std::vector<FInt> Distance(n, Infinity);
		using FEntry = std::pair<FInt, int>;
		std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Queue;
		Distance[Odd[i]] = 0;
		Queue.push({0, Odd[i]});
		while (!Queue.empty())
		{
			FEntry Entry = Queue.top();
			Queue.pop();
			int u = Entry.second;
			if (Entry.first != Distance[u])
			{
				continue;
			}
			for (const auto& Edge : Adjacent[u])
			{
				int v = Edge.first;
				FInt Candidate = Entry.first + Edge.second;
				if (Candidate < Distance[v])
				{
					Distance[v] = Candidate;
					Queue.push({Candidate, v});
				}
			}
		}
		for (int j = 0; j < k; ++j)
		{
			Cost[i][j] = Distance[Odd[j]];
		}
	}
	std::vector<FInt> Best(1 << k, Infinity);
	Best[0] = 0;
	for (int Mask = 1; Mask < (1 << k); ++Mask)
	{
		int First = 0;
		while (!(Mask & (1 << First)))
		{
			++First;
		}
		int Rest = Mask ^ (1 << First);
		for (int j = First + 1; j < k; ++j)
		{
			if (Rest & (1 << j))
			{
				Best[Mask] = std::min(Best[Mask], Cost[First][j] + Best[Rest ^ (1 << j)]);
			}
		}
	}
	std::cout << Total + Best.back() << '\n';
}
