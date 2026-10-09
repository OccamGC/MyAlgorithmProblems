// Codex (GPT-6): partition conjugation and the standard unbounded-knapsack recurrence.

#include <algorithm>
#include <iostream>
#include <vector>

constexpr int Modulus = 1000000007;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int m;
	std::cin >> n >> m;
	std::vector<int> Counts(n + 1, 0);
	Counts[0] = 1;
	for (int Part = 1; Part <= std::min(n, m); ++Part)
	{
		for (int Total = Part; Total <= n; ++Total)
		{
			Counts[Total] += Counts[Total - Part];
			if (Counts[Total] >= Modulus)
			{
				Counts[Total] -= Modulus;
			}
		}
	}
	for (int i = 1; i <= n; ++i)
	{
		std::cout << Counts[i] << '\n';
	}
}
