// GPT-6: completed specification, feasible-weight propagation, implementation.
#include <algorithm>
#include <iostream>
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
	for (int i = 0; i < n - 1; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		--u;
		--v;
		Adjacent[u].push_back({v, i});
		Adjacent[v].push_back({u, i});
	}
	std::vector<FInt> Low(n);
	std::vector<FInt> High(n);
	for (int i = 0; i < n; ++i)
	{
		std::cin >> Low[i] >> High[i];
	}
	std::vector<std::vector<FInt>> Weights(n - 1);
	while (m--)
	{
		int Edge;
		FInt Weight;
		std::cin >> Edge >> Weight;
		Weights[Edge - 1].push_back(Weight);
	}
	for (auto& List : Weights)
	{
		std::sort(List.begin(), List.end());
		List.erase(std::unique(List.begin(), List.end()), List.end());
	}
	for (int Start = 0; Start < n; ++Start)
	{
		std::vector<std::vector<FInt>> Possible(n);
		std::vector<int> Parent(n, -1);
		std::vector<int> Queue{Start};
		for (int Head = 0; Head < static_cast<int>(Queue.size()); ++Head)
		{
			int u = Queue[Head];
			for (const auto& Arc : Adjacent[u])
			{
				int v = Arc.first;
				if (v == Parent[u])
				{
					continue;
				}
				for (FInt Weight : Weights[Arc.second])
				{
					if (u == Start)
					{
						Possible[v].push_back(Weight);
					}
					else
					{
						auto Position = std::lower_bound(Possible[u].begin(), Possible[u].end(), Weight - High[u]);
						if (Position != Possible[u].end() && *Position <= Weight - Low[u])
						{
							Possible[v].push_back(Weight);
						}
					}
				}
				if (!Possible[v].empty())
				{
					Parent[v] = u;
					Queue.push_back(v);
				}
			}
		}
		std::cout << Queue.size() << (Start + 1 == n ? '\n' : ' ');
	}
}
