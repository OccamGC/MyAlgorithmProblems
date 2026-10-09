// Codex (GPT-6): deterministic divisor-frequency solution for this problem.
// Uses standard trial division, sorting and run-length counting.
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
	std::vector<int> Divisors;
	for (int i = 0; i < n; ++i)
	{
		int a;
		std::cin >> a;
		if (m == 0)
		{
			continue;
		}
		for (int d = 1; d <= a / d && d <= k; ++d)
		{
			if (a % d == 0)
			{
				Divisors.push_back(d);
				if (a / d != d && a / d <= k)
				{
					Divisors.push_back(a / d);
				}
			}
		}
	}
	if (m == 0)
	{
		std::cout << k << '\n';
		return 0;
	}
	std::sort(Divisors.begin(), Divisors.end());
	int Answer = 1;
	for (std::size_t Left = 0; Left < Divisors.size();)
	{
		std::size_t Right = Left + 1;
		while (Right < Divisors.size() && Divisors[Right] == Divisors[Left])
		{
			++Right;
		}
		if (Right - Left >= static_cast<std::size_t>(m))
		{
			Answer = Divisors[Left];
		}
		Left = Right;
	}
	std::cout << Answer << '\n';
}
