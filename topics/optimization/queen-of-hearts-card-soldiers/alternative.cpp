// Codex (GPT-6): decreasing-subsequence DP with a maximum Fenwick tree.

#include <algorithm>
#include <deque>
#include <iostream>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<std::pair<int, int>> Soldiers(n);
	for (auto& Soldier : Soldiers)
	{
		std::cin >> Soldier.first >> Soldier.second;
	}
	std::sort(Soldiers.begin(), Soldiers.end());
	std::vector<int> Values;
	for (const auto& Soldier : Soldiers)
	{
		Values.push_back(-Soldier.second);
	}
	std::sort(Values.begin(), Values.end());
	Values.erase(std::unique(Values.begin(), Values.end()), Values.end());
	std::vector<int> Tree(Values.size() + 1, 0);
	int Answer = 0;
	for (const auto& Soldier : Soldiers)
	{
		const int Rank = static_cast<int>(std::lower_bound(Values.begin(), Values.end(), -Soldier.second) - Values.begin()) + 1;
		int Best = 0;
		for (int Index = Rank - 1; Index > 0; Index -= Index & -Index)
		{
			Best = std::max(Best, Tree[Index]);
		}
		++Best;
		Answer = std::max(Answer, Best);
		for (int Index = Rank; Index < static_cast<int>(Tree.size()); Index += Index & -Index)
		{
			Tree[Index] = std::max(Tree[Index], Best);
		}
	}
	std::cout << Answer << '\n';
}
