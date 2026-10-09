// Problem setter's rank/Fenwick alternative. Codex (GPT-6): complete implementation and proof.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

struct FFenwick
{
	std::vector<int> Tree;

	explicit FFenwick(int Size) : Tree(Size + 1)
	{
	}

	void Add(int Position)
	{
		for (int i = Position; i < static_cast<int>(Tree.size()); i += i & -i)
		{
			++Tree[i];
		}
	}

	int Prefix(int Position) const
	{
		int Result = 0;
		for (int i = Position; i > 0; i -= i & -i)
		{
			Result += Tree[i];
		}
		return Result;
	}
};

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<std::pair<int, int>> Values(n);
	for (auto& Value : Values)
	{
		std::cin >> Value.first >> Value.second;
	}
	int Records = 0;
	auto Minimum = Values.front();
	for (int i = 0; i < n; ++i)
	{
		if (i == 0 || Values[i] < Minimum)
		{
			Minimum = Values[i];
			++Records;
		}
	}
	std::vector<std::pair<std::pair<int, int>, int>> Order(n);
	for (int i = 0; i < n; ++i)
	{
		Order[i] = {Values[i], i};
	}
	std::sort(Order.begin(), Order.end());
	std::vector<int> Rank(n);
	for (int i = 0; i < n; ++i)
	{
		Rank[Order[i].second] = i + 1;
	}
	FFenwick Tree(n);
	std::int64_t Inversions = 0;
	for (int i = 0; i < n; ++i)
	{
		Inversions += i - Tree.Prefix(Rank[i]);
		Tree.Add(Rank[i]);
	}
	std::cout << 2 * Inversions + n - Records << '\n';
}
