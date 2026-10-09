// Problem setter's solution: extend each left endpoint with two heaps.
// Codex (GPT-6): explicit size invariants, portable implementation and verification.
#include <functional>
#include <iostream>
#include <queue>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	std::cin >> n;
	std::vector<long long> a(n);
	for (long long& Value : a)
	{
		std::cin >> Value;
	}
	std::vector<std::vector<long long>> Answer(n + 1);
	for (int Length = 1; Length <= n; ++Length)
	{
		Answer[Length].resize(n - Length + 1);
	}
	for (int l = 0; l < n; ++l)
	{
		std::priority_queue<long long> Lower;
		std::priority_queue<long long, std::vector<long long>, std::greater<long long>> Upper;

		long long Sum = 0;
		for (int r = l; r < n; ++r)
		{
			int Length = r - l + 1;
			Lower.push(a[r]);
			if (static_cast<int>(Upper.size()) < (Length + 1) / 2)
			{
				Sum += Lower.top();
				Upper.push(Lower.top());
				Lower.pop();
			}
			if (!Lower.empty() && Lower.top() > Upper.top())
			{
				long long Low = Lower.top();
				long long High = Upper.top();
				Lower.pop();
				Upper.pop();
				Lower.push(High);
				Upper.push(Low);
				Sum += Low - High;
			}
			Answer[Length][l] = Sum;

		}
	}
	for (int Length = 1; Length <= n; ++Length)
	{
		for (long long Value : Answer[Length])
		{
			std::cout << Value << '\n';
		}
	}
}
