// Problem setter's solution: a heap containing one head per monotone sequence.
// Codex (GPT-6): C++17 cleanup and duplicate/empty-output verification.

#include <algorithm>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int k;
	int m;
	std::cin >> k >> m;
	std::vector<std::vector<int>> Sequences(k);
	std::vector<int> Position(k, 0);
	for (auto& Sequence : Sequences)
	{
		int Length;
		std::cin >> Length;
		Sequence.resize(Length);
		for (int& Value : Sequence)
		{
			std::cin >> Value;
		}
		if (Sequence.front() > Sequence.back())
		{
			std::reverse(Sequence.begin(), Sequence.end());
		}
	}

	using FEntry = std::pair<int, int>;
	std::priority_queue<FEntry, std::vector<FEntry>, std::greater<FEntry>> Heap;
	for (int i = 0; i < k; ++i)
	{
		Heap.emplace(Sequences[i][0], i);
	}
	for (int Step = 0; Step < m; ++Step)
	{
		auto [Value, Index] = Heap.top();
		Heap.pop();
		std::cout << Value << '\n';
		++Position[Index];
		if (Position[Index] < static_cast<int>(Sequences[Index].size()))
		{
			Heap.emplace(Sequences[Index][Position[Index]], Index);
		}
	}
}
