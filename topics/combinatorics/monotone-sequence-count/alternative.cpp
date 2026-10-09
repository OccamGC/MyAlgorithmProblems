// Problem setter: Pascal recurrence. Codex (GPT-6): one-row storage.
#include <algorithm>
#include <iostream>
#include <vector>
int main()
{
	int n;
	int m;
	std::cin >> n >> m;
	int Total = n + m - 1;
	int Selected = std::min(n, m - 1);
	const int Mod = 998244353;
	std::vector<int> Count(Selected + 1);
	Count[0] = 1;
	for (int i = 1; i <= Total; ++i)
	{
		for (int j = std::min(i, Selected); j > 0; --j)
		{
			Count[j] += Count[j - 1];
			if (Count[j] >= Mod)
			{
				Count[j] -= Mod;
			}
		}
	}
	std::cout << Count[Selected] << '\n';
}
