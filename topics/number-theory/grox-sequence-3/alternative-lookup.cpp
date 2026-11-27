// Full lookup table. C++17 implementation by Codex (GPT-6).
#include <cstdint>
#include <iostream>
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
	const int Width = n + 2;
	std::vector<int> Value(Width * Width);
	for (int a = n; a >= 0; --a)
	{
		for (int b = n; b >= 0; --b)
		{
			Value[a * Width + b] = a * (Fact[b] + Value[(a + 1) * Width + b + 1]) % Mod;
		}
	}
	for (int i = 0; i < q; ++i)
	{
		int a;
		int b;
		std::cin >> a >> b;
		std::cout << (a <= n && b <= n ? Value[a * Width + b] : 0) << '\n';
	}
}
