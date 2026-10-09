// Problem setter's solution: greedy nondecreasing-chain cover.
// Codex (GPT-6): standard C++17 organization and strictness proof.

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
	std::deque<int> Chains;
	for (const auto& Soldier : Soldiers)
	{
		auto Position = std::upper_bound(Chains.begin(), Chains.end(), Soldier.second);
		if (Position == Chains.begin())
		{
			Chains.push_front(Soldier.second);
		}
		else
		{
			*--Position = Soldier.second;
		}
	}
	std::cout << Chains.size() << '\n';
}
