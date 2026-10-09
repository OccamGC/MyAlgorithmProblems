// Problem setter's teaching-note DP with weights 3^(k-j).
// Codex (GPT-6): rolling storage, explicit unreachable states and fixed 64-bit type.
#include <algorithm>
#include <iostream>
#include <limits>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int k;
	std::cin >> n >> k;
	std::vector<long long> Power(k + 1, 1);
	for (int i = 1; i <= k; ++i)
	{
		Power[i] = Power[i - 1] * 3;
	}
	const long long Unreachable = std::numeric_limits<long long>::lowest() / 4;
	std::vector<long long> Best(k + 1, Unreachable);
	Best[0] = 0;
	for (int i = 1; i <= n; ++i)
	{
		long long v;
		std::cin >> v;
		for (int j = std::min(i, k); j >= 1; --j)
		{
			if (Best[j - 1] != Unreachable)
			{
				Best[j] = std::max(Best[j], Best[j - 1] + v * Power[k - j]);
			}
		}
	}
	std::cout << Best[k] << '\n';
}
