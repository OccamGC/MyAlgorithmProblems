// Offline diagonal DP. C++17 implementation by Codex (GPT-6).
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	constexpr std::int64_t Mod = 921260340;
	int n;
	int q;
	std::cin >> n >> q;
	std::vector<std::int64_t> Fact(n + 1, 1);
	for (int i = 1; i <= n; ++i)
	{
		Fact[i] = Fact[i - 1] * i % Mod;
	}
	std::vector<std::vector<std::pair<int, int>>> Queries(2 * n + 1);
	std::vector<int> Answer(q);
	for (int i = 0; i < q; ++i)
	{
		int a;
		int b;
		std::cin >> a >> b;
		if (a <= n && b <= n)
		{
			Queries[n + b - a].emplace_back(a, i);
		}
	}
	std::vector<int> Value(n + 1);
	for (int d = -n; d <= n; ++d)
	{
		const auto& Group = Queries[n + d];
		if (Group.empty())
		{
			continue;
		}
		std::int64_t Next = 0;
		for (int a = std::min(n, n - d); a >= std::max(0, -d); --a)
		{
			Next = a * (Fact[a + d] + Next) % Mod;
			Value[a] = static_cast<int>(Next);
		}
		for (auto [a, Id] : Group)
		{
			Answer[Id] = Value[a];
		}
	}
	for (int Result : Answer)
	{
		std::cout << Result << '\n';
	}
}
