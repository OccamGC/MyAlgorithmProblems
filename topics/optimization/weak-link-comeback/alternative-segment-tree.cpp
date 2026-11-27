// Monotone stack and segment tree. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

using FInt64 = std::int64_t;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);

	int n;
	if (!(std::cin >> n))
	{
		return 0;
	}
	std::vector<int> a(n);
	for (int& Value : a)
	{
		std::cin >> Value;
	}
	std::vector<FInt64> Prefix(n + 1, 0);
	for (int i = 0; i < n; ++i)
	{
		int b;
		std::cin >> b;
		Prefix[i + 1] = Prefix[i] + b;
	}

	// The minimum (left) and maximum (right) prefix give the extreme interval sums.
	int Base = 1;
	while (Base < n + 1)
	{
		Base *= 2;
	}
	using FRange = std::pair<FInt64, FInt64>;
	const FRange Empty{std::numeric_limits<FInt64>::max(), std::numeric_limits<FInt64>::lowest()};
	auto Merge = [](FRange a, FRange b) -> FRange
	{
		return {std::min(a.first, b.first), std::max(a.second, b.second)};
	};
	std::vector<FRange> Tree(2 * Base, Empty);
	for (int i = 0; i <= n; ++i)
	{
		Tree[Base + i] = {Prefix[i], Prefix[i]};
	}
	for (int i = Base - 1; i > 0; --i)
	{
		Tree[i] = Merge(Tree[2 * i], Tree[2 * i + 1]);
	}
	auto Query = [&](int l, int r)
	{
		FRange Result = Empty;
		for (l += Base, r += Base; l < r; l /= 2, r /= 2)
		{
			if (l & 1)
			{
				Result = Merge(Result, Tree[l++]);
			}
			if (r & 1)
			{
				Result = Merge(Result, Tree[--r]);
			}
		}
		return Result;
	};
	std::vector<int> Stack;
	FInt64 Best = std::numeric_limits<FInt64>::lowest();
	for (int r = 0; r <= n; ++r)
	{
		while (!Stack.empty() && (r == n || a[Stack.back()] > a[r]))
		{
			int i = Stack.back();
			Stack.pop_back();
			int l = Stack.empty() ? 0 : Stack.back() + 1;
			FRange Left = Query(l, i + 1);
			FRange Right = Query(i + 1, r + 1);
			FInt64 Sum = a[i] >= 0 ? Right.second - Left.first : Right.first - Left.second;
			Best = std::max(Best, a[i] * Sum);
		}
		Stack.push_back(r);
	}
	std::cout << Best << '\n';
}
