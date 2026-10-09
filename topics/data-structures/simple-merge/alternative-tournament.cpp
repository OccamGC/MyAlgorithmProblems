// Codex (GPT-6): apply a tournament tree to the sequence-head merge.
// Tournament trees are an established selection data structure.

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

	using FEntry = std::pair<long long, int>;
	const FEntry Infinity = {std::numeric_limits<long long>::max(), k};
	int Base = 1;
	while (Base < k)
	{
		Base *= 2;
	}
	std::vector<FEntry> Tree(Base * 2, Infinity);
	for (int i = 0; i < k; ++i)
	{
		Tree[Base + i] = {Sequences[i][0], i};
	}
	for (int Node = Base - 1; Node > 0; --Node)
	{
		Tree[Node] = std::min(Tree[Node * 2], Tree[Node * 2 + 1]);
	}
	for (int Step = 0; Step < m; ++Step)
	{
		auto [Value, Index] = Tree[1];
		std::cout << Value << '\n';
		++Position[Index];
		int Node = Base + Index;
		Tree[Node] = Position[Index] < static_cast<int>(Sequences[Index].size())
			? FEntry{Sequences[Index][Position[Index]], Index} : Infinity;
		for (Node /= 2; Node > 0; Node /= 2)
		{
			Tree[Node] = std::min(Tree[Node * 2], Tree[Node * 2 + 1]);
		}
	}
}
