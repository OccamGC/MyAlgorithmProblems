// Problem setter's solution: blocks of factorial indices and product-weighted sums.
// Codex (GPT-6): portable C++17 implementation and empty-range/zero-index handling.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using FInteger = std::int64_t;
constexpr FInteger Mod = 921260340;

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int n;
	int q;
	std::cin >> n >> q;
	int BlockSize = static_cast<int>(std::sqrt(n + 1)) + 1;
	int BlockCount = (n + BlockSize) / BlockSize;
	std::vector<FInteger> Factorial(n + 1, 1);
	std::vector<FInteger> Product(n + 1, 1);
	std::vector<std::vector<FInteger>> Sum(BlockCount, std::vector<FInteger>(n + 1));
	for (int i = 1; i <= n; ++i)
	{
		Factorial[i] = Factorial[i - 1] * i % Mod;
	}
	for (int i = 0; i + BlockSize - 1 <= n; ++i)
	{
		for (int k = 0; k < BlockSize; ++k)
		{
			Product[i] = Product[i] * (i + k) % Mod;
		}
	}
	for (int Block = 0; Block < BlockCount; ++Block)
	{
		int Start = Block * BlockSize;
		for (int i = 0; i <= n; ++i)
		{
			FInteger Current = 1;
			for (int k = 0; k < BlockSize && i + k <= n && Start + k <= n; ++k)
			{
				Current = Current * (i + k) % Mod;
				Sum[Block][i] = (Sum[Block][i] + Current * Factorial[Start + k]) % Mod;
			}
		}
	}
	while (q--)
	{
		int a;
		int b;
		std::cin >> a >> b;
		FInteger Answer = 0;
		FInteger Current = 1;
		while (a <= n && b <= n)
		{
			if (b % BlockSize == 0 && a + BlockSize - 1 <= n && b + BlockSize - 1 <= n)
			{
				Answer = (Answer + Current * Sum[b / BlockSize][a]) % Mod;
				Current = Current * Product[a] % Mod;
				a += BlockSize;
				b += BlockSize;
			}
			else
			{
				Current = Current * a % Mod;
				Answer = (Answer + Current * Factorial[b]) % Mod;
				++a;
				++b;
			}
		}
		std::cout << Answer << '\n';
	}
}
