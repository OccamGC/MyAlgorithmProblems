// Problem setter's solution: suffix-array LCP formulas for distinct and unique substrings.
// GPT-6: integer suffix sorting, expectation correction, 64-bit targets and modular edge cases.
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>
#include "expectation.hpp"
int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int Q;
	std::string Text;
	std::cin >> n >> Q >> Text;
	std::vector<int> Order(n);
	std::vector<int> Rank(n);
	std::vector<int> NextRank(n);
	std::vector<int> Buffer(n);
	std::iota(Order.begin(), Order.end(), 0);
	for (int i = 0; i < n; ++i)
	{
		Rank[i] = static_cast<unsigned char>(Text[i]) - 32;
	}
	int Classes = 94;
	for (int Width = 1; ; Width *= 2)
	{
		auto SortBy = [&](int Offset)
		{
			std::vector<int> Count(Classes + 1);
			for (int Position : Order)
			{
				++Count[Position + Offset < n ? Rank[Position + Offset] : 0];
			}
			for (int i = 1; i <= Classes; ++i)
			{
				Count[i] += Count[i - 1];
			}
			for (int i = n - 1; i >= 0; --i)
			{
				int Position = Order[i];
				int Key = Position + Offset < n ? Rank[Position + Offset] : 0;
				Buffer[--Count[Key]] = Position;
			}
			Order.swap(Buffer);
		};
		SortBy(Width);
		SortBy(0);
		int NewClasses = 1;
		NextRank[Order[0]] = NewClasses;
		for (int i = 1; i < n; ++i)
		{
			int a = Order[i - 1];
			int b = Order[i];
			int NextA = a + Width < n ? Rank[a + Width] : 0;
			int NextB = b + Width < n ? Rank[b + Width] : 0;
			if (Rank[a] != Rank[b] || NextA != NextB)
			{
				++NewClasses;
			}
			NextRank[b] = NewClasses;
		}
		Rank.swap(NextRank);
		Classes = NewClasses;
		if (Classes == n)
		{
			break;
		}
	}
	std::vector<int> Lcp(n + 1);
	int Common = 0;
	for (int i = 0; i < n; ++i)
	{
		int Position = Rank[i] - 1;
		if (Position == 0)
		{
			Common = 0;
			continue;
		}
		int Other = Order[Position - 1];
		while (i + Common < n && Other + Common < n && Text[i + Common] == Text[Other + Common])
		{
			++Common;
		}
		Lcp[Position] = Common;
		if (Common)
		{
			--Common;
		}
	}
	FInt Distinct = 0;
	FInt Unique = 0;
	for (int i = 0; i < n; ++i)
	{
		Distinct += n - Order[i] - Lcp[i];
		Unique += n - Order[i] - std::max(Lcp[i], Lcp[i + 1]);
	}
	AnswerQueries(Distinct, Unique, Q);
}
