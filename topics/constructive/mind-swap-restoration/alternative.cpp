// Evans, Huang, and Nguyen: combined-cycle two-helper construction (arXiv:1204.6086).
// Codex (GPT-6): adapt cycle orientation, implement, and independently verify the construction.
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
	std::vector<std::vector<int>> Cycles;
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
			Visited[u] = true;
			Cycle.push_back(u);
			u = Soul[u];
		} while (u != Start);
		Cycles.push_back(std::move(Cycle));
	}
	std::vector<std::pair<int, int>> Answer;
	if (!Cycles.empty())
	{
		int x = N + 1;
		int y = N + 2;
		for (int i = static_cast<int>(Cycles.size()) - 1; i >= 1; --i)
		{
			Answer.push_back({y, Cycles[i][0]});
		}
		const auto& First = Cycles[0];
		Answer.push_back({x, First[0]});
		for (int i = 1; i < static_cast<int>(First.size()); ++i)
		{
			Answer.push_back({y, First[i]});
		}
		Answer.push_back({y, First[0]});
		Answer.push_back({x, First[1]});
		for (int i = 1; i < static_cast<int>(Cycles.size()); ++i)
		{
			const auto& Cycle = Cycles[i];
			for (int j = 1; j < static_cast<int>(Cycle.size()); ++j)
			{
				Answer.push_back({x, Cycle[j]});
			}
			Answer.push_back({x, Cycle[0]});
		}
		Answer.push_back({x, y});
	}
	std::cout << Answer.size() << '\n';
	for (const auto& Swap : Answer)
	{
		std::cout << Swap.first << ' ' << Swap.second << '\n';
	}
}
