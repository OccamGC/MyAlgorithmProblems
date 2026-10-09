// Codex (GPT-6): derive the difference recurrence and apply a multiples sieve.
// Problem setter's quotient-block recurrence is preserved in alternative-quotient-blocks.cpp.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int Q;
	std::cin >> Q;
	std::vector<int> Queries(Q);
	int N = 0;
	for (int& x : Queries)
	{
		std::cin >> x;
		N = std::max(N, x);
	}
	constexpr int Mod = 998244353;
	std::vector<int> Difference(N + 1, 1);
	std::vector<int> Answer(N + 1, 0);
	for (int d = 1; d <= N; ++d)
	{
		Answer[d] = (Answer[d - 1] + Difference[d]) % Mod;
		for (int Multiple = d + d; Multiple <= N; Multiple += d)
		{
			Difference[Multiple] += Difference[d];
			if (Difference[Multiple] >= Mod)
			{
				Difference[Multiple] -= Mod;
			}
		}
	}
	for (int x : Queries)
	{
		std::cout << (x <= 0 ? x : Answer[x]) << '\n';
	}
}
