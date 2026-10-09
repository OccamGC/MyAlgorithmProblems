#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
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

	std::vector<int> LeftChild(n, -1);
	std::vector<int> RightChild(n, -1);
	std::vector<int> Stack;
	Stack.reserve(n);
	for (int i = 0; i < n; ++i)
	{
		int Last = -1;
		while (!Stack.empty() && a[Stack.back()] > a[i])
		{
			Last = Stack.back();
			Stack.pop_back();
		}
		LeftChild[i] = Last;
		if (!Stack.empty())
		{
			RightChild[Stack.back()] = i;
		}
		Stack.push_back(i);
	}
	const int Root = Stack.front();
	std::vector<int> Order;
	Order.reserve(n);
	Order.push_back(Root);
	for (std::size_t Index = 0; Index < Order.size(); ++Index)
	{
		const int u = Order[Index];
		if (LeftChild[u] != -1)
		{
			Order.push_back(LeftChild[u]);
		}
		if (RightChild[u] != -1)
		{
			Order.push_back(RightChild[u]);
		}
	}

	std::vector<FInt64> MinPrefix(n);
	std::vector<FInt64> MaxPrefix(n);
	FInt64 Answer = std::numeric_limits<FInt64>::lowest();
	for (int Index = n - 1; Index >= 0; --Index)
	{
		const int u = Order[Index];
		const FInt64 LeftMinimum = LeftChild[u] == -1 ? Prefix[u] : MinPrefix[LeftChild[u]];
		const FInt64 LeftMaximum = LeftChild[u] == -1 ? Prefix[u] : MaxPrefix[LeftChild[u]];
		const FInt64 RightMinimum = RightChild[u] == -1 ? Prefix[u + 1] : MinPrefix[RightChild[u]];
		const FInt64 RightMaximum = RightChild[u] == -1 ? Prefix[u + 1] : MaxPrefix[RightChild[u]];
		const FInt64 BestSum = a[u] >= 0
			? RightMaximum - LeftMinimum : RightMinimum - LeftMaximum;
		Answer = std::max(Answer, static_cast<FInt64>(a[u]) * BestSum);
		MinPrefix[u] = std::min(LeftMinimum, RightMinimum);
		MaxPrefix[u] = std::max(LeftMaximum, RightMaximum);
	}
	std::cout << Answer << '\n';
}
