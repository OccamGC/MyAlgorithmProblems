// Problem setter: cubic interval DP with smallest-root tie breaking.
// Codex (GPT-6): portable implementation and iterative reconstruction.

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>
int main()
{
	int n;
	std::cin >> n;
	const int Width = n + 2;
	std::vector<std::int64_t> Sum(Width);
	std::vector<std::int64_t> Cost(Width * Width);
	std::vector<int> Root(Width * Width);
	auto Index = [Width](int l, int r)
	{
		return l * Width + r;
	};
	for (int i = 1; i <= n; ++i)
	{
		std::int64_t Weight;
		std::cin >> Weight;
		Sum[i] = Sum[i - 1] + Weight;
		Cost[Index(i, i)] = Weight;
		Root[Index(i, i)] = i;
	}
	for (int Length = 2; Length <= n; ++Length)
	{
		for (int l = 1; l + Length - 1 <= n; ++l)
		{
			int r = l + Length - 1;
			std::int64_t Best = std::numeric_limits<std::int64_t>::max();
			int First = l;
			int Last = r;
			for (int k = First; k <= Last; ++k)
			{
				std::int64_t Candidate = Cost[Index(l, k - 1)] + Cost[Index(k + 1, r)];
				if (Candidate < Best)
				{
					Best = Candidate;
					Root[Index(l, r)] = k;
				}
			}
			Cost[Index(l, r)] = Best + Sum[r] - Sum[l - 1];
		}
	}
	std::cout << Cost[Index(1, n)] << '\n';
	std::vector<std::pair<int, int>> Stack{{1, n}};
	bool bFirst = true;
	while (!Stack.empty())
	{
		auto [l, r] = Stack.back();
		Stack.pop_back();
		if (l > r)
		{
			continue;
		}
		int k = Root[Index(l, r)];
		if (!bFirst)
		{
			std::cout << ' ';
		}
		bFirst = false;
		std::cout << k;
		Stack.emplace_back(k + 1, r);
		Stack.emplace_back(l, k - 1);
	}
	std::cout << '\n';
}
