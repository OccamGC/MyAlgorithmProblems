// Problem setter's solution: enumerate divisors of selected input positions.
// Codex (GPT-6): inspect n-m+1 positions to guarantee coverage; no sampling error.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	int k;
	std::cin >> n >> m >> k;
	std::vector<int> Values(n);
	for (int& Value : Values)
	{
		std::cin >> Value;
	}
	if (m == 0)
	{
		std::cout << k << '\n';
		return 0;
	}
	int Answer = 1;
	auto Test = [&](int Candidate)
	{
		if (Candidate <= Answer || Candidate > k)
		{
			return;
		}
		int Count = 0;
		for (int i = 0; i < n; ++i)
		{
			Count += Values[i] % Candidate == 0;
			if (Count >= m)
			{
				Answer = Candidate;
				return;
			}
			if (Count + n - i - 1 < m)
			{
				return;
			}
		}
	};
	for (int i = 0; i < n - m + 1 && Answer < k; ++i)
	{
		int a = Values[i];
		for (int d = 1; d <= a / d && d <= k; ++d)
		{
			if (a % d == 0)
			{
				Test(d);
				Test(a / d);
			}
		}
	}
	std::cout << Answer << '\n';
}
