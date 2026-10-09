// Keeler's two-helper construction. Codex (GPT-6): specification, application, implementation, and checks.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	int M;
	std::cin >> N >> M;
	std::vector<int> Soul(N + 1);
	std::iota(Soul.begin(), Soul.end(), 0);
	for (int i = 0; i < M; ++i)
	{
		int u;
		int v;
		std::cin >> u >> v;
		std::swap(Soul[u], Soul[v]);
	}
	std::vector<bool> Visited(N + 1);
	std::vector<std::pair<int, int>> Answer;
	int x = N + 1;
	int y = N + 2;
	bool bSwapped = false;
	for (int Start = 1; Start <= N; ++Start)
	{
		if (Visited[Start] || Soul[Start] == Start)
		{
			continue;
		}
		std::vector<int> Cycle;
		int u = Start;
		do
		{
			Cycle.push_back(u);
			Visited[u] = true;
			u = Soul[u];
		} while (u != Start);
		Answer.push_back({x, Cycle.front()});
		Answer.push_back({y, Cycle.back()});
		for (int i = 1; i < static_cast<int>(Cycle.size()); ++i)
		{
			Answer.push_back({x, Cycle[i]});
		}
		Answer.push_back({y, Cycle.front()});
		bSwapped = !bSwapped;
	}
	if (bSwapped)
	{
		Answer.push_back({x, y});
	}
	std::cout << Answer.size() << '\n';
	for (const auto& Swap : Answer)
	{
		std::cout << Swap.first << ' ' << Swap.second << '\n';
	}
}
