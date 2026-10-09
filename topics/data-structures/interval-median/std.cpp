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

		for (int r = l; r < n; ++r)
		{
			int Length = r - l + 1;
			if (Lower.empty() || a[r] <= Lower.top())
			{
				Lower.push(a[r]);
			}
			else
			{
				Upper.push(a[r]);
			}
			if (static_cast<int>(Lower.size()) > (Length + 1) / 2)
			{
				Upper.push(Lower.top());
				Lower.pop();
			}
			if (static_cast<int>(Lower.size()) < (Length + 1) / 2)
			{
				Lower.push(Upper.top());
				Upper.pop();
			}
			Answer[Length][l] = Length % 2 == 1
				? 2 * Lower.top() : Lower.top() + Upper.top();

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
