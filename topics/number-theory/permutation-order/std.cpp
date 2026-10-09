// Problem setter's solution: cycle lengths and maximum prime exponents.
// Codex (GPT-6): single-case interface and standard C++17 organization.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	int N;
	std::cin >> N;
	std::vector<int> Next(N + 1);
	std::vector<int> Exponent(N + 1, 0);
	for (int i = 1; i <= N; ++i)
	{
		std::cin >> Next[i];
	}
	for (int i = 1; i <= N; ++i)
	{
		int Length = 0;
		int Current = i;
		while (Next[Current] != 0)
		{
			const int Successor = Next[Current];
			Next[Current] = 0;
			Current = Successor;
			++Length;
		}
		for (int p = 2; p * p <= Length; ++p)
		{
			int Count = 0;
			while (Length % p == 0)
			{
				Length /= p;
				++Count;
			}
			Exponent[p] = std::max(Exponent[p], Count);
		}
		if (Length > 1)
		{
			Exponent[Length] = std::max(Exponent[Length], 1);
		}
	}
	constexpr long long Modulus = 998244353;
	long long Answer = 1;
	for (int p = 2; p <= N; ++p)
	{
		for (int Count = 0; Count < Exponent[p]; ++Count)
		{
			Answer = Answer * p % Modulus;
		}
	}
	std::cout << Answer << '\n';
}
